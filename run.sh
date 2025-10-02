#!/bin/bash

# Script to run the Course Materials RAG System

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if uv is installed
if ! command_exists uv; then
    echo "Error: uv is not installed."
    echo "Please install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if .env file exists and has API key
if [ ! -f .env ]; then
    echo "Warning: .env file not found."
    echo "Create a .env file in the root directory and add your Perplexity API key:"
    echo "  PERPLEXITY_API_KEY=your_perplexity_api_key_here"
    echo "For now, you can set the environment variable directly in your terminal:"
    echo "  export PERPLEXITY_API_KEY=your_perplexity_api_key_here"
else
    # Source the .env file to load environment variables
    set -a
    source .env
    set +a
fi

# Check if API key is set
if [ -z "$PERPLEXITY_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: PERPLEXITY_API_KEY or OPENAI_API_KEY environment variable is not set."
    echo "Make sure you have set your PERPLEXITY_API_KEY in .env"
    echo "or export your API key in your terminal:"
    echo "  export PERPLEXITY_API_KEY=your_perplexity_api_key_here"
    echo "or:"
    echo "  export OPENAI_API_KEY=your_perplexity_api_key_here"
fi

# Run the backend server
echo "Starting the Course Materials RAG System server..."
echo "Application will be available at http://localhost:8000"

exec uv run uvicorn backend.app:app --reload --port 8000