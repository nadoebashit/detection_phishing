from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import func
from app.models.database import get_db, Check, LegitimateSite
from app.services.screenshot import ScreenshotService
from app.services.detector import PhishingDetector
from loguru import logger

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
            
    new_check = Check(
        url=req.url,
        screenshot_path=screenshot_path,
        result="Phishing" if is_phishing else "Legitimate",
        confidence=highest_confidence
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
        original_screenshot_url=f"http://localhost:8000/{best_match.screenshot_path}" if is_phishing and best_match else None
    )

@router.get("/history")
async def get_history(limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Check).order_by(Check.created_at.desc()).limit(limit))
    return result.scalars().all()

@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    total_checks = await db.scalar(select(func.count(Check.id)))
    phishing_found = await db.scalar(select(func.count(Check.id)).where(Check.result == "Phishing"))
    
    return {
        "total_checks": total_checks or 0,
        "phishing_detected": phishing_found or 0,
        "legitimate": (total_checks or 0) - (phishing_found or 0)
    }
