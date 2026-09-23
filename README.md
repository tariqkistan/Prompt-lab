# Prompt-lab

[![CI Status](https://github.com/tariqkistan/Prompt-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/tariqkistan/Prompt-lab/actions/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A lightweight LLM evaluation framework for scoring text — call transcripts, support tickets, customer messages — against custom-defined rubrics. Built to explore how prompting strategy (zero-shot vs. few-shot vs. chain-of-thought) affects scoring consistency and reliability.

## Why I built this

Built as a technical exploration ahead of Nutun's AI Engineer role — modeling the kind of evaluation pipeline a QA/compliance scoring system would need: rubric-based scoring, validated LLM output, and an audit trail of every decision.

## What it does

- Scores any text against a JSON-defined rubric (binary or scale)
- Supports three prompting modes: zero-shot, few-shot, and chain-of-thought
- Validates LLM output with Pydantic — catches malformed JSON, out-of-range scores, and missing fields before they reach a log file
- Logs every scoring run to JSONL for downstream analysis
- Ships with tests (mocked LLM calls) and a GitHub Actions CI pipeline
## Quick start

```bash
git clone https://github.com/tariqkistan/prompt-lab
cd prompt-lab
pip install -e '.[dev]'
cp .env.example .env  # add your OpenAI API key
```

### Score a sample call (zero-shot)

```bash
promptlab --text 'Hi I am Zara from Nutun...' --rubric rubrics/greeting.json --mode zero-shot
```

### Score from a file (few-shot)

```bash
promptlab --file samples/good_call.txt --rubric rubrics/greeting.json --mode few-shot
```

### Chain-of-thought mode

```bash
promptlab --file samples/bad_call.txt --rubric rubrics/empathy.json --mode cot
```

## Design decisions

- **temperature=0** — Deterministic scoring; same input always produces same output
- **JSON mode** — Forces valid JSON from LLM, prevents parsing failures
- **Pydantic validation** — Catches bad LLM output before it hits the log file
- **JSONL logging** — One result per line, easily queryable and appendable
- **Three modes** — Demonstrates zero-shot vs few-shot vs CoT tradeoffs

## Running tests

```bash
pytest tests/ -v
```

## Project structure


## Installation

### Prerequisites

- Python 3.11+
- OpenAI API key

### Setup

```bash
# Clone repository
git clone https://github.com/tariqkistan/prompt-lab
cd prompt-lab

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e '.[dev]'

# Configure API key
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-...
```

## Usage

### Command-line interface

```bash
promptlab [OPTIONS]
```

**Options:**

- `--text TEXT, -t TEXT` — Score text directly (alternative to --file)
- `--file PATH, -f PATH` — Score from a text file (alternative to --text)
- `--rubric PATH, -r PATH` — Path to rubric JSON file (required)
- `--mode {zero-shot,few-shot,cot}, -m {zero-shot,few-shot,cot}` — Prompting mode (default: zero-shot)
- `--help` — Show help message

### Example

```bash
# Direct text
promptlab --text "Hello, I'm Alex from TechCorp" --rubric rubrics/greeting.json

# From file, few-shot mode
promptlab --file transcript.txt --rubric rubrics/greeting.json --mode few-shot

# Short flags
promptlab -t "Hi there" -r rubrics/greeting.json -m cot
```

## Rubric format

Create a JSON file in `rubrics/`:

```json
{
  "name": "greeting_compliance",
  "description": "Did the agent greet the customer properly?",
  "criteria": "Score 1 if agent stated their name AND company. Score 0 if either missing.",
  "scoring_type": "binary",
  "examples": [
    {
      "text": "Hi I'm Zara from Nutun calling about your account",
      "score": 1.0,
      "reason": "Name and company both stated"
    },
    {
      "text": "Hello, can I speak to the account holder?",
      "score": 0.0,
      "reason": "No name, no company"
    }
  ]
}
```

**Fields:**

- `name` — Rubric identifier
- `description` — What this rubric measures
- `criteria` — Scoring instruction for the LLM
- `scoring_type` — `"binary"` (0.0 or 1.0) or `"scale"` (0.0–1.0)
- `examples` — Few-shot examples (optional, used in few-shot mode)

## Output

Scores are logged to `logs/results.jsonl` (one JSON object per line):

```json
{"timestamp": "2024-01-15T14:30:45.123456+00:00", "mode": "zero-shot", "rubric_name": "greeting_compliance", "input_text": "Hi I'm Zara...", "score": 1.0, "confidence": 0.95, "rationale": "Agent stated name and company", "tokens_used": 150, "model": "gpt-4o"}
{"timestamp": "2024-01-15T14:31:10.234567+00:00", "mode": "few-shot", "rubric_name": "empathy", "input_text": "I understand your...", "score": 0.85, "confidence": 0.9, "rationale": "Empathetic tone detected", "tokens_used": 175, "model": "gpt-4o"}
```

## Prompting modes

### Zero-shot

Uses only the rubric criteria, no examples. Fast and simple.

**Best for:** Clear, unambiguous criteria

### Few-shot

Includes examples from the rubric before scoring. Teaches the model by example.

**Best for:** Complex criteria, when consistency matters

### Chain-of-Thought (CoT)

Asks the model to think step-by-step before scoring. Produces detailed reasoning.

**Best for:** Nuanced judgments, when you need detailed explanations

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_scorer.py -v

# Run with coverage
pytest tests/ --cov=src/promptlab --cov-report=term-missing
```

## CI/CD

GitHub Actions workflow runs on every push and pull request:
- Linting with Ruff
- All tests with coverage
- Python 3.11

See `.github/workflows/ci.yml` for details.

## Environment variables

Create a `.env` file (copy from `.env.example`):

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
LOG_DIR=logs
```

**Variables:**

- `OPENAI_API_KEY` — Your OpenAI API key (required)
- `OPENAI_MODEL` — Model to use (default: gpt-4o)
- `LOG_DIR` — Where to save results (default: logs/)

## Dependencies

**Core:**
- `openai>=1.0` — OpenAI API client
- `pydantic>=2.0` — Data validation
- `typer>=0.9` — CLI framework
- `rich>=13.0` — Terminal formatting
- `python-dotenv>=1.0` — Environment variables

**Development:**
- `pytest>=7.0` — Testing framework
- `pytest-mock>=3.0` — Mocking utilities
- `black>=23.0` — Code formatter
- `ruff>=0.1` — Linter

## License

MIT

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Questions?

Open an issue on GitHub.
