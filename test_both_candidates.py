"""
Test script to validate evaluation system with both strong and weak candidates.

Expected outcomes:
- Strong candidate (Alex Thompson): RECOMMEND or STRONG RECOMMEND
- Weak candidate (Jamie Martinez): DO NOT RECOMMEND or BORDERLINE
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.graph.graph import evaluation_graph
from src.graph.state import create_initial_state

# Load rubric (same for both)
with open('sample_data/sample_rubric.txt', 'r', encoding='utf-8') as f:
    rubric_text = f.read()

def run_evaluation(candidate_name, transcript_file, expected_outcome):
    """Run evaluation for a candidate and check if outcome matches expectations."""
    print("\n" + "="*80)
    print(f"EVALUATING: {candidate_name}")
    print(f"EXPECTED OUTCOME: {expected_outcome}")
    print("="*80 + "\n")

    # Load transcript
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    # Create candidate info based on name
    if "Alex" in candidate_name:
        candidate_info = {
            'name': 'Alex Thompson',
            'current_level': 'PM',
            'target_level': 'Senior PM',
            'years_experience': '3',
            'level_expectations': 'Senior PMs must define strategy, not just execute on roadmap. They should influence product direction at the company level, align executive stakeholders proactively, and drive business outcomes (not just ship features). Senior PMs operate 12-18 months ahead and expand their scope beyond assigned areas.'
        }
    else:  # Jamie
        candidate_info = {
            'name': 'Jamie Martinez',
            'current_level': 'PM',
            'target_level': 'Senior PM',
            'years_experience': '3',
            'level_expectations': 'Senior PMs must define strategy, not just execute on roadmap. They should influence product direction at the company level, align executive stakeholders proactively, and drive business outcomes (not just ship features). Senior PMs operate 12-18 months ahead and expand their scope beyond assigned areas.'
        }

    # Create initial state
    initial_state = create_initial_state(
        rubric=rubric_text,
        transcript=transcript_text,
        candidate_info=candidate_info
    )

    # Run evaluation
    result = None
    primary_eval = None
    challenges = None
    final_eval = None
    decision = None

    for chunk in evaluation_graph.stream(initial_state, stream_mode='updates'):
        for node_name, node_output in chunk.items():
            if node_name == 'primary_evaluator':
                primary_eval = node_output.get('primary_evaluation', '')
                print(f"[PRIMARY] {len(primary_eval)} chars")

            elif node_name == 'challenge_agent':
                challenges = node_output.get('challenges', '')
                print(f"[CHALLENGE] {len(challenges)} chars")

            elif node_name == 'primary_response':
                final_eval = node_output.get('final_evaluation', '')
                print(f"[RESPONSE] {len(final_eval)} chars")

            elif node_name == 'decision_agent':
                decision = node_output.get('decision', '')
                print(f"[DECISION] {len(decision)} chars")
                result = node_output

    # Extract key information
    metadata = result.get('metadata', {})

    # Save outputs to files
    safe_name = candidate_name.replace(' ', '_').lower()
    with open(f'{safe_name}_primary.txt', 'w', encoding='utf-8') as f:
        f.write(primary_eval)
    with open(f'{safe_name}_challenges.txt', 'w', encoding='utf-8') as f:
        f.write(challenges)
    with open(f'{safe_name}_response.txt', 'w', encoding='utf-8') as f:
        f.write(final_eval)
    with open(f'{safe_name}_decision.txt', 'w', encoding='utf-8') as f:
        f.write(decision)

    # Parse decision
    actual_decision = "UNKNOWN"
    overall_score = "UNKNOWN"
    critical_passed = "UNKNOWN"

    if 'Final Recommendation:' in decision:
        for line in decision.split('\n'):
            if 'Final Recommendation:' in line:
                if 'STRONG RECOMMEND' in line:
                    actual_decision = 'STRONG RECOMMEND'
                elif 'DO NOT RECOMMEND' in line:
                    actual_decision = 'DO NOT RECOMMEND'
                elif 'BORDERLINE' in line:
                    actual_decision = 'BORDERLINE'
                elif 'RECOMMEND' in line:
                    actual_decision = 'RECOMMEND'
            elif 'Overall Score:' in line:
                overall_score = line.split('Overall Score:')[1].strip().split()[0]
            elif 'Critical Criteria:' in line:
                critical_passed = line.split('Critical Criteria:')[1].strip()

    # Print summary
    print("\n" + "-"*80)
    print(f"RESULTS FOR {candidate_name}")
    print("-"*80)
    print(f"Expected:  {expected_outcome}")
    print(f"Actual:    {actual_decision}")
    print(f"Score:     {overall_score}")
    print(f"Critical:  {critical_passed}")
    print(f"Tokens:    {metadata.get('tokens', {}).get('total', 'N/A'):,}")
    print(f"Cost:      ${metadata.get('cost_usd', 'N/A')}")
    print(f"Time:      {metadata.get('execution_time_seconds', 'N/A')}s")
    print("-"*80)

    # Validate outcome
    if expected_outcome in actual_decision:
        print(f"✓ PASS - Got expected outcome: {actual_decision}")
        return True
    elif expected_outcome == "RECOMMEND/STRONG RECOMMEND" and actual_decision in ["RECOMMEND", "STRONG RECOMMEND"]:
        print(f"✓ PASS - Got expected outcome: {actual_decision}")
        return True
    elif expected_outcome == "DO NOT RECOMMEND/BORDERLINE" and actual_decision in ["DO NOT RECOMMEND", "BORDERLINE"]:
        print(f"✓ PASS - Got expected outcome: {actual_decision}")
        return True
    else:
        print(f"✗ FAIL - Expected {expected_outcome}, got {actual_decision}")
        return False

# Run both tests
print("="*80)
print("RUNNING EVALUATION SYSTEM VALIDATION")
print("="*80)

results = []

# Test 1: Strong candidate should pass
results.append(run_evaluation(
    "Alex Thompson",
    "test_data/strong_candidate_transcript.txt",
    "RECOMMEND/STRONG RECOMMEND"
))

# Test 2: Weak candidate should fail
results.append(run_evaluation(
    "Jamie Martinez",
    "test_data/weak_candidate_transcript.txt",
    "DO NOT RECOMMEND/BORDERLINE"
))

# Final summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)
print(f"Strong candidate (Alex):  {'✓ PASS' if results[0] else '✗ FAIL'}")
print(f"Weak candidate (Jamie):   {'✓ PASS' if results[1] else '✗ FAIL'}")
print("="*80)

if all(results):
    print("\n✓ ALL TESTS PASSED - Evaluation system working correctly!")
    sys.exit(0)
else:
    print("\n✗ SOME TESTS FAILED - Review output above for details")
    sys.exit(1)
