"""
Prompt version management - File-based system (V2)

Prompts stored as separate files, versions.json only contains metadata.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class PromptManager:
    """Manages prompt versions with file-based storage."""

    def __init__(self):
        # Use absolute path relative to this file
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.prompts_dir = os.path.join(self.base_dir, "data", "prompts")
        self.versions_file = os.path.join(self.prompts_dir, "versions.json")
        self._ensure_structure()

    def _ensure_structure(self):
        """Create directory structure if it doesn't exist."""
        os.makedirs(self.prompts_dir, exist_ok=True)

        if not os.path.exists(self.versions_file):
            # Create minimal versions.json with file references
            print(f"⚠️ Creating {self.versions_file} with file-based references")
            initial_data = {
                "primary_agent": {
                    "active_version": "1",
                    "versions": [
                        {
                            "version": "1",
                            "created_at": datetime.now().isoformat(),
                            "notes": "Initial version",
                            "file": "primary_agent_v1.txt"
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
                            "file": "challenge_agent_v1.txt"
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
                            "file": "decision_agent_v1.txt"
                        }
                    ]
                }
            }

            with open(self.versions_file, "w") as f:
                json.dump(initial_data, f, indent=2)

    def _load_versions(self) -> Dict:
        """Load versions metadata from file."""
        with open(self.versions_file, "r") as f:
            return json.load(f)

    def _save_versions(self, data: Dict):
        """Save versions metadata to file."""
        with open(self.versions_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_prompt_content(self, file_path: str) -> str:
        """Load prompt content from file."""
        full_path = os.path.join(self.prompts_dir, file_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Prompt file not found: {full_path}")

        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def get_active_prompt(self, prompt_type: str) -> str:
        """
        Get the active version of a prompt.

        Args:
            prompt_type: "primary_agent", "challenge_agent", or "decision_agent"

        Returns:
            Active prompt text
        """
        data = self._load_versions()
        active_version = data[prompt_type]["active_version"]

        for version in data[prompt_type]["versions"]:
            if version["version"] == active_version:
                # Load content from file
                return self._load_prompt_content(version["file"])

        raise ValueError(f"Active version {active_version} not found")

    def get_all_versions(self, prompt_type: str) -> List[Dict]:
        """Get all versions metadata (without content) for a prompt."""
        data = self._load_versions()
        return data[prompt_type]["versions"]

    def get_version(self, prompt_type: str, version: str) -> Dict:
        """Get a specific version with content."""
        data = self._load_versions()

        for v in data[prompt_type]["versions"]:
            if v["version"] == version:
                # Load content from file
                content = self._load_prompt_content(v["file"])
                return {**v, "content": content}

        raise ValueError(f"Version {version} not found")

    def save_new_version(
        self,
        prompt_type: str,
        content: str,
        notes: str,
        set_active: bool = False,
        filename: Optional[str] = None
    ) -> str:
        """
        Save a new prompt version.

        Args:
            prompt_type: "primary_agent", "challenge_agent", or "decision_agent"
            content: Prompt text
            notes: Version notes
            set_active: Whether to set as active version
            filename: Optional custom filename (defaults to {prompt_type}_v{N}.txt)

        Returns:
            New version number (integer as string)
        """
        data = self._load_versions()

        # Generate new version number
        existing_versions = [int(v["version"]) for v in data[prompt_type]["versions"]]
        new_version = str(max(existing_versions) + 1)

        # Generate filename if not provided
        if filename is None:
            filename = f"{prompt_type}_v{new_version}.txt"

        # Save content to file
        file_path = os.path.join(self.prompts_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # Create new version entry (metadata only)
        new_entry = {
            "version": new_version,
            "created_at": datetime.now().isoformat(),
            "notes": notes,
            "file": filename
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

    def delete_version(self, prompt_type: str, version: str, delete_file: bool = False):
        """
        Delete a version (cannot delete active).

        Args:
            prompt_type: Agent type
            version: Version to delete
            delete_file: If True, also delete the prompt file from disk
        """
        data = self._load_versions()

        if version == data[prompt_type]["active_version"]:
            raise ValueError("Cannot delete active version")

        # Find the version to get filename
        version_entry = None
        for v in data[prompt_type]["versions"]:
            if v["version"] == version:
                version_entry = v
                break

        if not version_entry:
            raise ValueError(f"Version {version} not found")

        # Delete file if requested
        if delete_file and "file" in version_entry:
            file_path = os.path.join(self.prompts_dir, version_entry["file"])
            if os.path.exists(file_path):
                os.remove(file_path)

        # Remove from versions list
        data[prompt_type]["versions"] = [
            v for v in data[prompt_type]["versions"]
            if v["version"] != version
        ]

        self._save_versions(data)

    def update_prompt_content(self, prompt_type: str, version: str, new_content: str):
        """
        Update the content of an existing prompt version.

        Args:
            prompt_type: Agent type
            version: Version to update
            new_content: New prompt content
        """
        data = self._load_versions()

        # Find version
        version_entry = None
        for v in data[prompt_type]["versions"]:
            if v["version"] == version:
                version_entry = v
                break

        if not version_entry:
            raise ValueError(f"Version {version} not found")

        # Update file content
        file_path = os.path.join(self.prompts_dir, version_entry["file"])
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✓ Updated {prompt_type} v{version} ({version_entry['file']})")
