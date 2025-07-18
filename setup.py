"""Setup script for BehaveAPI project."""

import shutil
from pathlib import Path


def setup_project():
    """Setup the BehaveAPI project."""
    print("Setting up BehaveAPI project...")

    env_file = Path(".env")

    # Create directories if they don't exist
    directories = [
        "features/rest", "features/websocket", "features/steps", "config",
        "test_data", "utils", "reports"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    print("✓ Created project directories")

    # Check if all required files exist
    required_files = [
        "requirements.txt", "config/config.yml", "features/environment.py",
        "utils/__init__.py"
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"⚠ Missing files: {', '.join(missing_files)}")
    else:
        print("✓ All required files are present")

    print("\nSetup complete! Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Configure your .env file with appropriate values")
    print("3. Run tests: behave")


if __name__ == "__main__":
    setup_project()
