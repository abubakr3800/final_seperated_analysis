#!/bin/bash

echo "============================================================"
echo "Starting LuxSCale API Server"
echo "============================================================"
echo ""
echo "Server will start on http://localhost:8001"
echo ""
echo "Starting API server..."
echo ""

cd "$(dirname "$0")"
python3 api_server.py

