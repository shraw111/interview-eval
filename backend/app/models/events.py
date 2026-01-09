"""WebSocket event models for real-time evaluation streaming."""

from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


class BaseWebSocketEvent(BaseModel):
    """Base model for all WebSocket events."""

    type: str
    timestamp: str


class ConnectedEvent(BaseWebSocketEvent):
    """Event sent when WebSocket connection is established."""

    type: Literal["connected"] = "connected"
    evaluation_id: str


class EvaluationStartedEvent(BaseWebSocketEvent):
    """Event sent when evaluation starts."""

    type: Literal["evaluation_started"] = "evaluation_started"
    evaluation_id: str


class NodeStartedEvent(BaseWebSocketEvent):
    """Event sent when a graph node starts processing."""

    type: Literal["node_started"] = "node_started"
    node: Literal["primary_evaluator", "challenge_agent", "decision_agent"]
    progress_percentage: int = Field(..., ge=0, le=100)


class NodeCompletedEvent(BaseWebSocketEvent):
    """Event sent when a graph node completes processing."""

    type: Literal["node_completed"] = "node_completed"
    node: Literal["primary_evaluator", "challenge_agent", "decision_agent"]
    progress_percentage: int = Field(..., ge=0, le=100)
    output_preview: Optional[str] = Field(None, description="First 200 chars of output")
    tokens: Optional[Dict[str, int]] = Field(None, description="Token usage for this node")


class EvaluationCompletedEvent(BaseWebSocketEvent):
    """Event sent when evaluation completes successfully."""

    type: Literal["evaluation_completed"] = "evaluation_completed"
    evaluation_id: str
    result: Dict[str, Any]


class ErrorEvent(BaseWebSocketEvent):
    """Event sent when an error occurs."""

    type: Literal["error"] = "error"
    error: str
    node: Optional[str] = None


class HeartbeatEvent(BaseWebSocketEvent):
    """Event sent periodically to keep connection alive."""

    type: Literal["heartbeat"] = "heartbeat"


# Union type for all events
WebSocketEvent = (
    ConnectedEvent
    | EvaluationStartedEvent
    | NodeStartedEvent
    | NodeCompletedEvent
    | EvaluationCompletedEvent
    | ErrorEvent
    | HeartbeatEvent
)
