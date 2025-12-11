#!/bin/bash

echo "🛡️  Starting WebGuard Security Scanner..."
echo "========================================"

# Activate virtual environment
source venv/bin/activate

# Start Tailwind watcher in background (optional)
echo "🎨 Starting Tailwind CSS watcher..."
cd theme/static_src
npm run dev &
TAILWIND_PID=$!
cd ../..

# Start Django server
echo "🚀 Starting Django server..."
python manage.py runserver

# Cleanup: kill Tailwind watcher when Django stops
kill $TAILWIND_PID

