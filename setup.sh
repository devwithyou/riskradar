#!/bin/bash

echo "🛡️  WebGuard Security Scanner - Setup Script"
echo "============================================"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations analyzer
python manage.py migrate

# Create superuser (optional)
echo ""
echo "📝 Create an admin user? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Install Tailwind dependencies
echo ""
echo "🎨 Installing Tailwind CSS dependencies..."
cd theme/static_src
npm install
npm run build
cd ../..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Terminal 1: source venv/bin/activate && python manage.py runserver"
echo "  2. Terminal 2 (optional): cd theme/static_src && npm run dev"
echo ""
echo "Then visit: http://localhost:8000"

