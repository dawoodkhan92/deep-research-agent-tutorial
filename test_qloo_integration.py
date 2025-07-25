#!/usr/bin/env python3
"""
Test Qloo API Integration

Quick test to verify the QlooInsightsTool is working correctly.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

load_dotenv()


async def test_qloo_tool():
    """Test the QlooInsightsTool directly"""
    print("🧪 Testing Qloo API Integration...")
    print("=" * 50)

    try:
        from agents import QlooInsightsTool

        # Test with a popular entity
        tool = QlooInsightsTool(
            entity="Taylor Swift",
            tags=["music", "pop"],
            demographics="Gen Z",
            location="United States",
            insight_type="recommendations"
        )

        print(f"🎯 Testing entity: {tool.entity}")
        print(f"📊 Demographics: {tool.demographics}")
        print(f"📍 Location: {tool.location}")
        print(f"🏷️ Tags: {tool.tags}")
        print("-" * 50)

        result = tool.run()
        print("🤖 Qloo API Response:")
        print(result)
        print("=" * 50)

        # Basic validation
        if "❌ Error" in result:
            print("⚠️ API call failed - check your QLOO_API_KEY")
            return False
        elif "Cultural Insights" in result:
            print("✅ Qloo integration working correctly!")
            return True
        else:
            print("⚠️ Unexpected response format")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_agency_with_qloo():
    """Test the DeepResearchAgency with a Qloo-relevant query"""
    print("\n🧪 Testing DeepResearchAgency with Qloo integration...")
    print("=" * 50)

    try:
        # Import the agency
        sys.path.insert(0, str(Path("DeepResearchAgency")))
        from DeepResearchAgency.agency import agency

        # Test query that should trigger Qloo usage
        query = "Analyze the cultural impact and consumer preferences for K-pop music among Gen Z in the United States"

        print(f"📝 Query: {query}")
        print("-" * 50)

        # Get response (non-streaming for testing)
        response = await agency.get_response(query)

        print("🤖 Agency Response:")
        print(str(response)[:500] + "..." if len(str(response)) > 500 else str(response))
        print("=" * 50)

        # Check if Qloo insights are included
        response_str = str(response).lower()
        if "qloo" in response_str or "cultural insights" in response_str:
            print("✅ Agency successfully integrated Qloo insights!")
            return True
        else:
            print("⚠️ Qloo insights may not have been used")
            return False

    except Exception as e:
        print(f"❌ Agency test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all Qloo integration tests"""
    print("🚀 Testing Qloo API Integration for Deep Research Agency")
    print("🎯 Preparing for Qloo LLM Hackathon submission")
    print()

    # Check API key
    if not os.getenv("QLOO_API_KEY"):
        print("❌ QLOO_API_KEY not found in environment")
        print("💡 Please add your Qloo API key to .env file:")
        print("   QLOO_API_KEY=your_qloo_api_key_here")
        return

    try:
        # Test 1: Direct tool test
        tool_success = await test_qloo_tool()

        # Test 2: Agency integration test
        agency_success = await test_agency_with_qloo()

        print("\n🎯 TEST RESULTS SUMMARY")
        print("=" * 50)
        print(f"✅ Qloo Tool: {'PASS' if tool_success else 'FAIL'}")
        print(f"✅ Agency Integration: {'PASS' if agency_success else 'FAIL'}")

        if tool_success and agency_success:
            print("\n🎉 SUCCESS! Qloo integration is ready for the hackathon!")
            print("\n📋 Next Steps:")
            print("   1. Test with various cultural queries")
            print("   2. Generate sample PDF reports")
            print("   3. Record demo video")
            print("   4. Prepare GitHub repository")
        else:
            print("\n⚠️ Some tests failed. Please review and fix issues.")

    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())