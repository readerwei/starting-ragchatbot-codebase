from fastapi.testclient import TestClient
from unittest.mock import MagicMock

def test_root_endpoint(client: TestClient):
    """Test the root endpoint to ensure the API is running."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_course_stats(client: TestClient, mock_rag_system: MagicMock):
    """Test the /api/courses endpoint for correct data and response structure."""
    # Configure the mock to return predictable analytics
    mock_rag_system.get_course_analytics.return_value = {
        "total_courses": 2,
        "course_titles": ["Test Course 1", "Test Course 2"],
    }

    response = client.get("/api/courses")
    assert response.status_code == 200
    assert response.json() == {
        "total_courses": 2,
        "course_titles": ["Test Course 1", "Test Course 2"],
    }

def test_query_documents_new_session(client: TestClient, mock_rag_system: MagicMock):
    """Test the /api/query endpoint when no session ID is provided."""
    # Configure mock for session creation and query processing
    mock_rag_system.session_manager.create_session.return_value = "new_session_123"
    mock_rag_system.query.return_value = ("Test answer", [{"text": "source1"}])

    response = client.post("/api/query", json={"query": "What is Python?"})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Test answer"
    assert data["sources"] == [{"text": "source1"}]
    assert data["session_id"] == "new_session_123"

    # Verify that a new session was created and the query was processed
    mock_rag_system.session_manager.create_session.assert_called_once()
    mock_rag_system.query.assert_called_once_with("What is Python?", "new_session_123")

def test_query_documents_existing_session(client: TestClient, mock_rag_system: MagicMock):
    """Test the /api/query endpoint with an existing session ID."""
    # Configure mock for query processing
    mock_rag_system.query.return_value = ("Another answer", [{"text": "source2"}])

    response = client.post(
        "/api/query",
        json={"query": "Tell me about FastAPI", "session_id": "existing_session_456"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Another answer"
    assert data["sources"] == [{"text": "source2"}]
    assert data["session_id"] == "existing_session_456"

    # Verify that no new session was created and the query was processed with the existing session
    mock_rag_system.session_manager.create_session.assert_not_called()
    mock_rag_system.query.assert_called_once_with(
        "Tell me about FastAPI", "existing_session_456"
    )

def test_query_endpoint_error_handling(client: TestClient, mock_rag_system: MagicMock):
    """Test that the /api/query endpoint handles exceptions gracefully."""
    # Configure the mock to raise an exception
    mock_rag_system.query.side_effect = Exception("Something went wrong")

    response = client.post("/api/query", json={"query": "This will fail"})

    assert response.status_code == 500
    assert response.json() == {"detail": "Something went wrong"}
