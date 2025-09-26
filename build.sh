#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Build React app
cd frontend
npm install
npm run build
cd ..

# Copy React build to the root so Django can find it
cp -r frontend/build/* ./

# Collect static files to STATIC_ROOT
python manage.py collectstatic --noinput --clear

# Run migrations
python manage.py migrate