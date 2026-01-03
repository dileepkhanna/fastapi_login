from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import os

from database import create_tables, init_db
from container import container
from routes import auth_router, job_router, api_router

# Create FastAPI app
app = FastAPI(
    title="Job Portal API",
    description="A FastAPI application for job role and skills management",
    version="1.0.0"
)

# Add session middleware with environment-based secret key
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Wire the dependency injection container
container.wire(modules=["routes"])

# Include routers
app.include_router(auth_router, tags=["Authentication"])
app.include_router(job_router, tags=["Job Management"])
app.include_router(api_router, tags=["API"])

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    create_tables()
    init_db()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Job Portal API is running"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)