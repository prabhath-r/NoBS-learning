#!/bin/bash

# Ensure the script is executable
# chmod +x run.sh

# Set up environment variables
export FLASK_APP=app.py
export FLASK_ENV=production
export SECRET_KEY='your_secret_key'
export DATABASE_URL="sqlite:///$(pwd)/instance/app.db"

# Create and activate virtual environment
python3 -m venv nobsenv
source nobsenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ensure the sessions directory exists
mkdir -p sessions

# Run the manage_db.py script to handle database creation, population, and checking
python manage_db.py

# Start the server
gunicorn -w 4 -b 127.0.0.1:8000 app:app
