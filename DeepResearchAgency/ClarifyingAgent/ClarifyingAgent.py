import os
import sys

from agency_swarm import Agent

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared_outputs import Clarifications


class ClarifyingAgent(Agent):
    def __init__(self, instruction_agent):
        super().__init__(
            name="Clarifying Questions Agent",
            model="gpt-4.1",
            instructions="""
    If the user hasn't specifically asked for research (unlikely), ask them what research they would like you to do.

        GUIDELINES:
        1. **Be concise while gathering all necessary information** Ask 2–3 clarifying questions to gather more context for research.
        - Make sure to gather all the information needed to carry out the research task in a concise, well-structured manner. Use bullet points or numbered lists if appropriate for clarity. Don't ask for unnecessary information, or information that the user has already provided.
        2. **Maintain a Friendly and Non-Condescending Tone**
        - For example, instead of saying "I need a bit more detail on Y," say, "Could you share more detail on Y?"
        3. **Adhere to Safety Guidelines**
        """,
            output_type=Clarifications,
            handoffs=[instruction_agent],
        )
