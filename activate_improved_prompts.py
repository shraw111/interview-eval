"""
Helper script to activate the improved prompt versions.

This script sets all agents to use the improved (latest) versions.
"""

from src.prompts.manager import PromptManager


def activate_improved_versions():
    """Activate improved prompt versions for all agents."""

    pm = PromptManager()

    print("Activating improved prompt versions...\n")

    agents = {
        "primary_agent": "3",
        "challenge_agent": "3",
        "decision_agent": "4"
    }

    for agent_type, version in agents.items():
        print(f"  {agent_type}: Activating v{version}")

        # Set as active
        pm.set_active_version(agent_type, version)

        # Verify it worked
        active = pm._load_versions()[agent_type]["active_version"]
        if active == version:
            print(f"    OK - Active version is now v{version}")
        else:
            print(f"    ERROR - Expected v{version}, got v{active}")

    print("\n" + "="*60)
    print("IMPROVED PROMPTS ACTIVATED")
    print("="*60)
    print("\nChanges:")
    print("  - Primary Agent: Removed hardcoded scoring, ~40% shorter output")
    print("  - Challenge Agent: Streamlined format, ~35% shorter output")
    print("  - Decision Agent: Consolidated sections, ~20% shorter output")
    print("\nTo edit prompts: Edit the .txt files in data/prompts/")
    print("  - primary_agent_v3.txt")
    print("  - challenge_agent_v3.txt")
    print("  - decision_agent_v4.txt")


if __name__ == "__main__":
    activate_improved_versions()
