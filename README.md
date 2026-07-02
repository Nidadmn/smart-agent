# 🧠 Smart Agent (Smol Autonomous AI Agent)

This project is a minimal autonomous AI agent built from scratch using Python and Ollama LLM.

It demonstrates how an AI agent can:
- Plan actions
- Use external tools
- Execute tasks
- Evaluate results
- Run in a loop-based workflow (smol autonomy)

---

## 🚀 Features

### 🧠 LLM Integration
- Uses Ollama (Qwen 2.5 model)
- Runs locally (no API key required)

### 🛠 Tool System
- Calculator Tool (math operations)
- File Reader Tool (read local files)
- Report Generator Tool (markdown output)

### 🧭 Agent Architecture
- Planner (decides which tool to use)
- Orchestrator (controls workflow)
- Evaluator (checks correctness)
- Loop-based execution (multi-step reasoning)

---

## 🔁 Workflow


```text
User Input
     │
     ▼
 Planner
     │
     ▼
Tool Selection
     │
     ▼
Execute Tool
     │
     ▼
LLM Reasoning
     │
     ▼
Evaluator
     │
     ▼
Final Response
```

### Workflow Steps

1. User enters a task.
2. The Planner analyzes the request.
3. If a tool is required, the appropriate tool is selected.
4. The tool executes the requested action.
5. The LLM combines the tool output with reasoning.
6. The Evaluator checks whether the answer is consistent.
7. The final response is returned to the user.
---

## ▶️ Installation

```bash
git clone https://github.com/Nidadmn/smart-agent.git
cd smart-agent
pip install -r requirements.txt
```

Install Ollama and pull the model:

```bash
ollama pull qwen2.5:3b
```

Start Ollama (if not already running):

```bash
ollama serve
```

Run the agent:

```bash
py test_agent.py
```

---

## 💬 Example

```text
>>> 12 * 8 + 5

101

>>> report AI Agent Project

report.md created

>>> read notes.txt

(file content...)
```

---

## 📂 Project Structure

```
smart-agent/
│
├── agent/
│   ├── llm.py
│   ├── planner.py
│   ├── orchestrator.py
│   └── evaluator.py
│
├── tools/
│   ├── base_tool.py
│   ├── calculator_tool.py
│   ├── file_tool.py
│   └── report_tool.py
│
├── test_agent.py
├── README.md
└── requirements.txt
```

---

## 📜 License

MIT License