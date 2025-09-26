#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Build React app
cd frontend
npm install
npm run build
cd ..

# Copy React build to where Django expects it
echo "Copying React build files..."
cp -r frontend/build/ ./build/

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate