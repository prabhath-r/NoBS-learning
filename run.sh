#!/bin/bash

# Ensure the script is executable
# chmod +x run.sh

export FLASK_APP=app.py
export FLASK_ENV=production
export SECRET_KEY='your_secret_key'
export DATABASE_URL="sqlite:///$(pwd)/instance/app.db"

python3 -m venv nobsenv
source nobsenv/bin/activate

pip install -r requirements.txt

mkdir -p sessions 

python manage_db.py

gunicorn -w 4 -b 127.0.0.1:8000 app:app  ## Start the server
