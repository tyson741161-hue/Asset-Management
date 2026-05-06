#!/bin/bash

# IT Asset Management System - Docker Stop Script

echo "=========================================="
echo "Stopping IT Asset Management System"
echo "=========================================="
echo ""

docker-compose down

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Container stopped successfully"
    echo ""
else
    echo ""
    echo "❌ Failed to stop container"
    echo ""
    exit 1
fi
