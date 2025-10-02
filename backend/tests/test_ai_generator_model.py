import unittest
from unittest.mock import patch
from ai_generator import AIGenerator


class TestAIGeneratorModel(unittest.TestCase):

    def test_default_model_configuration(self):
        """Test that the AI generator uses the default model when none is specified"""
        with patch('os.getenv', return_value='fake_api_key'):
            ai_generator = AIGenerator()
        
        # Check that the default model is set correctly
        self.assertEqual(ai_generator.model, "llama-3.1-sonar-hybrid")
        
        # Verify that the LLM was initialized with the correct model
        self.assertEqual(ai_generator.llm.model_name, "llama-3.1-sonar-hybrid")

    def test_custom_model_configuration(self):
        """Test that the AI generator uses a custom model when specified"""
        custom_model = "llama-3.1-8b-instruct"
        
        with patch('os.getenv', return_value='fake_api_key'):
            ai_generator = AIGenerator(model=custom_model)
        
        # Check that the custom model is set correctly
        self.assertEqual(ai_generator.model, custom_model)
        
        # Verify that the LLM was initialized with the correct model
        self.assertEqual(ai_generator.llm.model_name, custom_model)

    def test_model_parameter_passed_to_llm(self):
        """Test that the model parameter is properly stored and used"""
        test_models = [
            "llama-3.1-sonar-hybrid",
            "llama-3.1-8b-instruct", 
            "mistral-7b-instruct",
            "gpt-4-turbo"
        ]
        
        for model_name in test_models:
            with patch('os.getenv', return_value='fake_api_key'):
                ai_generator = AIGenerator(model=model_name)
                
                # Verify the model is correctly stored in both the instance and the LLM
                self.assertEqual(ai_generator.model, model_name)
                self.assertEqual(ai_generator.llm.model_name, model_name)


if __name__ == '__main__':
    unittest.main()