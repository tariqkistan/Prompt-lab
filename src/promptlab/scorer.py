import json
import os

from openai import OpenAI
from pydantic import ValidationError

from promptlab.models import Rubric, ScoreResult
from promptlab.prompts import (
    build_cot_prompt,
    build_few_shot_prompt,
    build_zero_shot_prompt,
)

# Load API key from environment — never hardcode
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o')


def score(text: str, rubric: Rubric, mode: str = 'zero-shot') -> tuple[ScoreResult, int]:
    """Score text against a rubric using the specified prompting mode.
    
    Returns:
        (ScoreResult, tokens_used)
    """
    # Build the right prompt for the mode
    if mode == 'zero-shot':
        messages = build_zero_shot_prompt(text, rubric)
    elif mode == 'few-shot':
        messages = build_few_shot_prompt(text, rubric)
    elif mode == 'cot':
        messages = build_cot_prompt(text, rubric)
    else:
        raise ValueError(f'Unknown mode: {mode}')

    # Call the LLM
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        response_format={'type': 'json_object'},
        max_tokens=500,
    )

    # Parse the response
    raw_text = response.choices[0].message.content
    tokens_used = response.usage.total_tokens

    # Parse JSON
    try:
        raw_dict = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(f'LLM returned invalid JSON: {e}\nRaw: {raw_text}')

    # Validate with Pydantic — catches wrong types, missing fields, out-of-range
    try:
        result = ScoreResult(**raw_dict)
    except ValidationError as e:
        raise ValueError(f'LLM output failed validation: {e}')

    return result, tokens_used