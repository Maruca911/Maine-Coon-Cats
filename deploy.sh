#!/bin/bash

# Stop any running server
echo "Stopping any running servers..."
pkill -f "python3 server.py" || true
sleep 2

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p css js images blog/guides-and-tips blog/wellbeing blog/behavior blog/breeding blog/toys-and-accessories

# Verify file structure
echo "Verifying file structure..."
if [ ! -f "index.html" ]; then
    echo "Error: index.html not found!"
    exit 1
fi

if [ ! -f "css/recipe.css" ]; then
    echo "Error: css/recipe.css not found!"
    exit 1
fi

if [ ! -f "css/nav.css" ]; then
    echo "Error: css/nav.css not found!"
    exit 1
fi

if [ ! -f "js/nav.js" ]; then
    echo "Error: js/nav.js not found!"
    exit 1
fi

# Set proper permissions
echo "Setting proper permissions..."
chmod -R 755 .

# Start the server
echo "Starting the server..."
python3 server.py &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Get the actual port being used
PORT=$(lsof -i -P | grep -i "listen" | grep "python3" | grep "$SERVER_PID" | awk '{print $9}' | cut -d':' -f2)
if [ -z "$PORT" ]; then
    PORT=8000
fi

# Print deployment status
echo "============================================="
echo "Deployment completed successfully!"
echo "Server is running at http://localhost:$PORT"
echo "Press Ctrl+C to stop the server"
echo "============================================="

# Keep the script running
wait $SERVER_PID 