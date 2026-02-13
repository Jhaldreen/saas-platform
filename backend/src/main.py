from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SaaS Platform API",
    description="Multi-tenant SaaS Platform Backend",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to SaaS Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/docs")
async def docs_redirect():
    return {"message": "API documentation available at /docs"}