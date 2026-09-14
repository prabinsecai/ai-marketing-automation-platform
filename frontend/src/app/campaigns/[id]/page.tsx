"use client";

import React, { useEffect, useState, useCallback, use } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  Sparkles,
  FileText,
  Info,
  ShieldCheck,
  Package,
  Users,
} from "lucide-react";
import { api } from "@/lib/api";
import { CampaignDetail, ContentAsset } from "@/lib/types";
import { StatusStepper } from "@/components/campaigns/StatusStepper";
import { StrategyView } from "@/components/campaigns/StrategyView";
import { ContentAssetCard } from "@/components/campaigns/ContentAssetCard";
import { ContentEditModal } from "@/components/campaigns/ContentEditModal";
import { RegenerateModal } from "@/components/campaigns/RegenerateModal";
import { ApprovalModal } from "@/components/campaigns/ApprovalModal";
import { Button, Card, Badge } from "@/lib/ui";
import { formatDate } from "@/lib/utils";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default function CampaignDetailPage({ params }: PageProps) {
  const resolvedParams = use(params);
  const campaignId = resolvedParams.id;

  const [campaign, setCampaign] = useState<CampaignDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"strategy" | "content" | "overview" | "approvals">("strategy");
  const [contentChannelFilter, setContentChannelFilter] = useState<string>("ALL");

  // AI Generation Loading States
  const [generatingStrategy, setGeneratingStrategy] = useState(false);
  const [generatingContent, setGeneratingContent] = useState(false);

  // Modals state
  const [editingAsset, setEditingAsset] = useState<ContentAsset | null>(null);
  const [regeneratingAsset, setRegeneratingAsset] = useState<ContentAsset | null>(null);
  const [reviewingAsset, setReviewingAsset] = useState<ContentAsset | null>(null);

  // Approvals list for audit tab
  const [approvals, setApprovals] = useState<any[]>([]);

  const loadCampaign = useCallback(async () => {
    try {
      setLoading(true);
      const data = await api.getCampaign(campaignId);
      setCampaign(data);
    } catch (err) {
      console.error("Failed to load campaign:", err);
    } finally {
      setLoading(false);
    }
  }, [campaignId]);

  const loadApprovals = useCallback(async () => {
    try {
      const data = await api.listApprovals(undefined, campaignId);
      setApprovals(data);
    } catch (err) {
      console.error("Failed to load approvals", err);
    }
  }, [campaignId]);

  useEffect(() => {
    loadCampaign();
    loadApprovals();
  }, [loadCampaign, loadApprovals]);

  const handleGenerateStrategy = async () => {
    try {
      setGeneratingStrategy(true);
      await api.generateStrategy(campaignId);
      await loadCampaign();
    } catch (err) {
      alert(`Strategy generation failed: ${err}`);
    } finally {
      setGeneratingStrategy(false);
    }
  };

  const handleGenerateContent = async () => {
    try {
      setGeneratingContent(true);
      await api.generateCampaignContent(campaignId);
      await loadCampaign();
      setActiveTab("content");
    } catch (err) {
      alert(`Content generation failed: ${err}`);
    } finally {
      setGeneratingContent(false);
    }
  };

  const handleSaveEdit = async (assetId: string, updatedData: any) => {
    await api.editContentAsset(assetId, updatedData);
    await loadCampaign();
  };

  const handleRegenerateVariation = async (assetId: string, instructions?: string) => {
    await api.regenerateContentAsset(assetId, instructions);
    await loadCampaign();
  };

  const handleToggleSelect = async (assetId: string) => {
    await api.toggleSelectContentAsset(assetId);
    await loadCampaign();
  };

  const handleApproveAction = async (assetId: string, action: any, feedback?: string) => {
    await api.approveContentAsset(assetId, action, feedback);
    await loadCampaign();
    await loadApprovals();
  };

  if (loading || !campaign) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin" />
          <p className="text-xs text-zinc-500">Loading campaign details...</p>
        </div>
      </div>
    );
  }

  const filteredAssets = (campaign.content_assets || []).filter((a) => {
    if (contentChannelFilter === "ALL") return true;
    return a.channel === contentChannelFilter;
  });

  return (
    <div className="space-y-6">
      {/* Back link & Header */}
      <div>
        <Link
          href="/campaigns"
          className="inline-flex items-center gap-1 text-xs text-zinc-400 hover:text-zinc-200 transition-colors mb-3"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to campaigns
        </Link>

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 tracking-tight">
                {campaign.name}
              </h1>
              <Badge variant="status" status={campaign.status} dot>
                {campaign.status.replace("_", " ")}
              </Badge>
            </div>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              Objective: {campaign.objective}
            </p>
          </div>

          <div className="flex items-center gap-2">
            {!campaign.strategy && (
              <Button
                variant="primary"
                size="sm"
                onClick={handleGenerateStrategy}
                loading={generatingStrategy}
                icon={<Sparkles className="w-4 h-4" />}
              >
                Generate Strategy
              </Button>
            )}

            {campaign.strategy && (!campaign.content_assets || campaign.content_assets.length === 0) && (
              <Button
                variant="primary"
                size="sm"
                onClick={handleGenerateContent}
                loading={generatingContent}
                icon={<Sparkles className="w-4 h-4" />}
              >
                Generate Multi-Channel Copy
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Campaign Status Stepper */}
      <StatusStepper currentStatus={campaign.status} />

      {/* Main Tabs Navigation */}
      <div className="border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between overflow-x-auto">
        <div className="flex items-center gap-6">
          <button
            onClick={() => setActiveTab("strategy")}
            className={`pb-3 text-xs font-semibold flex items-center gap-1.5 transition-colors border-b-2 ${
              activeTab === "strategy"
                ? "border-indigo-600 text-indigo-600 dark:text-indigo-400"
                : "border-transparent text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            AI Strategy
            {campaign.strategy && (
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            )}
          </button>

          <button
            onClick={() => setActiveTab("content")}
            className={`pb-3 text-xs font-semibold flex items-center gap-1.5 transition-colors border-b-2 ${
              activeTab === "content"
                ? "border-indigo-600 text-indigo-600 dark:text-indigo-400"
                : "border-transparent text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            AI Content Variations
            <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-zinc-100 dark:bg-zinc-800">
              {campaign.content_assets?.length || 0}
            </span>
          </button>

          <button
            onClick={() => setActiveTab("overview")}
            className={`pb-3 text-xs font-semibold flex items-center gap-1.5 transition-colors border-b-2 ${
              activeTab === "overview"
                ? "border-indigo-600 text-indigo-600 dark:text-indigo-400"
                : "border-transparent text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
            }`}
          >
            <Info className="w-3.5 h-3.5" />
            Product & Audience Context
          </button>

          <button
            onClick={() => setActiveTab("approvals")}
            className={`pb-3 text-xs font-semibold flex items-center gap-1.5 transition-colors border-b-2 ${
              activeTab === "approvals"
                ? "border-indigo-600 text-indigo-600 dark:text-indigo-400"
                : "border-transparent text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
            }`}
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            Governance & Approvals Log
            <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-zinc-100 dark:bg-zinc-800">
              {approvals.length}
            </span>
          </button>
        </div>
      </div>

      {/* TAB CONTENT: AI Strategy */}
      {activeTab === "strategy" && (
        <StrategyView
          strategy={campaign.strategy}
          onGenerate={handleGenerateStrategy}
          loading={generatingStrategy}
        />
      )}

      {/* TAB CONTENT: AI Content Variations */}
      {activeTab === "content" && (
        <div className="space-y-6">
          {/* Content Header & Channel Filter */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-1.5 overflow-x-auto pb-2 sm:pb-0">
              {["ALL", "EMAIL", "SOCIAL", "ADVERTISEMENT"].map((ch) => (
                <button
                  key={ch}
                  onClick={() => setContentChannelFilter(ch)}
                  className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                    contentChannelFilter === ch
                      ? "bg-indigo-600 text-white shadow-sm"
                      : "bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                  }`}
                >
                  {ch === "ALL" ? "All Channels" : ch}
                </button>
              ))}
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={handleGenerateContent}
              loading={generatingContent}
              icon={<Sparkles className="w-3.5 h-3.5" />}
            >
              Regenerate All Multi-Channel Copy
            </Button>
          </div>

          {/* Asset List */}
          {(!campaign.content_assets || campaign.content_assets.length === 0) ? (
            <Card className="text-center py-12 border-dashed border-2">
              <FileText className="w-10 h-10 text-zinc-400 mx-auto mb-3" />
              <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                No Content Variations Generated Yet
              </h3>
              <p className="text-xs text-zinc-500 max-w-md mx-auto mt-1 mb-5">
                Generate high-converting channel copy across Email, Social, and Paid Ads based on your strategy.
              </p>
              <Button
                variant="primary"
                onClick={handleGenerateContent}
                loading={generatingContent}
                icon={<Sparkles className="w-4 h-4" />}
              >
                Generate Multi-Channel Copy
              </Button>
            </Card>
          ) : filteredAssets.length === 0 ? (
            <Card className="text-center py-8">
              <p className="text-xs text-zinc-500">No content variations found for channel &quot;{contentChannelFilter}&quot;.</p>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredAssets.map((asset) => (
                <ContentAssetCard
                  key={asset.id}
                  asset={asset}
                  onEdit={(a) => setEditingAsset(a)}
                  onRegenerate={(a) => setRegeneratingAsset(a)}
                  onSelect={handleToggleSelect}
                  onReview={(a) => setReviewingAsset(a)}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {/* TAB CONTENT: Product & Audience Context */}
      {activeTab === "overview" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Product Overview */}
          <Card className="space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-zinc-100 dark:border-zinc-800">
              <Package className="w-4 h-4 text-indigo-500" />
              <h3 className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider">
                Associated Product / Service
              </h3>
            </div>

            {campaign.product ? (
              <div className="space-y-3 text-xs">
                <div>
                  <span className="font-semibold text-zinc-900 dark:text-zinc-100 text-sm block">
                    {campaign.product.name}
                  </span>
                  <span className="text-[11px] text-zinc-400 font-medium">
                    Category: {campaign.product.category || "General B2B"} • Pricing: {campaign.product.price || "Custom"}
                  </span>
                </div>

                <p className="text-zinc-600 dark:text-zinc-400">{campaign.product.description}</p>

                {campaign.product.usp && (
                  <div className="p-2.5 bg-indigo-50 dark:bg-indigo-950/40 rounded-lg border border-indigo-100 dark:border-indigo-900/40">
                    <span className="text-[10px] font-bold text-indigo-600 dark:text-indigo-400 uppercase block">
                      Unique Selling Proposition (USP)
                    </span>
                    <p className="text-xs text-indigo-900 dark:text-indigo-200 mt-0.5">
                      {campaign.product.usp}
                    </p>
                  </div>
                )}

                {campaign.product.features && campaign.product.features.length > 0 && (
                  <div>
                    <span className="font-semibold text-zinc-700 dark:text-zinc-300 block mb-1">
                      Key Features:
                    </span>
                    <ul className="space-y-1">
                      {campaign.product.features.map((f, i) => (
                        <li key={i} className="text-zinc-500 dark:text-zinc-400 flex items-center gap-1.5">
                          <span className="text-indigo-500">•</span> {f}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-xs text-zinc-500">No specific product linked to this campaign.</p>
            )}
          </Card>

          {/* Audience Overview */}
          <Card className="space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-zinc-100 dark:border-zinc-800">
              <Users className="w-4 h-4 text-indigo-500" />
              <h3 className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider">
                Target Buyer Persona
              </h3>
            </div>

            {campaign.audience ? (
              <div className="space-y-3 text-xs">
                <div>
                  <span className="font-semibold text-zinc-900 dark:text-zinc-100 text-sm block">
                    {campaign.audience.name}
                  </span>
                  <span className="text-[11px] text-zinc-400">{campaign.audience.description}</span>
                </div>

                {campaign.audience.pain_points && campaign.audience.pain_points.length > 0 && (
                  <div>
                    <span className="font-semibold text-rose-600 dark:text-rose-400 block mb-1">
                      Audience Pain Points:
                    </span>
                    <ul className="space-y-1">
                      {campaign.audience.pain_points.map((p, i) => (
                        <li key={i} className="text-zinc-600 dark:text-zinc-400 flex items-start gap-1.5">
                          <span className="text-rose-500">•</span> {p}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {campaign.audience.preferred_channels && campaign.audience.preferred_channels.length > 0 && (
                  <div className="pt-2">
                    <span className="font-semibold text-zinc-700 dark:text-zinc-300 block mb-1">
                      Preferred Channels:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {campaign.audience.preferred_channels.map((ch, i) => (
                        <Badge key={i} variant="outline">
                          {ch}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-xs text-zinc-500">No specific audience persona linked to this campaign.</p>
            )}
          </Card>
        </div>
      )}

      {/* TAB CONTENT: Approvals Log */}
      {activeTab === "approvals" && (
        <Card className="space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-zinc-100 dark:border-zinc-800">
            <h3 className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-indigo-500" /> Stakeholder Approval Audit Log
            </h3>
            <span className="text-xs text-zinc-400">{approvals.length} recorded actions</span>
          </div>

          {approvals.length === 0 ? (
            <div className="text-center py-8 text-xs text-zinc-500">
              No approval actions recorded for this campaign yet.
            </div>
          ) : (
            <div className="space-y-3">
              {approvals.map((appr) => (
                <div
                  key={appr.id}
                  className="p-3 rounded-lg border border-zinc-100 dark:border-zinc-800 text-xs space-y-1"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Badge variant="status" status={appr.action}>
                        {appr.action}
                      </Badge>
                      <span className="font-medium text-zinc-800 dark:text-zinc-200">
                        {appr.user_id ? "Marcus Vance (Reviewer)" : "Authorized Stakeholder"}
                      </span>
                    </div>
                    <span className="text-[10px] text-zinc-400">{formatDate(appr.created_at)}</span>
                  </div>
                  {appr.feedback && (
                    <p className="text-zinc-600 dark:text-zinc-400 pt-1 italic">
                      &quot;{appr.feedback}&quot;
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Content Edit Modal */}
      <ContentEditModal
        isOpen={!!editingAsset}
        onClose={() => setEditingAsset(null)}
        asset={editingAsset}
        onSave={handleSaveEdit}
      />

      {/* Single Variation Regenerate Modal */}
      <RegenerateModal
        isOpen={!!regeneratingAsset}
        onClose={() => setRegeneratingAsset(null)}
        asset={regeneratingAsset}
        onRegenerate={handleRegenerateVariation}
      />

      {/* Review & Approval Modal */}
      <ApprovalModal
        isOpen={!!reviewingAsset}
        onClose={() => setReviewingAsset(null)}
        asset={reviewingAsset}
        onApprove={handleApproveAction}
      />
    </div>
  );
}
