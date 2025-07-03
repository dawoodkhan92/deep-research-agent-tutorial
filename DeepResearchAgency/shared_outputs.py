"""Structured Outputs for Deep Research Agents"""

from pydantic import BaseModel


class Clarifications(BaseModel):
    """
    Structured output for the Clarifying Agent.

    Contains a list of clarification questions to gather more context
    for research tasks.
    """

    questions: list[str]
