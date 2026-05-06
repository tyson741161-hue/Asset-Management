#!/bin/bash
set -e

echo "=========================================="
echo "IT Asset Management System - Starting"
echo "=========================================="

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -U asset_admin -d asset_management; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"

# Initialize database tables
echo "Initializing database tables..."
python init_db.py

# Check if migration is needed (if JSON files exist and database is empty)
if [ -f "/app/assets_data.json" ] && [ -s "/app/assets_data.json" ]; then
    echo "Checking if migration is needed..."
    
    # Simple check: if assets table is empty, run migration
    ASSET_COUNT=$(python -c "
from models import db, Asset
from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    print(Asset.query.count())
" 2>/dev/null || echo "0")
    
    if [ "$ASSET_COUNT" = "0" ]; then
        echo "Database is empty. Running migration from JSON files..."
        python migrate_json_to_postgres.py
    else
        echo "Database already contains data. Skipping migration."
    fi
else
    echo "No JSON files found for migration."
fi

echo "=========================================="
echo "Starting Flask application..."
echo "=========================================="

# Start the Flask application
exec python server.py
