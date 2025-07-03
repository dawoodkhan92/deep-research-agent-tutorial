import os

from agency_swarm import Agent


class InstructionAgent(Agent):
    def __init__(self, research_agent):
        # Load instruction from file
        instructions_path = os.path.join(os.path.dirname(__file__), "instructions.md")
        if os.path.exists(instructions_path):
            with open(instructions_path, "r", encoding="utf-8") as f:
                instructions = f.read()
        else:
            instructions = "Rewrite user queries into detailed research instructions for the research agent."

        super().__init__(
            name="Research Instruction Agent",
            model="gpt-4.1",
            instructions=instructions,
            handoffs=[research_agent],
        )
