#!/usr/bin/env python3
"""
Deep Research Agency

Four-agent handoffs pattern with clarification workflow.
Triage → [Clarifying, Instruction] → Research using deep research model.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agency_swarm import Agency, Agent
from ClarifyingAgent.ClarifyingAgent import ClarifyingAgent
from InstructionBuilderAgent.InstructionBuilderAgent import InstructionBuilderAgent
from ResearchAgent.ResearchAgent import ResearchAgent

from utils import copilot_demo, save_research_to_pdf, stream_demo

# ─────────────────────────────────────────────────────────────
# Process files at application start
# ─────────────────────────────────────────────────────────────

# Get the files directory path
files_dir = Path("files")
if files_dir.exists() and files_dir.is_dir():
    print(f"📁 Found files directory with {len(list(files_dir.glob('*')))} files")
    # Files will be available through MCP server

# ─────────────────────────────────────────────────────────────
# Create agents with proper dependencies
# ─────────────────────────────────────────────────────────────

research_agent = ResearchAgent()
instruction_builder_agent = InstructionBuilderAgent(research_agent)
clarifying_agent = ClarifyingAgent(instruction_builder_agent)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Decide whether clarifications are required.\n"
        "• If yes → call transfer_to_clarifying_questions_agent\n"
        "• If no  → call transfer_to_research_instruction_agent\n"
        "Return exactly ONE function-call."
    ),
    handoffs=[clarifying_agent, instruction_builder_agent],
)

# Create agency
agency = Agency(triage_agent)

# ─────────────────────────────────────────────────────────────
# PDF generation helper
# ─────────────────────────────────────────────────────────────


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
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8001/sse")
    print(f"📡 MCP Server URL: {mcp_url}")
    if "ngrok" in mcp_url:
        print("✅ Using ngrok tunnel for public access")
    elif "localhost" in mcp_url:
        print(
            "⚠️  Using localhost - OK for local testing, but OpenAI API needs public URL (use ngrok)"
        )

    if len(sys.argv) > 1 and sys.argv[1] in ["--ui", "--copilot"]:
        print("🚀 Launching Copilot UI...")
        copilot_demo(agency, save_response_to_pdf)
    else:
        print("🚀 Launching Terminal Demo...")
        asyncio.run(stream_demo(agency, save_response_to_pdf))
