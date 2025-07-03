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

# Basic Research Agent - o4-mini-deep-research with web search
research_agent = Agent(
    name="Research Agent",
    model="o4-mini-deep-research-2025-06-26",
    tools=[WebSearchTool()],
    instructions="You perform deep empirical research based on the user's question.",
)

# Create the agency
agency = Agency(research_agent)


async def stream_response(message: str):
    """Stream a response and handle events properly following streaming.py pattern."""
    print(f"\n🔥 Streaming: {message}")
    print("📡 Response: ", end="", flush=True)

    full_text = ""

    async for event in agency.get_response_stream(message):
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

    print("\n✅ Stream complete")
    print(f"📋 Total: {len(full_text)} characters streamed")
    return full_text


async def stream_demo():
    """Interactive research terminal using proper Agency Swarm streaming."""
    print("🌟 Basic Research Agency - Deep Research Tool")
    print("=" * 50)
    print("Ask any research question. Type 'quit' to exit.\n")

    while True:
        try:
            query = input("🔥 Research Query: ").strip()
            if query.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if not query:
                print("Please enter a research question.")
                continue

            # Use proper streaming pattern
            result = await stream_response(query)
            print("=" * 50)

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback

            traceback.print_exc()


def copilot_demo():
    """Launch Copilot UI demo."""
    try:
        from agency_swarm.ui.demos.launcher import CopilotDemoLauncher

        launcher = CopilotDemoLauncher()
        launcher.start(agency)
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
