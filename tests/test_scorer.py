import json
from unittest.mock import MagicMock

import pytest

from promptlab.scorer import score


def test_score_returns_valid_result(mocker, sample_rubric):
    """Test that score() returns valid ScoreResult with mocked API"""
    # Mock the OpenAI client — no real API call
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps({
        'score': 1.0,
        'confidence': 0.95,
        'rationale': 'Agent stated name and company',
    })
    mock_response.usage.total_tokens = 150

    mocker.patch(
        'promptlab.scorer.client.chat.completions.create',
        return_value=mock_response,
    )

    result, tokens = score("Hi I'm Zara", sample_rubric, "zero-shot")

    assert result.score == 1.0
    assert result.confidence == 0.95
    assert tokens == 150


def test_invalid_mode_raises(sample_rubric):
    """Test that invalid mode raises ValueError"""
    with pytest.raises(ValueError):
        score("text", sample_rubric, "invalid-mode")