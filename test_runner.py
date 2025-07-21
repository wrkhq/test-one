"""
Advanced test runner with detailed results - in-memory version
No external dependencies required
"""

import pytest
import sys
import time


class InMemoryTestCollector:
    """Pytest plugin to collect test results in memory"""

    def __init__(self):
        self.tests = []
        self.start_time = None
        self.end_time = None
        self.summary = {"passed": 0, "failed": 0, "skipped": 0, "error": 0, "total": 0}

    def pytest_runtest_logreport(self, report):
        """Called for each test report"""
        if (
            report.when == "call"
        ):  # Only collect the main test result, not setup/teardown
            test_info = {
                "nodeid": report.nodeid,
                "outcome": report.outcome,
                "duration": getattr(report, "duration", 0),
                "setup": getattr(report, "setup", {}),
                "call": getattr(report, "call", {}),
                "teardown": getattr(report, "teardown", {}),
            }

            # Add failure info if test failed
            if report.failed and hasattr(report, "longrepr"):
                test_info["failure_info"] = str(report.longrepr)

            self.tests.append(test_info)

            # Update summary counts
            if report.outcome in self.summary:
                self.summary[report.outcome] += 1
            self.summary["total"] += 1

    def pytest_sessionstart(self, session):
        """Called at the start of test session"""
        self.start_time = time.time()

    def pytest_sessionfinish(self, session, exitstatus):
        """Called at the end of test session"""
        self.end_time = time.time()

    def get_json_report(self):
        """Generate JSON report similar to pytest-json-report format"""
        duration = (
            (self.end_time - self.start_time)
            if (self.end_time and self.start_time)
            else 0
        )

        return {"summary": self.summary, "duration": duration, "tests": self.tests}


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
    """Run tests with full JSON reporting - in memory version"""

    # Create our custom collector plugin
    collector = InMemoryTestCollector()

    # Run pytest with our custom plugin
    exit_code = pytest.main(
        [
            "-v",
            "test.py",
            "--tb=short",
            "-p",
            "no:cacheprovider",  # Disable cache to ensure clean run
        ],
        plugins=[collector],
    )

    # Get the in-memory JSON report
    json_data = collector.get_json_report()

    # Create results object
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

            # Show failure info if available
            if test["outcome"] == "failed" and "failure_info" in test:
                print(f"      ↳ {test['failure_info'][:100]}...")

    return results, exit_code


if __name__ == "__main__":
    results, exit_code = run_tests_with_json_report()

    print("\nProgrammatic Results:")
    print(f"Passed: {results.passed}, Failed: {results.failed}, Total: {results.total}")

    # Return appropriate exit code
    sys.exit(exit_code)
