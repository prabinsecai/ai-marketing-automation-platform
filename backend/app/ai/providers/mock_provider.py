import asyncio
import time
import json
import re
from typing import Optional, Type, TypeVar
from pydantic import BaseModel

from app.ai.base import BaseLLMProvider, LLMResult, TokenUsage
from app.schemas.strategy import AIStrategyOutput, ChannelStrategyItem, CampaignThemeItem, ContentRecommendationItem, MetricItem, RiskAssumptionItem
from app.schemas.content import (
    AIContentBatchOutput,
    AIEmailContentVariation,
    AISocialContentVariation,
    AIAdContentVariation,
    AIRegenerateEmailOutput,
    AIRegenerateSocialOutput,
    AIRegenerateAdOutput,
)

T = TypeVar("T", bound=BaseModel)


class MockLLMProvider(BaseLLMProvider):
    """
    High-fidelity Mock LLM Provider that synthesizes realistic, context-aware marketing
    intelligence and content without requiring third-party API keys or internet access.
    """

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def default_model(self) -> str:
        return "mock-marketing-agent-v1"

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Type[T],
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> LLMResult:
        start_time = time.time()
        # Realistic small processing delay
        await asyncio.sleep(0.08)

        used_model = model or self.default_model

        # Extract context clues from user_prompt
        product_name = self._extract_field(user_prompt, "Product(?: / SERVICE)?", "Product Name") or "AuraFlow Platform"
        category = self._extract_field(user_prompt, "Category") or "B2B SaaS Automation"
        audience = self._extract_field(user_prompt, "Audience Persona", "Target Persona") or "Growth Marketing Leaders"
        campaign_name = self._extract_field(user_prompt, "Campaign Name", "Campaign") or "Q3 Growth Initiative"
        objective = self._extract_field(user_prompt, "Objective") or "Pipeline Generation & Conversion"
        usp = self._extract_field(user_prompt, "USP", "Unique Selling Proposition (USP)") or f"The fastest way for {audience} to scale automated workflows"

        schema_name = response_schema.__name__

        if schema_name == "AIStrategyOutput":
            parsed_data = self._generate_strategy(product_name, category, audience, campaign_name, objective, usp)
        elif schema_name == "AIContentBatchOutput":
            parsed_data = self._generate_content_batch(product_name, audience, campaign_name, objective, usp)
        elif schema_name == "AIRegenerateEmailOutput":
            parsed_data = self._regenerate_email(product_name, audience, user_prompt)
        elif schema_name == "AIRegenerateSocialOutput":
            parsed_data = self._regenerate_social(product_name, audience, user_prompt)
        elif schema_name == "AIRegenerateAdOutput":
            parsed_data = self._regenerate_ad(product_name, audience, user_prompt)
        else:
            # Fallback for unexpected schema
            try:
                parsed_data = response_schema()
            except Exception:
                raise ValueError(f"MockProvider does not support generating schema '{schema_name}' automatically.")

        raw_json = json.dumps(parsed_data.model_dump(), indent=2)
        latency_ms = int((time.time() - start_time) * 1000)

        # Estimate realistic token counts
        prompt_tokens = max(120, len(user_prompt) // 4)
        completion_tokens = max(200, len(raw_json) // 4)

        return LLMResult(
            parsed=parsed_data,
            raw_response=raw_json,
            model=used_model,
            provider=self.provider_name,
            latency_ms=latency_ms,
            usage=TokenUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            ),
        )

    def _extract_field(self, text: str, *field_names: str) -> Optional[str]:
        for name in field_names:
            match = re.search(rf"-?\s*{name}\s*:\s*(.+)", text, re.IGNORECASE)
            if match:
                val = match.group(1).strip()
                if val and val != "None" and not val.startswith("{"):
                    return val
        return None

    def _generate_strategy(
        self,
        product: str,
        category: str,
        audience: str,
        campaign: str,
        objective: str,
        usp: str,
    ) -> AIStrategyOutput:
        return AIStrategyOutput(
            summary=(
                f"The '{campaign}' initiative positions {product} as the premier {category} solution for {audience}. "
                f"By focusing heavily on tangible efficiency gains and seamless workflow intelligence, this campaign directly addresses the friction of manual orchestration and accelerates qualified pipeline generation."
            ),
            audience_reasoning=(
                f"{audience} are currently pressured by rising operational overhead and demand for measurable ROI. "
                f"They respond best to peer-backed validation, concrete architectural differentiation, and direct demonstration of {usp}."
            ),
            positioning=(
                f"For {audience} seeking enterprise agility, {product} delivers turnkey marketing automation with provable governance, unlike traditional fragmented toolchains."
            ),
            key_message=(
                f"Eliminate campaign friction and unlock 4x marketing velocity with {product}."
            ),
            channel_strategy=[
                ChannelStrategyItem(
                    channel="Email Nurture",
                    priority="Primary",
                    rationale=f"Directly delivers targeted value-first teardowns and workflow templates into the inbox of {audience}.",
                    tactics=[
                        "3-part personalized problem-resolution sequence",
                        "Executive briefing newsletter blast",
                        "Post-webinar conversion trigger sequence",
                    ],
                ),
                ChannelStrategyItem(
                    channel="LinkedIn & Professional Social",
                    priority="Primary",
                    rationale="High concentration of B2B decision makers seeking thought leadership and workflow optimization benchmarks.",
                    tactics=[
                        "Founder/Product deep dive threads on automation bottlenecks",
                        "Interactive poll-based engagement posts",
                        "Video walkthrough clips showing 3-minute campaign setups",
                    ],
                ),
                ChannelStrategyItem(
                    channel="Paid Search & Targeted Ads",
                    priority="Secondary",
                    rationale="Captures high-intent search traffic evaluating marketing automation alternatives.",
                    tactics=[
                        "High-intent exact match keywords targeting pain points",
                        "Retargeting sponsored content on LinkedIn with customer outcome proof",
                    ],
                ),
            ],
            campaign_themes=[
                CampaignThemeItem(
                    theme="Efficiency & Velocity",
                    hook=f"Why high-growth marketing teams are replacing manual workflows with {product}.",
                    description="Emphasizes reduction in campaign launch cycle from 2 weeks to 2 hours.",
                ),
                CampaignThemeItem(
                    theme="Data & Accuracy",
                    hook="Zero hallucination, 100% brand consistency across every channel.",
                    description="Highlights governed AI frameworks and strict compliance with brand guidelines.",
                ),
                CampaignThemeItem(
                    theme="Revenue Attribution",
                    hook="Stop guessing which campaign drove the closed-won deal.",
                    description="Focuses on end-to-end campaign intelligence and clear pipeline attribution.",
                ),
            ],
            content_recommendations=[
                ContentRecommendationItem(
                    channel="Email",
                    asset_type="Nurture Playbook Sequence",
                    objective="Nurture top-of-funnel prospects to interactive demo registration",
                    best_practices=["Keep subject under 45 chars", "Single clear CTA", "Include 3 bullet ROI proof"],
                ),
                ContentRecommendationItem(
                    channel="LinkedIn",
                    asset_type="Architectural Teardown Post",
                    objective="Establish category authority and drive website traffic",
                    best_practices=["Open with counter-intuitive stat", "Format with readable whitespace"],
                ),
                ContentRecommendationItem(
                    channel="Meta / Google Ads",
                    asset_type="Direct-Response Value Ad",
                    objective="Capture demo requests with low CAC",
                    best_practices=["Clear value proposition in headline", "Use strong action CTA"],
                ),
            ],
            cta_strategy=(
                "Two-tier CTA ladder: Low friction top-of-funnel CTA ('Explore the Interactive Tour') progressing to high-intent bottom-of-funnel CTA ('Schedule Strategic Architecture Session')."
            ),
            timeline_suggestion=(
                "Week 1: Asset staging, persona segmentation & audience warming on LinkedIn. "
                "Weeks 2-3: Core launch of multi-touch email sequence & targeted paid search ads. "
                "Week 4: Retargeting push, case study highlights, and demo acceleration sprints."
            ),
            future_success_metrics=[
                MetricItem(
                    metric="Qualified Demo Request Rate",
                    rationale="Direct indicator of message-market resonance among key decision makers.",
                    target_benchmark="3.8% - 5.2% conversion rate on landing page visits",
                ),
                MetricItem(
                    metric="Email Open & Click-to-Open (CTOR)",
                    rationale="Validates email subject line appeal and body CTA engagement.",
                    target_benchmark="42%+ Open Rate, 18%+ CTOR",
                ),
                MetricItem(
                    metric="Social Engagement & Share of Voice",
                    rationale="Measures brand footprint and peer sharing in target community.",
                    target_benchmark="2.5x increase in qualified social impressions",
                ),
            ],
            risks_assumptions=[
                RiskAssumptionItem(
                    risk="Audience fatigue due to repetitive marketing automation messaging in the market.",
                    mitigation=f"Lead with concrete workflow demonstrations and verifiable {product} differentiation rather than generic claims.",
                ),
                RiskAssumptionItem(
                    risk="Longer enterprise sales cycles delaying immediate conversion metrics.",
                    mitigation="Implement interactive self-serve tours alongside enterprise demo booking options.",
                ),
            ],
        )

    def _generate_content_batch(
        self,
        product: str,
        audience: str,
        campaign: str,
        objective: str,
        usp: str,
    ) -> AIContentBatchOutput:
        return AIContentBatchOutput(
            email_variations=[
                AIEmailContentVariation(
                    variation_number=1,
                    subject=f"Tired of campaign bottlenecks? Meet {product}",
                    preview_text=f"How modern {audience} are cutting campaign cycle times by 75%.",
                    body=(
                        f"Hi {{FirstName}},\n\n"
                        f"If you're like most marketing leaders, your team spends 70% of their week wrestling with fragmented tools and manual campaign copy reviews instead of executing high-leverage strategy.\n\n"
                        f"That's exactly why we built {product}.\n\n"
                        f"With {product}, you can:\n"
                        f"• Formulate verified, audience-aligned campaign strategies in minutes\n"
                        f"• Generate multi-channel copy across Email, Social, and Ads that strictly adheres to your brand guidelines\n"
                        f"• Streamline team approvals with audit-ready workflows\n\n"
                        f"Ready to see how {product} eliminates friction for your growth team?\n\n"
                        f"Best regards,\nThe {product} Team"
                    ),
                    cta="Explore the Interactive Demo",
                ),
                AIEmailContentVariation(
                    variation_number=2,
                    subject=f"The playbook {audience} are using to 4x marketing velocity",
                    preview_text="A faster, verified approach to campaign intelligence.",
                    body=(
                        f"Hi {{FirstName}},\n\n"
                        f"Scaling multi-channel campaigns without burning out your team usually requires hiring an army of contractors or sacrificing copy consistency.\n\n"
                        f"{product} changes that equation. Powered by purpose-built AI marketing intelligence, it turns your product positioning and audience data into ready-to-publish campaign assets in seconds.\n\n"
                        f"Key capabilities:\n"
                        f"1. Precision Campaign Strategy generation\n"
                        f"2. Multi-format asset creation with zero hallucinations\n"
                        f"3. Centralized review & approval queue for enterprise governance\n\n"
                        f"Let's walk you through a tailored 10-minute preview for your brand."
                    ),
                    cta="Schedule a 10-Min Walkthrough",
                ),
            ],
            social_variations=[
                AISocialContentVariation(
                    variation_number=1,
                    platform="LinkedIn",
                    hook=f"Most marketing teams don't have a talent shortage—they have an orchestration bottleneck. 🧵",
                    caption=(
                        f"We spent months analyzing how {audience} build and deploy multi-channel campaigns.\n\n"
                        f"The average time from concept to live campaign? 14 days.\n"
                        f"The breakdown:\n"
                        f"- 4 days drafting briefs\n"
                        f"- 6 days waiting on copy revisions\n"
                        f"- 4 days circulating email threads for stakeholder approval\n\n"
                        f"We built {product} to collapse this entire loop down to under an hour—with strict brand governance and zero unsupported claims.\n\n"
                        f"How is your team modernizing its campaign workflow this quarter?"
                    ),
                    cta="Check out the full workflow teardown in the comments 👇",
                    hashtags=["B2BMarketing", "MarketingAutomation", "GrowthStrategy", "MarTech"],
                ),
                AISocialContentVariation(
                    variation_number=2,
                    platform="Twitter / X",
                    hook=f"Why modern {audience} are ditching disconnected marketing stacks for unified campaign intelligence:",
                    caption=(
                        f"1/ Campaign drafting shouldn't require 12 open browser tabs.\n\n"
                        f"2/ With {product}, your brand guidelines, product specs, and audience personas live in one unified brain.\n\n"
                        f"3/ Strategy -> Multi-channel copy -> Stakeholder review in minutes.\n\n"
                        f"Experience the speed of automated campaign intelligence."
                    ),
                    cta="Try the interactive tour: link in bio 🚀",
                    hashtags=["MarTech", "SaaSGrowth", "AIAutomation", "MarketingOps"],
                ),
                AISocialContentVariation(
                    variation_number=3,
                    platform="LinkedIn",
                    hook="What if your marketing campaigns practically orchestrated themselves with 100% brand consistency?",
                    caption=(
                        f"When building {product}, our core design principle was simple: AI should amplify strategic intelligence, not spam the internet with generic copy.\n\n"
                        f"Here is how {product} keeps your team in full control:\n"
                        f"✅ Context-grounded strategist agent\n"
                        f"✅ Multi-channel copy variations (Email, Social, Paid Search)\n"
                        f"✅ Role-based review and instant regeneration controls\n\n"
                        f"See how fast your next product launch can go live."
                    ),
                    cta="Book a personalized live architecture demo today.",
                    hashtags=["MarketingLeadership", "B2BSaaS", "CampaignStrategy"],
                ),
            ],
            ad_variations=[
                AIAdContentVariation(
                    variation_number=1,
                    platform="Google Search Ads",
                    headline=f"Automate Marketing with {product}",
                    primary_text=f"Generate verified campaign strategies and multi-channel copy in minutes. Designed specifically for {audience}.",
                    cta="Start Free Trial",
                ),
                AIAdContentVariation(
                    variation_number=2,
                    platform="LinkedIn Sponsored Ad",
                    headline="From Brief to Live Campaign in 1 Hour",
                    primary_text=f"Stop wasting weeks on copy rounds and fragmented tools. {product} delivers AI campaign strategy & copy with enterprise review workflows.",
                    cta="Get the Playbook",
                ),
                AIAdContentVariation(
                    variation_number=3,
                    platform="Meta / Facebook Ads",
                    headline="Scale Your B2B Marketing Velocity",
                    primary_text=f"Built for modern marketing teams. Generate, review, and approve high-converting Email, Social & Ad campaigns with {product}.",
                    cta="Book a Demo",
                ),
            ],
        )

    def _regenerate_email(self, product: str, audience: str, user_prompt: str) -> AIRegenerateEmailOutput:
        return AIRegenerateEmailOutput(
            subject=f"Accelerate your campaign pipeline with {product}",
            preview_text=f"Refined insights and faster execution for {audience}.",
            body=(
                f"Hi {{FirstName}},\n\n"
                f"We updated our recommendations specifically based on your latest focus.\n\n"
                f"{product} removes the guesswork from your marketing strategy. "
                f"By unifying your product positioning with direct audience insights, you get high-converting copy across Email, LinkedIn, and Paid Ads with zero friction.\n\n"
                f"Here is why leading teams trust {product}:\n"
                f"• Verified copy grounded strictly in your product truth\n"
                f"• Instant variation controls with built-in audit trails\n"
                f"• Accelerated time-to-market for every campaign\n\n"
                f"Let's get your next campaign live today."
            ),
            cta="Explore the Live Workspace",
        )

    def _regenerate_social(self, product: str, audience: str, user_prompt: str) -> AIRegenerateSocialOutput:
        return AIRegenerateSocialOutput(
            platform="LinkedIn",
            hook=f"The secret to scaling B2B marketing isn't more headcount—it's smarter campaign intelligence with {product}.",
            caption=(
                f"Every marketing leader knows the pain of slow campaign rollouts.\n\n"
                f"With {product}, {audience} are turning raw product briefs into full multi-channel campaigns (Email, Social, Ads) in under 60 minutes.\n\n"
                f"No generic fluff. No hallucinated stats. Just precision marketing assets with built-in review gates.\n\n"
                f"Are you ready to modernize your marketing ops?"
            ),
            cta="See the interactive walkthrough below 👇",
            hashtags=["B2BMarketing", "MarTech", "SaaSVelocity", "MarketingOps"],
        )

    def _regenerate_ad(self, product: str, audience: str, user_prompt: str) -> AIRegenerateAdOutput:
        return AIRegenerateAdOutput(
            headline=f"Supercharge Marketing with {product}",
            primary_text=f"Generate multi-channel B2B campaigns in minutes with built-in review and audit workflows. Trusted by {audience}.",
            cta="Try It Free",
        )
