"""
Qloo Insights Tool for Cultural Intelligence

Integrates with Qloo's Taste AI API to provide cultural and consumer preference insights.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

import httpx
from agency_swarm.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class QlooInsightsTool(BaseTool):
    """
    Tool for accessing Qloo's Taste AI API to get cultural intelligence and consumer preferences.
    
    Provides insights into how people interact with culture across music, TV, dining, fashion,
    travel, brands, books, podcasts, and more.
    """

    entity: str = Field(
        ...,
        description="The main entity to analyze (e.g., 'Taylor Swift', 'sushi', 'Netflix', 'Nike')"
    )
    
    tags: Optional[List[str]] = Field(
        default=None,
        description="Optional tags to refine the analysis (e.g., ['music', 'pop'], ['food', 'japanese'])"
    )
    
    demographics: Optional[str] = Field(
        default=None,
        description="Target demographic (e.g., 'Gen Z', 'millennials', 'adults 25-34')"
    )
    
    location: Optional[str] = Field(
        default=None,
        description="Geographic location for cultural context (e.g., 'United States', 'Tokyo', 'Europe')"
    )
    
    insight_type: str = Field(
        default="recommendations",
        description="Type of insight to retrieve: 'recommendations', 'affinities', 'trends', or 'analysis'"
    )

    def run(self) -> str:
        """
        Execute Qloo API call to get cultural insights.
        
        Returns:
            str: Formatted cultural insights and recommendations
        """
        api_key = os.getenv("QLOO_API_KEY")
        if not api_key:
            return "❌ Error: QLOO_API_KEY not found in environment variables. Please set your Qloo API key."

        try:
            # Prepare API request
            insights = self._get_qloo_insights(api_key)
            
            if not insights:
                return f"No cultural insights found for '{self.entity}'. The entity might not be in Qloo's database or the API request failed."
            
            # Format the response
            return self._format_insights(insights)
            
        except Exception as e:
            logger.error(f"Qloo API error: {e}")
            return f"❌ Error accessing Qloo API: {str(e)}"

    def _get_qloo_insights(self, api_key: str) -> Dict[str, Any]:
        """
        Make API call to Qloo's Taste AI API.
        
        Args:
            api_key: Qloo API key
            
        Returns:
            Dict containing API response data
        """
        base_url = "https://api.qloo.com/v1"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Build request parameters
        params = {
            "entity": self.entity,
            "limit": 20  # Get top 20 recommendations/insights
        }
        
        if self.tags:
            params["tags"] = ",".join(self.tags)
        if self.demographics:
            params["demographics"] = self.demographics
        if self.location:
            params["location"] = self.location
            
        try:
            with httpx.Client(timeout=30.0) as client:
                # Try different endpoints based on insight type
                if self.insight_type == "recommendations":
                    response = client.get(f"{base_url}/recommendations", headers=headers, params=params)
                elif self.insight_type == "affinities":
                    response = client.get(f"{base_url}/affinities", headers=headers, params=params)
                elif self.insight_type == "trends":
                    response = client.get(f"{base_url}/trends", headers=headers, params=params)
                else:
                    # Default to recommendations
                    response = client.get(f"{base_url}/recommendations", headers=headers, params=params)
                
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise Exception("Invalid Qloo API key. Please check your QLOO_API_KEY.")
            elif e.response.status_code == 429:
                raise Exception("Qloo API rate limit exceeded. Please try again later.")
            else:
                raise Exception(f"Qloo API error (HTTP {e.response.status_code}): {e.response.text}")
        except httpx.TimeoutException:
            raise Exception("Qloo API request timed out. Please try again.")
        except Exception as e:
            raise Exception(f"Network error accessing Qloo API: {str(e)}")

    def _format_insights(self, insights: Dict[str, Any]) -> str:
        """
        Format Qloo API response into readable insights.
        
        Args:
            insights: Raw API response data
            
        Returns:
            str: Formatted insights text
        """
        formatted = f"## 🎯 Qloo Cultural Insights for '{self.entity}'\n\n"
        
        # Add context information
        context_parts = []
        if self.demographics:
            context_parts.append(f"Demographics: {self.demographics}")
        if self.location:
            context_parts.append(f"Location: {self.location}")
        if self.tags:
            context_parts.append(f"Tags: {', '.join(self.tags)}")
            
        if context_parts:
            formatted += f"**Context:** {' | '.join(context_parts)}\n\n"
        
        # Process recommendations
        if "recommendations" in insights:
            recommendations = insights["recommendations"]
            if recommendations:
                formatted += "### 📊 Cultural Recommendations\n\n"
                for i, rec in enumerate(recommendations[:10], 1):  # Top 10
                    name = rec.get("name", "Unknown")
                    score = rec.get("score", 0)
                    category = rec.get("category", "")
                    
                    formatted += f"{i}. **{name}**"
                    if category:
                        formatted += f" ({category})"
                    if score:
                        formatted += f" - Affinity Score: {score:.2f}"
                    formatted += "\n"
                formatted += "\n"
        
        # Process affinities
        if "affinities" in insights:
            affinities = insights["affinities"]
            if affinities:
                formatted += "### 🔗 Cultural Affinities\n\n"
                for category, items in affinities.items():
                    if items:
                        formatted += f"**{category.title()}:**\n"
                        for item in items[:5]:  # Top 5 per category
                            name = item.get("name", "Unknown")
                            score = item.get("score", 0)
                            formatted += f"- {name}"
                            if score:
                                formatted += f" (Score: {score:.2f})"
                            formatted += "\n"
                        formatted += "\n"
        
        # Process trends
        if "trends" in insights:
            trends = insights["trends"]
            if trends:
                formatted += "### 📈 Cultural Trends\n\n"
                for trend in trends[:5]:  # Top 5 trends
                    name = trend.get("name", "Unknown")
                    momentum = trend.get("momentum", 0)
                    description = trend.get("description", "")
                    
                    formatted += f"- **{name}**"
                    if momentum:
                        formatted += f" (Momentum: {momentum:.2f})"
                    if description:
                        formatted += f": {description}"
                    formatted += "\n"
                formatted += "\n"
        
        # Add metadata
        if "metadata" in insights:
            metadata = insights["metadata"]
            formatted += "### 📋 Analysis Metadata\n\n"
            for key, value in metadata.items():
                formatted += f"- **{key.title()}:** {value}\n"
            formatted += "\n"
        
        # Add privacy note
        formatted += "---\n"
        formatted += "*Cultural insights powered by Qloo's Taste AI™ - privacy-first cultural intelligence with no personal identifying data.*\n"
        
        return formatted