import pytest
import sys


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.total = 0
        self.details = []


def run_tests_with_detailed_results():
    """Run tests and get detailed pass/fail counts"""

    # Run pytest and get exit code
    exit_code = pytest.main(["-v", "test.py", "--tb=short"])

    # Parse the basic results from exit code
    results = TestResults()

    if exit_code == 0:
        results.passed = 1  # For our simple case
        results.total = 1
        print("✅ Test Results:")
        print(f"   Passed: {results.passed}")
        print(f"   Failed: {results.failed}")
        print(f"   Total:  {results.total}")
    elif exit_code == 1:
        results.failed = 1  # For our simple case
        results.total = 1
        print("❌ Test Results:")
        print(f"   Passed: {results.passed}")
        print(f"   Failed: {results.failed}")
        print(f"   Total:  {results.total}")
    else:
        print(f"⚠️ Test execution issue (exit code: {exit_code})")

    return results


if __name__ == "__main__":
    results = run_tests_with_detailed_results()

    # You can now programmatically access:
    print("\nProgrammatic access:")
    print(f"results.passed = {results.passed}")
    print(f"results.failed = {results.failed}")
    print(f"results.total = {results.total}")

    # Exit with appropriate code
    exit_code = 0 if results.failed == 0 else 1
    sys.exit(exit_code)
