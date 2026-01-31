#!/bin/bash
# Startup script for development

echo "Starting Mapey Application..."
echo ""

# Start backend
echo "Starting Backend API..."
cd backend
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting Frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Backend running at http://localhost:8000"
echo "Frontend running at http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
wait $BACKEND_PID $FRONTEND_PID
