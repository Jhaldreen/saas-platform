from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .infrastructure.database import init_db
from .infrastructure.api.routes import auth

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="AI Cloud Cost Auditor - Hexagonal Architecture",
    description="Multi-tenant SaaS with Clean Architecture",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

# NOTE: Add more routers here:
# from .infrastructure.api.routes import organizations, audits, rules
# app.include_router(organizations.router)
# app.include_router(audits.router)
# app.include_router(rules.router)


@app.get("/")
async def root():
    return {
        "message": "AI Cloud Cost Auditor API - Hexagonal Architecture",
        "version": "1.0.0",
        "architecture": "Clean/Hexagonal"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
