import json
import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.ai.base import LLMResult
from app.ai.factory import get_llm_provider
from app.ai.prompts.strategy_prompts import STRATEGY_SYSTEM_PROMPT, STRATEGY_USER_PROMPT_TEMPLATE
from app.models.ai_log import AILog
from app.models.campaign import Campaign
from app.models.workspace import Workspace
from app.models.product import Product
from app.models.audience import Audience
from app.schemas.strategy import AIStrategyOutput

logger = logging.getLogger("app.ai.strategist")


class MarketingStrategist:
    def __init__(self, provider_mode: Optional[str] = None):
        self.provider = get_llm_provider(provider_mode)

    async def generate_strategy(
        self,
        db: Session,
        campaign: Campaign,
        workspace: Workspace,
        product: Optional[Product] = None,
        audience: Optional[Audience] = None,
    ) -> LLMResult:
        # Assemble context
        product_name = product.name if product else "Core B2B Offering"
        product_category = product.category if product else "Enterprise Platform"
        product_description = product.description if product else "Comprehensive business acceleration platform"
        product_price = product.price if product else "Custom Enterprise Pricing"
        product_features = ", ".join(product.features) if product and product.features else "Automated campaign orchestration, intelligent multi-channel analytics"
        product_benefits = ", ".join(product.target_benefits) if product and product.target_benefits else "Reduced campaign lead time, higher conversion velocity"
        product_usp = product.usp if product and product.usp else "Unified intelligence with enterprise review governance"
        product_url = product.url if product and product.url else workspace.website or "https://example.com"

        audience_name = audience.name if audience else "B2B Marketing & Growth Decision Makers"
        audience_desc = audience.description if audience else "VP of Marketing, CMOs, and Marketing Directors"
        audience_demographics = json.dumps(audience.demographics) if audience and audience.demographics else "Mid-Market to Enterprise B2B SaaS"
        audience_pain_points = ", ".join(audience.pain_points) if audience and audience.pain_points else "Fragmented toolchains, slow copywriting cycles, disjointed multi-channel attribution"
        audience_goals = ", ".join(audience.goals) if audience and audience.goals else "Accelerate qualified pipeline, maintain unified brand voice"
        audience_interests = ", ".join(audience.interests) if audience and audience.interests else "MarTech, SaaS scaling, automation frameworks"
        audience_channels = ", ".join(audience.preferred_channels) if audience and audience.preferred_channels else "Email, LinkedIn, Google Search"

        user_prompt = STRATEGY_USER_PROMPT_TEMPLATE.format(
            workspace_name=workspace.name,
            workspace_industry=workspace.industry or "B2B Software & Services",
            workspace_website=workspace.website or "https://example.com",
            brand_guidelines=workspace.brand_guidelines or "Professional, authoritative, high-impact, transparent",
            product_name=product_name,
            product_category=product_category,
            product_description=product_description,
            product_price=product_price,
            product_features=product_features,
            product_benefits=product_benefits,
            product_usp=product_usp,
            product_url=product_url,
            audience_name=audience_name,
            audience_description=audience_desc,
            audience_demographics=audience_demographics,
            audience_pain_points=audience_pain_points,
            audience_goals=audience_goals,
            audience_interests=audience_interests,
            audience_channels=audience_channels,
            campaign_name=campaign.name,
            campaign_objective=campaign.objective,
            campaign_budget=campaign.budget or "Flexible / Standard Allocation",
            campaign_timeline=campaign.target_timeline or "4-week multi-touch sprint",
            campaign_description=campaign.description or "High-priority strategic growth initiative",
        )

        try:
            result = await self.provider.generate_structured(
                system_prompt=STRATEGY_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_schema=AIStrategyOutput,
            )

            # Record AI Execution Log
            log_entry = AILog(
                workspace_id=workspace.id,
                campaign_id=campaign.id,
                agent_name="MarketingStrategist",
                provider=result.provider,
                model=result.model,
                prompt_template="STRATEGY_USER_PROMPT_TEMPLATE",
                prompt_preview=user_prompt[:500] + "...",
                response_preview=result.raw_response[:500] + "...",
                prompt_tokens=result.usage.prompt_tokens,
                completion_tokens=result.usage.completion_tokens,
                total_tokens=result.usage.total_tokens,
                latency_ms=result.latency_ms,
                status="SUCCESS",
            )
            db.add(log_entry)
            db.commit()

            return result

        except Exception as e:
            logger.error(f"Strategy generation failed: {e}", exc_info=True)
            # Record failed log
            log_entry = AILog(
                workspace_id=workspace.id,
                campaign_id=campaign.id,
                agent_name="MarketingStrategist",
                provider=self.provider.provider_name,
                model=self.provider.default_model,
                prompt_template="STRATEGY_USER_PROMPT_TEMPLATE",
                prompt_preview=user_prompt[:500] + "...",
                response_preview="",
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                latency_ms=0,
                status="FAILED",
                error_message=str(e),
            )
            db.add(log_entry)
            db.commit()
            raise e
