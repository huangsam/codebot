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

**Basic usage** (requires OpenAI API key):
```bash
python code_review_agent.py
```

This will review `test_script.py` and provide suggestions for improvements.

**Demo without API key** (shows tool functionality):
```bash
python demo.py
```

**Run examples** (see `examples.py` for more):
```bash
python examples.py
```

**Run tests**:
```bash
python test_code_review_agent.py
```

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

### Project Structure

```
codebot/
├── code_review_agent.py      # Main agent implementation with tools
├── test_script.py             # Sample Python file with code issues
├── demo.py                    # Demo script (no API key needed)
├── examples.py                # Usage examples with different configurations
├── test_code_review_agent.py # Unit tests for the agent
├── test_tools.py              # Simple tool testing script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Implementation Details

The implementation follows the requirements:

1. ✅ **LangChain Tools**: Both `read_code()` and `run_linter()` are decorated with `@tool` from LangChain
2. ✅ **Agent Initialization**: Uses `ChatOpenAI` with tools bound via `bind_tools()`
3. ✅ **Natural Language Instructions**: Agent accepts instructions like "Review `test_script.py` and suggest improvements"
4. ✅ **Autonomous Workflow**: Agent automatically decides when to read files and run linters based on the instruction
