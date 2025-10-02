import unittest
import os
import shutil
from unittest.mock import MagicMock, patch
from backend.rag_system import RAGSystem
from backend.config import Config
from langchain_core.messages import AIMessage

class TestRAGSystem(unittest.TestCase):

    def setUp(self):
        self.test_dir = "/home/wzhao/dev/starting-ragchatbot-codebase/backend/tests"
        self.doc_content = "Course Title: Test Course\nLesson 1: Test Lesson\nThis is a test about Python."
        self.doc_path = os.path.join(self.test_dir, "test_course.txt")
        os.makedirs(os.path.dirname(self.doc_path), exist_ok=True)
        with open(self.doc_path, "w") as f:
            f.write(self.doc_content)

        self.config = Config()
        self.config.CHROMA_PATH = os.path.join(self.test_dir, "test_chroma_db")
        
        # Patch os.getenv to avoid needing a real API key
        with patch('os.getenv', return_value='fake_api_key'):
            self.rag_system = RAGSystem(self.config)

        # Add the document to the system
        self.rag_system.add_course_document(self.doc_path)

        # Mock the LLM inside the AI generator
        self.patcher = patch('langchain_openai.ChatOpenAI')
        self.MockChatOpenAI = self.patcher.start()
        self.mock_llm = self.MockChatOpenAI.return_value
        self.rag_system.ai_generator.llm = self.mock_llm

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists(self.doc_path):
            os.remove(self.doc_path)
        if os.path.exists(self.config.CHROMA_PATH):
            shutil.rmtree(self.config.CHROMA_PATH)

    def test_query_content_question_triggers_tool(self):
        # Mock the LLM to return a tool call
        mock_tool_call = {"name": "search_course_content", "args": {"query": "python"}, "id": "tool_123"}
        mock_tool_response = AIMessage(content="", tool_calls=[mock_tool_call])
        self.mock_llm.bind_tools.return_value.invoke.return_value = mock_tool_response

        # Mock the final response after tool execution
        mock_final_response = AIMessage(content="The document is about Python.")
        self.mock_llm.invoke.return_value = mock_final_response

        # Query the RAG system
        answer, sources = self.rag_system.query("What is this course about?")

        # Assertions
        # 1. Check that the LLM was invoked to decide on the tool
        self.mock_llm.bind_tools.return_value.invoke.assert_called_once()
        
        # 2. Check that the final LLM call was made to generate the answer from tool results
        self.mock_llm.invoke.assert_called_once()
        
        # 3. Check the final answer
        self.assertEqual(answer, "The document is about Python.")
        
        # 4. Check that we got sources from the tool
        self.assertGreater(len(sources), 0)
        self.assertEqual(sources[0]['text'], 'Test Course - Lesson 1')

    def test_vector_store_direct_search(self):
        # Directly query the vector store
        search_results = self.rag_system.vector_store.search(query="python")
        self.assertFalse(search_results.is_empty())
        self.assertIn("Python", search_results.documents[0])

if __name__ == '__main__':
    unittest.main()