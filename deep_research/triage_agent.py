"""Triage Agent - From OpenAI Cookbook"""

from agency_swarm import Agent

def create_triage_agent(clarifying_agent, instruction_agent) -> Agent:
    """
    Create the Triage Agent.
    
    This agent decides whether clarifications are required before proceeding
    with research. It routes queries to either the clarifying agent or
    directly to the instruction agent.
    
    Args:
        clarifying_agent: Agent for gathering clarifications
        instruction_agent: Agent for creating research instructions
    """
    return Agent(
        name="Triage Agent",
        model="gpt-4o-mini",
        instructions=(
            "Decide whether clarifications are required.\n"
            "• If the query is clear and specific → transfer to Research Instruction Agent\n"
            "• If the query needs clarification → transfer to Clarifying Questions Agent\n"
            "Always make a clear decision and transfer to the appropriate agent."
        )
    ) 