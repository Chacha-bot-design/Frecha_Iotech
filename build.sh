#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Build React app
cd frontend
npm install
npm run build
cd ..

# MANUAL COPY - Nuclear option
echo "=== Manual file copy ==="
mkdir -p templates staticfiles/static/js staticfiles/static/css

# Copy index.html
cp frontend/build/index.html templates/

# Manual copy of static files
cp -r frontend/build/static/* staticfiles/static/ || echo "Manual copy failed"

# Verify files
echo "=== Verifying files ==="
find staticfiles -name "*.js" -o -name "*.css" | head -10

python manage.py migrate
echo "Build completed!"