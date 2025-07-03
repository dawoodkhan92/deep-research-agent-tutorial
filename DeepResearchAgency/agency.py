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
    """Interactive multi-agent research terminal with proper workflow management."""
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

            # Initialize workflow state
            current_agent = "Triage Agent"
            awaiting_clarifications = False
            clarification_questions = []
            research_content = ""
            agent_responses = {}  # Track responses by agent
            clarifying_agent_text = ""  # Track text from Clarifying Agent

            print(f"\n🤖 Starting with {current_agent}...")
            print("─" * 50)

            # Stream the response
            response_stream = agency.get_response_stream(query)

            async for event in response_stream:
                # Track agent switches
                if (
                    hasattr(event, "type")
                    and event.type == "agent_updated_stream_event"
                ):
                    if hasattr(event, "new_agent"):
                        current_agent = event.new_agent.name
                        print(f"\n\n🔄 Switched to: {current_agent}")
                        print("─" * 50)

                        # Show appropriate status based on agent
                        if current_agent == "Research Agent":
                            print(
                                "🔬 Performing deep research... This may take a few minutes."
                            )
                        elif current_agent == "Clarifying Questions Agent":
                            print("❓ Preparing clarification questions...")
                            clarifying_agent_text = ""  # Reset to capture new text
                        elif current_agent == "Research Instruction Agent":
                            print("📋 Building research instructions...")

                # Handle streaming events with data
                elif hasattr(event, "data"):
                    data = event.data

                    # Track tool calls for visibility
                    if (
                        hasattr(data, "type")
                        and data.type == "response.function_call_arguments.delta"
                    ):
                        # Don't display tool call arguments, but track if it's a web search
                        pass

                    # Handle actual response text
                    elif hasattr(data, "delta") and hasattr(data, "type"):
                        if data.type == "response.output_text.delta":
                            delta_text = data.delta
                            if delta_text:
                                # Only print if not from Clarifying Agent (we'll handle that specially)
                                if current_agent != "Clarifying Questions Agent":
                                    print(delta_text, end="", flush=True)

                                # Track content by agent
                                if current_agent not in agent_responses:
                                    agent_responses[current_agent] = ""
                                agent_responses[current_agent] += delta_text

                                # Track Clarifying Agent text separately to parse JSON
                                if current_agent == "Clarifying Questions Agent":
                                    clarifying_agent_text += delta_text

                                # Only track research content from Research Agent
                                if current_agent == "Research Agent":
                                    research_content += delta_text

                # Handle raw response events (for action visibility)
                elif hasattr(event, "type") and event.type == "raw_response_event":
                    if hasattr(event, "data") and hasattr(event.data, "item"):
                        item = event.data.item
                        if hasattr(item, "action"):
                            action = item.action or {}
                            if (
                                action.get("type") == "search"
                                and current_agent == "Research Agent"
                            ):
                                query_text = action.get("query", "")
                                if query_text:
                                    print(f"\n🔍 [Web Search]: {query_text}")

                # Handle structured output (Clarifications) - though this might not happen in streaming
                elif hasattr(event, "item") and isinstance(
                    getattr(event, "item", None), Clarifications
                ):
                    awaiting_clarifications = True
                    clarification_questions = event.item.questions

                # Handle errors
                elif isinstance(event, dict):
                    event_type = event.get("event", event.get("type"))
                    if event_type == "error":
                        print(
                            f"\n❌ Error: {event.get('content', event.get('data', 'Unknown error'))}"
                        )
                        break

            # After streaming completes, check if we got clarification questions as JSON
            if clarifying_agent_text and not clarification_questions:
                try:
                    import json

                    # Try to parse the JSON response from Clarifying Agent
                    clarifying_data = json.loads(clarifying_agent_text.strip())
                    if "questions" in clarifying_data:
                        clarification_questions = clarifying_data["questions"]
                        awaiting_clarifications = True
                except json.JSONDecodeError:
                    # If not valid JSON, maybe it's formatted differently
                    pass

            # After streaming completes, check if we need clarifications
            if awaiting_clarifications and clarification_questions:
                print("\n\n" + "─" * 50)
                print(
                    "✏️ Please answer the following questions to help me research better:\n"
                )

                # Collect answers
                answers = []
                for i, question in enumerate(clarification_questions, 1):
                    print(f"{i}. {question}")
                    answer = input("   Your answer: ").strip()
                    if not answer:
                        answer = "No preference."
                    answers.append(f"**{question}**\n{answer}")

                # Send clarification responses
                print("\n🔄 Processing your answers...")
                print("─" * 50)

                # Reset state for the follow-up
                current_agent = "Clarifying Questions Agent"
                awaiting_clarifications = False
                clarification_questions = []
                research_content = ""  # Reset until we get to Research Agent

                # Continue with clarification responses
                clarification_response = "\n\n".join(answers)

                async for event in agency.get_response_stream(clarification_response):
                    # Same event handling as above
                    if (
                        hasattr(event, "type")
                        and event.type == "agent_updated_stream_event"
                    ):
                        if hasattr(event, "new_agent"):
                            current_agent = event.new_agent.name
                            print(f"\n\n🔄 Switched to: {current_agent}")
                            print("─" * 50)

                            if current_agent == "Research Instruction Agent":
                                print("📋 Building research instructions...")
                            elif current_agent == "Research Agent":
                                print(
                                    "🔬 Performing deep research... This may take a few minutes."
                                )

                    elif hasattr(event, "data"):
                        data = event.data

                        if hasattr(data, "delta") and hasattr(data, "type"):
                            if data.type == "response.output_text.delta":
                                delta_text = data.delta
                                if delta_text:
                                    print(delta_text, end="", flush=True)

                                    if current_agent == "Research Agent":
                                        research_content += delta_text

                    elif hasattr(event, "type") and event.type == "raw_response_event":
                        if hasattr(event, "data") and hasattr(event.data, "item"):
                            item = event.data.item
                            if hasattr(item, "action"):
                                action = item.action or {}
                                if (
                                    action.get("type") == "search"
                                    and current_agent == "Research Agent"
                                ):
                                    query_text = action.get("query", "")
                                    if query_text:
                                        print(f"\n🔍 [Web Search]: {query_text}")

            # Save PDF only if we have research content from Research Agent
            if research_content.strip():
                print("\n\n" + "─" * 50)
                save_response_to_pdf(research_content, query)
            else:
                print("\n\n⚠️ No research content generated. PDF not saved.")

            print("\n" + "=" * 70)  # Separator for next query

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            # Suppress MockValSer conversion errors that happen after streaming completes
            error_msg = str(e)
            if "MockValSer" in error_msg and "to_input_item" in error_msg:
                # This is a known issue with agency_swarm streaming - ignore it
                pass
            else:
                print(f"\n❌ Error: {e}")
                import traceback

                traceback.print_exc()


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

    if len(sys.argv) > 1 and sys.argv[1] in ["--ui", "--copilot"]:
        print("🚀 Launching Copilot UI...")
        copilot_demo()
    else:
        print("🚀 Launching Terminal Demo...")
        asyncio.run(stream_demo())
