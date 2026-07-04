# Smart Agent Learning Handbook

This handbook summarizes the most important lessons learned while reviewing and
improving this project after the PIA Team AI Workshop 2026.

It is written for the project author as a practical reference. The goal is not
to criticize the first version of the project. The goal is to explain what was
found, why it mattered, what was improved, and what topics are worth studying
next.

## 1. Project Context

This project started as a post-workshop self-improvement exercise after an
agentic AI workshop. That is a good context: the first version does not need to
be perfect. A learning project should show curiosity, experimentation, and
iteration.

However, once a project is shared on GitHub, it also becomes a communication
artifact. Other developers should be able to understand:

- what the project does,
- how to run it,
- what dependencies it needs,
- what is intentionally simple,
- what is not production-ready yet,
- how to contribute safely.

Good engineering is not only writing code that works on your machine. It is
also making the project understandable, reproducible, maintainable, and honest
about its current limits.

## 2. Initial Findings

The first review found several important issues.

### 2.1 The Project Declared Dependencies It Did Not Use

The project listed packages such as `smolagents`, `litellm`, and `ollama`, but
the source code did not import or use them. The project was actually a custom
from-scratch agent that talked to Ollama through HTTP.

Why this matters:

- Unused dependencies confuse readers.
- They make installation slower and less predictable.
- They create a false impression about the architecture.
- They make dependency management harder.

Lesson:

Only list dependencies that the project actually imports and needs at runtime.

### 2.2 There Were Two Competing Agent Architectures

The project had multiple entrypoints and partially overlapping flows:

- an older `Agent` plus workflow path,
- a newer `Orchestrator` path,
- demo files named like tests,
- broken files left from earlier iterations.

Why this matters:

- New readers cannot tell which entrypoint is official.
- Old code can break even if the new code works.
- Tests and documentation become misleading.
- Maintenance becomes harder because fixes must be applied in multiple places.

Lesson:

One small project should have one clear entrypoint and one clear architecture.

### 2.3 Tool Interfaces Were Inconsistent

The base tool interface expected `run()`, but the agent code called
`execute()`. This caused runtime failures such as:

```text
AttributeError: 'CalculatorTool' object has no attribute 'execute'
```

Why this matters:

- Interfaces are contracts.
- If a base class defines one method, every caller must use that same method.
- A project can look organized but still fail if contracts are not enforced by
  tests.

Lesson:

Define one interface, use it everywhere, and test the contract.

### 2.4 The Calculator Used `eval()`

The original calculator tool used Python `eval()` on user-controlled input.

Why this matters:

- `eval()` can execute arbitrary Python code.
- In an agentic system, tool inputs may come from a user or an LLM.
- LLM-generated tool calls must be treated as untrusted input.

Lesson:

Never use `eval()` for user or model-generated input. Prefer explicit parsers
or safe, limited interpreters.

### 2.5 The File Tool Had No Workspace Boundary

The original file tool could read arbitrary paths.

Why this matters:

- A tool that reads files should not accidentally read secrets, SSH keys, or
  system files.
- Agent tools need explicit boundaries.

Lesson:

Normalize paths and restrict file access to a known workspace root.

### 2.6 Tests Were Actually Demo Scripts

Files named `test_agent.py`, `test_run.py`, and `test_llm.py` were not real
automated tests. Some executed code at import time.

Why this matters:

- Test discovery can hang or accidentally call live services.
- Developers expect files named `test_*.py` to be safe automated tests.
- Demo scripts and tests serve different purposes.

Lesson:

Keep real tests under `tests/`. Do not name manual demos like tests.

### 2.7 Documentation Was Incomplete

The README had useful intent, but it did not fully explain:

- the real entrypoint,
- the real architecture,
- environment configuration,
- security boundaries,
- testing,
- open-source contribution expectations.

Lesson:

A README is not a decoration. It is the front door of the project.

## 3. What Was Improved

The project was refactored toward a clean from-scratch learning architecture.

### 3.1 The Project Direction Was Clarified

The project now follows the from-scratch learning path. It does not pretend to
be a `smolagents` project.

This is a valid choice. For a learning project, building a small agent manually
can be more educational than immediately using a framework.

### 3.2 Unused Dependencies Were Removed

The dependency list was reduced to packages the project actually uses:

- `requests`
- `python-dotenv`

This makes installation simpler and makes the architecture easier to understand.

### 3.3 Environment-Based Configuration Was Added

The LLM configuration now uses environment variables:

- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`

The project also includes `.env.example` for safe local configuration.

Important detail:

```python
load_dotenv(override=False)
```

This means local `.env` values are useful during development, but real
environment variables from Docker, CI, or deployment environments are not
overwritten.

### 3.4 A Single Entry Point Was Kept

The official app entrypoint is now:

```bash
python3 main.py
```

This makes the project easier to run and document.

### 3.5 The Tool Contract Was Standardized

Every tool now follows the same interface:

```python
run(tool_input: str) -> ToolResult
```

This is simple and enough for the current project.

### 3.6 Typed Result Objects Were Added

The project now uses typed data objects for:

- `Plan`
- `ToolResult`
- `AgentResult`
- `HistoryEntry`

This makes the data flow easier to understand and test.

### 3.7 The Calculator Was Made Safer

The calculator no longer uses `eval()`. It uses a limited AST-based evaluator
for basic arithmetic.

This is safer and more explicit.

### 3.8 File Access Was Restricted

The file tool now resolves paths and rejects paths outside the workspace root.

This makes the agent safer by default.

### 3.9 Tests Were Added

Unit tests now cover:

- configuration loading,
- planner routing,
- orchestrator behavior,
- calculator safety,
- file access boundaries,
- report generation.

The full test suite can be run with:

```bash
python3 -m unittest discover -v
```

### 3.10 README and Community Files Were Improved

The repository now includes stronger open-source basics:

- `README.md`
- `CONTRIBUTING.md`
- `LICENSE`
- `.env.example`
- GitHub issue templates
- pull request template

These files make the project easier to understand, review, and improve.

## 4. Topics To Study Next

### 4.1 Dependency Management

Research:

- direct dependencies vs transitive dependencies,
- `requirements.txt` vs `pyproject.toml`,
- when `pip freeze` is useful,
- why blindly committing `pip freeze` output can be harmful,
- runtime dependencies vs development dependencies,
- lock files and reproducible environments.

Questions to answer:

- Should this project stay with `requirements.txt`?
- Should it move to `pyproject.toml`?
- Should versions be pinned exactly or constrained with ranges?
- How should test and lint dependencies be separated from runtime dependencies?

### 4.2 Python Packaging

Research:

- `pyproject.toml`,
- package metadata,
- console script entrypoints,
- editable installs with `pip install -e .`,
- source layout options.

Goal:

Make the project installable and runnable as a real Python package.

### 4.3 Testing Strategy

Study:

- unit tests,
- integration tests,
- mocking external services,
- testing environment variables,
- testing file system behavior safely,
- naming tests clearly.

Key idea:

Tests should prove behavior. They should not simply execute scripts.

### 4.4 CI/CD

Research GitHub Actions for:

- running tests on every pull request,
- checking formatting,
- checking linting,
- running on multiple Python versions.

Goal:

Make GitHub automatically verify that the project still works.

### 4.5 LLM and Agent Design

Study:

- tool calling,
- planning,
- ReAct loops,
- prompt design,
- structured outputs,
- tool schemas,
- safe tool execution,
- when not to use an agent.

Important lesson:

Not every problem needs an agent. If simple deterministic code solves the task,
prefer deterministic code.

### 4.6 Local Model Operations

Research:

- Ollama model sizes,
- context windows,
- GPU memory usage,
- model warm-up time,
- thinking models vs instruct models,
- latency tradeoffs.

Local LLMs can work well, but they are slower and less predictable than normal
Python functions. Use the LLM only where it adds value.

## 5. Building Agents: Engineering Principles

### 5.1 Keep the Agent Small at First

A small working agent is better than a large broken architecture.

Start with:

- one model,
- one planner,
- a few tools,
- one orchestrator,
- tests.

Add complexity only when there is a real need.

### 5.2 Prefer Deterministic Routing for Simple Tasks

If the user asks:

```text
2 + 2 hesapla
```

the project does not need an LLM to decide that this is math. Deterministic
routing is faster, cheaper, easier to test, and easier to debug.

Use the LLM for ambiguity, natural language, and reasoning. Do not use it for
everything.

### 5.3 Tool Inputs Are Untrusted

Tool input may come from:

- a user,
- an LLM,
- a file,
- another tool.

Treat all of it as untrusted.

Validate inputs before executing tools.

### 5.4 Tool Outputs Should Be Structured

Returning plain strings everywhere makes debugging harder.

Use a result object with:

- success status,
- user-facing content,
- optional structured data.

This is why `ToolResult` is useful.

### 5.5 Avoid Infinite or Slow Agent Loops

Agent loops can become slow quickly because each step may call an LLM.

If a loop is needed, define:

- max steps,
- clear stop conditions,
- error handling,
- logging,
- tests.

For this project, a simple one-step orchestrator is enough.

### 5.6 Make Failure Modes Clear

Bad:

```text
Something went wrong.
```

Better:

```text
Tool is not registered: calculator
```

Clear errors help users and future maintainers.

## 6. Python Project Guidelines

### 6.1 Use Clear Module Boundaries

Good boundaries in this project:

- `agent/llm.py`: LLM client
- `agent/planner.py`: planning
- `agent/orchestrator.py`: orchestration
- `agent/types.py`: shared data types
- `tools/`: tool implementations
- `tests/`: automated tests

Each file should have one clear reason to exist.

### 6.2 Avoid Dead Code

Dead code makes a project harder to understand.

Remove:

- unused classes,
- unused modules,
- old demo scripts,
- broken experiments,
- dependencies that are not imported.

If you want to keep an experiment, document it clearly or move it outside the
main application path.

### 6.3 Use Type Hints

Type hints make code easier to read and easier to refactor.

Use them for:

- function parameters,
- return values,
- shared data objects.

Type hints are not only for tools. They are documentation for humans.

### 6.4 Keep Comments Useful

Good comments explain why something exists.

Bad comments repeat what the code already says.

Prefer clear code first. Add comments only for non-obvious decisions.

### 6.5 Do Not Hide Errors Too Broadly

Avoid broad error handling such as:

```python
except:
    ...
```

Catch specific exceptions when possible.

### 6.6 Keep Runtime Configuration Out of Source Code

Do not hard-code local model names, API URLs, secrets, or deployment-specific
settings deep inside business logic.

Use environment variables and safe defaults.

## 7. GitHub and Open-Source Project Guidelines

### 7.1 README

A good README should answer:

- What is this project?
- Why does it exist?
- How do I install it?
- How do I configure it?
- How do I run it?
- How do I test it?
- What are the limitations?
- How can I contribute?

### 7.2 License

If the README says the project is MIT licensed, the repository should include a
`LICENSE` file.

### 7.3 Contributing Guide

A `CONTRIBUTING.md` file helps contributors understand expectations before they
open a pull request.

It should explain:

- setup,
- test commands,
- pull request expectations,
- coding style,
- issue reporting.

### 7.4 Issue and Pull Request Templates

Templates help people provide useful context.

Good templates ask for:

- expected behavior,
- actual behavior,
- reproduction steps,
- environment details,
- testing notes.

### 7.5 `.gitignore`

Do not commit:

- virtual environments,
- `.env`,
- cache files,
- generated reports,
- editor-specific local files.

Commit:

- `.env.example`,
- documentation,
- tests,
- source code,
- safe templates.

## 8. Commit Standards

Good commits are small, focused, and explain intent.

### 8.1 Commit One Logical Change at a Time

Good:

- one commit for runtime refactor,
- one commit for documentation,
- one commit for test setup.

Bad:

- one huge commit mixing refactor, docs, formatting, dependencies, and unrelated
  experiments.

### 8.2 Use Clear Commit Messages

Good examples:

```text
refactor: simplify custom agent runtime
docs: expand open source project guide
test: add planner and tool coverage
fix: read Ollama settings from environment
```

A useful commit message explains what changed and why it matters.

### 8.3 Do Not Commit Secrets

Never commit:

- `.env`,
- API keys,
- tokens,
- passwords,
- personal machine paths.

### 8.4 Keep Pull Requests Reviewable

Prefer pull requests that a reviewer can understand in one sitting.

If a change is too large, split it into smaller PRs.

## 9. Repo Standards

A healthy small Python repository should usually include:

- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `.gitignore`
- `.env.example`
- `requirements.txt` or `pyproject.toml`
- `tests/`
- GitHub templates
- one documented entrypoint

The repository should avoid:

- multiple competing entrypoints,
- unused dependencies,
- broken experimental files,
- generated artifacts,
- unclear test/demo naming.

## 10. Over-Engineering vs Simplicity

Over-engineering means adding complexity before the project needs it.

Examples:

- multiple agent classes when one orchestrator is enough,
- a separate memory package for a small in-memory list,
- an evaluator LLM loop before basic tool execution works,
- framework dependencies that are not used,
- many entrypoints with unclear responsibility.

Simplicity does not mean low quality.

Simplicity means:

- fewer moving parts,
- clearer contracts,
- easier tests,
- easier debugging,
- easier onboarding.

The best architecture is the smallest architecture that solves the current
problem well.

## 11. Outcome-Oriented Development

A good engineering workflow asks:

1. What user-visible problem are we solving?
2. What is the smallest change that solves it?
3. How will we prove it works?
4. What should not be changed right now?
5. What should be documented for the next developer?

Avoid working only to make code look more impressive. Work to make the project
more correct, understandable, and useful.

## 12. Suggested Next Milestones

Recommended next steps for this project:

1. Add GitHub Actions CI for `python3 -m unittest discover -v`.
2. Decide on dependency strategy: `requirements.txt`, `pyproject.toml`, or a
   lockfile-based workflow.
3. Add a non-interactive CLI command for scripted usage.
4. Add structured tool descriptions if the planner becomes more advanced.
5. Add logging for LLM calls and tool execution.
6. Explore a framework version separately if you want to compare from-scratch
   architecture with `smolagents`.

## 13. Final Advice

You did the most important thing already: you built something.

The next level is learning how to make that something:

- easier to run,
- easier to read,
- easier to test,
- easier to review,
- easier to maintain,
- safer by default.

That is the difference between a script and an engineering project.

Keep building, but keep the project honest. If something is experimental, say
so. If something is broken, write a test. If something is unused, remove it. If
something is confusing, simplify it.
