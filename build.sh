#!/bin/bash

# Build React app
echo "Building React app..."
npm run build

# Collect static files using Django
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"