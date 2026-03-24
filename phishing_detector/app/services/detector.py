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
