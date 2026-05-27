from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import func
from app.models.database import get_db, Check, LegitimateSite
from app.services.screenshot import ScreenshotService
from app.services.detector import PhishingDetector
from loguru import logger
from datetime import datetime

router = APIRouter()

class CheckRequest(BaseModel):
    url: str

class CheckResponse(BaseModel):
    url: str
    is_phishing: bool
    confidence: float
    similar_to: str | None
    scores: dict
    screenshot_url: str
    original_screenshot_url: str | None
    detailed_analysis: str

class HistoryItem(BaseModel):
    id: int
    url: str
    screenshot_path: str
    result: str
    is_phishing: bool
    confidence: float
    similar_to: str | None
    detailed_analysis: str | None
    checked_at: datetime

    class Config:
        from_attributes = True

@router.post("/check", response_model=CheckResponse)
async def check_url_endpoint(req: CheckRequest, db: AsyncSession = Depends(get_db)):
    try:
        screenshot_path = await ScreenshotService.capture(req.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    result = await db.execute(select(LegitimateSite))
    legit_sites = result.scalars().all()
    
    if not legit_sites:
        return CheckResponse(
            url=req.url,
            is_phishing=False,
            confidence=0.0,
            similar_to=None,
            scores={"phash": 0.0, "ssim": 0.0, "cnn": 0.0},
            screenshot_url=f"http://localhost:8000/{screenshot_path}" if screenshot_path else "",
            original_screenshot_url=None
        )
        
    best_match = None
    highest_confidence = 0.0
    best_scores = {"phash": 0.0, "ssim": 0.0, "cnn": 0.0}
    is_phishing = False
    
    for site in legit_sites:
        try:
            eval_result = PhishingDetector.evaluate_similarity(
                screenshot_path,
                site.screenshot_path,
                site.features,
                site.phash
            )
            
            if eval_result["confidence"] > highest_confidence:
                highest_confidence = eval_result["confidence"]
                best_match = site.domain
                best_scores = eval_result["scores"]
                is_phishing = eval_result["is_phishing"]
        except Exception as e:
            logger.error(f"Error evaluating against {site.domain}: {e}")
            continue

    # Strict check using Fireworks AI (Kimi multimodal)
    try:
        ai_result = await PhishingDetector.evaluate_with_ai(
            target_screenshot=screenshot_path,
            target_url=req.url,
            legit_sites=legit_sites,
            best_match_brand=best_match,
            best_scores=best_scores
        )
        is_phishing = ai_result["is_phishing"]
        highest_confidence = ai_result["confidence"]
        best_match = ai_result["similar_to"]
        detailed_text = ai_result["detailed_analysis"]
    except Exception as ai_err:
        logger.error(f"AI evaluation failed: {ai_err}. Falling back to default heuristics.")
        def generate_analysis(url_val, is_phish, conf, sim_to, cnn_s):
            if is_phish:
                score_pct = round((cnn_s or 0) * 100)
                return f'The URL "{url_val}" failed the deep visual inspection. Our neural network detected structural and conceptual similarities (CNN Score: {score_pct}%) with the legitimate brand "{sim_to}". Combined with perceptual and pixel-level checks, this strongly indicates a phishing spoof. Do not enter any sensitive information here.'
            elif conf == 0:
                return f'The URL "{url_val}" has fully passed the visual inspection. Deep CNN features and layout perceptual hashes show no resemblance to any protected brands in our database. The system concludes this layout is unique and safe from known templates.'
            else:
                return f'The URL "{url_val}" has been marked as SAFE. While there were minor structural similarities to some protected interfaces ({round(conf * 100)}% confidence), it did not surpass the multi-factor heuristic threshold required to trigger a phishing alert.'

        detailed_text = generate_analysis(
            req.url, 
            is_phishing, 
            highest_confidence, 
            best_match if is_phishing else None, 
            best_scores.get("cnn", 0.0)
        )

    # Find the legitimate site's screenshot path for UI side-by-side comparison
    legit_screenshot_path = None
    if is_phishing and best_match:
        for site in legit_sites:
            if site.domain.lower() == best_match.lower():
                legit_screenshot_path = site.screenshot_path
                break

    new_check = Check(
        url=req.url,
        screenshot_path=screenshot_path,
        result="Phishing" if is_phishing else "Legitimate",
        confidence=highest_confidence,
        similar_to=best_match if is_phishing else None,
        detailed_analysis=detailed_text
    )
    db.add(new_check)
    await db.commit()
    
    return CheckResponse(
        url=req.url,
        is_phishing=is_phishing,
        confidence=highest_confidence,
        similar_to=best_match if is_phishing else None,
        scores=best_scores,
        screenshot_url=f"http://localhost:8000/{screenshot_path}" if screenshot_path else "",
        original_screenshot_url=f"http://localhost:8000/{legit_screenshot_path}" if is_phishing and legit_screenshot_path else None,
        detailed_analysis=detailed_text
    )

@router.get("/history", response_model=list[HistoryItem])
async def get_history(limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Check).order_by(Check.created_at.desc()).limit(limit))
    checks = result.scalars().all()
    
    history_items = []
    for check in checks:
        history_items.append(HistoryItem(
            id=check.id,
            url=check.url,
            screenshot_path=check.screenshot_path,
            result=check.result,
            is_phishing=(check.result == "Phishing"),
            confidence=check.confidence,
            similar_to=check.similar_to,
            detailed_analysis=check.detailed_analysis,
            checked_at=check.created_at
        ))
    return history_items

@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    total_checks = await db.scalar(select(func.count(Check.id)))
    phishing_found = await db.scalar(select(func.count(Check.id)).where(Check.result == "Phishing"))
    
    return {
        "total_checks": total_checks or 0,
        "phishing_detected": phishing_found or 0,
        "legitimate": (total_checks or 0) - (phishing_found or 0)
    }
