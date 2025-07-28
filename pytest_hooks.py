"""PyTest hooks for running pre-checks before tests."""
import subprocess
import sys
from typing import List

def pytest_sessionstart(session):
    """Run pre-checks before any tests start."""
    if "--no-precheck" in sys.argv:
        return
        
    print("\nRunning pre-checks before tests...")
    checks = [
        (["pylint", "screens/", "tests/", "utils/"], "Pylint check"),
        (["mypy", "screens/", "tests/", "utils/"], "Type checking"),
        (["flake8", "screens/", "tests/", "utils/"], "Code style check")
    ]
    
    failed = False
    for command, description in checks:
        print(f"\nRunning {description}...")
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"✅ {description} passed")
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed:")
            print(e.stdout)
            print(e.stderr)
            failed = True
            
    if failed:
        print("\n❌ Pre-checks failed. Please fix the issues before running tests.")
        session.exitcode = 1
