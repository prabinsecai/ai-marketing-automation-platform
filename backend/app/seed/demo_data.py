import json
import logging
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.models.user import User
from app.models.product import Product
from app.models.audience import Audience
from app.models.campaign import Campaign, CampaignStatus
from app.models.strategy import CampaignStrategy
from app.models.content import ContentAsset, ContentChannel, ContentStatus
from app.models.approval import Approval, ApprovalAction
from app.models.ai_log import AILog

logger = logging.getLogger("app.seed")


def seed_demo_data(db: Session) -> Workspace:
    """
    Seeds a rich, realistic B2B e-commerce platform workspace with products,
    audiences, campaigns across multiple workflow stages, content assets, approvals, and AI execution logs.
    """
    # Check if demo workspace already exists
    existing = db.query(Workspace).filter(Workspace.slug == "auraflow-commerce").first()
    if existing:
        return existing

    logger.info("Seeding realistic B2B SaaS demo data...")

    # 1. Create Workspace
    workspace = Workspace(
        name="AuraFlow Commerce AI",
        slug="auraflow-commerce",
        industry="B2B E-Commerce & Retail Tech",
        website="https://auraflow.io",
        description="Next-generation intelligent commerce orchestration platform helping retailers automate omnichannel merchandising and personalized buyer journeys.",
        brand_guidelines="Tone: Authoritative, energetic, data-driven, and enterprise-friendly. Avoid hype words. Always emphasize speed, ROI, and governed AI automation.",
    )
    db.add(workspace)
    db.flush()

    # 2. Create Users
    user_admin = User(
        workspace_id=workspace.id,
        email="sarah.jenkins@auraflow.io",
        full_name="Sarah Jenkins",
        role="admin",
    )
    user_reviewer = User(
        workspace_id=workspace.id,
        email="marcus.vance@auraflow.io",
        full_name="Marcus Vance",
        role="reviewer",
    )
    db.add_all([user_admin, user_reviewer])
    db.flush()

    # 3. Create Products
    prod_1 = Product(
        workspace_id=workspace.id,
        name="AuraFlow Omnichannel Commerce Engine",
        category="Commerce Orchestration",
        description="Enterprise platform unifying inventory feeds, headless storefronts, and automated campaign triggering across all customer touchpoints.",
        price="$1,499 / month",
        features=[
            "Unified catalog & multi-warehouse inventory sync",
            "Real-time event streaming & cart abandonment triggers",
            "Headless API connector for Shopify Plus, BigCommerce, and custom ERPs",
            "AI-powered multi-channel product recommendation engine",
        ],
        target_benefits=[
            "70% faster campaign launch speed across email, social, and web",
            "3.2x increase in repeat purchase rates via personalized recommendations",
            "Zero downtime during seasonal peak traffic surges",
        ],
        usp="The only headless commerce intelligence platform that unifies real-time inventory triggers with governed AI copy generation.",
        url="https://auraflow.io/omnichannel-engine",
    )

    prod_2 = Product(
        workspace_id=workspace.id,
        name="Nexus Dynamic Personalizer",
        category="Conversion Rate Optimization",
        description="Self-optimizing merchandising widget and real-time banner personalization engine for fast-growing D2C & B2B ecommerce sites.",
        price="$799 / month",
        features=[
            "1-click integration with major ecommerce platforms",
            "Predictive dynamic intent scoring",
            "Automated A/B copy and layout variation testing",
        ],
        target_benefits=[
            "18% average lift in store-wide conversion rates",
            "Reduces merchandise setup time from days to minutes",
        ],
        usp="Instant on-site personalization that adapts within 200 milliseconds of visitor interaction.",
        url="https://auraflow.io/nexus-personalizer",
    )
    db.add_all([prod_1, prod_2])
    db.flush()

    # 4. Create Audiences
    aud_1 = Audience(
        workspace_id=workspace.id,
        name="Mid-Market E-commerce VP & Directors",
        description="Senior e-commerce and digital growth leaders at brands generating $10M-$100M annual GMV.",
        demographics={
            "job_titles": ["VP of Ecommerce", "Director of Digital Marketing", "Head of Growth"],
            "company_size": "50-500 employees",
            "annual_gmv": "$10M - $100M",
            "location": "North America & Western Europe",
        },
        pain_points=[
            "Siloed customer data across disparate marketing tools",
            "High customer acquisition costs (CAC) eroding store margins",
            "Engineering bottlenecks whenever marketing wants to launch new promotional landing pages",
            "Slow manual copywriting and review cycles for multi-channel sales",
        ],
        interests=[
            "Omnichannel commerce",
            "Headless architectures",
            "Automated merchandising",
            "MarTech consolidation",
        ],
        goals=[
            "Scale revenue efficiently without doubling marketing headcount",
            "Automate cross-channel campaign deployment",
            "Achieve measurable ROAS and pipeline predictability",
        ],
        preferred_channels=["Email", "LinkedIn", "Google Search", "B2B Webinars"],
    )

    aud_2 = Audience(
        workspace_id=workspace.id,
        name="D2C Performance Marketing Leads",
        description="Hands-on growth marketers managing paid ad budgets and lifecycle email nurture funnels.",
        demographics={
            "job_titles": ["Performance Marketing Manager", "Growth Lead", "Lifecycle Marketing Specialist"],
            "company_size": "20-200 employees",
            "location": "Global",
        },
        pain_points=[
            "Ad fatigue requiring constant creative and copy refreshing",
            "Low email click-through rates on generic promotion blasts",
            "Lack of real-time inventory data in active ad campaigns",
        ],
        interests=["Meta Ads", "Google Performance Max", "Klaviyo workflows", "Creative optimization"],
        goals=["Improve ROAS by 30%", "Accelerate weekly creative velocity", "Eliminate out-of-stock ad spend waste"],
        preferred_channels=["Meta Ads", "LinkedIn", "Twitter/X", "Email"],
    )
    db.add_all([aud_1, aud_2])
    db.flush()

    # 5. Create Campaign 1: Fully generated and in Review
    camp_1 = Campaign(
        workspace_id=workspace.id,
        product_id=prod_1.id,
        audience_id=aud_1.id,
        name="Q3 Omnichannel Velocity Sprint",
        description="Flagship promotional push targeting mid-market e-commerce directors to demonstrate how AuraFlow collapses campaign setup time and scales omnichannel revenue.",
        objective="Lead Generation & Product Demo Bookings",
        status=CampaignStatus.IN_REVIEW,
        budget="$25,000",
        target_timeline="6-Week Campaign Sprint (Q3)",
    )
    db.add(camp_1)
    db.flush()

    # Strategy for Campaign 1
    strat_1 = CampaignStrategy(
        campaign_id=camp_1.id,
        summary="Strategic multi-touch sprint positioning AuraFlow Omnichannel Engine as the critical infrastructure for $10M-$100M ecommerce brands suffering from disconnected toolchains.",
        audience_reasoning="Mid-Market Ecommerce Directors are under severe pressure to protect profit margins and accelerate campaign speed. Demonstrating 70% faster setup and instant inventory sync directly alleviates their primary daily bottlenecks.",
        positioning="AuraFlow is the unified commerce orchestration platform that bridges real-time inventory feeds with governed automated campaign execution.",
        key_message="Stop wasting 14 days launching campaigns. Turn inventory signals into high-converting multi-channel campaigns in under an hour.",
        channel_strategy=[
            {
                "channel": "Lifecycle Email Nurture",
                "priority": "Primary",
                "rationale": "High conversion channel for qualified opt-ins and webinar attendees.",
                "tactics": ["3-part teardown sequence", "Executive ROI calculator preview"],
            },
            {
                "channel": "LinkedIn Thought Leadership & Ads",
                "priority": "Primary",
                "rationale": "Directly reaches Ecommerce VPs actively searching for automation solutions.",
                "tactics": ["Sponsored content case studies", "Interactive benchmark polls"],
            },
            {
                "channel": "Google Search & Intent Ads",
                "priority": "Secondary",
                "rationale": "Captures active buyers searching for headless commerce and omnichannel automation.",
                "tactics": ["High-intent search terms", "Retargeting display banners"],
            },
        ],
        campaign_themes=[
            {
                "theme": "Campaign Velocity vs Toolchain Fatigue",
                "hook": "Why leading ecommerce brands are abandoning 12-tool marketing stacks.",
                "description": "Exposes the hidden operational cost of manual campaign orchestration.",
            },
            {
                "theme": "Real-Time Inventory Intelligence",
                "hook": "Never advertise an out-of-stock SKU again.",
                "description": "Highlights automated catalog feeds directly synchronizing with ad creative.",
            },
        ],
        content_recommendations=[
            {
                "channel": "Email",
                "asset_type": "Executive Problem-Resolution Sequence",
                "objective": "Drive 10-minute demo bookings",
                "best_practices": ["Clear value bullet points", "Social proof quote", "Single focused CTA"],
            },
            {
                "channel": "LinkedIn",
                "asset_type": "Data-backed Architectural Breakdown",
                "objective": "Build category authority and drive website visits",
                "best_practices": ["Use provocative opening hook", "Include checklist graphic suggestion"],
            },
        ],
        cta_strategy="Primary CTA: 'Book an Interactive Architecture Walkthrough'. Secondary CTA: 'Calculate Your Campaign Velocity Score'.",
        timeline_suggestion="Week 1-2: Persona warming on LinkedIn. Week 3-4: Email sequence launch and paid search activation. Week 5-6: Retargeting sprint and demo acceleration.",
        future_success_metrics=[
            {"metric": "Qualified Demo Bookings", "rationale": "Core pipeline conversion KPI", "target_benchmark": "45+ booked demos"},
            {"metric": "Email CTOR (Click-to-Open)", "rationale": "Measures message resonance", "target_benchmark": "22%+"},
            {"metric": "LinkedIn CTR", "rationale": "Measures creative engagement", "target_benchmark": "1.8%+"},
        ],
        risks_assumptions=[
            {"risk": "Prospects assume headless setup requires heavy engineering resources", "mitigation": "Highlight turnkey 1-click connectors for Shopify Plus and BigCommerce."},
        ],
        model_used="mock-marketing-agent-v1",
    )
    db.add(strat_1)
    db.flush()

    # Content Assets for Campaign 1
    asset_email_1 = ContentAsset(
        campaign_id=camp_1.id,
        channel=ContentChannel.EMAIL,
        variation_number=1,
        title="Tired of 14-day campaign launch cycles? Meet AuraFlow",
        preview_text="How mid-market ecommerce brands cut setup time by 70%.",
        body=(
            "Hi {{FirstName}},\n\n"
            "If your marketing and merchandising teams are spending 20+ hours a week exporting CSVs, manually rebuilding promo banners, and chasing copy approvals, you're not alone.\n\n"
            "We built the AuraFlow Omnichannel Engine to fix this exact bottleneck.\n\n"
            "With AuraFlow:\n"
            "• Unified catalog feeds automatically trigger multi-channel copy\n"
            "• Built-in brand guidelines prevent off-brand hallucinations\n"
            "• Stakeholder review and approval queues keep everyone aligned\n\n"
            "See how high-growth retailers are launching campaigns in minutes rather than weeks.\n\n"
            "Best,\nSarah Jenkins\nDirector of Growth, AuraFlow"
        ),
        cta="Book a 10-Min Architecture Demo",
        status=ContentStatus.IN_REVIEW,
        is_selected=True,
        model_used="mock-marketing-agent-v1",
    )

    asset_email_2 = ContentAsset(
        campaign_id=camp_1.id,
        channel=ContentChannel.EMAIL,
        variation_number=2,
        title="The omnichannel blueprint top ecommerce leaders use",
        preview_text="Automate inventory triggers and campaign copy in one unified platform.",
        body=(
            "Hi {{FirstName}},\n\n"
            "Scaling multi-channel campaigns without hiring an army of contractors is the #1 challenge ecommerce directors face this year.\n\n"
            "AuraFlow combines real-time inventory signals with governed marketing intelligence to deliver ready-to-publish Email, Social, and Ad assets in seconds.\n\n"
            "Key benefits:\n"
            "1. 70% faster campaign launch cycles\n"
            "2. Zero out-of-stock wasted ad spend\n"
            "3. 3.2x lift in repeat customer engagement\n\n"
            "Would you be open to a quick 10-minute walkthrough this week?"
        ),
        cta="Schedule a 10-Minute Walkthrough",
        status=ContentStatus.APPROVED,
        is_selected=False,
        model_used="mock-marketing-agent-v1",
    )

    asset_social_1 = ContentAsset(
        campaign_id=camp_1.id,
        channel=ContentChannel.SOCIAL,
        variation_number=1,
        platform="LinkedIn",
        hook="Most ecommerce brands don't have a traffic problem. They have a campaign orchestration bottleneck. 🧵",
        body=(
            "We analyzed how 50+ mid-market ecommerce brands launch promotional campaigns.\n\n"
            "The average timeline from concept to launch: 14 days.\n"
            "- 4 days formatting catalog feeds\n"
            "- 6 days waiting on copy variations\n"
            "- 4 days waiting on stakeholder email approvals\n\n"
            "AuraFlow collapses this entire workflow into under 60 minutes.\n\n"
            "How much time is your team spending on manual campaign assembly this quarter?"
        ),
        cta="Check out the full workflow teardown in the comments 👇",
        hashtags=["Ecommerce", "RetailTech", "MarketingAutomation", "MarTech", "Omnichannel"],
        status=ContentStatus.IN_REVIEW,
        is_selected=True,
        model_used="mock-marketing-agent-v1",
    )

    asset_social_2 = ContentAsset(
        campaign_id=camp_1.id,
        channel=ContentChannel.SOCIAL,
        variation_number=2,
        platform="Twitter / X",
        hook="Why top ecommerce growth leads are replacing 10+ disconnected marketing apps with AuraFlow:",
        body=(
            "1/ Catalog sync in real time.\n"
            "2/ Multi-channel copy generated in seconds.\n"
            "3/ Zero manual spreadsheet exports.\n\n"
            "Transform your store's campaign velocity."
        ),
        cta="Try the interactive demo: link in bio 🚀",
        hashtags=["Ecommerce", "D2C", "SaaSGrowth"],
        status=ContentStatus.DRAFT,
        is_selected=False,
        model_used="mock-marketing-agent-v1",
    )

    asset_ad_1 = ContentAsset(
        campaign_id=camp_1.id,
        channel=ContentChannel.ADVERTISEMENT,
        variation_number=1,
        platform="Google Search Ads",
        title="AuraFlow Commerce Engine | 70% Faster Campaign Launches",
        body="Unify inventory triggers and generate verified multi-channel marketing campaigns in minutes. Built for mid-market ecommerce brands.",
        cta="Start Free Trial",
        status=ContentStatus.IN_REVIEW,
        is_selected=True,
        model_used="mock-marketing-agent-v1",
    )

    asset_ad_2 = ContentAsset(
        campaign_id=camp_1.id,
        channel=ContentChannel.ADVERTISEMENT,
        variation_number=2,
        platform="LinkedIn Sponsored Content",
        title="Stop Wasting 14 Days on Campaign Setups",
        body="Turn real-time inventory signals into high-converting Email, Social, and Ad campaigns with enterprise governance and approval workflows.",
        cta="Book a Demo",
        status=ContentStatus.APPROVED,
        is_selected=False,
        model_used="mock-marketing-agent-v1",
    )

    db.add_all([asset_email_1, asset_email_2, asset_social_1, asset_social_2, asset_ad_1, asset_ad_2])
    db.flush()

    # 6. Approvals for Campaign 1
    appr_1 = Approval(
        workspace_id=workspace.id,
        campaign_id=camp_1.id,
        content_asset_id=asset_email_2.id,
        user_id=user_reviewer.id,
        action=ApprovalAction.APPROVE,
        feedback="Excellent value proposition and crisp bullet points. Approved for deployment.",
    )
    appr_2 = Approval(
        workspace_id=workspace.id,
        campaign_id=camp_1.id,
        content_asset_id=asset_ad_2.id,
        user_id=user_reviewer.id,
        action=ApprovalAction.APPROVE,
        feedback="Strong headline and clear CTA.",
    )
    db.add_all([appr_1, appr_2])

    # 7. Create Campaign 2: DRAFT status
    camp_2 = Campaign(
        workspace_id=workspace.id,
        product_id=prod_2.id,
        audience_id=aud_2.id,
        name="Holiday Prep: Dynamic On-Site Personalization",
        description="Drive urgency and showcase real-time personalization to D2C performance marketing leads ahead of Q4 shopping peak.",
        objective="Trial Sign-ups & Conversion Optimization",
        status=CampaignStatus.DRAFT,
        budget="$15,000",
        target_timeline="Q4 Ramp-Up",
    )
    db.add(camp_2)

    # 8. Create Campaign 3: APPROVED status
    camp_3 = Campaign(
        workspace_id=workspace.id,
        product_id=prod_1.id,
        audience_id=aud_1.id,
        name="Enterprise Omnichannel Modernization",
        description="Executive outreach to enterprise retail tech leaders focusing on headless integration and multi-warehouse sync.",
        objective="Enterprise Pipeline Acceleration",
        status=CampaignStatus.APPROVED,
        budget="$40,000",
        target_timeline="Completed Sprint",
    )
    db.add(camp_3)
    db.flush()

    # 9. AI Execution Logs
    log_1 = AILog(
        workspace_id=workspace.id,
        campaign_id=camp_1.id,
        agent_name="MarketingStrategist",
        provider="mock",
        model="mock-marketing-agent-v1",
        prompt_template="STRATEGY_USER_PROMPT_TEMPLATE",
        prompt_preview="Develop a comprehensive B2B Marketing Campaign Strategy for AuraFlow Commerce AI...",
        response_preview='{\n  "summary": "Strategic multi-touch sprint positioning AuraFlow Omnichannel Engine...",\n  "positioning": "AuraFlow is the unified commerce orchestration platform..."\n}',
        prompt_tokens=420,
        completion_tokens=680,
        total_tokens=1100,
        latency_ms=120,
        status="SUCCESS",
    )
    log_2 = AILog(
        workspace_id=workspace.id,
        campaign_id=camp_1.id,
        agent_name="ContentAgent",
        provider="mock",
        model="mock-marketing-agent-v1",
        prompt_template="CONTENT_USER_PROMPT_TEMPLATE",
        prompt_preview="Generate multi-channel marketing content variations based on this approved strategy...",
        response_preview='{\n  "email_variations": [...],\n  "social_variations": [...],\n  "ad_variations": [...]\n}',
        prompt_tokens=550,
        completion_tokens=940,
        total_tokens=1490,
        latency_ms=145,
        status="SUCCESS",
    )
    db.add_all([log_1, log_2])
    db.flush()

    # 10. Demo Analytics Metrics (Phase 3)
    from app.models.analytics import CampaignMetric
    from datetime import date, timedelta

    today = date.today()
    # Good performing metrics (Camp 3)
    m1 = CampaignMetric(campaign_id=camp_3.id, channel="EMAIL", date=today - timedelta(days=2), impressions=5000, clicks=250, spend=50.0, leads=20, conversions=5, revenue=5000.0)
    m2 = CampaignMetric(campaign_id=camp_3.id, channel="SOCIAL", date=today - timedelta(days=1), impressions=10000, clicks=150, spend=300.0, leads=10, conversions=1, revenue=800.0)

    # Poor performing metrics (Camp 1)
    m3 = CampaignMetric(campaign_id=camp_1.id, channel="ADVERTISEMENT", date=today - timedelta(days=3), impressions=20000, clicks=80, spend=1200.0, leads=2, conversions=0, revenue=0.0)

    db.add_all([m1, m2, m3])
    db.commit()
    logger.info("Demo data successfully seeded.")
    return workspace
