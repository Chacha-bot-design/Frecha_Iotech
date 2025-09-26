#!/bin/bash
# Build the React app
echo "Building React app..."
cd frontend
npm install
npm run build
cd ..

# Copy React build to Django static files
echo "Copying React build to Django static..."
mkdir -p staticfiles
cp -r frontend/build/* staticfiles/

# Collect Django static files
echo "Collecting Django static files..."
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate