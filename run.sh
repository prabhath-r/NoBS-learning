#!/bin/bash

# Create a log file for capturing the output and errors
LOGFILE="deploy.log"
exec > >(tee -i $LOGFILE)
exec 2>&1

echo "Starting deployment script..."

# Ensure the script is executable
echo "Setting executable permissions for run.sh..."
chmod +x run.sh

# Export environment variables
export FLASK_APP=app.py
export FLASK_ENV=production
export SECRET_KEY='your_secret_key'
export DATABASE_URL="sqlite:///$(pwd)/instance/app.db"

echo "Environment variables set:"
echo "FLASK_APP=$FLASK_APP"
echo "FLASK_ENV=$FLASK_ENV"
echo "SECRET_KEY=$SECRET_KEY"
echo "DATABASE_URL=$DATABASE_URL"

# Ensure the instance and sessions directories exist
echo "Ensuring instance and sessions directories exist..."
mkdir -p instance sessions || { echo "Failed to create directories"; exit 1; }

# Set the correct permissions
echo "Setting permissions for instance directory and app.db..."
chmod 777 instance || { echo "Failed to set permissions for instance directory"; exit 1; }
touch instance/app.db || { echo "Failed to create app.db file"; exit 1; }
chmod 666 instance/app.db || { echo "Failed to set permissions for app.db"; exit 1; }

# Initialize the database
echo "Initializing the database..."
python manage_db.py || { echo "Failed to initialize database"; exit 1; }

# List the contents of the instance directory for verification
echo "Contents of the instance directory:"
ls -la instance

# Start the server
echo "Starting Gunicorn..."
gunicorn -w 4 -b 0.0.0.0:10000 app:app || { echo "Failed to start Gunicorn"; exit 1; }

echo "Deployment script finished."
run.sh for Render setup