#
#!/bin/bash
set -o errexit

# Build React frontend if source exists
if [ -d "frontend" ]; then
    echo "Building React frontend..."
    cd frontend
    npm install
    npm run build
    cd ..
    # Move build to root
    mv frontend/build/ build/
fi

# Django setup
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
