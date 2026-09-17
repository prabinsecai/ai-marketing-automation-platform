from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models.analytics import CampaignMetric, OptimizationRecommendation
from app.models.campaign import Campaign

class AnalyticsService:
    @staticmethod
    def get_campaign_performance(db: Session, campaign_id: str) -> Dict[str, Any]:
        metrics = db.query(CampaignMetric).filter(CampaignMetric.campaign_id == campaign_id).all()
        
        total_spend = sum(m.spend for m in metrics)
        total_impressions = sum(m.impressions for m in metrics)
        total_clicks = sum(m.clicks for m in metrics)
        total_leads = sum(m.leads for m in metrics)
        total_conversions = sum(m.conversions for m in metrics)
        total_revenue = sum(m.revenue for m in metrics)
        
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0.0
        cpc = (total_spend / total_clicks) if total_clicks > 0 else 0.0
        cpl = (total_spend / total_leads) if total_leads > 0 else 0.0
        cpa = (total_spend / total_conversions) if total_conversions > 0 else 0.0
        conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0.0
        roas = (total_revenue / total_spend) if total_spend > 0 else 0.0
        roi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0.0
        
        channels = {}
        for m in metrics:
            if m.channel not in channels:
                channels[m.channel] = {"spend": 0, "clicks": 0, "impressions": 0, "conversions": 0}
            channels[m.channel]["spend"] += m.spend
            channels[m.channel]["clicks"] += m.clicks
            channels[m.channel]["impressions"] += m.impressions
            channels[m.channel]["conversions"] += m.conversions
            
        return {
            "spend": total_spend,
            "impressions": total_impressions,
            "clicks": total_clicks,
            "leads": total_leads,
            "conversions": total_conversions,
            "revenue": total_revenue,
            "ctr": ctr,
            "cpc": cpc,
            "cpl": cpl,
            "cpa": cpa,
            "conversion_rate": conversion_rate,
            "roas": roas,
            "roi": roi,
            "channels": channels
        }

    @staticmethod
    def run_diagnostics(db: Session, campaign_id: str) -> List[Dict[str, Any]]:
        perf = AnalyticsService.get_campaign_performance(db, campaign_id)
        issues = []
        
        if perf["spend"] > 0 and perf["ctr"] < 1.5:
            issues.append({"type": "LOW_CTR", "severity": "HIGH", "message": "Click-through rate is below 1.5%. Consider refreshing ad creative or adjusting audience."})
            
        if perf["cpa"] > 50:
            issues.append({"type": "HIGH_CPA", "severity": "MEDIUM", "message": f"Cost per acquisition is high (${perf['cpa']:.2f}). Check landing page conversion rates."})
            
        if perf["spend"] > 1000 and perf["conversions"] == 0:
            issues.append({"type": "CRITICAL_WASTE", "severity": "CRITICAL", "message": "High spend with zero conversions. Pause campaign immediately."})
            
        return issues
