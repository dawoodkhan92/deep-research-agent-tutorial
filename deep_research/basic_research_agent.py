"""Basic Research Agent - From OpenAI Cookbook"""

from agency_swarm import Agent
from agents import WebSearchTool  # Import from agents package

def create_basic_research_agent() -> Agent:
    """
    Create the Basic Research Agent using o4-mini-deep-research model.
    
    This agent performs Deep Research using the faster o4-mini model with
    native WebSearch access to the public internet.
    """
    return Agent(
        name="Research Agent",
        model="o4-mini-deep-research-2025-06-26", 
        instructions="You perform deep empirical research based on the user's question.",
        tools=[WebSearchTool()],  # Required for deep research models
        files_folder="./files"  # Agency Swarm file access
    ) 