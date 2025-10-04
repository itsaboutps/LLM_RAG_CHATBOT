#!/bin/bash

echo "Starting Document Chat Backend..."
echo "=================================="

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "Error: Java is not installed. Please install Java 17 or higher."
    exit 1
fi

# Check Java version
JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
if [ "$JAVA_VERSION" -lt 17 ]; then
    echo "Error: Java 17 or higher is required. Current version: $JAVA_VERSION"
    exit 1
fi

# Navigate to backend directory
cd backend

# Check if Maven is available
if ! command -v mvn &> /dev/null; then
    echo "Error: Maven is not installed. Please install Maven."
    exit 1
fi

# Start the application
echo "Starting Spring Boot application..."
echo "Backend will be available at: http://localhost:8080"
echo "H2 Database Console: http://localhost:8080/h2-console"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

mvn spring-boot:run
