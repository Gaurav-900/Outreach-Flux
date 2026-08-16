#!/bin/bash
echo "Starting Outreach-flux..."

# Start Backend
echo "Starting backend..."
cd backend
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 5000 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Outreach-flux is running!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop both servers."

# Wait and handle graceful shutdown
trap "echo 'Shutting down servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM
wait
