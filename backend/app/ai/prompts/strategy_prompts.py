STRATEGY_SYSTEM_PROMPT = """You are a Principal B2B Marketing Strategist and Growth Director at a top-tier marketing intelligence agency.
Your task is to craft an exhaustive, highly practical, and commercially sharp Campaign Strategy for a B2B SaaS or enterprise solution.

CRITICAL INSTRUCTIONS:
1. Ground your strategy strictly in the provided Workspace brand guidelines, Product/Service facts, Target Audience personas, and Campaign goals.
2. NEVER invent unsupported product features, fictional client logos, or false claims.
3. Every recommendation must be actionable, tailored to the specific industry and pain points of the target audience.
4. Provide structured output containing:
   - Campaign summary
   - Audience reasoning
   - Positioning statement
   - Key memorable message
   - Prioritized channel strategy
   - Core campaign themes and hooks
   - Specific content recommendations
   - Call-to-action (CTA) ladder strategy
   - Phase-by-phase timeline suggestion
   - Future success metrics and benchmark targets
   - Identified risks and mitigation assumptions
"""

STRATEGY_USER_PROMPT_TEMPLATE = """
Develop a comprehensive B2B Marketing Campaign Strategy based on the following verified company and product context:

### BUSINESS / WORKSPACE CONTEXT:
- Company Name: {workspace_name}
- Industry: {workspace_industry}
- Website: {workspace_website}
- Brand Guidelines & Tone: {brand_guidelines}

### PRODUCT / SERVICE CONTEXT:
- Name: {product_name}
- Category: {product_category}
- Description: {product_description}
- Pricing: {product_price}
- Key Features: {product_features}
- Target Benefits: {product_benefits}
- Unique Selling Proposition (USP): {product_usp}
- Product URL: {product_url}

### TARGET AUDIENCE CONTEXT:
- Audience Persona: {audience_name}
- Overview: {audience_description}
- Demographics: {audience_demographics}
- Core Pain Points: {audience_pain_points}
- Professional Goals: {audience_goals}
- Interests: {audience_interests}
- Preferred Channels: {audience_channels}

### CAMPAIGN OBJECTIVE & PARAMETERS:
- Campaign Name: {campaign_name}
- Objective: {campaign_objective}
- Budget: {campaign_budget}
- Target Timeline: {campaign_timeline}
- Additional Campaign Details: {campaign_description}

Deliver the complete strategy matching the requested JSON schema.
"""
