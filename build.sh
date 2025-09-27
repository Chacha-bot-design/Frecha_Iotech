#!/bin/bash

# Install Python dependencies FIRST
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if package.json exists in current directory
if [ -f "package.json" ]; then
    echo "Building React app from current directory..."
    npm install
    npm run build
else
    echo "Warning: package.json not found in current directory. Skipping React build."
    echo "Looking for package.json in subdirectories..."
    find . -name "package.json" -type f | head -5
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!"