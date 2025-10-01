#!/bin/bash

# FAQ Finance Chatbot - Startup Script
echo "Starting FAQ Finance Chatbot Service..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "Running tests..."
python -m pytest tests/ -v

if [ $? -eq 0 ]; then
    echo "All tests passed!"
    echo ""
    echo "Starting FastAPI server..."
    echo "Service will be available at: http://localhost:8001"
    echo "API Documentation at: http://localhost:8001/docs"
    echo ""
    echo "Press Ctrl+C to stop the service"
    echo ""
    
    # Start the service
    python main.py
else
    echo "Tests failed. Please fix the issues before starting the service."
    exit 1
fi