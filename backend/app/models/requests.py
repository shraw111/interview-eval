"""Request models for the Interview Agent API."""

from typing import Optional
from pydantic import BaseModel, Field


class CandidateInfo(BaseModel):
    """Candidate information for evaluation."""

    name: str = Field(..., min_length=1, description="Candidate's full name")
    current_level: Optional[str] = Field(None, description="Current role level (e.g., L5 PM) - optional, useful for promotions")
    target_level: Optional[str] = Field(None, description="Target role level (e.g., L6 Senior PM) - optional, useful for promotions")
    years_experience: Optional[int] = Field(None, ge=0, le=50, description="Years of experience at current level - optional")
    level_expectations: Optional[str] = Field(None, description="Expectations for target level - optional, useful for level transitions")


class CreateEvaluationRequest(BaseModel):
    """Request to create a new evaluation."""

    candidate_info: CandidateInfo = Field(..., description="Candidate information")
    rubric: str = Field(..., min_length=50, description="Natural language evaluation criteria")
    transcript: str = Field(..., min_length=100, description="Interview transcript")

    class Config:
        json_schema_extra = {
            "example": {
                "candidate_info": {
                    "name": "Sarah Chen",
                    "current_level": "L5 PM",
                    "target_level": "L6 Senior PM",
                    "years_experience": 3,
                    "level_expectations": "Expected to demonstrate strategic thinking, cross-team influence, and execution at scale."
                },
                "rubric": "## Strategic Thinking\n- Demonstrates long-term vision beyond immediate roadmap\n\n## Leadership\n- Evidence of influencing without authority",
                "transcript": "[Detailed interview transcript content...]"
            }
        }
