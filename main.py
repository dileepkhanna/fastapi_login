from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from database import create_tables, init_db
from container import container
from routes import auth_router, job_router, api_router

app = FastAPI()

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Wire the container
container.wire(modules=["routes"])

# Include routers
app.include_router(auth_router)
app.include_router(job_router)
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    create_tables()
    init_db()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)