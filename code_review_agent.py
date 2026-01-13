"""
LLM Code Review Agent using LangChain.

This module implements an autonomous agent that can read code files and run linters
to provide code review suggestions based on natural language instructions.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def read_code(file_path: str) -> str:
    """
    Read the contents of a code file.

    Args:
        file_path: Path to the code file to read

    Returns:
        The contents of the file as a string
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"File contents of {file_path}:\n{content}"
    except FileNotFoundError:
        return f"Error: File {file_path} not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def run_linter(file_path: str) -> str:
    """
    Run pylint on a Python file to check for code quality issues.

    Args:
        file_path: Path to the Python file to lint

    Returns:
        Linter output with issues found and suggestions
    """
    try:
        # Validate file path to prevent command injection
        path = Path(file_path)
        if not path.exists():
            return f"Error: File {file_path} not found"
        if not path.is_file():
            return f"Error: {file_path} is not a file"
        if path.suffix not in [".py", ".pyw"]:
            return f"Error: {file_path} is not a Python file"

        # Run pylint with custom options
        # Note: check=False because pylint returns non-zero for code with issues
        result = subprocess.run(
            ["pylint", str(path.resolve()), "--output-format=text"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        output = result.stdout
        if result.stderr:
            output += f"\n{result.stderr}"

        if not output.strip():
            output = "No linting issues found. Code looks good!"

        return f"Pylint results for {file_path}:\n{output}"
    except FileNotFoundError:
        return "Error: pylint is not installed. Please install it with: pip install pylint"
    except subprocess.TimeoutExpired:
        return "Error: Linting timed out"
    except Exception as e:
        return f"Error running linter: {str(e)}"


def create_code_review_agent(openai_api_key: Optional[str] = None, model: str = "gpt-3.5-turbo") -> Runnable:
    """
    Create a LangChain agent for code review.

    Args:
        openai_api_key: OpenAI API key (if not set in environment)
        model: OpenAI model to use (default: gpt-3.5-turbo)

    Returns:
        Runnable model configured with code review tools
    """
    # Set API key if provided
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key

    # Initialize LLM with tools
    llm = ChatOpenAI(model=model, temperature=0)

    # Bind tools to the LLM
    tools = [read_code, run_linter]
    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools


def run_agent(llm_with_tools: Runnable, instruction: str) -> str:
    """
    Run the agent with a given instruction.

    Args:
        llm_with_tools: LLM configured with tools
        instruction: The instruction to execute

    Returns:
        The agent's response
    """
    # System message to guide the agent
    system_prompt = """You are a helpful code review assistant. You have access to tools that can:
1. Read code files
2. Run pylint to check for code quality issues

When reviewing code, you should:
- First read the code file to understand what it does
- Then run the linter to identify issues
- Finally, provide a comprehensive review with specific suggestions for improvements
- Focus on code quality, best practices, and potential bugs
- Be constructive and helpful in your feedback"""

    # Create messages
    messages: list[BaseMessage] = [HumanMessage(content=f"{system_prompt}\n\nUser instruction: {instruction}")]

    # Invoke the LLM
    response = llm_with_tools.invoke(messages)

    # Check if tools need to be called
    if hasattr(response, "tool_calls") and response.tool_calls:
        print("\n🔧 Agent is using tools...\n")

        # Execute tool calls
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"Calling tool: {tool_name} with args: {tool_args}")

            # Execute the appropriate tool
            if tool_name == "read_code":
                result = read_code.invoke(tool_args)
            elif tool_name == "run_linter":
                result = run_linter.invoke(tool_args)
            else:
                result = f"Unknown tool: {tool_name}"

            print(f"Tool result (first 200 chars): {result[:200]}...\n")

            # Add tool result to messages
            messages.append(response)
            messages.append(HumanMessage(content=f"Tool {tool_name} returned: {result}"))

        # Get final response after tool execution
        final_response = llm_with_tools.invoke(messages)
        return str(final_response.content)

    return str(response.content)


def main():
    """
    Main function to demonstrate the code review agent.
    """
    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        return

    # Create agent
    print("Initializing code review agent...")
    llm_with_tools = create_code_review_agent()

    # Run agent with instruction
    instruction = "Review `test_script.py` and suggest improvements"
    print(f"\nInstruction: {instruction}\n")
    print("=" * 80)

    # Execute agent
    result = run_agent(llm_with_tools, instruction)

    print("\n" + "=" * 80)
    print("\nAgent Response:")
    print(result)


if __name__ == "__main__":
    main()
