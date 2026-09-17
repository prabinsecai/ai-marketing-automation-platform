"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Megaphone,
  CheckCircle2,
  Clock,
  Package,
  ArrowRight,
  TrendingUp,
  Bot,
  Zap,
} from "lucide-react";
import { api } from "@/lib/api";
import { DashboardStats, CampaignExecution } from "@/lib/types";
import { Card, Badge, Button } from "@/lib/ui";
import { formatDate } from "@/lib/utils";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [executions, setExecutions] = useState<CampaignExecution[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const [data, execList] = await Promise.all([
        api.getDashboardStats(),
        api.listExecutions(),
      ]);
      setStats(data);
      setExecutions(execList);
    } catch (err: any) {
      console.error("Dashboard error:", err);
      setError(err.message || "Failed to load dashboard data");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin" />
          <p className="text-xs text-zinc-500">Loading campaign intelligence dashboard...</p>
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <Card className="text-center py-12 border-rose-500/20 bg-rose-500/5">
        <p className="text-sm font-semibold text-rose-600 dark:text-rose-400">
          {error || "No workspace data found."}
        </p>
        <p className="text-xs text-zinc-500 mt-1 mb-4">
          Click below to seed realistic fictional e-commerce demo data or retry.
        </p>
        <Button variant="primary" size="sm" onClick={loadDashboard}>
          Retry Connection
        </Button>
      </Card>
    );
  }

  return (
    <div className="space-y-8">
      {/* Top Welcome Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-indigo-900/40 via-zinc-900 to-zinc-900 border border-indigo-500/20 rounded-2xl p-6 shadow-sm">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-xl font-bold text-white tracking-tight">
              Marketing Intelligence Dashboard
            </h1>
            <Badge variant="brand">Phase 2 Live • LangGraph + n8n</Badge>
          </div>
          <p className="text-xs text-zinc-400 max-w-2xl leading-relaxed">
            Manage your verified products, target audience personas, AI strategy formulation,
            multi-channel copy generation, and LangGraph-driven autonomous campaign execution through local n8n.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/executions">
            <Button variant="outline" size="sm" icon={<Zap className="w-4 h-4 text-amber-500" />}>
              Live Executions ({executions.length})
            </Button>
          </Link>
          <Link href="/campaigns">
            <Button variant="primary" size="sm" icon={<Megaphone className="w-4 h-4" />}>
              View Campaigns
            </Button>
          </Link>
        </div>
      </div>

      {/* Real Metric Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="space-y-1">
          <div className="flex items-center justify-between text-zinc-500">
            <span className="text-xs font-semibold uppercase tracking-wider">Total Campaigns</span>
            <Megaphone className="w-4 h-4 text-indigo-500" />
          </div>
          <p className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {stats.total_campaigns}
          </p>
          <p className="text-[11px] text-zinc-400">
            {stats.campaign_status_counts.approved} Approved • {stats.campaign_status_counts.in_review} In Review
          </p>
        </Card>

        <Card className="space-y-1">
          <div className="flex items-center justify-between text-zinc-500">
            <span className="text-xs font-semibold uppercase tracking-wider">In Review Queue</span>
            <Clock className="w-4 h-4 text-amber-500" />
          </div>
          <p className="text-2xl font-bold text-amber-600 dark:text-amber-400">
            {stats.campaign_status_counts.in_review}
          </p>
          <p className="text-[11px] text-zinc-400">
            {stats.content_status_counts.in_review} content assets pending review
          </p>
        </Card>

        <Card className="space-y-1">
          <div className="flex items-center justify-between text-zinc-500">
            <span className="text-xs font-semibold uppercase tracking-wider">Approved Campaigns</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
          </div>
          <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
            {stats.campaign_status_counts.approved}
          </p>
          <p className="text-[11px] text-zinc-400">
            {stats.content_status_counts.approved} approved copy variations
          </p>
        </Card>

        <Card className="space-y-1">
          <div className="flex items-center justify-between text-zinc-500">
            <span className="text-xs font-semibold uppercase tracking-wider">Product Catalog</span>
            <Package className="w-4 h-4 text-blue-500" />
          </div>
          <p className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {stats.total_products}
          </p>
          <p className="text-[11px] text-zinc-400">
            Targeting {stats.total_audiences} defined buyer personas
          </p>
        </Card>
      </div>

      {/* Campaign Lifecycle Pipeline Overview */}
      <Card className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-indigo-500" /> Campaign Lifecycle Funnel
          </h2>
          <span className="text-xs text-zinc-400">Real-time DB Counts</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2">
          <div className="p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-xl border border-zinc-200 dark:border-zinc-800 text-center">
            <span className="text-[11px] font-semibold text-zinc-500 uppercase tracking-wider block">
              1. Draft
            </span>
            <span className="text-xl font-bold text-zinc-700 dark:text-zinc-300">
              {stats.campaign_status_counts.draft}
            </span>
          </div>

          <div className="p-3 bg-blue-50/50 dark:bg-blue-950/20 rounded-xl border border-blue-200 dark:border-blue-900/50 text-center">
            <span className="text-[11px] font-semibold text-blue-600 dark:text-blue-400 uppercase tracking-wider block">
              2. Strategy
            </span>
            <span className="text-xl font-bold text-blue-600 dark:text-blue-400">
              {stats.campaign_status_counts.strategy_generated}
            </span>
          </div>

          <div className="p-3 bg-indigo-50/50 dark:bg-indigo-950/20 rounded-xl border border-indigo-200 dark:border-indigo-900/50 text-center">
            <span className="text-[11px] font-semibold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider block">
              3. Content
            </span>
            <span className="text-xl font-bold text-indigo-600 dark:text-indigo-400">
              {stats.campaign_status_counts.content_generated}
            </span>
          </div>

          <div className="p-3 bg-amber-50/50 dark:bg-amber-950/20 rounded-xl border border-amber-200 dark:border-amber-900/50 text-center">
            <span className="text-[11px] font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wider block">
              4. In Review
            </span>
            <span className="text-xl font-bold text-amber-600 dark:text-amber-400">
              {stats.campaign_status_counts.in_review}
            </span>
          </div>

          <div className="p-3 bg-emerald-50/50 dark:bg-emerald-950/20 rounded-xl border border-emerald-200 dark:border-emerald-900/50 text-center">
            <span className="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider block">
              5. Approved
            </span>
            <span className="text-xl font-bold text-emerald-600 dark:text-emerald-400">
              {stats.campaign_status_counts.approved}
            </span>
          </div>
        </div>
      </Card>

      {/* Two-Column Grid: Recent Campaigns & AI Execution Logs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Campaigns */}
        <Card className="space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-zinc-100 dark:border-zinc-800">
            <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
              <Megaphone className="w-4 h-4 text-indigo-500" /> Recent Marketing Campaigns
            </h2>
            <Link
              href="/campaigns"
              className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1 font-medium"
            >
              All campaigns <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {stats.recent_campaigns.length === 0 ? (
            <div className="text-center py-8 text-xs text-zinc-500">No campaigns created yet.</div>
          ) : (
            <div className="space-y-2.5">
              {stats.recent_campaigns.map((camp) => (
                <Link
                  key={camp.id}
                  href={`/campaigns/${camp.id}`}
                  className="flex items-center justify-between p-3 rounded-lg border border-zinc-100 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-zinc-800/60 transition-all group"
                >
                  <div className="space-y-1">
                    <p className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                      {camp.name}
                    </p>
                    <p className="text-[11px] text-zinc-400">{camp.objective}</p>
                  </div>
                  <Badge variant="status" status={camp.status} dot>
                    {camp.status.replace("_", " ")}
                  </Badge>
                </Link>
              ))}
            </div>
          )}
        </Card>

        {/* AI Execution & Generation Feed */}
        <Card className="space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-zinc-100 dark:border-zinc-800">
            <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
              <Bot className="w-4 h-4 text-indigo-500" /> Recent AI Agent Activity
            </h2>
            <Link
              href="/settings"
              className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1 font-medium"
            >
              Audit logs <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {stats.recent_ai_activity.length === 0 ? (
            <div className="text-center py-8 text-xs text-zinc-500">
              No AI generations recorded yet.
            </div>
          ) : (
            <div className="space-y-2.5">
              {stats.recent_ai_activity.map((log) => (
                <div
                  key={log.id}
                  className="p-3 rounded-lg border border-zinc-100 dark:border-zinc-800 text-xs space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                      {log.agent_name}
                    </span>
                    <span className="text-[10px] text-zinc-400 font-mono">
                      {log.latency_ms}ms • {log.total_tokens} tokens
                    </span>
                  </div>
                  <p className="text-[11px] text-zinc-600 dark:text-zinc-400 truncate">
                    {log.prompt_preview}
                  </p>
                  <div className="flex items-center justify-between text-[10px] text-zinc-400 pt-1">
                    <span>Provider: {log.provider} ({log.model})</span>
                    <span>{formatDate(log.created_at)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
