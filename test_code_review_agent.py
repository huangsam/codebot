"""
Unit tests for the code review agent.
Tests the tools and agent structure without requiring an OpenAI API key.
"""

import os
import sys
import unittest
from unittest.mock import patch

from code_review_agent import read_code, run_linter, create_code_review_agent


class TestCodeReviewTools(unittest.TestCase):
    """Test cases for code review tools."""

    def test_read_code_success(self):
        """Test that read_code successfully reads a file."""
        result = read_code.invoke({"file_path": "test_script.py"})
        self.assertIn("File contents of test_script.py", result)
        self.assertIn("def calculate_sum", result)

    def test_read_code_file_not_found(self):
        """Test that read_code handles missing files."""
        result = read_code.invoke({"file_path": "nonexistent_file.py"})
        self.assertIn("Error", result)
        self.assertIn("not found", result)

    def test_run_linter_success(self):
        """Test that run_linter successfully lints a file."""
        result = run_linter.invoke({"file_path": "test_script.py"})
        self.assertIn("Pylint results for test_script.py", result)
        # The test file should have some linting issues
        self.assertTrue("trailing-whitespace" in result or "missing-function-docstring" in result or "Your code has been rated" in result)

    def test_run_linter_file_not_found(self):
        """Test that run_linter handles missing files."""
        result = run_linter.invoke({"file_path": "nonexistent_file.py"})
        # Should return an error message for missing files
        self.assertIn("Error", result)
        self.assertIn("not found", result)

    def test_run_linter_non_python_file(self):
        """Test that run_linter rejects non-Python files."""
        result = run_linter.invoke({"file_path": "README.md"})
        # Should return an error message for non-Python files
        self.assertIn("Error", result)
        self.assertIn("not a Python file", result)

    def test_tools_have_correct_names(self):
        """Test that tools have the expected names."""
        self.assertEqual(read_code.name, "read_code")
        self.assertEqual(run_linter.name, "run_linter")

    def test_tools_have_descriptions(self):
        """Test that tools have proper descriptions."""
        self.assertIsNotNone(read_code.description)
        self.assertIsNotNone(run_linter.description)
        self.assertIn("Read", read_code.description)
        self.assertIn("pylint", run_linter.description)


class TestAgentCreation(unittest.TestCase):
    """Test cases for agent creation."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    def test_create_agent_with_env_key(self):
        """Test agent creation with environment API key."""
        agent = create_code_review_agent()
        self.assertIsNotNone(agent)
        # Verify it's a ChatOpenAI instance with tools bound
        self.assertTrue(hasattr(agent, "invoke"))

    @patch.dict(os.environ, {}, clear=True)
    def test_create_agent_with_provided_key(self):
        """Test agent creation with provided API key."""
        agent = create_code_review_agent(openai_api_key="test-key")
        self.assertIsNotNone(agent)
        self.assertEqual(os.environ.get("OPENAI_API_KEY"), "test-key")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    def test_create_agent_with_custom_model(self):
        """Test agent creation with custom model."""
        agent = create_code_review_agent(model="gpt-4")
        self.assertIsNotNone(agent)


class TestModuleStructure(unittest.TestCase):
    """Test the overall module structure."""

    def test_module_imports(self):
        """Test that all required imports are available."""
        import code_review_agent

        self.assertTrue(hasattr(code_review_agent, "read_code"))
        self.assertTrue(hasattr(code_review_agent, "run_linter"))
        self.assertTrue(hasattr(code_review_agent, "create_code_review_agent"))
        self.assertTrue(hasattr(code_review_agent, "run_agent"))
        self.assertTrue(hasattr(code_review_agent, "main"))


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestCodeReviewTools))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentCreation))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleStructure))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
