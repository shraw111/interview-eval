"""WebSocket endpoints for real-time evaluation streaming."""

import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .manager import websocket_manager


router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/ws/evaluations/{evaluation_id}")
async def websocket_evaluation_stream(websocket: WebSocket, evaluation_id: str):
    """WebSocket endpoint for streaming evaluation progress.

    Args:
        websocket: FastAPI WebSocket connection
        evaluation_id: Unique identifier for the evaluation

    This endpoint:
    1. Accepts WebSocket connection
    2. Streams real-time progress events as the evaluation runs
    3. Handles client disconnection gracefully
    """
    await websocket_manager.connect(websocket, evaluation_id)

    try:
        # Keep connection alive - just wait for disconnect
        # The manager broadcasts events to all connected clients
        while True:
            try:
                # Wait for client message or disconnect (with 30s timeout)
                await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                # Send heartbeat to keep connection alive
                await websocket_manager.send_heartbeat(evaluation_id)

    except WebSocketDisconnect:
        # Normal disconnect - no logging needed
        pass
    except Exception as e:
        logger.error(f"WebSocket error for evaluation {evaluation_id}: {e}")
    finally:
        # Clean up connection
        await websocket_manager.disconnect(websocket, evaluation_id)
