# Project Overview

This project is a full-stack web application that provides a Retrieval-Augmented Generation (RAG) system for answering questions about course materials. It uses a Python backend with FastAPI and a vanilla JavaScript frontend.

**Key Technologies:**

*   **Backend:**
    *   [FastAPI](https://fastapi.tiangolo.com/): For building the REST API.
    *   [Perplexity](https://www.perplexity.ai/): As the generative AI model.
    *   [ChromaDB](https://www.trychroma.com/): As the vector store for semantic search.
    *   [SentenceTransformers](https://www.sbert.net/): For creating text embeddings.
*   **Frontend:**
    *   Vanilla JavaScript, HTML, and CSS.
    *   [marked.js](https://marked.js.org/): For rendering Markdown in the chat interface.

**Architecture:**

The application is divided into a backend and a frontend.

*   **Backend:**
    *   The main entry point is `app.py`, which creates a FastAPI application.
    *   The `RAGSystem` class in `rag_system.py` orchestrates the entire RAG pipeline.
    *   `DocumentProcessor` (`document_processor.py`) reads, parses, and chunks the course documents from the `docs` directory.
    *   `VectorStore` (`vector_store.py`) uses ChromaDB to store and retrieve document chunks and metadata.
    *   `AIGenerator` (`ai_generator.py`) interacts with the Perplexity API to generate responses.
    *   The backend exposes two API endpoints:
        *   `POST /api/query`: Takes a user query and returns an AI-generated answer with sources.
        *   `GET /api/courses`: Returns statistics about the available courses.
*   **Frontend:**
    *   The user interface is defined in `index.html` and styled with `style.css`.
    *   `script.js` handles all user interactions, communication with the backend API, and rendering of chat messages.

# Building and Running

1.  **Install Dependencies:**

    This project uses `uv` for Python package management. To install the dependencies, run:

    ```bash
    uv sync
    ```

2.  **Set up Environment Variables:**

    Create a `.env` file in the root directory and add your Perplexity API key:

    ```
    PERPLEXITY_API_KEY=your_perplexity_api_key_here
    ```

3.  **Run the Application:**

    The easiest way to run the application is to use the provided shell script:

    ```bash
    chmod +x run.sh
    ./run.sh
    ```

    Alternatively, you can run the backend manually:

    ```bash
    cd backend
    uvicorn app:app --reload --port 8000
    ```

    The application will be available at `http://localhost:8000`.

# Development Conventions

*   **Code Style:** The Python code generally follows the PEP 8 style guide.
*   **Modular Design:** The backend code is well-structured into modules with specific responsibilities (e.g., `rag_system.py`, `vector_store.py`).
*   **Configuration:** Application configuration is managed in the `config.py` file.
*   **Dependencies:** Python dependencies are managed in the `pyproject.toml` file.
*   **API:** The API is documented using OpenAPI and can be accessed at `http://localhost:8000/docs`.
*   **Frontend:** The frontend is kept simple with vanilla JavaScript, HTML, and CSS. The `marked` library is used for rendering Markdown.
