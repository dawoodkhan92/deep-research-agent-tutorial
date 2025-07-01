# Deep Research Agent Tutorial - CRITICAL CODEBASE NAVIGATION

## ⚠️ CRITICAL LESSON LEARNED - AI AGENT FAILURE PATTERN ⚠️

**FAILURE MODE DISCOVERED**: AI agent attempted to commit changes without reading ALL staged changes comprehensively first.

**WHAT HAPPENED**: 
- Agent ran `git status` but failed to thoroughly read `git diff --staged | cat`
- Agent attempted to proceed with commit based on partial review
- User correctly rejected this approach - "WTF? read ALL CHANGES IN FULL!"

**MANDATORY PROCEDURE - NO EXCEPTIONS**:
1. **ALWAYS run `git diff --staged | cat` FIRST and READ EVERY LINE**
2. **NEVER proceed with commit until ALL changes reviewed comprehensively**  
3. **If changes are extensive, read each file completely to understand context**
4. **Only after full review → ask for explicit user approval to commit**

**This failure pattern MUST be avoided by all future AI agents working on this codebase!**

**CRITICAL RULE**: AGENTS.md is a HANDBOOK ONLY - NEVER use as scratchpad or for status reports!

## ⚠️ CRITICAL SAFETY INSTRUCTIONS - READ FIRST ⚠️

**🚨 MANDATORY REQUIREMENT: ALWAYS UPDATE THIS FILE WHEN MAKING ANY CHANGES OR DISCOVERIES! 🚨**

This file MUST be the single source of truth for **PROJECT-SPECIFIC** information only.

### OBLIGATION: REFERENCE, DON'T DUPLICATE
**When updating this file, you MUST**:
1. **Reference official docs** instead of copying content
2. **Keep this file minimal** - only project-specific critical info
3. **Point to authoritative sources** for Agency Swarm patterns
4. **NO code examples** - link to official examples instead

If you touch ANY code or discover ANY issues:
1. **IMMEDIATELY update this AGENTS.md file** 
2. **Run `git status` and `git diff` to monitor changes**
3. **Test with `python main.py` after ANY modification**
4. **NO EXCEPTIONS - Lives depend on accuracy!**

---

## 📚 OFFICIAL AGENCY SWARM DOCUMENTATION

### Get Official Patterns & Examples
```bash
# Clone official repository for reference
git clone https://github.com/VRSEN/agency-swarm.git
cd agency-swarm
git checkout release/v1.0.0-beta

# Key files to read:
# - docs/core-framework/agencies/communication-flows.mdx
# - docs/core-framework/agencies/agency-parameters.mdx  
# - docs/core-framework/agencies/visualization.mdx
# - examples/ (for real implementation patterns)
```

**CRITICAL**: Always reference official docs at `github.com/VRSEN/agency-swarm/tree/release/v1.0.0-beta/docs` instead of duplicating here!

---

## 🔥 CRITICAL FOLDER NAMING REQUIREMENTS

### ⚠️ NEVER USE `/agents` OR `/agents_modules` FOLDER NAMES! ⚠️

**CRITICAL BUG DISCOVERED**: If you name the folder `/agents`, it creates a namespace collision with the `openai-agents` package:


**MANDATORY FOLDER STRUCTURE**:
- ✅ **ALWAYS USE**: `deep_research/` folder for modular components

**Current safe structure**: All agents defined in `main.py` with exact cookbook preservation + modular components in `deep_research/`

---

## 🗂️ FILES FOLDER BEHAVIOR - CRITICAL UNDERSTANDING

### How Agent File Processing Works

When you configure agents with file access, the system automatically:
1. Scans `./files/` directory for all documents
2. **Creates unique file IDs** with random suffixes for internal processing
3. Processes documents into vector store for agent access
4. Agent can analyze these documents via MCP tools

**Current files/ folder structure**:
```
files/
└── sample_research_data.md                # Manual knowledge file
```

**CRITICAL**: Files are processed automatically by the agents SDK for internal knowledge search!

---

## 🎯 Project Overview

**Deep Research Agent Tutorial** - Implementation of OpenAI cookbook patterns using agents SDK with Agency Swarm extensions.

## 🚨 CRITICAL PRESERVATION REQUIREMENT 🚨

**MANDATORY**: Every single line, class, parameter, function from `original_cookbook.ipynb` MUST be preserved EXACTLY as-is. 

**FORBIDDEN CHANGES**:
- ❌ NO model changes (must use exact models from cookbook)
- ❌ NO import changes (must use exact imports from cookbook) 
- ❌ NO parameter changes (must use exact parameters from cookbook)
- ❌ NO function signature changes (must preserve exact signatures)
- ❌ NO prompt changes (must preserve exact prompt text)
- ❌ NO logic changes (must preserve exact logic flow)

**REQUIRED VERIFICATION**:
- ✅ Line-by-line comparison with original cookbook
- ✅ Every import statement exactly preserved
- ✅ Every function exactly preserved  
- ✅ Every class exactly preserved
- ✅ Every parameter exactly preserved

**EVIDENCE-BASED APPROACH**: Before changing ANYTHING, must read original cookbook and verify exact preservation!

### Current File Structure

```
deep-research-agent-tutorial/
├── main.py
├── AGENTS.md                             # THIS FILE - CRITICAL WORKFLOW INFO ONLY!
├── README.md                             # Usage documentation
├── requirements.txt                      # Dependencies
├── deep_research/
│   ├── __init__.py                       # Module definition
│   ├── basic_research_agent.py           # Basic research agent factory
│   ├── research_agent.py                 # Multi-agent research agent
│   ├── instruction_agent.py              # Instruction building agent
│   ├── clarifying_agent.py               # Clarification agent
│   ├── triage_agent.py                   # Triage agent
│   ├── structured_outputs.py             # Pydantic models
│   ├── prompts.py                        # Agent prompts
│   ├── utils.py                          # Utility functions
│   ├── visualization.py                  # Agency visualization
│   └── pdf_generator.py                  # PDF generation
├── files/                                # Knowledge files for MCP processing
│   └── sample_research_data.md          # Sample data for agents
└── outputs/                              # Generated research results
```

---

## 🧪 TESTING - MANDATORY AFTER ANY CHANGE

### Always Run After Changes
```bash
# ⚠️ MANDATORY - Run after ANY code change:
python main.py                    # Must execute without errors
git status                        # Monitor what changed
git diff                          # Review all changes
```

---

## 📦 Dependencies - ESSENTIAL

### Core Requirements
```
agency-swarm>=1.0.0b3           # Agency Swarm extensions
python-dotenv>=1.0.0            # Environment variables
typing-extensions>=4.0.0        # Type support
reportlab>=4.0.0                # PDF generation
```

---

## 🚨 CRITICAL MAINTENANCE OBLIGATIONS

### MANDATORY ACTIONS for ANY Code Change

1. **UPDATE THIS FILE IMMEDIATELY** - Add discoveries, changes, warnings
2. **RUN GIT COMMANDS**:
   ```bash
   git status                   # What changed?
   git diff                     # Review changes  
   git add . && git commit -m "..." # Commit when stable
   ```
3. **RUN TESTS**: `python main.py` - Must execute successfully
4. **VERIFY IMPORTS**: No namespace collisions with `openai-agents`
5. **CHECK FILE PROCESSING**: Ensure files/ directory works correctly

### CRITICAL WARNINGS TO ADD HERE

**Add any new discoveries, bugs, or critical patterns here immediately!**

---

## 🎯 Common Tasks - SAFE PROCEDURES

### Modifying Agent Behavior
1. **Edit agent definitions in `main.py`** - All agents are defined there
2. **Preserve exact cookbook patterns** - Don't modify core functionality
3. **UPDATE THIS AGENTS.md FILE** with any discoveries
4. **Test**: `python main.py` - Must work correctly

### Modifying Files Folder
1. **Add new `.md` files** to `/files` directory for agent knowledge
2. **Agent auto-processes** files via MCP integration
3. **UPDATE THIS AGENTS.md FILE** with changes
4. **DO NOT** manually edit auto-generated files with random suffixes

### Emergency Debugging
```bash
# If anything breaks, immediately run:
git status                      # What changed?
git diff                        # See exact changes
python main.py                  # Test execution
ls -la files/                   # Check file processing
```

---

**🚨 REMEMBER: THIS FILE MUST BE UPDATED WITH EVERY CHANGE OR DISCOVERY! 🚨**  
**Lives depend on accurate documentation and maintaining this single source of truth!**
