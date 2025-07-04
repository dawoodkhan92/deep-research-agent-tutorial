import json
from typing import Callable

from agency_swarm import Agency


def _print_debug(event, seen):
    """Enhanced debug logging to show key research events."""
    event_type = getattr(event, "type", None)

    # Show new event types once
    if (
        event_type
        and event_type not in seen
        and event_type != "response.output_text.delta"
    ):
        print(f"\n[DEBUG] Event: {event_type}")
        seen.add(event_type)

        # Show additional details for key events
        if event_type == "raw_response_event":
            if hasattr(event, "data") and hasattr(event.data, "item"):
                action = getattr(event.data.item, "action", None)
                if action and getattr(action, "type", None) == "search":
                    query_text = getattr(action, "query", "")
                    if query_text:
                        print(f"[DEBUG]   → Search Query: {query_text}")

        elif event_type == "handoff_call_item":
            if hasattr(event, "raw_item"):
                function_name = getattr(event.raw_item, "name", "Unknown")
                print(f"[DEBUG]   → Handoff: {function_name}")

    # Show agent switches
    elif event_type == "agent_updated_stream_event" and hasattr(event, "new_agent"):
        agent_name = event.new_agent.name
        print(f"\n[DEBUG] 🔄 Agent Switch: {agent_name}")

    # Show web searches
    elif event_type == "raw_response_event":
        if hasattr(event, "data") and hasattr(event.data, "item"):
            action = getattr(event.data.item, "action", None)
            if action and getattr(action, "type", None) == "search":
                query_text = getattr(action, "query", "")
                if query_text:
                    print(f"[DEBUG] 🔍 Web Search: {query_text}")


async def stream_demo(
    agency: Agency,
    save_pdf: Callable[[str, str], str] | None = None,
    debug: bool = True,
):
    """Interactive terminal demo following Agency Swarm patterns."""
    print("🌟 Research Agency Demo")
    print("Ask any research question. Type 'quit' to exit.")
    print("🔍 Debug logging enabled - you'll see key events during research.\n")

    while True:
        try:
            query = input("🔥 Research Query: ").strip()
            if query.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if not query:
                continue

            print(f"\n🔥 Researching: {query}")
            print("📡 Response: ", end="", flush=True)

            full_text = ""
            clarifying_text = ""
            current_agent = None
            seen_events = set()
            research_completed = False
            stream_error = None

            # Stream the response
            try:
                async for event in agency.get_response_stream(query):
                    if debug:
                        _print_debug(event, seen_events)

                    # Track agent switches for cleaner output
                    if getattr(
                        event, "type", None
                    ) == "agent_updated_stream_event" and hasattr(event, "new_agent"):
                        current_agent = event.new_agent.name
                        print(f"\n\n🔄 Switched to: {current_agent}")
                        print("─" * 50)
                        continue

                    # Handle text streaming
                    if hasattr(event, "data"):
                        data = event.data
                        if getattr(data, "type", "") == "response.output_text.delta":
                            delta = getattr(data, "delta", "")
                            if delta:
                                if current_agent == "Clarifying Questions Agent":
                                    # Accumulate clarifying text for JSON parsing
                                    clarifying_text += delta
                                else:
                                    print(delta, end="", flush=True)
                                    full_text += delta
                                    if current_agent == "Research Agent":
                                        research_completed = True

                    # Handle web search events
                    elif getattr(event, "type", None) == "raw_response_event":
                        if hasattr(event, "data") and hasattr(event.data, "item"):
                            action = getattr(event.data.item, "action", None)
                            if action and getattr(action, "type", None) == "search":
                                query_text = getattr(action, "query", "")
                                if query_text:
                                    print(f"\n🔍 [Web Search]: {query_text}")

                    # Handle errors
                    elif isinstance(event, dict) and event.get("event") == "error":
                        print(
                            f"\n❌ Error: {event.get('content', event.get('data', 'Unknown'))}"
                        )
                        break
            except Exception as e:
                stream_error = e

            # Handle clarification questions if we have them
            if clarifying_text.strip():
                try:
                    clarification_data = json.loads(clarifying_text.strip())
                    questions = clarification_data.get("questions", [])

                    if questions:
                        print("\n\n✏️ Please answer the following questions:\n")
                        answers = []
                        for q in questions:
                            ans = (
                                input(f"{q}\n   Your answer: ").strip()
                                or "No preference."
                            )
                            answers.append(f"**{q}**\n{ans}")

                        # Send clarifications and continue research
                        clarification_response = "\n\n".join(answers)
                        print("\n🔥 Continuing with clarifications...")
                        print("📡 Response: ", end="", flush=True)

                        # Reset for follow-up research
                        current_agent = None

                        try:
                            async for event in agency.get_response_stream(
                                clarification_response
                            ):
                                if debug:
                                    _print_debug(event, seen_events)

                                if getattr(
                                    event, "type", None
                                ) == "agent_updated_stream_event" and hasattr(
                                    event, "new_agent"
                                ):
                                    current_agent = event.new_agent.name
                                    print(f"\n\n🔄 Switched to: {current_agent}")
                                    print("─" * 50)
                                    continue

                                if hasattr(event, "data"):
                                    data = event.data
                                    if (
                                        getattr(data, "type", "")
                                        == "response.output_text.delta"
                                    ):
                                        delta = getattr(data, "delta", "")
                                        if delta:
                                            print(delta, end="", flush=True)
                                            full_text += delta
                                            if current_agent == "Research Agent":
                                                research_completed = True

                                elif (
                                    getattr(event, "type", None) == "raw_response_event"
                                ):
                                    if hasattr(event, "data") and hasattr(
                                        event.data, "item"
                                    ):
                                        action = getattr(
                                            event.data.item, "action", None
                                        )
                                        if (
                                            action
                                            and getattr(action, "type", None)
                                            == "search"
                                        ):
                                            query_text = getattr(action, "query", "")
                                            if query_text:
                                                print(
                                                    f"\n🔍 [Web Search]: {query_text}"
                                                )
                        except Exception as e:
                            stream_error = e
                except json.JSONDecodeError:
                    # If it's not JSON, treat as regular text
                    full_text += clarifying_text
                    research_completed = True

            if research_completed:
                print("\n✅ Research complete")
            else:
                print("\n⚠️ Process ended (research not completed)")

            # Only save to PDF if we have substantial research content
            if (
                save_pdf
                and full_text.strip()
                and research_completed
                and len(full_text) > 100
            ):
                save_pdf(full_text, query)

            print("\n" + "=" * 70)

            if stream_error:
                print(f"\n❌ Error during streaming: {stream_error}")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback

            traceback.print_exc()


def copilot_demo(agency: Agency, save_pdf: Callable[[str, str], str] | None = None):
    """Launch Copilot UI demo with optional PDF saving."""
    try:
        from agency_swarm.ui.demos.launcher import CopilotDemoLauncher

        if save_pdf:

            class PDFSavingAgency(Agency):
                def get_response(self, query: str, **kwargs):
                    response = super().get_response(query, **kwargs)
                    save_pdf(str(response), query)
                    return response

            agency = PDFSavingAgency(agency.entry_agent)

        launcher = CopilotDemoLauncher()
        launcher.start(agency)
    except ImportError:
        print("❌ Copilot demo requires additional dependencies")
        print("Install with: pip install agency-swarm[copilot]")
