"""Response models for the Interview Agent API."""

from typing import Optional, Literal, Dict, Any
from pydantic import BaseModel, Field
from .requests import CandidateInfo


class TokenMetadata(BaseModel):
    """Token usage metadata."""

    primary_evaluator_input: int = 0
    primary_evaluator_output: int = 0
    challenge_agent_input: int = 0
    challenge_agent_output: int = 0
    decision_agent_input: int = 0
    decision_agent_output: int = 0
    total_input: int = 0
    total_output: int = 0
    total: int = 0


class TimestampMetadata(BaseModel):
    """Timestamps for each evaluation step."""

    start: Optional[str] = None
    primary_evaluator: Optional[str] = None
    challenge_agent: Optional[str] = None
    decision_agent: Optional[str] = None


class EvaluationMetadata(BaseModel):
    """Metadata for the evaluation."""

    tokens: TokenMetadata
    timestamps: TimestampMetadata
    execution_time_seconds: float = 0.0
    cost_usd: float = 0.0
    model_version: str = "gpt-4o"


class EvaluationResult(BaseModel):
    """Complete evaluation result."""

    candidate_info: CandidateInfo
    primary_evaluation: str
    challenges: str
    final_evaluation: str
    decision: str
    metadata: EvaluationMetadata


class EvaluationResponse(BaseModel):
    """Response for evaluation endpoints."""

    evaluation_id: str = Field(..., description="Unique evaluation identifier")
    status: Literal["pending", "processing", "completed", "failed"] = Field(..., description="Current status")
    current_step: Optional[Literal["primary_evaluator", "challenge_agent", "decision_agent"]] = None
    progress_percentage: int = Field(0, ge=0, le=100, description="Progress percentage (0-100)")
    result: Optional[EvaluationResult] = None
    error: Optional[str] = None
    created_at: str = Field(..., description="ISO timestamp when evaluation was created")
    completed_at: Optional[str] = None
    websocket_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "evaluation_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "processing",
                "current_step": "challenge_agent",
                "progress_percentage": 50,
                "result": None,
                "error": None,
                "created_at": "2026-01-06T10:30:00Z",
                "completed_at": None,
                "websocket_url": "ws://localhost:8000/ws/evaluations/550e8400-e29b-41d4-a716-446655440000"
            }
        }


class EvaluationListItem(BaseModel):
    """Summary item for evaluation list."""

    evaluation_id: str
    candidate_name: str
    status: Literal["pending", "processing", "completed", "failed"]
    created_at: str
    completed_at: Optional[str] = None


class EvaluationListResponse(BaseModel):
    """Response for listing evaluations."""

    evaluations: list[EvaluationListItem]
    total: int
    limit: int
    offset: int


class HealthResponse(BaseModel):
    """Health check response."""

    status: Literal["healthy", "unhealthy"]
    version: str = "1.0.0"
    azure_openai_configured: bool
