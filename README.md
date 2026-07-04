# Smart Agent

Smart Agent is a small learning project that demonstrates the core building
blocks of an agentic AI application with Python and a locally running Ollama
model.

The project intentionally keeps the implementation simple so that the agent
loop, tool usage, planning, and evaluation steps can be studied without relying
on a full agent framework.

## What This Project Demonstrates

- Planning a user request before taking action
- Selecting and running simple tools
- Passing tool results back into an LLM
- Evaluating whether the result is useful
- Running a small loop-based agent workflow

## Features

- Local LLM integration with Ollama
- Planner component for tool selection
- Orchestrator component for workflow control
- Evaluator component for result checking
- Calculator, file reader, and markdown report tools
- In-memory history for simple task tracking

## Requirements

- Python 3.10 or newer
- Ollama installed locally
- The recommended `qwen3.5:4b` Ollama model

## Installation

Clone the repository:

```bash
git clone https://github.com/Nidadmn/smart-agent.git
cd smart-agent
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Install the Ollama model:

```bash
ollama pull qwen3.5:4b
```

Start Ollama if it is not already running:

```bash
ollama serve
```

## Configuration

The application reads Ollama settings from environment variables:

- `OLLAMA_BASE_URL`: Ollama server URL
- `OLLAMA_MODEL`: Local model name

For local development, copy the example file and adjust it if needed:

```bash
cp .env.example .env
```

The default documented model is `qwen3.5:4b`, but any installed local Ollama
model can be used by changing `OLLAMA_MODEL`.

## Usage

Run the interactive agent demo:

```bash
python3 test_agent.py
```

Example prompts:

```text
>>> 12 * 8 + 5
>>> read test.txt
>>> report AI Agent Project
```

Type `exit` or `quit` to stop the interactive session.

## Architecture

```text
User Input
    |
    v
Planner
    |
    v
Tool Selection
    |
    v
Tool Execution
    |
    v
LLM Reasoning
    |
    v
Evaluator
    |
    v
Final Response
```

## Project Structure

```text
smart-agent/
├── agent/
│   ├── agent.py
│   ├── evaluator.py
│   ├── llm.py
│   ├── orchestrator.py
│   └── planner.py
├── memory/
│   ├── __init__.py
│   └── memory.py
├── tools/
│   ├── __init__.py
│   ├── base_tool.py
│   ├── calculator_tool.py
│   ├── file_tool.py
│   └── report_tool.py
├── workflows/
│   ├── __init__.py
│   └── task_workflow.py
├── main.py
├── requirements.txt
├── test_agent.py
├── test_llm.py
├── test_run.py
└── test.txt
```

## Current Limitations

This is a learning project, not a production-ready agent runtime. Some useful
next improvements are:

- Add automated tests for tools, planning, and orchestration
- Add a single documented application entry point
- Align the tool interface used by every component
- Read Ollama settings from environment variables instead of hard-coded defaults
- Make dependency management reproducible
- Harden file access and calculator execution
- Add CI after tests are introduced

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md)
before opening a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
