"""Health check endpoint."""

import os
from fastapi import APIRouter

from ...models.responses import HealthResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint.

    Returns:
        HealthResponse with system status and configuration
    """
    # Check if Azure OpenAI is configured
    azure_configured = bool(
        (os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_KEY")) and
        os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        azure_openai_configured=azure_configured
    )
