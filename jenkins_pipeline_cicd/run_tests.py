#!/usr/bin/env python3
"""
Test Runner Script - Simple interface to run tests locally

Usage:
    python run_tests.py --suite smoke
    python run_tests.py --suite regression
    python run_tests.py --suite all
    python run_tests.py --suite smoke --headless false
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a shell command and report results."""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(
        description="Simple test runner for Playwright tests"
    )
    parser.add_argument(
        "--suite",
        choices=["smoke", "regression", "all"],
        default="smoke",
        help="Test suite to run"
    )
    parser.add_argument(
        "--headless",
        choices=["true", "false"],
        default="true",
        help="Run in headless mode"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel workers (default: auto)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip Allure report generation"
    )
    
    args = parser.parse_args()
    
    # Set environment variables
    os.environ["HEADLESS_MODE"] = args.headless
    
    # Determine test path
    if args.suite == "smoke":
        test_path = "tests/smoke"
    elif args.suite == "regression":
        test_path = "tests/regression"
    else:
        test_path = "tests"
    
    print(f"\n🚀 Starting Test Execution")
    print(f"{'='*60}")
    print(f"Test Suite: {args.suite}")
    print(f"Test Path: {test_path}")
    print(f"Headless Mode: {args.headless}")
    print(f"{'='*60}\n")
    
    # Build pytest command
    pytest_cmd = f"python3 -m pytest {test_path}"
    
    if args.verbose:
        pytest_cmd += " -vv"
    else:
        pytest_cmd += " -v"
    
    pytest_cmd += " --alluredir=allure-results"
    pytest_cmd += " --html=reports/report.html --self-contained-html"
    
    if args.workers:
        pytest_cmd += f" -n {args.workers}"
    else:
        pytest_cmd += " -n auto"
    
    # Run tests
    success = run_command(pytest_cmd, f"Running {args.suite} tests")
    
    if not success:
        print("\n⚠️  Some tests failed. Check output above.")
    
    # Generate Allure report
    if not args.no_report:
        success = run_command(
            "allure generate allure-results -o allure-reports --clean",
            "Generating Allure Report"
        )
        
        if success:
            print("\n✅ Allure report generated successfully!")
            print(f"📊 Report location: allure-reports/index.html")
            print(f"📊 Open report: allure open allure-reports")
        else:
            print("\n⚠️  Failed to generate Allure report")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Test Execution Summary")
    print(f"{'='*60}")
    print(f"Suite: {args.suite}")
    print(f"Status: {'✅ PASSED' if success else '❌ FAILED'}")
    print(f"Results: allure-results/")
    print(f"Reports: reports/report.html")
    print(f"{'='*60}\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
