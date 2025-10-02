import unittest
from unittest.mock import MagicMock, patch
from ai_generator import AIGenerator
from langchain_core.messages import AIMessage

class TestAIGenerator(unittest.TestCase):

    def setUp(self):
        self.mock_tool_manager = MagicMock()
        # Patch ChatOpenAI instead of ChatOllama
        self.patcher = patch('langchain_openai.ChatOpenAI')
        self.MockChatOpenAI = self.patcher.start()
        self.mock_llm = self.MockChatOpenAI.return_value
        
        # Mock os.getenv to avoid needing a real API key
        with patch('os.getenv', return_value='fake_api_key'):
            self.ai_generator = AIGenerator(model="test_model")
        
        self.ai_generator.llm = self.mock_llm

    def tearDown(self):
        self.patcher.stop()

    def test_generate_response_with_tool_call(self):
        # Mock the ChatOpenAI client and its response
        mock_tool_call = {"name": "search_course_content", "args": {"query": "test"}, "id": "tool_123"}
        mock_response = AIMessage(content="", tool_calls=[mock_tool_call])
        self.mock_llm.bind_tools.return_value.invoke.return_value = mock_response

        # Mock the tool manager's execution result
        self.mock_tool_manager.execute_tool.return_value = "Tool search result"

        # Mock the final response after tool execution
        mock_final_response = AIMessage(content="Final answer")
        # The first call is the tool use, the second is the final answer
        self.mock_llm.invoke.return_value = mock_final_response

        # Generate a response
        response = self.ai_generator.generate_response(
            query="test query",
            tools=[{"name": "search_course_content"}],
            tool_manager=self.mock_tool_manager
        )

        # Assert that the tool was called and the final response is correct
        self.mock_tool_manager.execute_tool.assert_called_once_with(
            "search_course_content", query="test"
        )
        self.assertEqual(response, "Final answer")

    def test_generate_response_no_tool_call(self):
        # Mock the ChatOpenAI client and its response
        mock_response = AIMessage(content="Direct answer", tool_calls=[])
        # This test needs to mock the regular invoke, not the bind_tools().invoke()
        self.mock_llm.invoke.return_value = mock_response

        # Generate a response without tools
        response = self.ai_generator.generate_response(
            query="test query",
            tool_manager=self.mock_tool_manager
        )

        # Assert that the tool was not called and the direct answer is returned
        self.mock_tool_manager.execute_tool.assert_not_called()
        self.assertEqual(response, "Direct answer")

if __name__ == '__main__':
    unittest.main()
