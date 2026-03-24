import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, JSON, DateTime, ForeignKey, Column
from datetime import datetime
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class LegitimateSite(Base):
    __tablename__ = "legitimate_sites"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    domain: Mapped[str] = mapped_column(String, unique=True, index=True)
    screenshot_path: Mapped[str] = mapped_column(String)
    phash: Mapped[str] = mapped_column(String)
    features: Mapped[list] = mapped_column(JSON)
    
class Check(Base):
    __tablename__ = "checks"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String, index=True)
    screenshot_path: Mapped[str] = mapped_column(String)
    result: Mapped[str] = mapped_column(String) 
    confidence: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
class Match(Base):
    __tablename__ = "matches"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    check_id: Mapped[int] = mapped_column(Integer, ForeignKey("checks.id"))
    legitimate_id: Mapped[int] = mapped_column(Integer, ForeignKey("legitimate_sites.id"))
    similarity_score: Mapped[float] = mapped_column(Float)
    method: Mapped[str] = mapped_column(String)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
