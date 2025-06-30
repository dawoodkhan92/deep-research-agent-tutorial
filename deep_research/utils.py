"""Utility Functions - From OpenAI Cookbook"""

import json
from .structured_outputs import Clarifications

def parse_agent_interaction_flow(stream):
    """
    Parse and display agent interaction flow with tool calls.
    
    Provides a human-readable sequence of agent steps including:
    - Agent name
    - Type of event (handoff, tool call, message output)  
    - Brief tool call info (tool name and arguments)
    """
    print("=== Agent Interaction Flow ===")
    count = 1

    for item in stream.new_items:
        # Agent name, fallback if missing
        agent_name = getattr(item.agent, "name", "Unknown Agent") if hasattr(item, "agent") else "Unknown Agent"

        if item.type == "handoff_call_item":
            func_name = getattr(item.raw_item, "name", "Unknown Function")
            print(f"{count}. [{agent_name}] → Handoff Call: {func_name}")
            count += 1

        elif item.type == "handoff_output_item":
            print(f"{count}. [{agent_name}] → Handoff Output")
            count += 1

        elif item.type == "mcp_list_tools_item":
            print(f"{count}. [{agent_name}] → mcp_list_tools_item")
            count += 1

        elif item.type == "reasoning_item":
            print(f"{count}. [{agent_name}] → Reasoning step")
            count += 1

        elif item.type == "tool_call_item":
            tool_name = getattr(item.raw_item, "name", None)

            # Skip tool call if tool_name is missing or empty
            if not isinstance(tool_name, str) or not tool_name.strip():
                continue  # skip silently

            tool_name = tool_name.strip()

            args = getattr(item.raw_item, "arguments", None)
            args_str = ""

            if args:
                try:
                    parsed_args = json.loads(args)
                    if parsed_args:
                        args_str = json.dumps(parsed_args)
                except Exception:
                    if args.strip() and args.strip() != "{}":
                        args_str = args.strip()

            args_display = f" with args {args_str}" if args_str else ""

            print(f"{count}. [{agent_name}] → Tool Call: {tool_name}{args_display}")
            count += 1

        elif item.type == "message_output_item":
            print(f"{count}. [{agent_name}] → Message Output")
            count += 1

        else:
            print(f"{count}. [{agent_name}] → {item.type}")
            count += 1

def print_final_output_citations(stream, preceding_chars=50):
    """
    Extract and print URL citations from the final output.
    
    Args:
        stream: The result stream from agent execution
        preceding_chars: Number of characters to show before citation
    """
    # Iterate over new_items in reverse to find the last message_output_item(s)
    for item in reversed(stream.new_items):
        if item.type == "message_output_item":
            for content in getattr(item.raw_item, 'content', []):
                if not hasattr(content, 'annotations') or not hasattr(content, 'text'):
                    continue
                text = content.text
                for ann in content.annotations:
                    if getattr(ann, 'type', None) == 'url_citation':
                        title = getattr(ann, 'title', '<no title>')
                        url = getattr(ann, 'url', '<no url>')
                        start = getattr(ann, 'start_index', None)
                        end = getattr(ann, 'end_index', None)

                        if start is not None and end is not None and isinstance(text, str):
                            # Calculate preceding snippet start index safely
                            pre_start = max(0, start - preceding_chars)
                            preceding_text = text[pre_start:start].replace('\n', ' ').strip()
                            excerpt = text[start:end].replace('\n', ' ').strip()
                            print("# --------")
                            print("# MCP CITATION SAMPLE:")
                            print(f"#   Title:       {title}")
                            print(f"#   URL:         {url}")
                            print(f"#   Location:    chars {start}–{end}")
                            print(f"#   Preceding:   '{preceding_text}'")
                            print(f"#   Excerpt:     '{excerpt}'\n")
                        else:
                            # fallback if no indices available
                            print(f"- {title}: {url}")
            break 