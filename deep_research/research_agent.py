"""Advanced Research Agent - From OpenAI Cookbook"""

from agency_swarm import Agent
from agents import WebSearchTool  # Import from agents package

def create_research_agent() -> Agent:
    """
    Create the Advanced Research Agent using o3-deep-research model.
    
    This agent performs comprehensive research with file access for internal
    knowledge search through Agency Swarm's simplified file integration.
    """
    return Agent(
        name="Research Agent", 
        model="o3-deep-research-2025-06-26",
        instructions="Perform deep empirical research based on the user's instructions.",
        tools=[WebSearchTool()],  # Required for deep research models
        files_folder="./files"  # Simplified file access instead of complex MCP setup
    ) 