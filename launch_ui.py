#!/usr/bin/env python3
"""
Quick launcher for Deep Research Agency UI

This script provides an easy way to launch the Copilot UI for either agency.
"""

import os
import sys
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def main():
    """Launch the UI with agency selection"""
    print("🚀 Deep Research Agency UI Launcher")
    print("=" * 50)
    
    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in .env file")
        print("💡 Please add your OpenAI API key to the .env file")
        return
    
    if not os.getenv("QLOO_API_KEY"):
        print("⚠️  QLOO_API_KEY not found - cultural intelligence features will be limited")
    else:
        print("✅ Qloo API key configured for cultural intelligence")
    
    # Show MCP status
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8001/sse")
    print(f"📡 MCP Server: {mcp_url}")
    
    print("\nChoose an agency to launch:")
    print("1. BasicResearchAgency (Single agent, faster)")
    print("2. DeepResearchAgency (Multi-agent with clarification)")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n🚀 Launching BasicResearchAgency UI...")
            sys.path.insert(0, str(Path("BasicResearchAgency")))
            from BasicResearchAgency.agency import agency
            from utils import copilot_demo, save_research_report
            copilot_demo(agency, save_research_report)
            break
            
        elif choice == "2":
            print("\n🚀 Launching DeepResearchAgency UI...")
            sys.path.insert(0, str(Path("DeepResearchAgency")))
            from DeepResearchAgency.agency import agency
            from utils import copilot_demo, save_research_report
            copilot_demo(agency, save_research_report)
            break
            
        elif choice == "3":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()