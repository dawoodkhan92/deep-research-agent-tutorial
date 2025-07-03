#!/usr/bin/env python3
"""
Deep Research Agency

Four-agent handoffs pattern with clarification workflow.
Triage → [Clarifying, Instruction] → Research using o3-deep-research model.
"""

from dotenv import load_dotenv

load_dotenv()

import os
import sys
from pathlib import Path

from agency_swarm import Agency, Agent
from ClarifyingAgent.ClarifyingAgent import ClarifyingAgent
from InstructionAgent.InstructionAgent import InstructionAgent
from ResearchAgent.ResearchAgent import ResearchAgent
from shared_outputs import Clarifications
from utils import save_research_to_pdf

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
instruction_agent = InstructionAgent(research_agent)
clarifying_agent = ClarifyingAgent(instruction_agent)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Decide whether clarifications are required.\n"
        "• If yes → call transfer_to_clarifying_questions_agent\n"
        "• If no  → call transfer_to_research_instruction_agent\n"
        "Return exactly ONE function-call."
    ),
    handoffs=[clarifying_agent, instruction_agent],
)

# Create agency
agency = Agency(triage_agent)

# ─────────────────────────────────────────────────────────────
# Enhanced agency wrapper with automatic PDF generation
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


def basic_research(query: str, mock_answers: dict[str, str] | None = None):
    """Run research with automatic clarification handling and PDF generation."""

    # Get initial response
    response = agency.get_response(query)

    # Handle clarification questions if they arise
    if hasattr(response, "output_type") and isinstance(
        response.output_type, Clarifications
    ):
        reply = []
        for q in response.output_type.questions:
            ans = (mock_answers or {}).get(q, "No preference.")
            reply.append(f"**{q}**\n{ans}")

        # Send clarification responses back
        response = agency.get_response("\n\n".join(reply))

    # Always save to PDF
    save_response_to_pdf(response, query)
    return response


async def stream_demo():
    """Interactive multi-agent research terminal with PDF generation."""
    print("🎯 Deep Research Agency - Advanced Multi-Agent Research")
    print("Multi-agent workflow: Triage → [Clarifying] → Instruction → Research")
    print("=" * 70)
    print("Ask any research question. Type 'quit' to exit.")
    print("📄 Research reports will be automatically saved as PDF files.\n")

    while True:
        try:
            query = input("🔥 Research Query: ").strip()
            if query.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if not query:
                print("Please enter a research question.")
                continue

            # Stream the response and capture full text
            print("📡 Response: ", end="", flush=True)
            full_text = ""

            async for event in agency.get_response_stream(query):
                # Handle streaming events with data
                if hasattr(event, "data"):
                    data = event.data
                    # Only capture actual response text, not tool call arguments
                    if hasattr(data, "delta") and hasattr(data, "type"):
                        if data.type == "response.output_text.delta":
                            # Stream the actual response text in real-time
                            delta_text = data.delta
                            if delta_text:
                                print(delta_text, end="", flush=True)
                                full_text += delta_text
                        # Skip tool call deltas (we don't want to show those to users)
                        elif data.type == "response.function_call_arguments.delta":
                            continue

                # Handle validation errors
                elif isinstance(event, dict):
                    event_type = event.get("event", event.get("type"))
                    if event_type == "error":
                        print(
                            f"\n❌ Error: {event.get('content', event.get('data', 'Unknown error'))}"
                        )
                        break

            # Save to PDF after streaming completes
            if full_text.strip():
                save_response_to_pdf(full_text, query)

            print("\n" + "=" * 50)  # Separator for next query

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def copilot_demo():
    """Launch Copilot UI demo with PDF generation wrapper."""
    print("🎯 Starting Copilot UI with automatic PDF generation...")
    print("📄 All research reports will be automatically saved as PDF files.")

    try:
        from agency_swarm.ui.demos.launcher import CopilotDemoLauncher

        # Create a wrapper agency that saves to PDF
        class PDFSavingAgency(Agency):
            def get_response(self, query: str, **kwargs):
                response = super().get_response(query, **kwargs)
                save_response_to_pdf(response, query)
                return response

        # Create PDF-saving version of the agency
        pdf_agency = PDFSavingAgency(triage_agent)

        launcher = CopilotDemoLauncher()
        launcher.start(pdf_agency)

    except ImportError:
        print("❌ Copilot demo requires additional dependencies")
        print("Install with: pip install agency-swarm[copilot]")


if __name__ == "__main__":
    import asyncio
    import sys

    if len(sys.argv) > 1 and sys.argv[1] in ["--terminal", "--stream"]:
        print("🚀 Launching Terminal Demo...")
        asyncio.run(stream_demo())
    else:
        print("🚀 Launching Copilot UI...")
        copilot_demo()
