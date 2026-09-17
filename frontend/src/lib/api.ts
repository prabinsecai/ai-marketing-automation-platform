import {
  Workspace,
  Product,
  Audience,
  Campaign,
  CampaignDetail,
  CampaignStrategy,
  ContentAsset,
  Approval,
  AILog,
  DashboardStats,
  CampaignAnalyticsReport,
  CampaignExecution,
  ExecutionCreatePayload,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetcher<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    let errorMsg = `API Error ${response.status}: ${response.statusText}`;
    try {
      const errData = await response.json();
      if (errData?.detail) {
        errorMsg = typeof errData.detail === "string" ? errData.detail : JSON.stringify(errData.detail);
      }
    } catch {
      // ignore json parse error
    }
    throw new Error(errorMsg);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

export const api = {
  getCampaignAnalytics: (id: string) =>
    fetcher<CampaignAnalyticsReport>(`/campaigns/${id}/analytics`),
  analyzeCampaign: (id: string) =>
    fetcher<any>(`/campaigns/${id}/analyze`, { method: 'POST' }),
  // Health
  getHealth: () => fetcher<{ status: string; service: string; version: string; llm_mode: string }>("/health"),

  // Workspaces
  listWorkspaces: () => fetcher<Workspace[]>("/workspaces"),
  getWorkspace: (id: string) => fetcher<Workspace>(`/workspaces/${id}`),
  createWorkspace: (data: Partial<Workspace>) =>
    fetcher<Workspace>("/workspaces", { method: "POST", body: JSON.stringify(data) }),
  updateWorkspace: (id: string, data: Partial<Workspace>) =>
    fetcher<Workspace>(`/workspaces/${id}`, { method: "PUT", body: JSON.stringify(data) }),

  // Products
  listProducts: (workspaceId?: string) =>
    fetcher<Product[]>(`/products${workspaceId ? `?workspace_id=${workspaceId}` : ""}`),
  getProduct: (id: string) => fetcher<Product>(`/products/${id}`),
  createProduct: (data: Partial<Product> & { workspace_id: string }) =>
    fetcher<Product>("/products", { method: "POST", body: JSON.stringify(data) }),
  updateProduct: (id: string, data: Partial<Product>) =>
    fetcher<Product>(`/products/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteProduct: (id: string) => fetcher<void>(`/products/${id}`, { method: "DELETE" }),

  // Audiences
  listAudiences: (workspaceId?: string) =>
    fetcher<Audience[]>(`/audiences${workspaceId ? `?workspace_id=${workspaceId}` : ""}`),
  getAudience: (id: string) => fetcher<Audience>(`/audiences/${id}`),
  createAudience: (data: Partial<Audience> & { workspace_id: string }) =>
    fetcher<Audience>("/audiences", { method: "POST", body: JSON.stringify(data) }),
  updateAudience: (id: string, data: Partial<Audience>) =>
    fetcher<Audience>(`/audiences/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteAudience: (id: string) => fetcher<void>(`/audiences/${id}`, { method: "DELETE" }),

  // Campaigns
  listCampaigns: (workspaceId?: string, status?: string) => {
    const params = new URLSearchParams();
    if (workspaceId) params.append("workspace_id", workspaceId);
    if (status) params.append("status", status);
    const qs = params.toString();
    return fetcher<Campaign[]>(`/campaigns${qs ? `?${qs}` : ""}`);
  },
  getCampaign: (id: string) => fetcher<CampaignDetail>(`/campaigns/${id}`),
  createCampaign: (data: Partial<Campaign> & { workspace_id: string; name: string; objective: string }) =>
    fetcher<Campaign>("/campaigns", { method: "POST", body: JSON.stringify(data) }),
  updateCampaign: (id: string, data: Partial<Campaign>) =>
    fetcher<Campaign>(`/campaigns/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  updateCampaignStatus: (id: string, status: string) =>
    fetcher<Campaign>(`/campaigns/${id}/status`, { method: "PATCH", body: JSON.stringify({ status }) }),
  deleteCampaign: (id: string) => fetcher<void>(`/campaigns/${id}`, { method: "DELETE" }),

  // Strategy
  getStrategy: (campaignId: string) => fetcher<CampaignStrategy>(`/campaigns/${campaignId}/strategy`),
  generateStrategy: (campaignId: string) =>
    fetcher<CampaignStrategy>(`/campaigns/${campaignId}/strategy/generate`, { method: "POST" }),

  // Content
  getCampaignContent: (campaignId: string, channel?: string) =>
    fetcher<ContentAsset[]>(`/campaigns/${campaignId}/content${channel ? `?channel=${channel}` : ""}`),
  generateCampaignContent: (campaignId: string) =>
    fetcher<ContentAsset[]>(`/campaigns/${campaignId}/content/generate`, { method: "POST" }),

  // Content Assets
  listContentAssets: (workspaceId?: string, channel?: string, status?: string) => {
    const params = new URLSearchParams();
    if (workspaceId) params.append("workspace_id", workspaceId);
    if (channel) params.append("channel", channel);
    if (status) params.append("status", status);
    const qs = params.toString();
    return fetcher<ContentAsset[]>(`/content-assets${qs ? `?${qs}` : ""}`);
  },
  getContentAsset: (id: string) => fetcher<ContentAsset>(`/content-assets/${id}`),
  editContentAsset: (id: string, data: Partial<ContentAsset> & { edit_summary?: string }) =>
    fetcher<ContentAsset>(`/content-assets/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  toggleSelectContentAsset: (id: string) =>
    fetcher<ContentAsset>(`/content-assets/${id}/select`, { method: "POST" }),
  regenerateContentAsset: (id: string, instructions?: string) =>
    fetcher<ContentAsset>(`/content-assets/${id}/regenerate`, {
      method: "POST",
      body: JSON.stringify({ instructions }),
    }),
  approveContentAsset: (id: string, action: "APPROVE" | "REJECT" | "REQUEST_CHANGES", feedback?: string) =>
    fetcher<Approval>(`/content-assets/${id}/approve`, {
      method: "POST",
      body: JSON.stringify({ action, feedback }),
    }),

  // Approvals & Logs
  listApprovals: (workspaceId?: string, campaignId?: string) => {
    const params = new URLSearchParams();
    if (workspaceId) params.append("workspace_id", workspaceId);
    if (campaignId) params.append("campaign_id", campaignId);
    const qs = params.toString();
    return fetcher<Approval[]>(`/approvals${qs ? `?${qs}` : ""}`);
  },
  listAILogs: (workspaceId?: string, campaignId?: string, limit = 50) => {
    const params = new URLSearchParams();
    if (workspaceId) params.append("workspace_id", workspaceId);
    if (campaignId) params.append("campaign_id", campaignId);
    params.append("limit", limit.toString());
    const qs = params.toString();
    return fetcher<AILog[]>(`/ai-logs${qs ? `?${qs}` : ""}`);
  },

  // Dashboard
  getDashboardStats: (workspaceId?: string) =>
    fetcher<DashboardStats>(`/dashboard/stats${workspaceId ? `?workspace_id=${workspaceId}` : ""}`),

  // Phase 2: Campaign Executions
  executeCampaign: (campaignId: string, payload?: ExecutionCreatePayload) =>
    fetcher<CampaignExecution>(`/campaigns/${campaignId}/execute`, {
      method: "POST",
      body: JSON.stringify(payload || {}),
    }),
  listExecutions: (workspaceId?: string, campaignId?: string, status?: string) => {
    const params = new URLSearchParams();
    if (workspaceId) params.append("workspace_id", workspaceId);
    if (campaignId) params.append("campaign_id", campaignId);
    if (status) params.append("status", status);
    const qs = params.toString();
    return fetcher<CampaignExecution[]>(`/executions${qs ? `?${qs}` : ""}`);
  },
  getExecution: (id: string, workspaceId?: string) =>
    fetcher<CampaignExecution>(`/executions/${id}${workspaceId ? `?workspace_id=${workspaceId}` : ""}`),
  retryExecution: (id: string, workspaceId?: string) =>
    fetcher<CampaignExecution>(`/executions/${id}/retry`, {
      method: "POST",
      body: JSON.stringify({ workspace_id: workspaceId }),
    }),

  // Demo
  seedDemoData: () => fetcher<Workspace>("/demo/seed", { method: "POST" }),
};
