# Contributing

Thank you for your interest in improving Smart Agent.

This is a learning-oriented project, so contributions should prioritize clear
code, small changes, and explanations that help future readers understand the
agent architecture.

## Development Setup

1. Fork or clone the repository.
2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install and start Ollama:

```bash
ollama pull qwen3.5:4b
ollama serve
```

5. Run the interactive demo:

```bash
python3 test_agent.py
```

## Pull Request Guidelines

- Keep pull requests focused on one topic.
- Explain the motivation behind the change.
- Include before/after behavior when changing runtime logic.
- Avoid mixing documentation updates with large code refactors.
- Prefer simple Python code over unnecessary abstractions.
- Do not commit secrets, local `.env` files, virtual environments, or generated
  cache files.

## Code Style

- Use clear English names for modules, classes, functions, and variables.
- Keep tool interfaces consistent across the project.
- Prefer explicit errors over silent failures.
- Add comments only when they explain non-obvious behavior.

## Reporting Issues

When opening an issue, include:

- What you expected to happen
- What actually happened
- Steps to reproduce the behavior
- Your Python version
- Whether Ollama was running
