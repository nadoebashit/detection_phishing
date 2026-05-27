import base64
import json
import httpx
from loguru import logger
from app.config import settings
from app.services.similarity.phash import PHashSimilarity
from app.services.similarity.ssim import SSIMSimilarity
from app.services.similarity.cnn import cnn_similarity

class PhishingDetector:
    @staticmethod
    def evaluate_similarity(target_screenshot: str, legitimate_screenshot: str, legitimate_features: list[float], legitimate_phash: str) -> dict:
        # 1. pHash calculation
        target_phash = PHashSimilarity.compute_hash(target_screenshot)
        phash_dist = PHashSimilarity.compare(target_phash, legitimate_phash)
        phash_similar = PHashSimilarity.is_similar(phash_dist)
        
        # 2. SSIM calculation
        ssim_score, _ = SSIMSimilarity.compare(target_screenshot, legitimate_screenshot)
        ssim_similar = SSIMSimilarity.is_similar(ssim_score)
        
        # 3. CNN calculation
        target_features = cnn_similarity.extract_features(target_screenshot)
        cnn_score = cnn_similarity.compare(target_features, legitimate_features)
        cnn_similar = cnn_similarity.is_similar(cnn_score)
        
        scores = {
            "phash": float(phash_dist),
            "ssim": float(ssim_score),
            "cnn": float(cnn_score)
        }
        
        votes = sum([phash_similar, ssim_similar, cnn_similar])
        is_phishing = votes >= 2 
        confidence = votes / 3.0
        
        return {
            "is_phishing": is_phishing,
            "confidence": confidence,
            "scores": scores
        }

    @staticmethod
    async def evaluate_with_ai(target_screenshot: str, target_url: str, legit_sites: list, best_match_brand: str | None, best_scores: dict) -> dict:
        """Evaluates the target website using Fireworks AI (Kimi multimodal model) for a strict decision."""
        if not settings.FIREWORKS_API_KEY:
            logger.error("FIREWORKS_API_KEY is not configured. Falling back to default heuristics.")
            raise ValueError("Fireworks API key is not configured.")

        # Read and base64-encode the screenshot image
        try:
            with open(target_screenshot, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to read screenshot file {target_screenshot}: {e}")
            raise e

        # Prepare protected brands metadata
        brands_list = []
        for site in legit_sites:
            brands_list.append(f"- Domain: {site.domain}")
        brands_context = "\n".join(brands_list) if brands_list else "No protected brands configured in database."

        # Construct prompt
        prompt = f"""You are an expert cybersecurity AI specialized in phishing detection and brand spoofing analysis.
Analyze the provided screenshot and metadata of a website to determine if it is a phishing website.

WEBSITE UNDER ANALYSIS:
- Target URL being scanned: {target_url}

PROTECTED LEGITIMATE BRANDS IN SYSTEM (Note: you must detect phishing for ANY brand, not just these. Use this database list as additional context):
{brands_context}

COMPUTED SIMILARITY METRICS WITH BEST MATCH BRAND ({best_match_brand or 'None'}):
- Perceptual Hash (pHash) Distance: {best_scores.get('phash', 0.0)}
- Structural Similarity (SSIM) Index: {best_scores.get('ssim', 0.0)}
- CNN Deep Learning Concept Similarity: {best_scores.get('cnn', 0.0)}

INSTRUCTIONS FOR DECISION MAKING (CRITICAL - YOU HAVE COMPLETE CONTROL):
1. Determine if the website in the screenshot is mimicking or spoofing ANY legitimate brand (e.g. Steam, Roblox, Google, GitHub, Microsoft, Facebook, Netflix, Amazon, PayPal, bank sites, etc.) OR presents a suspicious login form/credentials harvesting page.
2. If it is mimicking ANY brand (visually identical or highly similar login pages, logo, layouts, etc.) or presents a suspicious credential collection interface, but the Target URL is NOT the official domain of that brand, classify it as PHISHING (is_phishing = true).
3. Under this rule:
   - For example, if the site screenshot is clearly a Steam login page, but the URL is 'kleankelp.duckdns.org' (not steampowered.com or steamcommunity.com), classify it as PHISHING (is_phishing = true) with the domain being spoofed specified in "similar_to" (e.g. "steampowered.com").
4. If the website does not mimic any brand or is the official domain of that brand, classify it as SAFE (is_phishing = false).
5. Provide a confidence score between 0.0 (completely safe/unknown) and 1.0 (highly confident phishing).
6. Provide a detailed analysis report explaining your findings (highlighting logo mismatches, suspicious domains, forms, etc.). Write the detailed analysis report in Russian. Keep the analysis report concise and strictly under 150 words (1000 characters) so that the response is not truncated.
7. Return your response STRICTLY as a JSON object with the following schema:
{{
  "is_phishing": boolean,
  "confidence": float,
  "similar_to": string or null (the brand domain being spoofed, e.g., "steampowered.com"),
  "detailed_analysis": string (detailed report in Russian)
}}
Do not include any markdown wrappers like ```json or additional text outside of the raw JSON object."""

        payload = {
            "model": settings.FIREWORKS_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
            "max_tokens": 2048
        }

        headers = {
            "Authorization": f"Bearer {settings.FIREWORKS_API_KEY}",
            "Content-Type": "application/json"
        }

        url = "https://api.fireworks.ai/inference/v1/chat/completions"

        logger.info(f"Sending check request to Fireworks AI using model {settings.FIREWORKS_MODEL}...")
        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                logger.error(f"Fireworks API error: {response.status_code} - {response.text}")
                raise ValueError(f"Fireworks API error: {response.text}")
            
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            
            logger.debug(f"Fireworks AI raw response: {content}")
            
            # Robust JSON cleaning/parsing
            if content.startswith("```"):
                lines = content.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()
            
            try:
                parsed = json.loads(content)
            except Exception as json_err:
                logger.warning(f"JSON parsing failed, trying manual extraction: {json_err}")
                # Regex/string extraction fallback
                is_phish_val = False
                if '"is_phishing": true' in content.lower() or '"is_phishing":true' in content.lower():
                    is_phish_val = True
                
                confidence_val = 0.5
                import re
                conf_match = re.search(r'"confidence":\s*([0-9.]+)', content)
                if conf_match:
                    try:
                        confidence_val = float(conf_match.group(1))
                    except:
                        pass
                        
                similar_match = re.search(r'"similar_to":\s*"([^"]*)"', content)
                similar_val = similar_match.group(1) if (similar_match and similar_match.group(1) != "null") else None
                
                analysis_match = re.search(r'"detailed_analysis":\s*"([^"]+)"', content)
                if analysis_match:
                    try:
                        analysis_val = analysis_match.group(1).encode().decode('unicode-escape', errors='ignore')
                    except Exception as dec_err:
                        logger.warning(f"Unicode decode failed: {dec_err}")
                        analysis_val = analysis_match.group(1)
                else:
                    analysis_val = "Обнаружены признаки фишинга при анализе ИИ." if is_phish_val else "Сайт признан безопасным ИИ."
                
                parsed = {
                    "is_phishing": is_phish_val,
                    "confidence": confidence_val,
                    "similar_to": similar_val,
                    "detailed_analysis": analysis_val
                }

            return {
                "is_phishing": bool(parsed.get("is_phishing", False)),
                "confidence": float(parsed.get("confidence", 0.0)),
                "similar_to": parsed.get("similar_to"),
                "detailed_analysis": parsed.get("detailed_analysis", "Анализ не предоставлен.")
            }
