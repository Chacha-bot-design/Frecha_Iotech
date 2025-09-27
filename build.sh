#!/bin/bash

# Install Python dependencies
echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

# Build React app
echo "=== Building React app ==="
cd frontend
npm install
npm run build
cd ..

echo "=== Build directory structure ==="
find ./frontend/build -type f | head -15

# Create templates directory if it doesn't exist
mkdir -p templates

# Copy ONLY the index.html to templates
echo "=== Copying index.html to templates ==="
cp frontend/build/index.html templates/

# IMPORTANT: Use --link option to avoid duplication and ensure proper paths
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --clear --link

echo "=== Checking collected static files ==="
find ./staticfiles -name "*.js" -o -name "*.css" | head -10

echo "=== File sizes ==="
ls -la staticfiles/static/js/ || echo "JS directory not found"
ls -la staticfiles/static/css/ || echo "CSS directory not found"

# Run migrations
echo "=== Running migrations ==="
python manage.py migrate

echo "=== Build completed successfully ==="