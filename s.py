import os

# Base project name
BASE_DIR = "mental-health-signal-detection"

# Folder structure
folders = [
    "data/raw",
    "data/processed",
    "data/outputs",
    "models",
    "src/config",
    "src/data",
    "src/preprocessing",
    "src/features",
    "src/models",
    "src/alert",
    "src/storage",
    "src/visualization",
    "src/utils",
    "app",
    "notebooks",
    "tests"
]

# Files to create
files = [
    "src/config/config.py",
    "src/data/reddit_fetcher.py",
    "src/data/data_loader.py",
    "src/preprocessing/preprocessor.py",
    "src/features/vectorizer.py",
    "src/models/train_model.py",
    "src/models/predict_model.py",
    "src/alert/alert_system.py",
    "src/storage/storage_manager.py",
    "src/visualization/dashboard.py",
    "src/utils/helpers.py",
    "app/app.py",
    "notebooks/experiments.ipynb",
    "tests/test_pipeline.py",
    "requirements.txt",
    "README.md",
    ".gitignore"
]

def create_structure():
    print("🚀 Creating project structure...\n")

    # Create base directory
    os.makedirs(BASE_DIR, exist_ok=True)

    # Create folders
    for folder in folders:
        path = os.path.join(BASE_DIR, folder)
        os.makedirs(path, exist_ok=True)
        print(f"📁 Created folder: {path}")

    # Create files
    for file in files:
        path = os.path.join(BASE_DIR, file)
        with open(path, "w") as f:
            pass
        print(f"📄 Created file: {path}")

    print("\n✅ Project structure created successfully!")

if __name__ == "__main__":
    create_structure()