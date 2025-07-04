from agency_swarm import Agent
from agents import HostedMCPTool, WebSearchTool
from openai.types.responses.web_search_tool_param import UserLocation


class ResearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Research Agent",
            model="o4-mini-deep-research-2025-06-26",
            instructions="Perform deep empirical research based on the user's instructions.",
            tools=[
                WebSearchTool(
                    user_location=UserLocation(type="approximate", country="US"),
                    search_context_size="low",
                ),
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
