from promptlab.prompts import (
    build_cot_prompt,
    build_few_shot_prompt,
    build_zero_shot_prompt,
)


def test_zero_shot_returns_two_messages(sample_rubric):
    """Test that zero-shot prompt returns system + user messages"""
    messages = build_zero_shot_prompt("Hello", sample_rubric)

    assert len(messages) == 2
    assert messages[0]['role'] == 'system'
    assert messages[1]['role'] == 'user'


def test_zero_shot_contains_criterion(sample_rubric):
    """Test that system prompt includes criterion and name"""
    messages = build_zero_shot_prompt("Hello", sample_rubric)

    assert sample_rubric.name in messages[0]['content']
    assert sample_rubric.criteria in messages[0]['content']


def test_few_shot_contains_examples(sample_rubric):
    """Test that few-shot prompt includes all examples"""
    messages = build_few_shot_prompt("Hello", sample_rubric)
    system = messages[0]['content']

    # Both examples should appear in the system prompt
    assert sample_rubric.examples[0].text in system
    assert sample_rubric.examples[1].text in system


def test_cot_contains_step_instruction(sample_rubric):
    """Test that chain-of-thought prompt includes reasoning steps"""
    messages = build_cot_prompt("Hello", sample_rubric)
    system = messages[0]['content']

    assert 'Step 1' in system
