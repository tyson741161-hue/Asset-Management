#!/bin/bash

# IT Asset Management System - Docker Startup Script

echo "=========================================="
echo "IT Asset Management System"
echo "Docker Container Setup"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Please install Docker Compose first: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker is installed"
echo "✓ Docker Compose is installed"
echo ""

# Create data files if they don't exist
if [ ! -f "assets_data.json" ]; then
    echo "[]" > assets_data.json
    echo "✓ Created assets_data.json"
fi

if [ ! -f "tickets_data.json" ]; then
    echo "[]" > tickets_data.json
    echo "✓ Created tickets_data.json"
fi

if [ ! -f "requests_data.json" ]; then
    echo "[]" > requests_data.json
    echo "✓ Created requests_data.json"
fi

echo ""
echo "Building Docker image..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Failed to build Docker image"
    exit 1
fi

echo ""
echo "✓ Docker image built successfully"
echo ""
echo "Starting container..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start container"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Container started successfully!"
echo "=========================================="
echo ""
echo "Access the application at:"
echo "  - Local: http://localhost:5000"
echo "  - Network: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Login credentials:"
echo "  - Username: admin"
echo "  - Password: admin"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop: docker-compose down"
echo "  - Restart: docker-compose restart"
echo ""
echo "For more information, see DOCKER_SETUP.md"
echo "=========================================="
