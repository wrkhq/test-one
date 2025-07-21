"""
Advanced test runner with detailed results using pytest-json-report
Install with: pip install pytest-json-report
"""

import pytest
import json
import sys
import os


class DetailedTestResults:
    def __init__(self, json_report=None):
        if json_report:
            summary = json_report["summary"]
            self.passed = summary.get("passed", 0)
            self.failed = summary.get("failed", 0)
            self.skipped = summary.get("skipped", 0)
            self.error = summary.get("error", 0)
            self.total = summary.get("total", 0)
            self.duration = json_report.get("duration", 0)
            self.test_details = json_report.get("tests", [])
        else:
            self.passed = 0
            self.failed = 0
            self.skipped = 0
            self.error = 0
            self.total = 0
            self.duration = 0
            self.test_details = []


def run_tests_with_json_report():
    """Run tests with full JSON reporting"""

    json_file = "test_results.json"

    # Clean up previous report
    if os.path.exists(json_file):
        os.remove(json_file)

    # Run pytest with JSON report
    exit_code = pytest.main(
        [
            "-v",
            "test.py",
            "--json-report",
            f"--json-report-file={json_file}",
            "--tb=short",
        ]
    )

    # Load and parse JSON report
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            json_data = json.load(f)

        results = DetailedTestResults(json_data)

        print("📊 Detailed Test Results:")
        print(f"   Passed:   {results.passed}")
        print(f"   Failed:   {results.failed}")
        print(f"   Skipped:  {results.skipped}")
        print(f"   Errors:   {results.error}")
        print(f"   Total:    {results.total}")
        print(f"   Duration: {results.duration:.2f}s")

        # Show individual test details
        if results.test_details:
            print("\n📋 Individual Test Results:")
            for test in results.test_details:
                status = "✅" if test["outcome"] == "passed" else "❌"
                print(f"   {status} {test['nodeid']} - {test['outcome']}")

        # Clean up
        os.remove(json_file)

    else:
        print("⚠️ Could not generate JSON report")
        print("Install pytest-json-report with: pip install pytest-json-report")
        results = DetailedTestResults()

    return results, exit_code


if __name__ == "__main__":
    results, exit_code = run_tests_with_json_report()

    print("\nProgrammatic Results:")
    print(f"Passed: {results.passed}, Failed: {results.failed}, Total: {results.total}")

    # Return appropriate exit code
    sys.exit(exit_code)
