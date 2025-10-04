#!/bin/bash

echo "🔑 Setting up Gemini API Key for Document Chat Application"
echo "=================================================="

# Check if API key is already set
if [ -n "$GEMINI_API_KEY" ]; then
    echo "✅ GEMINI_API_KEY is already set"
    echo "Current value: ${GEMINI_API_KEY:0:10}..."
else
    echo "❌ GEMINI_API_KEY is not set"
    echo ""
    echo "To get your Gemini API key:"
    echo "1. Go to: https://makersuite.google.com/app/apikey"
    echo "2. Create a new API key"
    echo "3. Copy the API key"
    echo ""
    echo "Then run one of these commands:"
    echo ""
    echo "Option 1 - Set for current session:"
    echo "export GEMINI_API_KEY=your_api_key_here"
    echo ""
    echo "Option 2 - Set permanently (add to ~/.bashrc or ~/.zshrc):"
    echo "echo 'export GEMINI_API_KEY=your_api_key_here' >> ~/.bashrc"
    echo "source ~/.bashrc"
    echo ""
    echo "Option 3 - Set temporarily for testing:"
    echo "GEMINI_API_KEY=your_api_key_here ./start-backend.sh"
    echo ""
fi

echo ""
echo "🚀 After setting the API key, restart the backend:"
echo "cd backend && mvn spring-boot:run"