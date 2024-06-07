#!/bin/bash

# Comment out the log file creation
: '
LOGFILE="deploy.log"
exec > >(tee -i $LOGFILE)
exec 2>&1
'

chmod +x run.sh ## makes the bash executable

export DATABASE_URL="sqlite:///$(pwd)/instance/app.db" # export environment variable (works, but need to change to read from ext env var)

mkdir -p instance sessions || { echo "Failed to create directories"; exit 1; } ## create sessions directory to track progress locally

## reqd permissions to run the bash script
chmod 777 instance || { echo "Failed to set permissions for instance directory"; exit 1; } 
touch instance/app.db || { echo "Failed to create app.db file"; exit 1; }
chmod 666 instance/app.db || { echo "Failed to set permissions for app.db"; exit 1; }

python3 manage_db.py || { echo "Failed to initialize database"; exit 1; } ## creates, loads, checks and shows the db functionality from jsonl files

gunicorn -w 4 -b 0.0.0.0:10000 app:app || { echo "Failed to start Gunicorn"; exit 1; } ## starts the server locally at (http://0.0.0.0:10000)