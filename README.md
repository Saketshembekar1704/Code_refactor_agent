# 🔧 Autonomous Code Refactoring Agent

An AI-powered multi-agent system built with **CrewAI** that autonomously analyzes and refactors Python codebases — improving code quality, reducing complexity, and generating professional documentation.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Agents](#agents)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI Mode](#cli-mode)
  - [Streamlit UI](#streamlit-ui)
- [Benchmarking](#benchmarking)
- [Tools](#tools)
- [Tech Stack](#tech-stack)

---

## Overview

The **Autonomous Code Refactoring Agent** is a multi-agent AI system that orchestrates a crew of specialized agents to analyze Python source code and automatically apply refactoring improvements. It works with local LLMs via **Ollama** (default: `deepseek-r1:1.5b`) or can be configured for OpenAI/Anthropic models.

The system operates in two modes:
- **Analysis** – scans a codebase and produces a detailed quality report with recommendations
- **Refactor** – executes a full refactoring pipeline: analysis → strategy → implementation → documentation

---

## Features

- 🔍 **Static Code Analysis** — detects code smells, high cyclomatic complexity, missing docstrings, and more
- 🧠 **AI-Driven Strategy** — generates step-by-step refactoring plans tailored to each codebase
- ✏️ **Safe Code Modifications** — applies incremental, functionality-preserving changes
- 📝 **Automated Documentation** — writes PEP 257-compliant docstrings for all functions and classes
- 💾 **Automatic Backups** — creates a copy of the original code before any modifications
- 📊 **Benchmarking Suite** — measures before/after metrics (LOC, complexity, docstring coverage)
- 🖥️ **Streamlit Web UI** — interactive browser-based interface as an alternative to the CLI
- 🔌 **LLM Agnostic** — supports Ollama (local), OpenAI, and Anthropic via environment variables

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    RefactorCrew                      │
│              (Orchestration Layer)                   │
└───────────┬─────────────┬──────────────┬────────────┘
            │             │              │
    ┌───────▼──────┐ ┌────▼────────┐ ┌──▼────────────┐
    │ Code Profiler│ │  Strategist  │ │ Implementation│
    │    Agent     │ │    Agent     │ │    Agent      │
    └───────┬──────┘ └────┬────────┘ └──┬────────────┘
            │             │              │
            └─────────────┼──────────────┘
                          │
                 ┌────────▼────────┐
                 │  DocString      │
                 │  Writer Agent   │
                 └─────────────────┘
```

---

## Agents

| Agent | Role | Responsibility |
|---|---|---|
| **Code Profiler** | Senior Code Quality Analyst | Analyzes Python files for quality issues, complexity, and documentation gaps |
| **Refactor Strategist** | Software Architect | Designs a safe, step-by-step refactoring plan based on the analysis report |
| **Code Implementation** | Skilled Development Engineer | Executes the refactoring plan with surgical precision, preserving functionality |
| **DocString Writer** | Technical Documentation Specialist | Generates PEP 257-compliant docstrings for all functions and classes |

---

## Project Structure

```
CodeRefactorAgent/
├── agents/
│   ├── code_profiler_agent.py        # Code quality analysis agent
│   ├── refactor_strategist_agent.py  # Refactoring strategy agent
│   ├── code_implementation_agent.py  # Code modification agent
│   └── docstring_writer_agent.py     # Documentation agent
├── crew/
│   └── refactor_crew.py              # Main orchestration class (RefactorCrew)
├── tools/
│   ├── code_analysis_tools.py        # Static analysis & file-reading tools
│   └── file_operations.py            # Safe file modification tools
├── ui/
│   └── streamlit_ui.py               # Browser-based Streamlit interface
├── test_projects/                    # Sample codebases for testing
├── Papers/                           # Research papers & references
├── main_application.py               # CLI entry point
├── run_benchmark.py                  # Benchmarking & evaluation script
├── generate_result_charts.py         # Result visualization charts
├── benchmark_results.json            # Stored benchmark output
├── requirements.txt                  # Python dependencies
├── env_config.sh                     # Environment variable template
├── run_ui.bat                        # Windows shortcut to launch UI
└── configure_deepseek_14b.bat        # Windows setup for DeepSeek 14B model
```

---

## Prerequisites

- **Python** 3.9+
- **Ollama** installed and running locally ([install guide](https://ollama.com/download))
- A supported LLM pulled in Ollama, e.g.:
  ```bash
  ollama pull deepseek-r1:1.5b      # Fast, lightweight (default)
  ollama pull deepseek-coder:14b    # Larger, more capable
  ```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Saketshembekar1704/Code_refactor_agent.git
   cd Code_refactor_agent
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env_config.sh .env
   # Edit .env to match your LLM provider and model
   ```

---

## Configuration

Create a `.env` file in the project root (use `env_config.sh` as a template):

```env
# Local LLM via Ollama (default)
OPENAI_API_KEY=ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL_NAME=deepseek-r1:1.5b
OLLAMA_MODEL=deepseek-r1:1.5b

# --- OR use a cloud provider ---
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# Application Settings
BACKUP_ENABLED=true
MAX_COMPLEXITY_THRESHOLD=10
DEFAULT_MODE=analysis
CREWAI_TELEMETRY_OPT_OUT=true
```

> **Tip (Windows):** Run `configure_deepseek_14b.bat` to auto-configure the environment for the DeepSeek Coder 14B model.

---

## Usage

### CLI Mode

**Analyze a codebase (no changes made):**
```bash
python main_application.py --target-dir ./my_project --mode analysis
```

**Refactor a codebase (creates `my_project_refactored/`):**
```bash
python main_application.py --target-dir ./my_project --mode refactor
```

**CLI Arguments:**

| Argument | Default | Description |
|---|---|---|
| `--target-dir` | *(required)* | Path to the Python project to analyze/refactor |
| `--mode` | `analysis` | `analysis` (report only) or `refactor` (apply changes) |
| `--backup` | `true` | Create a backup before making changes |
| `--ui` | `false` | Launch the Streamlit web UI instead |

**Output:**
- **Analysis mode** → saves `analysis_report_<timestamp>.txt`
- **Refactor mode** → saves `refactoring_report_<timestamp>.json` and a `*_refactored/` directory

---

### Streamlit UI

Launch the interactive web interface:

```bash
# Windows shortcut
run_ui.bat

# Or manually
streamlit run ui/streamlit_ui.py
```

Then open `http://localhost:8501` in your browser. The UI supports:
- Uploading or specifying a project directory
- Running analysis or full refactoring
- Viewing results, metrics, and recommendations in real time
- Downloading the refactored project as a ZIP

---

## Benchmarking

Run the evaluation suite against the included test projects:

```bash
python run_benchmark.py
```

Metrics measured **before and after** refactoring:
- Lines of Code (LOC)
- Cyclomatic Complexity (average and high-complexity function count)
- Docstring coverage (functions, classes, modules)
- Code quality issue count

Results are saved to `benchmark_results.json`. To generate charts from results:

```bash
python generate_result_charts.py
```

Five sample projects are included in `test_projects/` for benchmarking:

| Project | Domain |
|---|---|
| `project1_utils` | General utilities |
| `project2_fileops` | File operations |
| `project3_taskmanager` | Task management |
| `project4_mathutils` | Math utilities |
| `project5_webutils` | Web utilities |

---

## Tools

### `code_analysis_tools.py`
- `analyze_code` — performs static analysis using AST and Radon; detects complexity, missing docstrings, and code smells
- `read_file_system` — safely reads files and directory structures for agents

### `file_operations.py`
- `modify_file` — applies targeted modifications to source files with rollback support

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent Orchestration | [CrewAI](https://github.com/joaomdmoura/crewai) |
| LLM Backend | [Ollama](https://ollama.com/) (local) / OpenAI / Anthropic |
| LLM Framework | LangChain, LangChain-Ollama |
| Code Analysis | Python `ast`, [Radon](https://radon.readthedocs.io/), Pylint |
| Web UI | [Streamlit](https://streamlit.io/) |
| Git Integration | [GitPython](https://gitpython.readthedocs.io/) |
| Config Management | python-dotenv |

---

## License

This project is open source. See the repository for license details.

---

*Built with ❤️ using CrewAI and local LLMs for fully autonomous, privacy-preserving code refactoring.*
