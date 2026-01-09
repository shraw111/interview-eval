"""Main FastAPI application for Interview Agent backend."""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load .env from parent directory (project root)
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

from .api.routes import evaluations, health
from .api.websocket import evaluation_stream
from .api.websocket.manager import websocket_manager
from .services.evaluation_service import evaluation_service


# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Interview Agent API",
    description="REST API and WebSocket server for AI-powered interview evaluations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Wire up WebSocket manager to evaluation service
evaluation_service.set_websocket_manager(websocket_manager)


# Include REST API routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(evaluations.router, prefix="/api/v1")

# Include WebSocket router
app.include_router(evaluation_stream.router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("Interview Agent API started")
    print("API docs: http://localhost:8000/docs")
    print("WebSocket: ws://localhost:8000/ws/evaluations/{evaluation_id}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print("Interview Agent API shutting down")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Interview Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
