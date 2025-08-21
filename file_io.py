# ==============================================================================
# FILE INPUT/OUTOUT FUNCTIONS
# Purpose: Helper functions for file operations.
# ==============================================================================
import json
import os

def load_data(filepath: str):
    """Loads property data from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data: dict, filepath: str):
    """Saves property data to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\nSuccessfully saved current data to '{filepath}'.")
