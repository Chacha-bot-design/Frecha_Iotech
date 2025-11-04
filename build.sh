#!/usr/bin/env bash
set -o errexit

echo "🚀 Starting production build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🔄 Applying database migrations..."
python manage.py migrate

# Create superuser if environment variables are set (secure method)
echo "👤 Setting up superuser..."
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput || echo "⚠️ Superuser creation skipped (may already exist)"
else
    echo "ℹ️ Superuser environment variables not set, skipping superuser creation"
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "✅ Production build completed successfully!"
echo "🌐 Your application is ready at: https://frecha-iotech.onrender.com"