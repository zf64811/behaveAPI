#!/usr/bin/env python3
"""Run tests with Allure report generation."""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_allure_installed():
    """Check if Allure command line is installed."""
    try:
        subprocess.run(['allure', '--version'],
                       capture_output=True,
                       check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_allure_windows():
    """Provide instructions for installing Allure on Windows."""
    print("\n" + "=" * 60)
    print("Allure Command Line is not installed!")
    print("=" * 60)
    print("\nTo install Allure on Windows, you have several options:")
    print("\n1. Using Scoop (Recommended):")
    print("   > scoop install allure")
    print("\n2. Using Chocolatey:")
    print("   > choco install allure")
    print("\n3. Manual installation:")
    print(
        "   - Download from: https://github.com/allure-framework/allure2/releases"
    )
    print("   - Extract and add to PATH")
    print("\n4. Using npm:")
    print("   > npm install -g allure-commandline")
    print("=" * 60 + "\n")


def run_tests_with_allure():
    """Run Behave tests with Allure formatter."""
    # Create directories
    reports_dir = Path("reports")
    allure_results_dir = reports_dir / "allure-results"
    allure_report_dir = reports_dir / "allure-report"

    # Clean previous results
    if allure_results_dir.exists():
        shutil.rmtree(allure_results_dir)

    reports_dir.mkdir(exist_ok=True)
    allure_results_dir.mkdir(exist_ok=True)

    print("Running tests with Allure formatter...")

    # Run behave with Allure formatter
    cmd = [
        sys.executable, "-m", "behave", "-f",
        "allure_behave.formatter:AllureFormatter", "-o",
        str(allure_results_dir), "-f", "pretty"
    ]

    # Add any additional arguments passed to the script
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])

    result = subprocess.run(cmd)

    # Check if Allure is installed
    if not check_allure_installed():
        install_allure_windows()
        print("\nAllure results generated in:", allure_results_dir)
        print("After installing Allure, run:")
        print(f"  allure serve {allure_results_dir}")
        return result.returncode

    # Generate and open Allure report
    print("\nGenerating Allure report...")

    # Generate report
    subprocess.run([
        "allure", "generate",
        str(allure_results_dir), "-o",
        str(allure_report_dir), "--clean"
    ])

    print(f"\nAllure report generated in: {allure_report_dir}")

    # Ask if user wants to open the report
    response = input("\nOpen Allure report in browser? (y/n): ")
    if response.lower() == 'y':
        subprocess.run(["allure", "open", str(allure_report_dir)])

    return result.returncode


def main():
    """Main function."""
    print("BehaveAPI Test Runner with Allure Report")
    print("=" * 40)

    # Check if behave and allure-behave are installed
    try:
        import behave
        import allure_behave
    except ImportError as e:
        print(f"Error: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return 1

    return run_tests_with_allure()


if __name__ == "__main__":
    sys.exit(main())
