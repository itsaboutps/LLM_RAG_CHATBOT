#!/bin/bash

echo "Installing Maven and running Document Chat Application..."
echo "========================================================"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Install Maven
echo "Installing Maven..."
brew install maven

# Verify Maven installation
mvn -version

# Navigate to backend and run
echo "Starting backend..."
cd backend
mvn spring-boot:run &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 20

# Check if backend is running
if curl -s http://localhost:8080/api/documents > /dev/null; then
    echo "Backend started successfully!"
    
    # Start frontend
    echo "Starting frontend..."
    cd ../frontend
    
    # Install Node.js if not present
    if ! command -v node &> /dev/null; then
        echo "Installing Node.js..."
        brew install node
    fi
    
    # Install dependencies and start
    npm install
    npm start &
    FRONTEND_PID=$!
    
    echo ""
    echo "🎉 Application is running!"
    echo "Frontend: http://localhost:4200"
    echo "Backend: http://localhost:8080"
    echo "Database Console: http://localhost:8080/h2-console"
    echo ""
    echo "Press Ctrl+C to stop both services"
    
    # Wait for user interrupt
    trap 'echo ""; echo "Stopping services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT
    wait
    
else
    echo "Failed to start backend. Please check the logs."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
