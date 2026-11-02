#!/bin/bash

echo "🚀 Setting up HostHive Django Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Setting up admin user..."
python manage.py shell -c "
from accounts.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@hosthive.com', 'admin123', user_type='host')
    print('✅ Admin user created: admin/admin123')
else:
    print('ℹ️ Admin user already exists')
"

# Populate sample data
echo "🎭 Adding sample data..."
python manage.py populate_data

echo "✨ Setup complete!"
echo ""
echo "🎉 HostHive is ready to use!"
echo ""
echo "To start the development server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000"
echo ""
echo "Admin panel: http://127.0.0.1:8000/admin"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Sample users:"
echo "Host: host1/password123"
echo "Client: client1/password123"