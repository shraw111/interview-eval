"""
Test script for Sarah Chen sample data evaluation.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.graph.graph import evaluation_graph
from src.graph.state import create_initial_state

# Load Sarah Chen sample data
with open('sample_data/candidate_info.txt', 'r', encoding='utf-8') as f:
    candidate_text = f.read()

with open('sample_data/sample_rubric.txt', 'r', encoding='utf-8') as f:
    rubric_text = f.read()

with open('sample_data/sample_transcript.txt', 'r', encoding='utf-8') as f:
    transcript_text = f.read()

# Parse candidate info - extract values after markdown headers
candidate_info = {
    'name': 'Sarah Chen',
    'current_level': 'PM',
    'target_level': 'Senior PM',
    'years_experience': '3',
    'level_expectations': 'Senior PMs must define strategy, not just execute on roadmap. They should influence product direction at the company level, align executive stakeholders proactively, and drive business outcomes (not just ship features). Senior PMs operate 12-18 months ahead and expand their scope beyond assigned areas. They develop other PMs and create leverage through their team.'
}

# Create initial state
initial_state = create_initial_state(
    rubric=rubric_text,
    transcript=transcript_text,
    candidate_info=candidate_info
)

print('Starting Sarah Chen evaluation...')
print('='*60)
print(f"Candidate: {candidate_info['name']}")
print(f"Current Level: {candidate_info['current_level']}")
print(f"Target Level: {candidate_info['target_level']}")
print('='*60)
print()

# Run evaluation
result = None
for chunk in evaluation_graph.stream(initial_state, stream_mode='updates'):
    for node_name, node_output in chunk.items():
        if node_name == 'primary_evaluator':
            print('[PRIMARY_EVALUATOR]')
            primary_eval = node_output.get('primary_evaluation', '')
            print(f"Primary evaluation: {len(primary_eval)} chars")
            with open('sarah_chen_primary.txt', 'w', encoding='utf-8') as f:
                f.write(primary_eval)
            print()
        elif node_name == 'challenge_agent':
            print('[CHALLENGE_AGENT]')
            challenges = node_output.get('challenges', '')
            print(f"Challenges: {len(challenges)} chars")
            with open('sarah_chen_challenges.txt', 'w', encoding='utf-8') as f:
                f.write(challenges)
            print()
        elif node_name == 'decision_agent':
            print('[DECISION_AGENT]')
            decision = node_output.get('decision', '')
            print(f"Decision: {len(decision)} chars")
            print()
            print('='*60)
            print('FINAL DECISION')
            print('='*60)
            # Write to file to avoid encoding issues
            with open('sarah_chen_decision.txt', 'w', encoding='utf-8') as f:
                f.write(decision)
            print(f"Decision written to sarah_chen_decision.txt ({len(decision)} chars)")
            print('='*60)

            result = node_output

print()
print('='*60)
print('EVALUATION SUMMARY')
print('='*60)
if result:
    metadata = result.get('metadata', {})
    print(f"Total tokens: {metadata.get('tokens', {}).get('total', 'N/A'):,}")
    print(f"Cost: ${metadata.get('cost_usd', 'N/A')}")
    print(f"Time: {metadata.get('execution_time_seconds', 'N/A')}s")
