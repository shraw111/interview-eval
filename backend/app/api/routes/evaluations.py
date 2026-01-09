"""REST API endpoints for evaluations."""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import List

from ...models.requests import CreateEvaluationRequest
from ...models.responses import (
    EvaluationResponse,
    EvaluationListResponse,
    EvaluationListItem
)
from ...services.evaluation_service import evaluation_service


router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("/", response_model=EvaluationResponse, status_code=202)
async def create_evaluation(
    request: CreateEvaluationRequest,
    background_tasks: BackgroundTasks
):
    """Create a new evaluation and start processing.

    This endpoint:
    1. Validates the evaluation request
    2. Creates a unique evaluation ID
    3. Starts the LangGraph evaluation in the background
    4. Returns immediately with the evaluation ID and WebSocket URL

    The client should connect to the WebSocket URL to receive real-time progress updates.

    Args:
        request: Evaluation request with candidate info, rubric, and transcript
        background_tasks: FastAPI background tasks handler

    Returns:
        EvaluationResponse with ID, status, and WebSocket URL
    """
    return await evaluation_service.create_evaluation(request, background_tasks)


@router.get("/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation(evaluation_id: str):
    """Get evaluation status and results by ID.

    This endpoint returns:
    - Current status (pending, processing, completed, failed)
    - Progress percentage (0-100)
    - Results (if completed)
    - Error message (if failed)

    Args:
        evaluation_id: Unique identifier for the evaluation

    Returns:
        EvaluationResponse with current status and results

    Raises:
        HTTPException: 404 if evaluation not found
    """
    evaluation = await evaluation_service.get_evaluation(evaluation_id)

    if not evaluation:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation {evaluation_id} not found"
        )

    return evaluation


@router.get("/", response_model=EvaluationListResponse)
async def list_evaluations(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """List all evaluations with pagination.

    Args:
        limit: Maximum number of results to return (1-100)
        offset: Number of results to skip for pagination

    Returns:
        EvaluationListResponse with list of evaluations and total count
    """
    items, total = await evaluation_service.list_evaluations(limit, offset)

    return EvaluationListResponse(
        evaluations=items,
        total=total,
        limit=limit,
        offset=offset
    )
