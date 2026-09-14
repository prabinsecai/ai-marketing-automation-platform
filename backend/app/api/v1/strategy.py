from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.campaign import Campaign, CampaignStatus
from app.models.strategy import CampaignStrategy
from app.schemas.strategy import StrategyResponse
from app.ai.agents.strategist import MarketingStrategist

router = APIRouter(prefix="/campaigns/{campaign_id}/strategy", tags=["AI Strategy"])


@router.get("", response_model=StrategyResponse)
def get_campaign_strategy(campaign_id: str, db: Session = Depends(get_db)):
    strategy = db.query(CampaignStrategy).filter(CampaignStrategy.campaign_id == campaign_id).first()
    if not strategy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found for this campaign")
    return strategy


@router.post("/generate", response_model=StrategyResponse, status_code=status.HTTP_200_OK)
async def generate_campaign_strategy(campaign_id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

    workspace = campaign.workspace
    if not workspace:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Workspace not associated with campaign")

    strategist = MarketingStrategist()

    try:
        result = await strategist.generate_strategy(
            db=db,
            campaign=campaign,
            workspace=workspace,
            product=campaign.product,
            audience=campaign.audience,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate strategy: {str(e)}"
        )

    data = result.parsed

    # Upsert strategy
    strategy = db.query(CampaignStrategy).filter(CampaignStrategy.campaign_id == campaign_id).first()
    if not strategy:
        strategy = CampaignStrategy(campaign_id=campaign_id)
        db.add(strategy)

    strategy.summary = data.summary
    strategy.audience_reasoning = data.audience_reasoning
    strategy.positioning = data.positioning
    strategy.key_message = data.key_message
    strategy.channel_strategy = [item.model_dump() for item in data.channel_strategy]
    strategy.campaign_themes = [item.model_dump() for item in data.campaign_themes]
    strategy.content_recommendations = [item.model_dump() for item in data.content_recommendations]
    strategy.cta_strategy = data.cta_strategy
    strategy.timeline_suggestion = data.timeline_suggestion
    strategy.future_success_metrics = [item.model_dump() for item in data.future_success_metrics]
    strategy.risks_assumptions = [item.model_dump() for item in data.risks_assumptions]
    strategy.raw_response = result.raw_response
    strategy.model_used = result.model

    # Advance campaign status if still in DRAFT
    if campaign.status == CampaignStatus.DRAFT:
        campaign.status = CampaignStatus.STRATEGY_GENERATED

    db.commit()
    db.refresh(strategy)
    return strategy
