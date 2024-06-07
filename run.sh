#!/bin/bash

# Ensure the script is executable
chmod +x run.sh

export FLASK_APP=app.py
export FLASK_ENV=production
export SECRET_KEY='your_secret_key'
export DATABASE_URL="sqlite:///$(pwd)/instance/app.db"

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv nobsenv
source nobsenv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt 

# Ensure the instance and sessions directories exist
echo "Ensuring instance and sessions directories exist..."
mkdir -p instance sessions

# Set the correct permissions
chmod 777 instance
chmod 666 instance/app.db

# Initialize the database
echo "Initializing the database..."
python manage_db.py

# List the contents of the instance directory for verification
echo "Contents of the instance directory:"
ls -la instance

# Start the server
echo "Starting Gunicorn..."
gunicorn -w 4 -b 0.0.0.0:10000 app:app  # Start the server
