import json
from typing import Callable, List, Tuple

from agency_swarm import Agency


def _print_debug(event, seen):
    event_type = getattr(event, "type", None)
    if event_type and event_type not in seen and event_type != "response.output_text.delta":
        print(f"\n[DEBUG] {event_type}")
        seen.add(event_type)


async def stream_response(
    agency: Agency, message: str, debug: bool = False
) -> Tuple[str, List[str]]:
    """Stream a response from an agency with optional debug logging."""
    print(f"\n🔥 Streaming: {message}")
    print("📡 Response: ", end="", flush=True)

    full_text = ""
    clarification_questions: List[str] = []
    clarifying_text = ""
    current_agent = None
    seen_events = set()

    async for event in agency.get_response_stream(message):
        if debug:
            _print_debug(event, seen_events)

        if getattr(event, "type", None) == "agent_updated_stream_event" and hasattr(event, "new_agent"):
            current_agent = event.new_agent.name
            print(f"\n\n🔄 Switched to: {current_agent}")
            print("─" * 50)
            continue

        if hasattr(event, "data"):
            data = event.data
            if getattr(data, "type", "") == "response.output_text.delta":
                delta = getattr(data, "delta", "")
                if delta:
                    if current_agent != "Clarifying Questions Agent":
                        print(delta, end="", flush=True)
                    if current_agent == "Clarifying Questions Agent":
                        clarifying_text += delta
                    if current_agent == "Research Agent" or not current_agent:
                        full_text += delta
            elif getattr(data, "type", "") == "response.function_call_arguments.delta" and debug:
                print(f"\n[DEBUG] Tool call: {data.delta}")

        elif getattr(event, "type", None) == "raw_response_event":
            if hasattr(event, "data") and hasattr(event.data, "item"):
                action = getattr(event.data.item, "action", {}) or {}
                if action.get("type") == "search" and current_agent == "Research Agent":
                    query_text = action.get("query", "")
                    if query_text:
                        print(f"\n🔍 [Web Search]: {query_text}")

        elif hasattr(event, "item") and hasattr(event.item, "questions"):
            clarification_questions = list(event.item.questions)

        elif isinstance(event, dict) and event.get("event") == "error":
            print(f"\n❌ Error: {event.get('content', event.get('data', 'Unknown'))}")
            break

    if clarifying_text and not clarification_questions:
        try:
            data = json.loads(clarifying_text.strip())
            clarification_questions = data.get("questions", [])
        except json.JSONDecodeError:
            pass

    print("\n✅ Stream complete")
    return full_text, clarification_questions


async def stream_demo(
    agency: Agency,
    save_pdf: Callable[[str, str], str] | None = None,
    debug: bool = False,
):
    """Interactive terminal demo for any research agency."""
    print("🌟 Research Agency Demo")
    print("Ask any research question. Type 'quit' to exit.\n")

    while True:
        try:
            query = input("🔥 Research Query: ").strip()
            if query.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if not query:
                continue

            response_text, questions = await stream_response(agency, query, debug)

            if questions:
                print("\n✏️ Please answer the following questions:\n")
                answers = []
                for q in questions:
                    ans = input(f"{q}\n   Your answer: ").strip() or "No preference."
                    answers.append(f"**{q}**\n{ans}")
                follow_text, _ = await stream_response(agency, "\n\n".join(answers), debug)
                response_text += follow_text

            if save_pdf and response_text.strip():
                pdf = save_pdf(response_text, query)
                print(f"\n📄 Research report saved to: {pdf}")

            print("\n" + "=" * 70)

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
