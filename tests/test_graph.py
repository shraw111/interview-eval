"""
Basic graph workflow tests.
"""

import os
import sys
import yaml

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.graph.state import create_initial_state, EvaluationState
from src.graph.graph import create_evaluation_graph


def test_state_creation():
    """Test creating initial evaluation state."""
    # Load sample rubric
    rubric_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample_rubric.yaml')
    with open(rubric_path, 'r') as f:
        rubric = yaml.safe_load(f)

    # Load sample transcript
    transcript_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample_transcript.txt')
    with open(transcript_path, 'r') as f:
        transcript = f.read()

    # Create state
    state = create_initial_state(
        rubric=rubric,
        transcript=transcript,
        candidate_info={
            'name': 'Test Candidate',
            'current_level': 'PM',
            'target_level': 'Senior PM',
            'years_experience': 3,
            'level_expectations': 'Strategic thinking, execution excellence'
        }
    )

    # Verify state structure
    assert state['rubric'] == rubric
    assert state['transcript'] == transcript
    assert state['candidate_info']['name'] == 'Test Candidate'
    assert state['primary_evaluation'] is None
    assert state['challenges'] is None
    assert state['final_evaluation'] is None
    assert state['decision'] is None  # NEW - check decision field
    assert state['metadata']['tokens']['total'] == 0

    print("State creation test passed")


def test_graph_structure():
    """Test graph structure and nodes."""
    graph = create_evaluation_graph()

    # Graph should be compiled and ready
    assert graph is not None

    # Verify graph has correct structure
    # Note: This is a basic structural test
    # Full end-to-end test requires Azure OpenAI credentials

    print("Graph structure test passed")


if __name__ == "__main__":
    print("Running basic tests...")
    test_state_creation()
    test_graph_structure()
    print("\n✅ All basic tests passed!")
    print("\nNote: End-to-end evaluation tests require:")
    print("  1. Azure OpenAI credentials in .env")
    print("  2. Valid deployment names in config.yaml")
    print("  3. Run with: python -m pytest tests/")
