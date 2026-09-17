from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.models.campaign import Campaign
from app.models.analytics import CampaignMetric, OptimizationRecommendation
from app.schemas.analytics import CampaignMetricCreate, CampaignMetricOut, CampaignAnalyticsReport, OptimizationRecommendationOut
from app.services.analytics_service import AnalyticsService
from app.ai.agents.analytics_agent import AnalyticsAgent

router = APIRouter()

@router.post("/campaigns/{id}/metrics", response_model=CampaignMetricOut, status_code=status.HTTP_201_CREATED)
def add_campaign_metrics(id: str, metric_in: CampaignMetricCreate, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    metric = CampaignMetric(**metric_in.dict())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

@router.get("/campaigns/{id}/analytics", response_model=CampaignAnalyticsReport)
async def get_campaign_analytics(id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    perf = AnalyticsService.get_campaign_performance(db, id)
    diagnostics = AnalyticsService.run_diagnostics(db, id)
    db_recs = db.query(OptimizationRecommendation).filter(OptimizationRecommendation.campaign_id == id).all()
    
    insights = []
    
    return {
        "performance": perf,
        "diagnostics": diagnostics,
        "insights": insights,
        "recommendations": [
            {
                "type": r.type,
                "description": r.description,
                "evidence": r.evidence or {}
            } for r in db_recs
        ]
    }

@router.post("/campaigns/{id}/analyze", response_model=CampaignAnalyticsReport)
async def analyze_campaign(id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    perf = AnalyticsService.get_campaign_performance(db, id)
    diagnostics = AnalyticsService.run_diagnostics(db, id)
    
    agent = AnalyticsAgent()
    agent_result = await agent.run(campaign.name, perf, diagnostics)
    
    for rec in agent_result["recommendations"]:
        db_rec = OptimizationRecommendation(
            campaign_id=id,
            type=rec.get("type", "GENERAL"),
            description=rec.get("description", ""),
            evidence=rec.get("evidence", {}),
            status="PENDING"
        )
        db.add(db_rec)
    db.commit()
    
    return {
        "performance": perf,
        "diagnostics": diagnostics,
        "insights": agent_result["insights"],
        "recommendations": agent_result["recommendations"]
    }
