import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database import AsyncSessionLocal, LegitimateSite, init_db
from app.services.screenshot import ScreenshotService
from app.services.similarity.phash import PHashSimilarity
from app.services.similarity.cnn import cnn_similarity

async def seed_legitimate_sites():
    await init_db()
    
    brands = [
        {"domain": "github.com", "url": "https://github.com/login"},
        {"domain": "google.com", "url": "https://accounts.google.com/"},
    ]

    async with AsyncSessionLocal() as session:
        for brand in brands:
            print(f"[*] Processing seed for {brand['domain']}...")
            try:
                # 1. Take a screenshot
                print(f" -> Capturing screenshot for {brand['domain']}...")
                screenshot_path = await ScreenshotService.capture(brand['url'])
                
                # 2. Extract features
                print(" -> Calculating CNN features and pHash...")
                features = cnn_similarity.extract_features(screenshot_path)
                phash_val = PHashSimilarity.compute_hash(screenshot_path)
                
                # 3. Save to DB
                new_site = LegitimateSite(
                    domain=brand['domain'],
                    screenshot_path=screenshot_path,
                    phash=phash_val,
                    features=features
                )
                session.add(new_site)
                await session.commit()
                print(f"[+] Successfully saved {brand['domain']} to database!\n")
                
            except Exception as e:
                print(f"[!] Error processing {brand['domain']}: {e}\n")
                await session.rollback()

if __name__ == "__main__":
    asyncio.run(seed_legitimate_sites())
