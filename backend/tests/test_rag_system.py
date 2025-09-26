import unittest
import os
from unittest.mock import MagicMock, patch
from backend.rag_system import RAGSystem
from backend.config import Config

class TestRAGSystem(unittest.TestCase):

    def setUp(self):
        # Create a dummy course file
        self.doc_content = "Course Title: Test Course\nLesson 1: Test Lesson\nThis is a test."
        self.doc_path = "/home/wzhao/dev/starting-ragchatbot-codebase/backend/tests/test_course.txt"
        with open(self.doc_path, "w") as f:
            f.write(self.doc_content)

        # Configure and initialize the RAG system
        self.config = Config()
        # Use a temporary directory for the test database
        self.config.CHROMA_PATH = "/home/wzhao/dev/starting-ragchatbot-codebase/backend/tests/test_chroma_db"
        self.rag_system = RAGSystem(self.config)
        self.rag_system.ai_generator = MagicMock()

    def tearDown(self):
        # Clean up the dummy file and test database
        os.remove(self.doc_path)
        # This is a bit of a hack, but for testing purposes it's fine
        # A better solution would be to have a dedicated test DB that gets wiped
        import shutil
        if os.path.exists(self.config.CHROMA_PATH):
            shutil.rmtree(self.config.CHROMA_PATH)

    def test_query_content_question(self):
        # Mock the AI generator
        self.rag_system.ai_generator.generate_response.return_value = "This is a test response."

        # Query the RAG system
        answer, sources = self.rag_system.query("What is this about?")

        # Assert the response
        self.assertEqual(answer, "This is a test response.")
        # Check that the AI generator was called with the tool definitions
        self.rag_system.ai_generator.generate_response.assert_called_once()
        call_args = self.rag_system.ai_generator.generate_response.call_args[1]
        self.assertIn('tools', call_args)
        self.assertIn('tool_manager', call_args)

if __name__ == '__main__':
    unittest.main()
