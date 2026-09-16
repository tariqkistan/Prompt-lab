from promptlab.models import Rubric

RESPONSE_FORMAT_INSTRUCTION = """
Respond ONLY with valid JSON in this exact format — no other text:
{"score": 0.0, "confidence": 0.0, "rationale": "your reason here"}
"""


def build_zero_shot_prompt(text: str, rubric: Rubric) -> list[dict]:
    """No examples — just instruction + text"""
    system = f"""
You are a quality analyst. Score the following text against this criterion.

Criterion: {rubric.name}
Description: {rubric.description}
Scoring instruction: {rubric.criteria}
Scoring type: {rubric.scoring_type}

- If binary: score must be exactly 0.0 or 1.0
- If scale: score must be between 0.0 and 1.0

{RESPONSE_FORMAT_INSTRUCTION}
"""
    return [
        {"role": "system", "content": system.strip()},
        {"role": "user", "content": f"Text to score:\n{text}"},
    ]


def build_few_shot_prompt(text: str, rubric: Rubric) -> list[dict]:
    """Include examples from rubric before the real text"""
    examples_text = ""
    for i, ex in enumerate(rubric.examples, 1):
        examples_text += f"Example {i}:\n"
        examples_text += f"Text: {ex.text}\n"
        examples_text += f"Score: {ex.score}\n"
        examples_text += f"Reason: {ex.reason}\n\n"

    system = f"""
You are a quality analyst. Score the following text against this criterion.

Criterion: {rubric.name}
Scoring instruction: {rubric.criteria}

{examples_text}

Now score the new text using the same standard as the examples above.

{RESPONSE_FORMAT_INSTRUCTION}
"""
    return [
        {"role": "system", "content": system.strip()},
        {"role": "user", "content": f"Text to score:\n{text}"},
    ]


def build_cot_prompt(text: str, rubric: Rubric) -> list[dict]:
    """Chain-of-thought — model thinks step by step first"""
    system = f"""
You are a quality analyst. Score the following text against this criterion.

Criterion: {rubric.name}
Scoring instruction: {rubric.criteria}

IMPORTANT: Before giving your score, think through it step by step:

Step 1: What is the criterion asking for?
Step 2: What specific evidence do you see in the text?
Step 3: Does the evidence meet the criterion? Why or why not?
Step 4: Based on this reasoning, what score is appropriate?

Include your step-by-step reasoning in the rationale field.

{RESPONSE_FORMAT_INSTRUCTION}
"""
    return [
        {"role": "system", "content": system.strip()},
        {"role": "user", "content": f"Text to score:\n{text}"},
    ]