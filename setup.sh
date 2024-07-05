#!/bin/bash

# Define the name of the virtual environment directory
VENV_DIR="venv"

# Check if the virtual environment directory already exists
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists. Activating..."
else
    # Create a virtual environment
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Install the required packages
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Inform the user that the setup is complete
echo "Setup complete. Virtual environment is ready and requirements are installed."
