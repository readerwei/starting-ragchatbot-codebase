# Course Materials RAG System - Project Context

This is a full-stack web application that provides a Retrieval-Augmented Generation (RAG) system for answering questions about course materials. It uses semantic search and AI-powered responses to help users query course content and receive intelligent, context-aware answers.

## Project Overview

The application is built with a Python backend using FastAPI and a vanilla JavaScript frontend. It enables users to ask questions about course materials and receive AI-generated responses with relevant sources.

### Key Technologies:
- **Backend:**
  - [FastAPI](https://fastapi.tiangolo.com/): REST API framework
  - [Anthropic's Claude](https://www.anthropic.com/): Generative AI model
  - [ChromaDB](https://www.trychroma.com/): Vector database for semantic search
  - [SentenceTransformers](https://www.sbert.net/): Text embedding generation
- **Frontend:**
  - Vanilla JavaScript, HTML, and CSS
  - [marked.js](https://marked.js.org/): Markdown rendering

### Architecture:

The application follows a client-server architecture:

1. **Backend (`/backend`):**
   - `app.py`: Main FastAPI application and entry point
   - `RAGSystem` (`rag_system.py`): Orchestrates the RAG pipeline
   - `DocumentProcessor` (`document_processor.py`): Processes course documents
   - `VectorStore` (`vector_store.py`): Manages ChromaDB for semantic search
   - `AIGenerator` (`ai_generator.py`): Interfaces with Anthropic Claude API
   - `SessionManager` (`session_manager.py`): Manages conversation history
   - Configuration in `config.py`

2. **Frontend (`/frontend`):**
   - `index.html`: Main user interface
   - `style.css`: Styling
   - `script.js`: Client-side logic and API communication

3. **Data (`/docs`):**
   - Contains course materials in text format
   - Currently includes 4 course scripts about Anthropic technologies

## Building and Running

### Prerequisites:
- Python 3.13 or higher
- `uv` package manager (always use uv instead of pip for this project)
- Anthropic API key

### Setup:
1. Install `uv` if not already installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install Python dependencies:
   ```bash
   uv sync
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

### Running the Application:
Use the provided shell script:
```bash
chmod +x run.sh
./run.sh
```

Or run manually:
```bash
cd backend
uv run uvicorn app:app --reload --port 8000
```

The application will be available at:
- Web Interface: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`

## Development Conventions

### Code Structure:
- **Backend:** Modular design with specific responsibilities per module
- **Frontend:** Vanilla JavaScript with minimal dependencies
- **Configuration:** Centralized in `config.py`
- **Dependencies:** Managed in `pyproject.toml`

### Testing:
- Tests are located in `/backend/tests`
- Uses pytest for testing framework
- Includes test files for core components

### API Endpoints:
1. `POST /api/query`: Process user queries and return AI-generated answers
2. `GET /api/courses`: Retrieve course statistics

### Styling:
- Backend follows PEP 8 style guide
- Frontend uses clean CSS with responsive design
- Markdown rendering for AI responses

## Key Components

### RAG System (`rag_system.py`)
Main orchestrator that handles the complete RAG workflow:
- Document processing and chunking
- Vector storage and retrieval
- AI response generation
- Session management

### Document Processing (`document_processor.py`)
Processes course documents by:
- Parsing text files with course metadata
- Chunking content for vector storage
- Extracting lesson information

### Vector Store (`vector_store.py`)
Manages ChromaDB operations:
- Storing document chunks and metadata
- Semantic search functionality
- Course analytics

### AI Generator (`ai_generator.py`)
Interfaces with Anthropic Claude API:
- Generates responses to user queries
- Implements tool-based search functionality

### Frontend (`script.js`)
Handles all client-side functionality:
- User input processing
- API communication
- Response rendering with Markdown support
- Session management

## Data Format

Course materials in `/docs` follow a structured format:
- Course title and metadata at the beginning
- Lesson sections with titles and content
- Each lesson includes relevant links

This format is parsed by the document processor to extract structured information for the RAG system.