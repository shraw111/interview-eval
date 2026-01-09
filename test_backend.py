"""Quick test script for backend API."""

import requests
import time
import subprocess
import sys

def test_backend():
    print("Testing Backend API...")
    print("-" * 50)

    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        print(f"[OK] Health Check: {response.status_code}")
        data = response.json()
        print(f"  Status: {data['status']}")
        print(f"  Version: {data['version']}")
        print(f"  Azure Configured: {data['azure_openai_configured']}")

        if not data['azure_openai_configured']:
            print("  [WARNING] Azure OpenAI not detected (but may still work)")

        print()

        # Test root endpoint
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"[OK] Root Endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")

        print()
        print("=" * 50)
        print("[SUCCESS] Backend is working!")
        print("=" * 50)
        print()
        print("Next steps:")
        print("1. Install frontend: cd frontend && npm install")
        print("2. Start frontend: cd frontend && npm run dev")
        print("3. Visit http://localhost:3000")

        return True

    except requests.exceptions.ConnectionError:
        print("[ERROR] Backend not running!")
        print()
        print("Start the backend first:")
        print("  cd backend")
        print("  python run.py")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    sys.exit(0 if success else 1)
