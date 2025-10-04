#!/bin/bash

echo "Starting Document Chat Application..."
echo "===================================="
echo ""

# Check if both backend and frontend directories exist
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "Error: Backend or frontend directory not found."
    echo "Please ensure you're running this script from the project root directory."
    exit 1
fi

# Function to start backend
start_backend() {
    echo "Starting backend..."
    cd backend
    chmod +x ./mvnw
    ./mvnw spring-boot:run &
    BACKEND_PID=$!
    cd ..
    echo "Backend started with PID: $BACKEND_PID"
}

# Function to start frontend
start_frontend() {
    echo "Waiting for backend to start..."
    sleep 10
    
    echo "Starting frontend..."
    cd frontend
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install
    fi
    
    npm start &
    FRONTEND_PID=$!
    cd ..
    echo "Frontend started with PID: $FRONTEND_PID"
}

# Start both services
start_backend
start_frontend

echo ""
echo "Application is starting up..."
echo "Backend: http://localhost:8080"
echo "Frontend: http://localhost:4200"
echo "H2 Database Console: http://localhost:8080/h2-console"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for user interrupt
trap 'echo ""; echo "Stopping services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT

# Keep script running
wait
