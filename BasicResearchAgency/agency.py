#!/usr/bin/env python3
"""
Basic Research Agency

Single agent with o4-mini-deep-research model.
Using Agency Swarm v1.x with proper streaming pattern.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agency_swarm import Agency, Agent
from agents import WebSearchTool
from agents.mcp import MCPServerSse

from utils import run_agency_demo

# Get MCP server URL from environment or use default
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://0.0.0.0:8001/sse")

print(f"📡 MCP Server URL: {MCP_SERVER_URL}")

sse_server = MCPServerSse(
    name="FilesServer", # Tools will be accessed like My_Custom_SSE_Server.some_tool
    params={
        "url": MCP_SERVER_URL,
    },
    cache_tools_list=True,
    # Not providing allowed_tools will attach all available tools to the agent
)

# Basic Research Agent - o4-mini-deep-research with web search
research_agent = Agent(
    name="Research Agent",
    model="o4-mini-deep-research-2025-06-26",
    tools=[
        WebSearchTool(),
        # HostedMCPTool(
        #     tool_config={
        #         "type": "mcp",
        #         "server_label": "file_search",
        #         "server_url": MCP_SERVER_URL,
        #         "require_approval": "never",
        #     }
        # ),
    ],
    mcp_servers=[sse_server],
    instructions="You perform deep empirical research based on the user's question.",
)

# Create the agency
agency = Agency(research_agent)

if __name__ == "__main__":
    run_agency_demo(agency)
