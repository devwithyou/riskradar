#!/bin/bash

echo "🛡️  Starting WebGuard Security Scanner..."
echo ""

# Navigate to project directory
cd /home/workspace/Projects/uni_project_information_security

# Activate virtual environment
source venv/bin/activate

# Start Django server
echo "✅ Virtual environment activated"
echo "🚀 Starting server at http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver


