
import unittest
from unittest.mock import MagicMock, patch
from backend.search_tools import CourseSearchTool
from backend.vector_store import SearchResults

class TestCourseSearchTool(unittest.TestCase):

    def setUp(self):
        self.mock_vector_store = MagicMock()
        self.search_tool = CourseSearchTool(self.mock_vector_store)

    def test_execute_success(self):
        # Mock the search results
        mock_search_results = SearchResults(
            documents=["doc1", "doc2"],
            metadata=[
                {"course_title": "Test Course", "lesson_number": 1},
                {"course_title": "Test Course", "lesson_number": 2},
            ],
            distances=[0.1, 0.2]
        )
        self.mock_vector_store.search.return_value = mock_search_results
        self.mock_vector_store.get_lesson_link.side_effect = ["link1", "link2"]

        # Execute the tool
        result = self.search_tool.execute(query="test query")

        # Assert the results
        self.assertIn("[Test Course - Lesson 1]", result)
        self.assertIn("doc1", result)
        self.assertIn("[Test Course - Lesson 2]", result)
        self.assertIn("doc2", result)
        self.assertEqual(len(self.search_tool.last_sources), 2)
        self.assertEqual(self.search_tool.last_sources[0]["text"], "Test Course - Lesson 1")
        self.assertEqual(self.search_tool.last_sources[0]["link"], "link1")

    def test_execute_no_results(self):
        # Mock empty search results
        mock_search_results = SearchResults(documents=[], metadata=[], distances=[])
        self.mock_vector_store.search.return_value = mock_search_results

        # Execute the tool
        result = self.search_tool.execute(query="test query")

        # Assert the result
        self.assertEqual(result, "No relevant content found.")

    def test_execute_with_filters(self):
        # Mock the search results
        mock_search_results = SearchResults(
            documents=["doc1"],
            metadata=[{"course_title": "Filtered Course", "lesson_number": 3}],
            distances=[0.1]
        )
        self.mock_vector_store.search.return_value = mock_search_results
        self.mock_vector_store.get_lesson_link.return_value = "link3"

        # Execute the tool with filters
        result = self.search_tool.execute(
            query="test query",
            course_name="Filtered Course",
            lesson_number=3
        )

        # Assert the results and that the filter was used
        self.mock_vector_store.search.assert_called_with(
            query="test query",
            course_name="Filtered Course",
            lesson_number=3
        )
        self.assertIn("[Filtered Course - Lesson 3]", result)
        self.assertIn("doc1", result)
        self.assertEqual(len(self.search_tool.last_sources), 1)
        self.assertEqual(self.search_tool.last_sources[0]["text"], "Filtered Course - Lesson 3")

    def test_execute_error(self):
        # Mock an error
        mock_search_results = SearchResults(documents=[], metadata=[], distances=[], error="Test error")
        self.mock_vector_store.search.return_value = mock_search_results

        # Execute the tool
        result = self.search_tool.execute(query="test query")

        # Assert the result
        self.assertEqual(result, "Test error")

if __name__ == '__main__':
    unittest.main()
