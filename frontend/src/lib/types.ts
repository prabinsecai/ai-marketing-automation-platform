export interface Workspace {
  id: string;
  name: string;
  slug: string;
  industry?: string;
  website?: string;
  description?: string;
  brand_guidelines?: string;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: string;
  workspace_id: string;
  name: string;
  category?: string;
  description: string;
  price?: string;
  features: string[];
  target_benefits: string[];
  usp?: string;
  url?: string;
  created_at: string;
  updated_at: string;
}

export interface Audience {
  id: string;
  workspace_id: string;
  name: string;
  description?: string;
  demographics: Record<string, any>;
  pain_points: string[];
  interests: string[];
  goals: string[];
  preferred_channels: string[];
  created_at: string;
  updated_at: string;
}

export type CampaignStatusType =
  | "DRAFT"
  | "STRATEGY_GENERATED"
  | "CONTENT_GENERATED"
  | "IN_REVIEW"
  | "APPROVED";

export interface ChannelStrategyItem {
  channel: string;
  priority: string;
  rationale: string;
  tactics: string[];
}

export interface CampaignThemeItem {
  theme: string;
  hook: string;
  description: string;
}

export interface ContentRecommendationItem {
  channel: string;
  asset_type: string;
  objective: string;
  best_practices: string[];
}

export interface MetricItem {
  metric: string;
  rationale: string;
  target_benchmark: string;
}

export interface RiskAssumptionItem {
  risk: string;
  mitigation: string;
}

export interface CampaignStrategy {
  id: string;
  campaign_id: string;
  summary: string;
  audience_reasoning: string;
  positioning: string;
  key_message: string;
  channel_strategy: ChannelStrategyItem[];
  campaign_themes: CampaignThemeItem[];
  content_recommendations: ContentRecommendationItem[];
  cta_strategy: string;
  timeline_suggestion: string;
  future_success_metrics: MetricItem[];
  risks_assumptions: RiskAssumptionItem[];
  model_used?: string;
  created_at: string;
  updated_at: string;
}

export type ContentChannelType = "EMAIL" | "SOCIAL" | "ADVERTISEMENT";
export type ContentStatusType = "DRAFT" | "IN_REVIEW" | "APPROVED" | "REJECTED";

export interface EditHistoryItem {
  edited_at: string;
  previous_title?: string;
  previous_body?: string;
  previous_cta?: string;
  summary?: string;
}

export interface ContentAsset {
  id: string;
  campaign_id: string;
  channel: ContentChannelType;
  variation_number: number;
  title?: string;
  preview_text?: string;
  body: string;
  hook?: string;
  cta?: string;
  hashtags: string[];
  platform?: string;
  status: ContentStatusType;
  is_selected: boolean;
  edit_history: EditHistoryItem[];
  model_used?: string;
  created_at: string;
  updated_at: string;
}

export interface Campaign {
  id: string;
  workspace_id: string;
  name: string;
  description?: string;
  objective: string;
  status: CampaignStatusType;
  budget?: string;
  target_timeline?: string;
  product_id?: string;
  audience_id?: string;
  created_at: string;
  updated_at: string;
}

export interface CampaignDetail extends Campaign {
  product?: Product;
  audience?: Audience;
  strategy?: CampaignStrategy;
  content_assets: ContentAsset[];
}

export interface Approval {
  id: string;
  workspace_id: string;
  campaign_id: string;
  content_asset_id?: string;
  user_id?: string;
  action: "APPROVE" | "REJECT" | "REQUEST_CHANGES";
  feedback?: string;
  created_at: string;
}

export interface AILog {
  id: string;
  workspace_id: string;
  campaign_id?: string;
  agent_name: string;
  provider: string;
  model: string;
  prompt_template?: string;
  prompt_preview?: string;
  response_preview?: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  latency_ms: number;
  status: "SUCCESS" | "FAILED";
  error_message?: string;
  created_at: string;
}

export interface DashboardStats {
  workspace_name: string;
  workspace_id: string;
  total_campaigns: number;
  campaign_status_counts: {
    draft: number;
    strategy_generated: number;
    content_generated: number;
    in_review: number;
    approved: number;
    total: number;
  };
  total_products: number;
  total_audiences: number;
  content_status_counts: {
    draft: number;
    in_review: number;
    approved: number;
    rejected: number;
    total: number;
    email: number;
    social: number;
    advertisement: number;
  };
  recent_campaigns: Campaign[];
  recent_ai_activity: AILog[];
}

export type ExecutionStatusType =
  | "PENDING"
  | "RUNNING"
  | "SUCCESS"
  | "FAILED"
  | "RETRYING"
  | "ESCALATED";

export type StepStatusType = "RUNNING" | "SUCCESS" | "FAILED" | "SKIPPED";

export interface ExecutionStep {
  id: string;
  execution_id: string;
  step_name: string;
  step_type: string;
  status: StepStatusType;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  error_message?: string;
  started_at: string;
  completed_at?: string;
  created_at: string;
}

export interface AgentTraceItem {
  node: string;
  timestamp: string;
  message: string;
  details?: Record<string, any>;
}

export interface CampaignExecution {
  id: string;
  campaign_id: string;
  workspace_id: string;
  status: ExecutionStatusType;
  idempotency_key: string;
  retry_count: number;
  max_retries: number;
  n8n_execution_id?: string;
  n8n_workflow_id?: string;
  error_message?: string;
  agent_trace: AgentTraceItem[];
  trigger_source: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
  steps: ExecutionStep[];
}

export interface ExecutionCreatePayload {
  workspace_id?: string;
  idempotency_key?: string;
  trigger_source?: string;
}
