#!/bin/sh


# Check if the database is ready
echo "Checking database connection..."
python /app/api/pre_db_healthcheck.py

sleep 5

# Run Alembic migrations
echo "Running database migrations"
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI application"
exec gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker api.main:app