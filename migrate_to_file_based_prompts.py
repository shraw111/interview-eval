"""
Migration script: Convert embedded prompts to file-based system

This script:
1. Reads existing versions.json with embedded prompt content
2. Extracts each prompt to separate files
3. Creates new versions.json with file references only
4. Backs up original versions.json
"""

import json
import os
import shutil
from datetime import datetime


def migrate_prompts():
    """Migrate from embedded to file-based prompt storage."""

    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_dir = os.path.join(base_dir, "data", "prompts")
    versions_file = os.path.join(prompts_dir, "versions.json")
    backup_file = os.path.join(prompts_dir, f"versions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    print("="*60)
    print("PROMPT MIGRATION: Embedded -> File-Based")
    print("="*60)

    # Step 1: Backup existing versions.json
    print("\n[1/4] Backing up existing versions.json...")
    if os.path.exists(versions_file):
        shutil.copy2(versions_file, backup_file)
        print(f"OK Backed up to: {os.path.basename(backup_file)}")
    else:
        print("!  versions.json not found - nothing to migrate")
        return

    # Step 2: Load existing data
    print("\n[2/4] Loading existing prompts...")
    with open(versions_file, "r", encoding="utf-8") as f:
        old_data = json.load(f)

    prompt_types = ["primary_agent", "challenge_agent", "decision_agent"]
    total_prompts = sum(len(old_data.get(pt, {}).get("versions", [])) for pt in prompt_types)
    print(f"OK Found {total_prompts} prompts to migrate")

    # Step 3: Extract prompts to files
    print("\n[3/4] Extracting prompts to separate files...")

    new_data = {}
    files_created = 0

    for prompt_type in prompt_types:
        if prompt_type not in old_data:
            continue

        print(f"\n  Processing {prompt_type}...")

        agent_data = old_data[prompt_type]
        new_versions = []

        for version_entry in agent_data["versions"]:
            version = version_entry["version"]
            content = version_entry.get("content", "")

            # Generate filename
            filename = f"{prompt_type}_v{version}.txt"
            file_path = os.path.join(prompts_dir, filename)

            # Write content to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"    OK Created {filename} ({len(content)} chars)")
            files_created += 1

            # Create new metadata entry (without content)
            new_version_entry = {
                "version": version,
                "created_at": version_entry.get("created_at", datetime.now().isoformat()),
                "notes": version_entry.get("notes", ""),
                "file": filename
            }
            new_versions.append(new_version_entry)

        # Store new structure
        new_data[prompt_type] = {
            "active_version": agent_data["active_version"],
            "versions": new_versions
        }

    print(f"\nOK Created {files_created} prompt files")

    # Step 4: Write new versions.json
    print("\n[4/4] Writing new versions.json (file-based)...")

    with open(versions_file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2)

    # Calculate size reduction
    old_size = os.path.getsize(backup_file)
    new_size = os.path.getsize(versions_file)
    reduction = ((old_size - new_size) / old_size) * 100

    print(f"OK New versions.json written")
    print(f"  Old size: {old_size:,} bytes")
    print(f"  New size: {new_size:,} bytes")
    print(f"  Reduction: {reduction:.1f}%")

    # Step 5: Add improved versions
    print("\n[5/5] Adding improved prompt versions...")

    improved_files = {
        "primary_agent": "primary_agent_prompt_improved.txt",
        "challenge_agent": "challenge_agent_prompt_improved.txt",
        "decision_agent": "decision_agent_prompt_improved.txt"
    }

    for prompt_type, source_file in improved_files.items():
        source_path = os.path.join(base_dir, source_file)

        if not os.path.exists(source_path):
            print(f"  !  {source_file} not found, skipping")
            continue

        # Read improved content
        with open(source_path, "r", encoding="utf-8") as f:
            improved_content = f.read()

        # Determine next version number
        existing_versions = [int(v["version"]) for v in new_data[prompt_type]["versions"]]
        next_version = str(max(existing_versions) + 1)

        # Save to new file
        filename = f"{prompt_type}_v{next_version}.txt"
        file_path = os.path.join(prompts_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(improved_content)

        # Add to metadata
        new_data[prompt_type]["versions"].append({
            "version": next_version,
            "created_at": datetime.now().isoformat(),
            "notes": "Improved version - streamlined output, removed hardcoded assumptions, better flexibility",
            "file": filename
        })

        print(f"  OK Added {prompt_type} v{next_version} (improved)")

    # Write final versions.json with improved versions
    with open(versions_file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2)

    print("\n" + "="*60)
    print("MIGRATION COMPLETE OK")
    print("="*60)
    print(f"\nBackup saved: {os.path.basename(backup_file)}")
    print(f"Prompt files: data/prompts/*.txt")
    print(f"Metadata: data/prompts/versions.json")
    print("\nTo edit prompts: Just edit the .txt files directly!")
    print("To activate improved versions: Use PromptManager.set_active_version()")


if __name__ == "__main__":
    migrate_prompts()
