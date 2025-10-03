import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

# Import the global app instance to access its routes
from backend.app import app

# Create a new, test-only FastAPI app.
# We will selectively copy API routes to it, excluding static file mounts
# that cause issues in a test environment.
test_api = FastAPI(title="Test RAG System")

# Copy only the API routes (those under /api) from the main app
for route in app.routes:
    if hasattr(route, "path") and route.path.startswith("/api"):
        test_api.router.routes.append(route)

# Add a root endpoint for basic connectivity checks during testing
@test_api.get("/")
def read_root():
    """A simple root endpoint for testing API availability."""
    return {"status": "ok"}

@pytest.fixture
def mock_rag_system(monkeypatch):
    """
    Mocks the RAGSystem instance used by the API endpoints.
    This fixture ensures that tests do not depend on the real RAG system,
    allowing for controlled and predictable testing.
    """
    mock = MagicMock()
    mock.session_manager = MagicMock()
    # The API endpoints in backend/app.py use a global `rag_system` instance.
    # We use monkeypatch to replace this instance with our mock for the duration of a test.
    monkeypatch.setattr("backend.app.rag_system", mock)
    return mock

@pytest.fixture(scope="session")
def client():
    """
    Provides a FastAPI TestClient for making requests to the test API.
    This is session-scoped to be efficient, as the test client setup
    is the same for all tests.
    """
    with TestClient(test_api) as c:
        yield c
