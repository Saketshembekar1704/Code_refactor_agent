import os
import shutil
import importlib

def clear_pycache(root_dir="."):
    """Remove all __pycache__ directories recursively"""
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "__pycache__" in dirnames:
            full_path = os.path.join(dirpath, "__pycache__")
            print(f"🗑️ Removing {full_path}")
            shutil.rmtree(full_path)

def verify_import():
    """Verify which refactor_crew file is being imported"""
    try:
        module = importlib.import_module("crew.refactor_crew")
        print(f"✅ Loaded crew.refactor_crew from: {module.__file__}")
    except Exception as e:
        print(f"❌ Import failed: {e}")

if __name__ == "__main__":
    print("Cleaning up...")
    clear_pycache(".")
    print("Done.\n")

    print("Verifying import path...")
    verify_import()
