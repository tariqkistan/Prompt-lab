import os
from datetime import UTC, datetime
from pathlib import Path

from promptlab.models import LogEntry, ScoreResult


def log_result(
    mode: str,
    rubric_name: str,
    input_text: str,
    result: ScoreResult,
    tokens_used: int,
    model: str | None = None,
) -> None:
    """Append the scoring result to logs/results.jsonl"""
    log_dir = Path(os.environ.get('LOG_DIR', 'logs'))
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'results.jsonl'

    entry = LogEntry(
        timestamp=datetime.now(UTC),
        mode=mode,
        rubric_name=rubric_name,
        input_text=input_text[:200],  # truncate long inputs
        score=result.score,
        confidence=result.confidence,
        rationale=result.rationale,
        tokens_used=tokens_used,
        model=model or os.environ.get('OPENAI_MODEL', 'gpt-4o'),
    )

    # Append to file — one JSON object per line
    with log_file.open('a') as f:
        f.write(entry.model_dump_json() + '\n')
