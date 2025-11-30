#!/bin/bash

echo "============================================================"
echo "Starting Web Compliance API Server"
echo "============================================================"
echo ""
echo "Make sure the Report API is running on port 5000"
echo ""
echo "Starting Compliance API on port 8000..."
echo ""

cd "$(dirname "$0")"
python3 api_server.py

