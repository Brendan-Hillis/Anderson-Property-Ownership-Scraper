#!/bin/bash

# --- Configuration ---
PROJECT_DIR="$HOME/gitRepos/" # Directory where the project will be stored
REPO_URL="https://github.com/Brendan-Hillis/Anderson-Property-Ownership-Scraper.git" # IMPORTANT: Replace with your GitHub repo URL
VENV_NAME="venv" # Name of your virtual environment
MAIN_SCRIPT="main.py" # Name of your main Python script

# --- Script Execution ---chmod +x run_scraper.command

echo "Starting Property Ownership Scraper setup and run..."
echo "----------------------------------------------------"

# 1. Navigate to the parent directory
mkdir -p "$PROJECT_DIR" # Create directory if it doesn't exist
cd "$PROJECT_DIR" || { echo "Error: Could not navigate to $PROJECT_DIR. Exiting."; exit 1; }

# 2. Check if the project directory already exists and remove if it does (to get latest version)
if [ -d "./$(basename "$REPO_URL" .git)" ]; then
    echo "Found existing project directory. Removing to get latest version..."
    rm -rf "./$(basename "$REPO_URL" .git)"
fi

# 3. Clone the latest version of the repository
echo "Cloning the latest project from GitHub..."
git clone "$REPO_URL" || { echo "Error: Git clone failed. Ensure Git is installed and URL is correct. Exiting."; exit 1; }

# Navigate into the cloned repository
cd "$(basename "$REPO_URL" .git)" || { echo "Error: Could not navigate into cloned directory. Exiting."; exit 1; }

# 4. Create and activate virtual environment
echo "Setting up virtual environment..."
if [ ! -d "$VENV_NAME" ]; then
    python3 -m venv "$VENV_NAME" || { echo "Error: Could not create virtual environment. Ensure Python 3 is installed. Exiting."; exit 1; }
fi
source "$VENV_NAME/bin/activate" || { echo "Error: Could not activate virtual environment. Exiting."; exit 1; }

# 5. Install requirements
echo "Installing required Python packages..."
pip install -r requirements.txt || { echo "Error: Could not install requirements. Check requirements.txt and internet connection. Exiting."; deactivate; exit 1; }

# 6. Run the main script
echo "Running the main property ownership script..."
python "$MAIN_SCRIPT"

# 7. Deactivate the virtual environment
deactivate

echo "----------------------------------------------------"
echo "Script finished. Press Enter to close this window."
read -r # Keeps the terminal window open until a key is pressed