# codebot
Reviewing code via a Robot

## LLM Code Review Agent

An autonomous agent built with LangChain that reads code and runs linters based on natural language instructions.

### Features

- **Autonomous Code Review**: Uses LangChain agents with OpenAI to understand and execute code review tasks
- **Code Reading**: Reads and analyzes Python code files
- **Automated Linting**: Runs pylint to identify code quality issues
- **Natural Language Interface**: Accepts instructions in plain English

### Installation

1. Clone the repository:
```bash
git clone https://github.com/huangsam/codebot.git
cd codebot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Usage

Run the agent with the default instruction:
```bash
python code_review_agent.py
```

This will review `test_script.py` and provide suggestions for improvements.

### How It Works

The agent uses two main tools:

1. **`read_code(file_path)`**: Reads the contents of a code file
2. **`run_linter(file_path)`**: Runs pylint to check for code quality issues

When you give the agent an instruction like "Review `test_script.py` and suggest improvements", the agent will:
1. Read the file to understand the code
2. Run pylint to identify issues
3. Generate a comprehensive review with specific suggestions

### Example

```python
from code_review_agent import create_code_review_agent, run_agent

# Create the agent
llm_with_tools = create_code_review_agent()

# Run a code review
result = run_agent(llm_with_tools, "Review `test_script.py` and suggest improvements")

print(result)
```

### Technologies Used

- **LangChain**: Framework for building LLM-powered applications
- **OpenAI**: GPT models for natural language understanding
- **pylint**: Python code linter for identifying quality issues
