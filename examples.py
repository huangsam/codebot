"""
Example usage of the code review agent with different configurations.
"""

import os
from code_review_agent import create_code_review_agent, run_agent


def example_basic_review():
    """Basic example: Review a single file."""
    print("Example 1: Basic Code Review")
    print("=" * 80)

    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Please set it to run this example.")
        print("   export OPENAI_API_KEY='your-api-key'")
        return

    # Create agent
    llm_with_tools = create_code_review_agent()

    # Run review
    result = run_agent(llm_with_tools, "Review `test_script.py` and suggest improvements")

    print(result)
    print("\n" + "=" * 80 + "\n")


def example_custom_model():
    """Example using GPT-4 model."""
    print("Example 2: Using GPT-4 Model")
    print("=" * 80)

    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Please set it to run this example.")
        return

    # Create agent with GPT-4
    llm_with_tools = create_code_review_agent(model="gpt-4")

    # Run review
    result = run_agent(llm_with_tools, "Analyze test_script.py for potential bugs and security issues")

    print(result)
    print("\n" + "=" * 80 + "\n")


def example_custom_instruction():
    """Example with custom review instructions."""
    print("Example 3: Custom Review Instructions")
    print("=" * 80)

    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Please set it to run this example.")
        return

    # Create agent
    llm_with_tools = create_code_review_agent()

    # Custom instruction focusing on specific aspects
    result = run_agent(
        llm_with_tools,
        "Review test_script.py focusing only on error handling and edge cases",
    )

    print(result)
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Code Review Agent - Usage Examples")
    print("=" * 80 + "\n")

    # Run examples (comment out the ones you don't want to run)
    example_basic_review()
    # example_custom_model()  # Uncomment to run with GPT-4
    # example_custom_instruction()  # Uncomment for custom instructions
