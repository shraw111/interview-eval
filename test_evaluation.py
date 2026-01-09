"""End-to-end test for evaluation with real agents."""

import requests
import json
import time

def test_evaluation():
    print("Testing Full Evaluation Pipeline...")
    print("=" * 60)

    # Sample evaluation data
    evaluation_request = {
        "candidate_info": {
            "name": "Test Candidate",
            "current_level": "L5 PM",
            "target_level": "L6 Senior PM",
            "years_experience": 3,
            "level_expectations": "Expected to demonstrate strategic thinking beyond immediate roadmap, influence across teams, and execution at scale."
        },
        "rubric": """## Strategic Thinking
- Demonstrates long-term vision beyond immediate roadmap
- Makes decisions considering broader organizational impact

## Leadership & Influence
- Influences without authority across teams
- Builds consensus among stakeholders

## Execution Excellence
- Delivers complex projects on time
- Manages risks proactively""",
        "transcript": """Interviewer: Can you walk me through a recent project where you had to influence stakeholders?

Candidate: Sure, I recently led the launch of our new analytics dashboard. The challenge was getting buy-in from multiple teams who each had different priorities and timelines.

I started by understanding each team's concerns individually. The engineering team was worried about technical debt, while the sales team needed quick wins for customer demos. Product wanted comprehensive features.

I created a phased approach that addressed each concern. Phase 1 focused on core functionality that sales could demo. Phase 2 tackled the technical architecture improvements engineering wanted. Phase 3 added the advanced features product requested.

By showing how everyone's needs fit into the roadmap, I got all teams aligned. We launched on time, sales hit their demo targets, and engineering was happy with the clean architecture."""
    }

    try:
        # Submit evaluation
        print("\n1. Submitting evaluation request...")
        print(f"   Candidate: {evaluation_request['candidate_info']['name']}")

        response = requests.post(
            "http://localhost:8000/api/v1/evaluations",
            json=evaluation_request,
            timeout=10
        )

        if response.status_code != 202:
            print(f"[ERROR] Failed to create evaluation: {response.status_code}")
            print(f"Response: {response.text}")
            return False

        data = response.json()
        evaluation_id = data['evaluation_id']
        print(f"   [OK] Evaluation created: {evaluation_id}")

        # Poll for results
        print("\n2. Waiting for agents to complete (may take 2-3 minutes)...")

        max_attempts = 60
        attempt = 0

        while attempt < max_attempts:
            time.sleep(5)
            attempt += 1

            response = requests.get(
                f"http://localhost:8000/api/v1/evaluations/{evaluation_id}",
                timeout=10
            )

            result = response.json()
            status = result['status']
            progress = result['progress_percentage']

            print(f"   [{attempt*5}s] Status: {status}, Progress: {progress}%", end='\r')

            if status == 'completed':
                print(f"\n   [OK] Completed in ~{attempt*5} seconds!")
                break
            elif status == 'failed':
                print(f"\n   [ERROR] Failed: {result.get('error')}")
                return False

        if status != 'completed':
            print(f"\n   [TIMEOUT] Did not complete in {max_attempts*5}s")
            return False

        # Check results
        print("\n3. Checking Agent Outputs:")
        print("=" * 60)

        eval_result = result.get('result')
        agents = [
            ('primary_evaluation', 'Primary Evaluator'),
            ('challenges', 'Challenge Agent'),
            ('final_evaluation', 'Calibrated Response'),
            ('decision', 'Decision Agent')
        ]

        all_ok = True
        for key, name in agents:
            output = eval_result.get(key)
            if output and len(output) > 50:
                print(f"   [OK] {name}: {len(output)} chars")
            else:
                print(f"   [ERROR] {name}: MISSING or too short!")
                all_ok = False

        metadata = eval_result.get('metadata', {})
        tokens = metadata.get('tokens', {})
        total = tokens.get('total_input', 0) + tokens.get('total_output', 0)
        print(f"\n   Total Tokens: {total}")
        print(f"   Time: {metadata.get('execution_time_seconds', 0):.1f}s")
        print(f"   Model: {metadata.get('model_version')}")

        print("\n" + "=" * 60)
        if all_ok:
            print("[SUCCESS] All agents working!")
        else:
            print("[FAILED] Some agents failed")
        print("=" * 60)
        return all_ok

    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == "__main__":
    import sys
    success = test_evaluation()
    sys.exit(0 if success else 1)
