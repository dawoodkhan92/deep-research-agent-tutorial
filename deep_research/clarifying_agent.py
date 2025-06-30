"""Clarifying Questions Agent - From OpenAI Cookbook"""

from agency_swarm import Agent
from .prompts import CLARIFYING_AGENT_PROMPT
from .structured_outputs import Clarifications

def create_clarifying_agent(instruction_agent) -> Agent:
    """
    Create the Clarifying Questions Agent.
    
    This agent asks follow-up questions to gather more context for research
    and uses structured output to format the questions properly.
    
    Args:
        instruction_agent: The instruction agent to hand off to
    """
    return Agent(
        name="Clarifying Questions Agent",
        model="gpt-4o-mini", 
        instructions=CLARIFYING_AGENT_PROMPT
        # Note: Agency Swarm handles structured outputs differently
    ) 