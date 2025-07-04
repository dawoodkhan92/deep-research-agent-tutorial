# Deep Research Agent Tutorial

**Beginner-friendly tutorial** implementing OpenAI Deep Research API patterns using Agency Swarm v1.x framework.

## 🎯 Project Overview

This tutorial demonstrates two research patterns from the [OpenAI Deep Research Cookbook](https://cookbook.openai.com/examples/deep_research_api/deep_research_agents):

1. **Basic Research** - Single agent with web search
2. **Multi-Agent Research** - Four agents with handoffs pattern

## 📁 Current Structure

```
deep-research-agent-tutorial/
├── BasicResearchAgency/
│   └── agency.py                     # 🎯 Single agent research (simplest)
├── DeepResearchAgency/
│   ├── agency.py                     # 🎯 Multi-agent handoffs pattern
│   ├── ClarifyingAgent/              # Asks clarification questions
│   ├── InstructionBuilderAgent/      # Enriches research queries
│   ├── ResearchAgent/                # Performs final research
│   └── utils.py                      # Citation processing + PDF generation
├── files/                            # Knowledge files for research context
└── mcp/                              # MCP server for internal search
```

## 🚀 Quick Start

### 1. Set up environment
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Add knowledge files to ./files folder (optional)
# Supports: .txt, .md, .json, .csv
```

### 2. Start MCP Server (for internal file search)
```bash
# Start the local MCP server in a separate terminal
python mcp/start_mcp_server.py

# The server will run on http://localhost:8001
# Keep this running while using the research agencies
```

### 3. Run Basic Research (Simplest)
```bash
cd BasicResearchAgency
python agency.py                      # Terminal streaming demo with PDF generation (default)
python agency.py --ui                 # Launch Copilot UI
```

### 4. Run Multi-Agent Research (Advanced)
```bash
cd DeepResearchAgency
python agency.py                      # Terminal streaming demo with PDF generation (default)
python agency.py --ui                 # Launch Copilot UI
```



## 🔧 Architecture

### BasicResearchAgency
- **Single Agent**: Research Agent
- **Model**: `o4-mini-deep-research-2025-06-26` (fast)
- **Tools**: WebSearchTool + MCP internal search
- **Perfect for**: Beginners, simple research tasks

### DeepResearchAgency
- **Entry Point**: Triage Agent
- **Flow**: Triage → [Clarifying] → Instruction → Research
- **Pattern**: Sequential handoffs (cookbook exact)
- **Features**: Citation processing, agent interaction flow
- **Perfect for**: Complex research with clarification workflow

## 🧪 Testing

```bash
python tests/test_simple.py
# Should output: ✅ BasicResearchAgency ✅ DeepResearchAgency
```

## 📚 Key Features

- ✅ **Beginner-friendly**: Simple Agency Swarm v1.0 patterns
- ✅ **Cookbook aligned**: Exact prompts and models from OpenAI cookbook
- ✅ **Modern demos**: Streaming terminal + Copilot UI support
- ✅ **Hybrid search**: Web + internal documents via MCP integration
- ✅ **Auto file upload**: Agency Swarm handles files/ folder automatically
- ✅ **Citation processing**: Extract and display research sources
- ✅ **Enhanced PDF Generation**: Professional PDFs with numbered URL references using WeasyPrint and full markdown support


## 🔗 MCP Integration ⚠️ CRITICAL

**Why MCP is Required**: OpenAI's FILE SEARCH TOOL is **NOT supported** with deep research models. MCP is the ONLY way to access internal documents.

### 🎯 How Vector Store Detection Works (Automatic!)

**Simple 3-Step Process**:
1. **Run an Agency** → Agency Swarm uploads `./files/` and creates `files_vs_[id]` folder
2. **Start MCP Server** → Automatically finds the `files_vs_*` folder and extracts vector store ID
3. **Research Works** → Agents can now search both web + your internal documents

**Priority Order** (for advanced users):
- **Environment Variable**: `VECTOR_STORE_ID=vs_xxxxx` (manual override)
- **Auto-Detection**: Finds `files_vs_*` folders automatically
- **Error**: Clear guidance if no vector store exists

**Key Benefits**:
- ✅ **Zero Configuration** - Works automatically after first agency run
- ✅ **Persistent** - Vector store persists and gets reused across sessions
- ✅ **Multi-Agency** - Handles multiple agencies (uses most recent)

### 🔧 Technical Implementation

**MCP Server Architecture**:
- **Auto-Detection**: Finds `files_vs_*` folders across agency directories automatically
- **Priority System**: Environment variable override → folder detection → clear error guidance
- **Modular Design**: Clean separation between server and detection utilities

## 🛠️ Requirements

```bash
pip install -r requirements.txt
```

Set `OPENAI_API_KEY` in `.env` file. Start with BasicResearchAgency for simplest example!
