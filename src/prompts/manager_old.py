"""
Prompt version management - SINGLE SOURCE OF TRUTH in versions.json
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class PromptManager:
    """Manages prompt versions with versions.json as single source of truth."""

    def __init__(self):
        # Use absolute path relative to this file
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.versions_file = os.path.join(self.base_dir, "data", "prompts", "versions.json")
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create versions file if it doesn't exist."""
        os.makedirs(os.path.dirname(self.versions_file), exist_ok=True)

        if not os.path.exists(self.versions_file):
            # If file doesn't exist, create it with placeholder
            # In production, this file should already exist with full prompts
            print(f"⚠️ Creating {self.versions_file} - should contain full prompts")
            initial_data = {
                "rubric_structuring_agent": {
                    "active_version": "1",
                    "versions": [
                        {
                            "version": "1",
                            "created_at": datetime.now().isoformat(),
                            "notes": "Initial version",
                            "content": "[PROMPT CONTENT HERE]"
                        }
                    ]
                },
                "primary_agent": {
                    "active_version": "1",
                    "versions": [
                        {
                            "version": "1",
                            "created_at": datetime.now().isoformat(),
                            "notes": "Initial version",
                            "content": "[PROMPT CONTENT HERE]"
                        }
                    ]
                },
                "challenge_agent": {
                    "active_version": "1",
                    "versions": [
                        {
                            "version": "1",
                            "created_at": datetime.now().isoformat(),
                            "notes": "Initial version",
                            "content": "[PROMPT CONTENT HERE]"
                        }
                    ]
                },
                "decision_agent": {
                    "active_version": "1",
                    "versions": [
                        {
                            "version": "1",
                            "created_at": datetime.now().isoformat(),
                            "notes": "Initial version",
                            "content": "[PROMPT CONTENT HERE]"
                        }
                    ]
                }
            }

            with open(self.versions_file, "w") as f:
                json.dump(initial_data, f, indent=2)

    def _load_versions(self) -> Dict:
        """Load versions data from file."""
        with open(self.versions_file, "r") as f:
            return json.load(f)

    def _save_versions(self, data: Dict):
        """Save versions data to file."""
        with open(self.versions_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_active_prompt(self, prompt_type: str) -> str:
        """
        Get the active version of a prompt.

        Args:
            prompt_type: "rubric_structuring_agent", "primary_agent", "challenge_agent", or "decision_agent"

        Returns:
            Active prompt text
        """
        data = self._load_versions()
        active_version = data[prompt_type]["active_version"]

        for version in data[prompt_type]["versions"]:
            if version["version"] == active_version:
                return version["content"]

        raise ValueError(f"Active version {active_version} not found")

    def get_all_versions(self, prompt_type: str) -> List[Dict]:
        """Get all versions of a prompt."""
        data = self._load_versions()
        return data[prompt_type]["versions"]

    def get_version(self, prompt_type: str, version: str) -> Dict:
        """Get a specific version."""
        data = self._load_versions()

        for v in data[prompt_type]["versions"]:
            if v["version"] == version:
                return v

        raise ValueError(f"Version {version} not found")

    def save_new_version(
        self,
        prompt_type: str,
        content: str,
        notes: str,
        set_active: bool = False
    ) -> str:
        """
        Save a new prompt version.

        Args:
            prompt_type: "rubric_structuring_agent", "primary_agent", "challenge_agent", or "decision_agent"
            content: Prompt text
            notes: Version notes
            set_active: Whether to set as active version

        Returns:
            New version number (integer as string)
        """
        data = self._load_versions()

        # Generate new version number (simple integer increment)
        existing_versions = [int(v["version"]) for v in data[prompt_type]["versions"]]
        new_version = str(max(existing_versions) + 1)

        # Create new version entry
        new_entry = {
            "version": new_version,
            "created_at": datetime.now().isoformat(),
            "notes": notes,
            "content": content
        }

        # Add to versions list
        data[prompt_type]["versions"].append(new_entry)

        # Set as active if requested
        if set_active:
            data[prompt_type]["active_version"] = new_version

        self._save_versions(data)
        return new_version

    def set_active_version(self, prompt_type: str, version: str):
        """Set a version as active."""
        data = self._load_versions()

        # Verify version exists
        if not any(v["version"] == version for v in data[prompt_type]["versions"]):
            raise ValueError(f"Version {version} not found")

        data[prompt_type]["active_version"] = version
        self._save_versions(data)

    def delete_version(self, prompt_type: str, version: str):
        """Delete a version (cannot delete active)."""
        data = self._load_versions()

        if version == data[prompt_type]["active_version"]:
            raise ValueError("Cannot delete active version")

        data[prompt_type]["versions"] = [
            v for v in data[prompt_type]["versions"]
            if v["version"] != version
        ]

        self._save_versions(data)
