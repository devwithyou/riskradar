#!/bin/bash

echo "🛡️  Starting WebGuard Security Scanner..."
echo "========================================"
echo ""

# Activate virtual environment
source venv/bin/activate

# Start Django server
echo "🚀 Starting Django server on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver


