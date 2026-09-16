from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class RubricExample(BaseModel):
    """A few-shot example — text + expected score + reason"""
    text: str
    score: float
    reason: str


class Rubric(BaseModel):
    """The scoring rubric — loaded from a JSON file"""
    name: str
    description: str
    criteria: str  # The actual scoring instruction
    scoring_type: Literal['binary', 'scale']  # binary=0 or 1, scale=0.0-1.0
    examples: list[RubricExample] = []  # for few-shot mode


class ScoreResult(BaseModel):
    """What the LLM must return — validated before logging"""
    score: float = Field(ge=0.0, le=1.0)  # must be between 0 and 1
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str


class LogEntry(BaseModel):
    """What gets written to the JSON log file"""
    timestamp: datetime
    mode: Literal['zero-shot', 'few-shot', 'cot']
    rubric_name: str
    input_text: str
    score: float
    confidence: float
    rationale: str
    tokens_used: int
    model: str