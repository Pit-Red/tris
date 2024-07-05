#!/bin/bash

# Define the name of the virtual environment directory
VENV_DIR="venv"

# Check if the virtual environment directory exists
if [ -d "$VENV_DIR" ]; then
    echo "Activating virtual environment..."
    # Activate the virtual environment
    source $VENV_DIR/bin/activate

    # Run the ui.py script
    echo "Starting ui.py..."
    python ui.py
else
    echo "Virtual environment not found. Please run the setup script first."
fi
