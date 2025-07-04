#!/usr/bin/env python3
"""
Basic Research Agency

Single agent with o4-mini-deep-research model.
Using Agency Swarm v1.x with proper streaming pattern.
"""

import os
import sys

from openai.types.responses.web_search_tool_param import UserLocation

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agency_swarm import Agency, Agent
from agents import WebSearchTool

from demo_utils import copilot_demo, stream_demo

# Basic Research Agent - o4-mini-deep-research with web search
research_agent = Agent(
    name="Research Agent",
    model="o4-mini-deep-research-2025-06-26",
    tools=[
        WebSearchTool(
            user_location=UserLocation(type="approximate", country="US"),
            search_context_size="low",
        )
    ],
    instructions="You perform deep empirical research based on the user's question.",
)

# Create the agency
agency = Agency(research_agent)


if __name__ == "__main__":
    import asyncio
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ["--ui", "--copilot"]:
        print("🚀 Launching Copilot UI...")
        copilot_demo(agency)
    else:
        print("🚀 Launching Terminal Demo...")
        asyncio.run(stream_demo(agency))
