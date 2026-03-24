from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.models.database import init_db
from app.api.routes import router
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("screenshots", exist_ok=True)
    await init_db()
    yield

app = FastAPI(title="Phishing Detection API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")
app.include_router(router)
