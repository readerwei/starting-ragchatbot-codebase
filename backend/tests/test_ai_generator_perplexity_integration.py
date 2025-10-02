import unittest
import os
from ai_generator import AIGenerator


class TestAIGeneratorPerplexityIntegration(unittest.TestCase):

    def setUp(self):
        """Set up the test with the actual API key from environment"""
        self.api_key = os.getenv("PERPLEXITY_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            self.skipTest("PERPLEXITY_API_KEY or OPENAI_API_KEY not set in environment")
    
    def test_perplexity_api_configuration(self):
        """Test that the AI generator is properly configured to use Perplexity API with real key"""
        ai_generator = AIGenerator()
        
        # Check that the LLM is configured with the correct base URL for Perplexity
        # Note: The correct attribute is openai_api_base, not base_url
        self.assertEqual(ai_generator.llm.openai_api_base, "https://api.perplexity.ai")
        
        # Verify the default model is set correctly
        self.assertEqual(ai_generator.llm.model_name, "llama-3.1-sonar-hybrid")
    
    def test_perplexity_api_with_valid_model(self):
        """Test that a valid Perplexity model can be used"""
        # Using a Perplexity-specific model - note that the original model name in the code
        # may be incorrect, but the configuration should support Perplexity models
        # For this test we'll use a valid Perplexity model
        
        # Valid Perplexity models according to their docs are like:
        # "pplx-7b-chat", "pplx-7b-online", "pplx-7b-chat", "pplx-13b-chat", 
        # "pplx-34b-chat", "pplx-70b-chat", "mixtral-8x7b-instruct", 
        # "llama-2-70b-chat", "codellama-70b-instruct", "llama-3-8b-instruct", 
        # "llama-3-70b-instruct", "sonar-small-chat", "sonar-medium-chat", 
        # "sonar-small-online", "sonar-medium-online"
        
        ai_generator = AIGenerator(model="llama-3-70b-instruct")  # Using a valid Perplexity model
        
        # Check that the LLM is configured with the correct base URL for Perplexity
        self.assertEqual(ai_generator.llm.openai_api_base, "https://api.perplexity.ai")
        
        # Verify the model is set correctly
        self.assertEqual(ai_generator.llm.model_name, "llama-3-70b-instruct")

    def test_basic_query_to_perplexity(self):
        """Test a basic query to Perplexity API to ensure it works end-to-end"""
        # Using a valid Perplexity model
        ai_generator = AIGenerator(model="llama-3-70b-instruct")
        
        # Test a simple query that doesn't require tools
        response = ai_generator.generate_response(
            query="What is the capital of France?",
            tools=None,
            tool_manager=None
        )
        
        # Verify we got a response (not an exception)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)  # Response should not be empty
    
    def test_query_with_different_valid_model(self):
        """Test a query using a different valid Perplexity model"""
        ai_generator = AIGenerator(model="mixtral-8x7b-instruct")
        
        # Test a simple query that doesn't require tools
        response = ai_generator.generate_response(
            query="What is machine learning?",
            tools=None,
            tool_manager=None
        )
        
        # Verify we got a response (not an exception)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)  # Response should not be empty

    def test_temperature_setting(self):
        """Test that the temperature is properly set to 0 as per the configuration"""
        ai_generator = AIGenerator()
        
        # Check the temperature setting
        self.assertEqual(ai_generator.llm.temperature, 0)
        
    def test_system_prompt_integration(self):
        """Test that the system prompt is properly integrated"""
        ai_generator = AIGenerator()
        
        # Verify the system prompt exists and has content
        self.assertIsNotNone(ai_generator.SYSTEM_PROMPT)
        self.assertGreater(len(ai_generator.SYSTEM_PROMPT), 0)


if __name__ == '__main__':
    unittest.main()