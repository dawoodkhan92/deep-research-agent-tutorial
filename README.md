# Deep Research Agents - Agency Swarm Implementation

Implementation based on the [OpenAI Deep Research API Cookbook](https://cookbook.openai.com/examples/deep_research_api/introduction_to_deep_research_api_agents) using Agency Swarm as a drop-in replacement for the Agents SDK.

## Features

✅ **WebSearchTool** - Web search capabilities
✅ **Streaming Progress** - Real-time research updates
✅ **Async Execution** - Runner.run_streamed support
✅ **Structured Outputs** - Pydantic output_type validation
✅ **Citation Tracking** - URL citation extraction
✅ **Agent Interaction Flow** - Detailed workflow logging
✅ **Multi-Agent Handoffs** - Triage → Clarifying → Instruction → Research

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Run examples:**
   ```bash
   python main.py
   ```

## Implementation Structure

`main.py` contains the complete implementation:

- **Basic Research Agent** (o4-mini-deep-research model)
- **Multi-Agent Pipeline** (Triage → Clarifying → Instruction → Research)
- **Streaming Functions** with progress tracking
- **Utility Functions** for agent interaction flow and citations
- **Research Prompts** for optimal results

### Agent Flow

1. **Triage Agent** - Routes queries for clarification or direct research
2. **Clarifying Agent** - Asks follow-up questions (with structured output)
3. **Instruction Agent** - Converts queries into detailed research briefs
4. **Research Agent** - Performs deep research with web search and MCP

## Zero Data Retention

Enabled by default with `OPENAI_AGENTS_DISABLE_TRACING=1` for enterprise compliance.

## Files

- `files/` - Knowledge files for internal MCP search
- `outputs/` - Generated research results  
- `.env` - API key configuration
