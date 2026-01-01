"""
State definition for the evaluation graph.
"""

from typing import TypedDict, Optional, Dict, Any
from datetime import datetime


class CandidateInfo(TypedDict):
    """Information about the candidate being evaluated."""
    name: str
    current_level: str
    target_level: str
    years_experience: int
    level_expectations: str


class TokenMetadata(TypedDict):
    """Token usage tracking with input/output split."""
    primary_input: int
    primary_output: int
    challenge_input: int
    challenge_output: int
    final_input: int
    final_output: int
    decision_input: int  # NEW - for decision agent
    decision_output: int  # NEW - for decision agent
    total: int


class TimestampMetadata(TypedDict):
    """Execution timestamps."""
    start: str
    primary: str
    challenge: str
    final: str
    decision: str  # NEW - for decision agent


class EvaluationMetadata(TypedDict):
    """Metadata about the evaluation execution."""
    tokens: TokenMetadata
    timestamps: TimestampMetadata
    model_version: str
    cost_usd: float
    execution_time_seconds: float


class EvaluationState(TypedDict):
    """
    Complete state passed between graph nodes.
    """
    # Inputs (immutable)
    rubric: str  # Natural language rubric text
    transcript: str
    candidate_info: CandidateInfo

    # Outputs (mutable - updated by nodes)
    primary_evaluation: Optional[str]
    challenges: Optional[str]
    final_evaluation: Optional[str]
    decision: Optional[str]  # NEW - Final promotion decision from decision agent

    # Metadata
    metadata: EvaluationMetadata


def create_initial_state(
    rubric: str,
    transcript: str,
    candidate_info: Dict[str, Any]
) -> EvaluationState:
    """
    Create initial state for evaluation graph.

    Args:
        rubric: Natural language rubric text describing evaluation criteria
        transcript: Interview transcript text
        candidate_info: Dictionary containing candidate information
    """
    return EvaluationState(
        rubric=rubric,
        transcript=transcript,
        candidate_info=CandidateInfo(**candidate_info),
        primary_evaluation=None,
        challenges=None,
        final_evaluation=None,
        decision=None,  # NEW - Initialize as None
        metadata=EvaluationMetadata(
            tokens=TokenMetadata(
                primary_input=0,
                primary_output=0,
                challenge_input=0,
                challenge_output=0,
                final_input=0,
                final_output=0,
                decision_input=0,  # NEW
                decision_output=0,  # NEW
                total=0
            ),
            timestamps=TimestampMetadata(
                start=datetime.now().isoformat(),
                primary="",
                challenge="",
                final="",
                decision=""  # NEW
            ),
            model_version="",
            cost_usd=0.0,
            execution_time_seconds=0.0
        )
    )
