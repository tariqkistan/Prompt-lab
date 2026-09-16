import pytest

from promptlab.models import Rubric, RubricExample


@pytest.fixture
def sample_rubric():
    """Fixture: sample rubric for testing"""
    return Rubric(
        name="greeting_compliance",
        description="Did agent introduce themselves?",
        criteria="Score 1 if name AND company stated. Score 0 otherwise.",
        scoring_type="binary",
        examples=[
            RubricExample(
                text="Hi I'm Zara from Nutun",
                score=1.0,
                reason="Name and company stated",
            ),
            RubricExample(
                text="Hello can I speak to account holder",
                score=0.0,
                reason="No name no company",
            ),
        ],
    )