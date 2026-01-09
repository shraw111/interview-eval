"""WebSocket connection manager for real-time evaluation streaming."""

import json
import logging
from typing import Dict, Set
from fastapi import WebSocket
from datetime import datetime
import asyncio


logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections for real-time evaluation updates."""

    def __init__(self):
        """Initialize the WebSocket manager."""
        # Map evaluation_id to set of connected WebSocket clients
        self.connections: Dict[str, Set[WebSocket]] = {}
        # Lock for thread-safe connection management
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, evaluation_id: str):
        """Accept a new WebSocket connection.

        Args:
            websocket: FastAPI WebSocket instance
            evaluation_id: ID of the evaluation to subscribe to
        """
        await websocket.accept()

        # Add to connections with lock
        async with self._lock:
            if evaluation_id not in self.connections:
                self.connections[evaluation_id] = set()
            self.connections[evaluation_id].add(websocket)

        # Send connection confirmed event
        await websocket.send_json({
            "type": "connected",
            "evaluation_id": evaluation_id,
            "timestamp": datetime.now().isoformat()
        })

        logger.info(f"WebSocket connected for evaluation {evaluation_id}")

    async def disconnect(self, websocket: WebSocket, evaluation_id: str):
        """Remove a WebSocket connection.

        Args:
            websocket: FastAPI WebSocket instance
            evaluation_id: ID of the evaluation
        """
        async with self._lock:
            if evaluation_id in self.connections:
                self.connections[evaluation_id].discard(websocket)

                # Clean up empty sets
                if not self.connections[evaluation_id]:
                    del self.connections[evaluation_id]
                    logger.info(f"All WebSocket connections closed for evaluation {evaluation_id}")

    async def broadcast(self, evaluation_id: str, message: dict):
        """Broadcast a message to all connected clients for an evaluation.

        Args:
            evaluation_id: ID of the evaluation
            message: Message data to broadcast
        """
        # Get copy of connections with lock
        async with self._lock:
            if evaluation_id not in self.connections:
                return
            connections = self.connections[evaluation_id].copy()

        # Send to all connected clients (outside lock to avoid blocking)
        disconnected = []
        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception as e:
                # Log specific error and mark for removal
                logger.warning(f"Failed to send message to WebSocket client: {e}")
                disconnected.append(websocket)

        # Clean up disconnected clients
        for websocket in disconnected:
            await self.disconnect(websocket, evaluation_id)

    async def send_heartbeat(self, evaluation_id: str):
        """Send heartbeat to keep connections alive.

        Args:
            evaluation_id: ID of the evaluation
        """
        await self.broadcast(evaluation_id, {
            "type": "heartbeat",
            "timestamp": datetime.now().isoformat()
        })

    def get_connection_count(self, evaluation_id: str) -> int:
        """Get number of active connections for an evaluation.

        Args:
            evaluation_id: ID of the evaluation

        Returns:
            Number of active connections
        """
        return len(self.connections.get(evaluation_id, set()))


# Global instance (singleton pattern)
websocket_manager = WebSocketManager()
