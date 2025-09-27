#!/bin/bash

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Build React app from frontend directory
echo "Building React app from frontend directory..."
cd frontend
npm install
npm run build
cd ..

# Copy React build to root build directory
echo "Copying React build files..."
cp -r frontend/build/ ./build/

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations
echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!"