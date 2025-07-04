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
from agents import HostedMCPTool, WebSearchTool

from utils import copilot_demo, save_research_to_pdf, stream_demo

# Get MCP server URL from environment or use default
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001/sse")

# Basic Research Agent - o4-mini-deep-research with web search
research_agent = Agent(
    name="Research Agent",
    model="o4-mini-deep-research-2025-06-26",
    tools=[
        WebSearchTool(),
        HostedMCPTool(
            tool_config={
                "type": "mcp",
                "server_label": "file_search",
                "server_url": MCP_SERVER_URL,
                "require_approval": "never",
            }
        ),
    ],
    instructions="You perform deep empirical research based on the user's question.",
)

# Create the agency
agency = Agency(research_agent)


def save_response_to_pdf(response, query):
    """Save response to PDF with error handling."""
    try:
        pdf_path = save_research_to_pdf(
            research_content=str(response), query=query, output_dir="reports"
        )
        print(f"\n📄 Research report saved to: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"\n❌ Error saving PDF: {e}")
        return None


if __name__ == "__main__":
    import asyncio
    import sys

    # Show MCP configuration
    print(f"📡 MCP Server URL: {MCP_SERVER_URL}")
    if "ngrok" in MCP_SERVER_URL:
        print("✅ Using ngrok tunnel for public access")
    elif "localhost" in MCP_SERVER_URL:
        print(
            "⚠️  Using localhost - OK for local testing, but OpenAI API needs public URL (use ngrok)"
        )

    if len(sys.argv) > 1 and sys.argv[1] in ["--ui", "--copilot"]:
        print("🚀 Launching Copilot UI...")
        copilot_demo(agency, save_response_to_pdf)
    else:
        print("🚀 Launching Terminal Demo...")
        asyncio.run(stream_demo(agency, save_response_to_pdf))
