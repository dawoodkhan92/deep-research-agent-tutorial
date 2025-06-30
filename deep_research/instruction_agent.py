"""Research Instruction Agent - From OpenAI Cookbook"""

from agency_swarm import Agent
from .prompts import RESEARCH_INSTRUCTION_AGENT_PROMPT

def create_instruction_agent(research_agent) -> Agent:
    """
    Create the Research Instruction Agent.
    
    This agent converts user queries into detailed research instructions
    and hands off to the research agent for execution.
    
    Args:
        research_agent: The research agent to hand off to
    """
    return Agent(
        name="Research Instruction Agent",
        model="gpt-4o-mini",
        instructions=RESEARCH_INSTRUCTION_AGENT_PROMPT
    ) 