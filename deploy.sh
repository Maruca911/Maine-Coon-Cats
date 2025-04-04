#!/bin/bash

# Stop any running servers
echo "Stopping any running servers..."
pkill -f "python3 server.py" || true

# Update pip
echo "Updating pip..."
python3 -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p static/images
mkdir -p static/css
mkdir -p static/js

# Set proper permissions
echo "Setting proper permissions..."
chmod -R 755 static
chmod +x server.py

# Start the server
echo "Starting the server..."
# Try ports 8000-8005
for port in {8000..8005}; do
    if ! lsof -i :$port > /dev/null; then
        echo "Using port $port"
        python3 server.py $port &
        echo "============================================="
        echo "Deployment completed successfully!"
        echo "Server is running at http://localhost:$port"
        echo "Press Ctrl+C to stop the server"
        echo "============================================="
        exit 0
    fi
done

echo "Error: Could not find an available port between 8000-8005"
exit 1 