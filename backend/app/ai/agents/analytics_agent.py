import json
import asyncio
from typing import Dict, Any, List
from typing_extensions import TypedDict
from app.ai.factory import get_llm_provider
from app.schemas.analytics import CampaignAnalyticsReport, AIAnalyticsInsight, AIAnalyticsRecommendation
from pydantic import BaseModel

class InsightsResponse(BaseModel):
    insights: List[AIAnalyticsInsight]

class RecommendationsResponse(BaseModel):
    recommendations: List[AIAnalyticsRecommendation]

class AnalyticsAgent:
    def __init__(self):
        self.llm = get_llm_provider("mock")

    async def run(self, campaign_name: str, performance: Dict[str, Any], diagnostics: List[Dict[str, Any]]) -> Dict[str, Any]:
        system_prompt_insights = "You are an expert AI Marketing Analyst. Generate evidence-based insights."
        user_prompt_insights = (
            f"Campaign: {campaign_name}\n"
            f"Performance: {json.dumps(performance, indent=2)}\n"
            f"Diagnostics: {json.dumps(diagnostics, indent=2)}\n"
            "Identify anomalies, strong performing channels, and areas of waste."
        )
        
        insight_res = await self.llm.generate_structured(
            system_prompt_insights,
            user_prompt_insights,
            InsightsResponse
        )
        
        system_prompt_recs = "You are an expert AI Marketing Analyst. Generate safe optimization recommendations. Never recommend autonomous spending."
        user_prompt_recs = (
            f"Campaign: {campaign_name}\n"
            f"Insights: {json.dumps([i.dict() for i in insight_res.parsed.insights], indent=2)}\n"
        )
        
        rec_res = await self.llm.generate_structured(
            system_prompt_recs,
            user_prompt_recs,
            RecommendationsResponse
        )
        
        return {
            "insights": [i.dict() for i in insight_res.parsed.insights],
            "recommendations": [r.dict() for r in rec_res.parsed.recommendations]
        }
