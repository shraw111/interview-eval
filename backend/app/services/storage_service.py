"""In-memory storage service for evaluations."""

from typing import Dict, Optional
from datetime import datetime, timedelta
import asyncio


class StorageService:
    """Simple in-memory storage for evaluation data.

    In production, this should be replaced with Redis or a database.
    Thread-safe using asyncio.Lock for concurrent access.
    """

    def __init__(self, ttl_hours: int = 24):
        """Initialize storage with optional TTL for cleanup.

        Args:
            ttl_hours: Time-to-live in hours for stored evaluations
        """
        self._storage: Dict[str, dict] = {}
        self._lock = asyncio.Lock()
        self._ttl_hours = ttl_hours

    async def save(self, evaluation_id: str, data: dict) -> None:
        """Save or update evaluation data.

        Args:
            evaluation_id: Unique identifier for the evaluation
            data: Evaluation data to store
        """
        async with self._lock:
            data["last_updated"] = datetime.now().isoformat()
            self._storage[evaluation_id] = data

    async def get(self, evaluation_id: str) -> Optional[dict]:
        """Retrieve evaluation data by ID.

        Args:
            evaluation_id: Unique identifier for the evaluation

        Returns:
            Evaluation data if found, None otherwise
        """
        async with self._lock:
            return self._storage.get(evaluation_id)

    async def list_all(self, limit: int = 20, offset: int = 0) -> tuple[list[dict], int]:
        """List all evaluations with pagination.

        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            Tuple of (evaluation list, total count)
        """
        async with self._lock:
            all_evals = list(self._storage.values())
            # Sort by created_at descending
            all_evals.sort(
                key=lambda x: x.get("created_at", ""),
                reverse=True
            )
            total = len(all_evals)
            paginated = all_evals[offset:offset + limit]
            return paginated, total

    async def delete(self, evaluation_id: str) -> bool:
        """Delete an evaluation by ID.

        Args:
            evaluation_id: Unique identifier for the evaluation

        Returns:
            True if deleted, False if not found
        """
        async with self._lock:
            if evaluation_id in self._storage:
                del self._storage[evaluation_id]
                return True
            return False

    async def cleanup_expired(self) -> int:
        """Remove evaluations older than TTL.

        Returns:
            Number of evaluations deleted
        """
        cutoff_time = datetime.now() - timedelta(hours=self._ttl_hours)
        deleted_count = 0

        async with self._lock:
            expired_ids = []
            for eval_id, data in self._storage.items():
                created_at_str = data.get("created_at")
                if created_at_str:
                    try:
                        created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                        if created_at < cutoff_time:
                            expired_ids.append(eval_id)
                    except (ValueError, AttributeError):
                        pass

            for eval_id in expired_ids:
                del self._storage[eval_id]
                deleted_count += 1

        return deleted_count

    async def get_stats(self) -> dict:
        """Get storage statistics.

        Returns:
            Dictionary with storage stats
        """
        async with self._lock:
            status_counts = {}
            for data in self._storage.values():
                status = data.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1

            return {
                "total_evaluations": len(self._storage),
                "status_counts": status_counts
            }


# Global instance (singleton pattern)
storage = StorageService()
