#!/bin/bash

echo "🚀 Starting API Converter..."
echo ""

echo "📦 Starting backend..."
cd backend && poetry run python src/main.py &
BACKEND_PID=$!

sleep 2

echo "🎨 Starting frontend..."
cd ../frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers running!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
