import pytest
import sys


def run_tests_and_get_results():
    """Run tests programmatically and return results"""

    # Run pytest and capture the exit code
    exit_code = pytest.main(["-v", "test.py", "--tb=short"])

    # pytest exit codes:
    # 0: All tests passed
    # 1: Some tests failed
    # 2: Test execution was interrupted
    # 3: Internal error
    # 4: pytest command line usage error
    # 5: No tests found

    if exit_code == 0:
        print("✅ All tests passed!")
        return {"passed": True, "exit_code": exit_code}
    elif exit_code == 1:
        print("❌ Some tests failed!")
        return {"passed": False, "exit_code": exit_code}
    else:
        print(f"⚠️ Test execution issue (exit code: {exit_code})")
        return {"passed": False, "exit_code": exit_code}


if __name__ == "__main__":
    result = run_tests_and_get_results()
    print(f"Test result: {result}")

    # Exit with the same code as pytest for CI/CD integration
    sys.exit(result["exit_code"])
