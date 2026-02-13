from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.v1 import api_router
from backend.src.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the SaaS Platform API!"}