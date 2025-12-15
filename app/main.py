import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.ws import router as ws_router
from app.database import engine
from app.database import Base


logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Support Chat Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(ws_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"app": "Support Chat Bot", "docs": "/docs", "health": "/health"}
