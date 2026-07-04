# Smart Agent

Smart Agent is a small, from-scratch Python project for learning the basic
building blocks of an agentic AI application. It runs against a local Ollama
model and intentionally avoids full agent frameworks so the core architecture is
easy to read, debug, and extend.

This repository is designed as a learning project, not a production agent
runtime. The code favors clear interfaces, simple control flow, and testable
components over framework complexity.

This project was created as a post-workshop self-improvement project after the
[PIA Team AI Workshop 2026](https://pia-team.github.io/workshop-ai-2026).

## Table of Contents

- [Why This Project Exists](#why-this-project-exists)
- [Features](#features)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Learning Handbook](#learning-handbook)
- [Security Notes](#security-notes)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Why This Project Exists

The goal is to show how a small agent can be assembled from understandable
parts:

- an LLM client for local Ollama inference
- a planner that decides whether a tool is needed
- tools with one consistent input/output interface
- an orchestrator that connects planning, tools, and chat responses
- tests that document expected behavior

The project currently follows the from-scratch learning path. Dependencies such
as `smolagents`, `litellm`, and the Ollama Python client are not used because
the implementation talks to Ollama directly through HTTP.

## Features

- Local Ollama integration with configurable model and base URL
- Environment-based configuration via `.env.example`
- Deterministic routing for common tool commands
- LLM fallback for ambiguous planning and direct chat
- Safe calculator tool for basic arithmetic
- Workspace-limited file reader tool
- Markdown report generator tool
- Typed result objects for plans, tool results, and agent responses
- Unit tests for configuration, planning, tools, and orchestration

## How It Works

```text
User Input
    |
    v
Planner
    |
    v
Tool needed?
    | yes
    v
Tool Execution
    |
    v
Final Response

Tool needed?
    | no
    v
Ollama Chat
    |
    v
Final Response
```

For known commands such as math, file reading, and report generation, the
planner routes directly to a local tool. For normal chat requests, the
orchestrator sends the prompt to Ollama and returns the model response.

## Requirements

- Python 3.10 or newer
- Ollama installed locally
- A local Ollama model

The recommended default model is:

```bash
ollama pull qwen3.5:4b
```

Other small local models are listed in `.env.example`.

## Quick Start

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

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the recommended model:

```bash
ollama pull qwen3.5:4b
```

Start Ollama if it is not already running:

```bash
ollama serve
```

Run the agent:

```bash
python3 main.py
```

## Configuration

The application reads runtime settings from environment variables:

- `OLLAMA_BASE_URL`: Ollama server URL
- `OLLAMA_MODEL`: local model name

For local development, copy the example file:

```bash
cp .env.example .env
```

The committed `.env.example` file is safe to share. The real `.env` file is for
local values and should not be committed. In Docker, CI, or production-like
environments, set real environment variables instead of editing source code.

## Usage

Start the interactive prompt:

```bash
python3 main.py
```

Example commands:

```text
>>> 12 * 8 + 5
101

>>> read test.txt
# Agent Report

Bu benim ilk agent raporum.

>>> report AI Agent Project
Report created: report.md
```

Chat requests are sent to the configured Ollama model:

```text
>>> Merhaba, tek cümle cevap ver.
Merhaba! Size nasıl yardımcı olabilirim?
```

Type `exit` or `quit` to stop the interactive session.

## Testing

Run the full unit test suite:

```bash
python3 -m unittest discover -v
```

The tests cover:

- Ollama configuration loading
- planner routing behavior
- orchestrator behavior
- calculator safety
- workspace-limited file reading
- report generation

## Project Structure

```text
smart-agent/
├── agent/
│   ├── __init__.py
│   ├── llm.py
│   ├── orchestrator.py
│   ├── planner.py
│   └── types.py
├── tools/
│   ├── __init__.py
│   ├── base_tool.py
│   ├── calculator_tool.py
│   ├── file_tool.py
│   └── report_tool.py
├── tests/
│   ├── __init__.py
│   ├── test_llm_config.py
│   ├── test_orchestrator.py
│   ├── test_planner.py
│   └── test_tools.py
├── .env.example
├── CONTRIBUTING.md
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
└── test.txt
```

## Learning Handbook

This repository includes a detailed learning handbook for future development:

- [Smart Agent Learning Handbook](docs/learning-handbook.md)

## Security Notes

This project executes local tools, so tool boundaries matter:

- The calculator tool does not use Python `eval`.
- The file tool only reads files inside the configured workspace root.
- `.env` files are ignored by git and should not contain committed secrets.
- Ollama runs locally by default at `http://localhost:11434`.

This is still a learning project. Review tool behavior carefully before adding
tools that write files, call external services, or process untrusted input.

## Roadmap

Useful next improvements:

- Add GitHub Actions CI for the unit test suite.
- Add `pyproject.toml` packaging metadata.
- Decide whether to keep `requirements.txt` or move to a lockfile workflow.
- Add richer tool schemas if the project grows.
- Add a non-interactive CLI mode for scripted usage.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md)
before opening a pull request.

When contributing, prefer small pull requests with clear motivation and tests
for behavior changes.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
