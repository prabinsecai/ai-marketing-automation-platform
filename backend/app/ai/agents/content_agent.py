import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.ai.base import LLMResult
from app.ai.factory import get_llm_provider
from app.ai.prompts.content_prompts import (
    CONTENT_SYSTEM_PROMPT,
    CONTENT_USER_PROMPT_TEMPLATE,
    REGENERATE_VARIATION_PROMPT,
)
from app.models.ai_log import AILog
from app.models.campaign import Campaign
from app.models.content import ContentAsset, ContentChannel
from app.models.product import Product
from app.models.audience import Audience
from app.models.strategy import CampaignStrategy
from app.models.workspace import Workspace
from app.schemas.content import (
    AIContentBatchOutput,
    AIRegenerateEmailOutput,
    AIRegenerateSocialOutput,
    AIRegenerateAdOutput,
)

logger = logging.getLogger("app.ai.content_agent")


class ContentAgent:
    def __init__(self, provider_mode: Optional[str] = None):
        self.provider = get_llm_provider(provider_mode)

    async def generate_batch_content(
        self,
        db: Session,
        campaign: Campaign,
        workspace: Workspace,
        strategy: Optional[CampaignStrategy] = None,
        product: Optional[Product] = None,
        audience: Optional[Audience] = None,
    ) -> LLMResult:
        product_name = product.name if product else "Core B2B Product"
        product_category = product.category if product else "Software Solution"
        product_description = product.description if product else "Intelligent enterprise workflow automation"
        product_usp = product.usp if product and product.usp else "Unified campaign lifecycle automation with governed outputs"
        product_features = ", ".join(product.features) if product and product.features else "Automated workflows, real-time intelligence, multi-channel copy"
        product_benefits = ", ".join(product.target_benefits) if product and product.target_benefits else "Reduced campaign lead time, accelerated pipeline velocity"

        audience_name = audience.name if audience else "B2B Marketing & Growth Decision Makers"
        audience_pain_points = ", ".join(audience.pain_points) if audience and audience.pain_points else "Slow campaign rollouts, disjointed messaging, manual review overhead"
        audience_goals = ", ".join(audience.goals) if audience and audience.goals else "Scale high-converting multi-channel campaigns with minimal friction"

        strategy_positioning = strategy.positioning if strategy else f"Enterprise-grade marketing intelligence for {audience_name}"
        strategy_key_message = strategy.key_message if strategy else f"Accelerate marketing velocity and conversions with {product_name}"
        strategy_cta = strategy.cta_strategy if strategy else "Direct demo booking and interactive walkthrough"

        user_prompt = CONTENT_USER_PROMPT_TEMPLATE.format(
            workspace_name=workspace.name,
            brand_guidelines=workspace.brand_guidelines or "Professional, authoritative, high-impact, transparent",
            product_name=product_name,
            product_category=product_category,
            product_description=product_description,
            product_usp=product_usp,
            product_features=product_features,
            product_benefits=product_benefits,
            audience_name=audience_name,
            audience_pain_points=audience_pain_points,
            audience_goals=audience_goals,
            campaign_name=campaign.name,
            campaign_objective=campaign.objective,
            strategy_positioning=strategy_positioning,
            strategy_key_message=strategy_key_message,
            strategy_cta=strategy_cta,
        )

        try:
            result = await self.provider.generate_structured(
                system_prompt=CONTENT_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_schema=AIContentBatchOutput,
            )

            # Record AI Execution Log
            log_entry = AILog(
                workspace_id=workspace.id,
                campaign_id=campaign.id,
                agent_name="ContentAgent",
                provider=result.provider,
                model=result.model,
                prompt_template="CONTENT_USER_PROMPT_TEMPLATE",
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
            logger.error(f"Content batch generation failed: {e}", exc_info=True)
            log_entry = AILog(
                workspace_id=workspace.id,
                campaign_id=campaign.id,
                agent_name="ContentAgent",
                provider=self.provider.provider_name,
                model=self.provider.default_model,
                prompt_template="CONTENT_USER_PROMPT_TEMPLATE",
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

    async def regenerate_variation(
        self,
        db: Session,
        asset: ContentAsset,
        campaign: Campaign,
        workspace: Workspace,
        instructions: Optional[str] = None,
        product: Optional[Product] = None,
        audience: Optional[Audience] = None,
    ) -> LLMResult:
        product_name = product.name if product else "Core B2B Product"
        product_description = product.description if product else "Intelligent enterprise workflow automation"
        product_usp = product.usp if product and product.usp else "Turnkey marketing automation"
        audience_name = audience.name if audience else "B2B Decision Makers"

        user_prompt = REGENERATE_VARIATION_PROMPT.format(
            channel=asset.channel,
            variation_number=asset.variation_number,
            product_name=product_name,
            product_description=product_description,
            product_usp=product_usp,
            audience_name=audience_name,
            campaign_objective=campaign.objective,
            previous_title=asset.title or "",
            previous_body=asset.body or "",
            previous_cta=asset.cta or "",
            feedback_instructions=instructions or "Refine tone, enhance conversion focus, and sharpen the value proposition.",
        )

        schema_map = {
            ContentChannel.EMAIL: AIRegenerateEmailOutput,
            ContentChannel.SOCIAL: AIRegenerateSocialOutput,
            ContentChannel.ADVERTISEMENT: AIRegenerateAdOutput,
        }
        target_schema = schema_map.get(asset.channel, AIRegenerateEmailOutput)

        try:
            result = await self.provider.generate_structured(
                system_prompt=CONTENT_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_schema=target_schema,
            )

            # Record AI Execution Log
            log_entry = AILog(
                workspace_id=workspace.id,
                campaign_id=campaign.id,
                agent_name="ContentAgent (Regeneration)",
                provider=result.provider,
                model=result.model,
                prompt_template="REGENERATE_VARIATION_PROMPT",
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
            logger.error(f"Single variation regeneration failed: {e}", exc_info=True)
            log_entry = AILog(
                workspace_id=workspace.id,
                campaign_id=campaign.id,
                agent_name="ContentAgent (Regeneration)",
                provider=self.provider.provider_name,
                model=self.provider.default_model,
                prompt_template="REGENERATE_VARIATION_PROMPT",
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
