import os
import sys

from agency_swarm import Agent

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared_outputs import Clarifications


class ClarifyingAgent(Agent):
    def __init__(self, instruction_agent):
        # Load instruction from file
        instructions_path = os.path.join(os.path.dirname(__file__), "instructions.md")
        with open(instructions_path, "r", encoding="utf-8") as f:
            instructions = f.read()

        super().__init__(
            name="Clarifying Questions Agent",
            model="gpt-4.1",
            temperature=0,
            instructions=instructions,
            output_type=Clarifications,
            handoffs=[instruction_agent],
        )
