#!/bin/bash

# Install Python dependencies
echo "=== Installing dependencies ==="
pip install -r requirements.txt

# Build React app
echo "=== Building React app ==="
cd frontend
npm install
npm run build
cd ..

# Debug: Show what was built
echo "=== React build contents ==="
find ./frontend/build -type f | head -10

# Create templates directory
mkdir -p templates

# Copy ONLY index.html to templates
cp frontend/build/index.html templates/

# IMPORTANT: Manual copy of static files to staticfiles directory
echo "=== Manually copying static files ==="
mkdir -p staticfiles/static
cp -r frontend/build/static/* staticfiles/static/ || echo "Manual copy completed"

# Verify the files are there
echo "=== Verifying static files ==="
find ./staticfiles -name "*.js" -o -name "*.css" | head -10

# Run Django setup
echo "=== Django setup ==="
python manage.py migrate
python manage.py collectstatic --noinput --clear

echo "=== Build complete ==="