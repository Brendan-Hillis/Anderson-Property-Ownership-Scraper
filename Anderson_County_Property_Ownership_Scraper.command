#!/bin/bash

# --- Configuration ---
PROJECT_PARENT_DIR="$HOME/gitRepos/" # Directory where the project will be stored
REPO_URL="https://github.com/Brendan-Hillis/Anderson-Property-Ownership-Scraper.git" # IMPORTANT: Replace with your GitHub repo URL (e.g., https://github.com/your-username/your-repo-name.git)
VENV_NAME="venv" # Name of your virtual environment
MAIN_SCRIPT="main.py" # Name of your main Python script

# Full path to the directory where the Git repository will be cloned
# This assumes the repo name is the last part of the URL without .git
REPO_DIR_NAME=$(basename "$REPO_URL" .git)
FULL_REPO_PATH="$PROJECT_PARENT_DIR/$REPO_DIR_NAME"

# Define the persistent data file path outside the repository
PERSISTENT_DATA_FILE_PATH="$PROJECT_PARENT_DIR/property_owners.json"

# --- Script Execution ---

echo "Starting Property Ownership Scraper setup and run..."
echo "----------------------------------------------------"

# Create the parent project directory if it doesn't exist
mkdir -p "$PROJECT_PARENT_DIR" || { echo "Error: Could not create $PROJECT_PARENT_DIR. Exiting."; exit 1; }

# Navigate to the project's parent directory for git operations
cd "$PROJECT_PARENT_DIR" || { echo "Error: Could not navigate to $PROJECT_PARENT_DIR. Exiting."; exit 1; }

# Check if the repository already exists
if [ -d "$REPO_DIR_NAME" ]; then
    echo "Project directory '$REPO_DIR_NAME' found. Updating with git pull..."
    cd "$REPO_DIR_NAME" || { echo "Error: Could not navigate into existing repo directory. Exiting."; exit 1; }
    git pull || { echo "Error: Git pull failed. Check internet connection or Git setup. Exiting."; exit 1; }
else
    # Clone the latest version of the repository
    echo "Project directory '$REPO_DIR_NAME' not found. Cloning from GitHub..."
    git clone "$REPO_URL" || { echo "Error: Git clone failed. Ensure Git is installed and URL is correct. Exiting."; exit 1; }
    # Navigate into the newly cloned repository
    cd "$REPO_DIR_NAME" || { echo "Error: Could not navigate into cloned directory. Exiting."; exit 1; }
fi

# Create and activate virtual environment
echo "Setting up virtual environment..."
if [ ! -d "$VENV_NAME" ]; then
    python3 -m venv "$VENV_NAME" || { echo "Error: Could not create virtual environment. Ensure Python 3 is installed. Exiting."; exit 1; }
fi
source "$VENV_NAME/bin/activate" || { echo "Error: Could not activate virtual environment. Exiting."; exit 1; }

# Install requirements
echo "Installing required Python packages..."
# Ensure requirements.txt exists before trying to install
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || { echo "Error: Could not install requirements. Check requirements.txt and internet connection. Exiting."; deactivate; exit 1; }
else
    echo "Warning: requirements.txt not found. Skipping package installation."
fi

# Set the environment variable for the data file path before running the Python script
# This ensures main.py knows where to find/save the JSON file persistently
export SCRAPER_DATA_FILE_PATH="$PERSISTENT_DATA_FILE_PATH"

# Run the main script
echo "Running the main property ownership script..."
python "$MAIN_SCRIPT" || { echo "Error: Failed to run the main script. Check script for errors. Exiting."; deactivate; exit 1; }

# Deactivate the virtual environment
deactivate

echo "----------------------------------------------------"
echo "Script finished. Press Enter to close this window."
read -r # Keeps the terminal window open until a key is pressed
