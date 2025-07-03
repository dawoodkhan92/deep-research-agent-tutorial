import os

from agency_swarm import Agent
from agents import HostedMCPTool, WebSearchTool


class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Research Agent",
            model="o4-mini-deep-research-2025-06-26",
            instructions="Perform deep empirical research based on the user's instructions.",
            tools=[
                WebSearchTool(),
                #     HostedMCPTool(
                #         tool_config={
                #             "type": "mcp",
                #             "server_label": "file_search",
                #             "server_url": "http://localhost:8001/sse",
                #             "require_approval": "never",
                #         }
                #     ),
                # ],
                # HostedMCPTool is not supported by the o3-deep-research model
            ],
        )
