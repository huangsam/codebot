"""
Simple test to verify the tools work independently.
"""

from code_review_agent import read_code, run_linter


def test_read_code():
    """Test the read_code tool."""
    print("Testing read_code tool...")
    result = read_code.invoke({"file_path": "test_script.py"})
    print(result[:200] + "...")
    print("✓ read_code tool works!\n")


def test_run_linter():
    """Test the run_linter tool."""
    print("Testing run_linter tool...")
    result = run_linter.invoke({"file_path": "test_script.py"})
    print(result[:300] + "...")
    print("✓ run_linter tool works!\n")


if __name__ == "__main__":
    test_read_code()
    test_run_linter()
    print("All tools are functioning correctly!")
