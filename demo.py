"""
Demo script showing how the agent tools work independently.
This can be run without an OpenAI API key.
"""

from code_review_agent import read_code, run_linter


def demo_tools():
    """Demonstrate the code review agent tools."""
    print("=" * 80)
    print("LLM Code Review Agent - Tool Demonstration")
    print("=" * 80)

    print("\n1. Reading code file...")
    print("-" * 80)
    code_content = read_code.invoke({"file_path": "test_script.py"})
    print(code_content)

    print("\n" + "=" * 80)
    print("\n2. Running linter...")
    print("-" * 80)
    linter_results = run_linter.invoke({"file_path": "test_script.py"})
    print(linter_results)

    print("\n" + "=" * 80)
    print("\n✓ Tools are working correctly!")
    print("\nTo run the full agent with LLM-powered code review:")
    print("  1. Set OPENAI_API_KEY environment variable")
    print("  2. Run: python code_review_agent.py")
    print("=" * 80)


if __name__ == "__main__":
    demo_tools()
