"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import {
  Zap,
  RefreshCw,
  AlertTriangle,
  ExternalLink,
} from "lucide-react";
import { api } from "@/lib/api";
import { CampaignExecution, Campaign } from "@/lib/types";
import { Button, Card, Badge } from "@/lib/ui";
import { formatDate } from "@/lib/utils";

export default function ExecutionsPage() {
  const [executions, setExecutions] = useState<CampaignExecution[]>([]);
  const [campaigns, setCampaigns] = useState<Record<string, Campaign>>({});
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [retryingId, setRetryingId] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [execList, campList] = await Promise.all([
        api.listExecutions(),
        api.listCampaigns(),
      ]);
      setExecutions(execList);

      const campMap: Record<string, Campaign> = {};
      campList.forEach((c) => {
        campMap[c.id] = c;
      });
      setCampaigns(campMap);
    } catch (err) {
      console.error("Failed to load executions:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleRetry = async (id: string) => {
    try {
      setRetryingId(id);
      await api.retryExecution(id);
      await loadData();
    } catch (err: any) {
      alert(`Retry failed: ${err.message || err}`);
    } finally {
      setRetryingId(null);
    }
  };

  const filteredExecutions = executions.filter((e) => {
    if (statusFilter !== "ALL" && e.status !== statusFilter) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const campaignName = (campaigns[e.campaign_id]?.name || "").toLowerCase();
      const idMatch = e.id.toLowerCase().includes(q);
      const campMatch = campaignName.includes(q);
      const n8nMatch = (e.n8n_execution_id || "").toLowerCase().includes(q);
      return idMatch || campMatch || n8nMatch;
    }
    return true;
  });

  const stats = {
    total: executions.length,
    success: executions.filter((e) => e.status === "SUCCESS").length,
    running: executions.filter((e) => e.status === "RUNNING" || e.status === "RETRYING").length,
    failed: executions.filter((e) => e.status === "FAILED").length,
    escalated: executions.filter((e) => e.status === "ESCALATED").length,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 tracking-tight flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-500" />
            Campaign Execution & Automation Center
          </h1>
          <p className="text-xs text-zinc-500 mt-1">
            Real-time LangGraph multi-node execution state, local n8n workflow dispatching, retry loops, and human escalation.
          </p>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={loadData}
          icon={<RefreshCw className="w-3.5 h-3.5" />}
        >
          Refresh Feed
        </Button>
      </div>

      {/* KPI Stats Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        <Card className="p-3 text-center">
          <span className="text-[10px] font-semibold uppercase text-zinc-400 block">Total Runs</span>
          <span className="text-lg font-bold text-zinc-900 dark:text-zinc-100">{stats.total}</span>
        </Card>
        <Card className="p-3 text-center border-emerald-200 dark:border-emerald-900/40">
          <span className="text-[10px] font-semibold uppercase text-emerald-600 dark:text-emerald-400 block">Succeeded</span>
          <span className="text-lg font-bold text-emerald-600 dark:text-emerald-400">{stats.success}</span>
        </Card>
        <Card className="p-3 text-center border-indigo-200 dark:border-indigo-900/40">
          <span className="text-[10px] font-semibold uppercase text-indigo-600 dark:text-indigo-400 block">Running / Retrying</span>
          <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400">{stats.running}</span>
        </Card>
        <Card className="p-3 text-center border-rose-200 dark:border-rose-900/40">
          <span className="text-[10px] font-semibold uppercase text-rose-600 dark:text-rose-400 block">Failed</span>
          <span className="text-lg font-bold text-rose-600 dark:text-rose-400">{stats.failed}</span>
        </Card>
        <Card className="p-3 text-center border-amber-200 dark:border-amber-900/40">
          <span className="text-[10px] font-semibold uppercase text-amber-600 dark:text-amber-400 block">Escalated</span>
          <span className="text-lg font-bold text-amber-600 dark:text-amber-400">{stats.escalated}</span>
        </Card>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-2 sm:pb-0">
          {["ALL", "SUCCESS", "RUNNING", "FAILED", "ESCALATED", "RETRYING"].map((s) => (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                statusFilter === s
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800"
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        <div className="w-full sm:w-64">
          <input
            type="text"
            placeholder="Search executions..."
            value={searchQuery}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchQuery(e.target.value)}
            className="w-full text-xs px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Executions Feed */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-8 h-8 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin" />
        </div>
      ) : filteredExecutions.length === 0 ? (
        <Card className="text-center py-16 border-dashed border-2">
          <Zap className="w-10 h-10 text-zinc-400 mx-auto mb-3" />
          <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
            No Executions Matching Query
          </h3>
          <p className="text-xs text-zinc-500 max-w-sm mx-auto mt-1 mb-4">
            Approve a campaign to unlock automated LangGraph agent dispatching and n8n webhook triggers.
          </p>
          <Link href="/campaigns">
            <Button variant="primary" size="sm">
              Explore Campaigns
            </Button>
          </Link>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredExecutions.map((exec) => {
            const campaign = campaigns[exec.campaign_id];
            return (
              <Card
                key={exec.id}
                className="space-y-4 border-l-4 border-l-indigo-600 transition-all hover:shadow-md"
              >
                {/* Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-zinc-100 dark:border-zinc-800">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <Link
                        href={`/campaigns/${exec.campaign_id}`}
                        className="text-sm font-bold text-zinc-900 dark:text-zinc-100 hover:text-indigo-600 transition-colors flex items-center gap-1.5"
                      >
                        {campaign?.name || `Campaign: ${exec.campaign_id.slice(0, 8)}...`}
                        <ExternalLink className="w-3.5 h-3.5 text-zinc-400" />
                      </Link>

                      <Badge
                        variant="status"
                        status={
                          exec.status === "SUCCESS"
                            ? "APPROVED"
                            : exec.status === "FAILED"
                            ? "REJECTED"
                            : exec.status === "ESCALATED"
                            ? "DRAFT"
                            : "IN_REVIEW"
                        }
                      >
                        {exec.status}
                      </Badge>

                      <span className="text-[10px] px-2 py-0.5 rounded bg-zinc-100 dark:bg-zinc-800 text-zinc-500 font-mono">
                        Retry: {exec.retry_count}/{exec.max_retries}
                      </span>
                    </div>

                    <div className="text-[11px] text-zinc-400 flex flex-wrap items-center gap-3">
                      <span>ID: <code className="font-mono text-zinc-500">{exec.id.slice(0, 13)}...</code></span>
                      <span>Trigger: {exec.trigger_source}</span>
                      <span>Started: {formatDate(exec.started_at || exec.created_at)}</span>
                      {exec.completed_at && <span>Completed: {formatDate(exec.completed_at)}</span>}
                      {exec.n8n_execution_id && (
                        <span className="text-indigo-500 font-mono">
                          n8n: {exec.n8n_execution_id}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <Link href={`/campaigns/${exec.campaign_id}`}>
                      <Button variant="outline" size="sm">
                        View Campaign
                      </Button>
                    </Link>

                    {(exec.status === "FAILED" || exec.status === "ESCALATED") && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleRetry(exec.id)}
                        loading={retryingId === exec.id}
                        icon={<RefreshCw className="w-3.5 h-3.5" />}
                        className="text-amber-600 dark:text-amber-400 border-amber-300 dark:border-amber-800 hover:bg-amber-50 dark:hover:bg-amber-950/40"
                      >
                        {exec.retry_count >= exec.max_retries ? "Escalate" : "Retry Run"}
                      </Button>
                    )}
                  </div>
                </div>

                {/* Error Banner */}
                {exec.error_message && (
                  <div className="p-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/50 rounded-lg text-xs text-rose-800 dark:text-rose-200 flex items-start gap-2">
                    <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-semibold block">Failure Diagnostics:</span>
                      <p className="mt-0.5">{exec.error_message}</p>
                    </div>
                  </div>
                )}

                {/* LangGraph Steps */}
                {exec.steps && exec.steps.length > 0 && (
                  <div className="space-y-2">
                    <span className="text-[11px] font-semibold uppercase tracking-wider text-zinc-500 block">
                      Execution Graph Node Sequence ({exec.steps.length} Steps)
                    </span>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2">
                      {exec.steps.map((step, idx) => (
                        <div
                          key={step.id || idx}
                          className="p-2.5 bg-zinc-50 dark:bg-zinc-900 rounded-lg border border-zinc-200 dark:border-zinc-800 text-xs space-y-1"
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-mono font-bold text-zinc-800 dark:text-zinc-200 text-[11px] truncate">
                              {step.step_name}
                            </span>
                            <Badge
                              variant="status"
                              status={step.status === "SUCCESS" ? "APPROVED" : step.status === "FAILED" ? "REJECTED" : "IN_REVIEW"}
                            >
                              {step.status}
                            </Badge>
                          </div>
                          <span className="text-[10px] text-zinc-400 block">
                            Type: {step.step_type}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Trace Accordion */}
                {exec.agent_trace && exec.agent_trace.length > 0 && (
                  <details className="text-xs pt-1 text-zinc-500">
                    <summary className="cursor-pointer font-semibold hover:text-zinc-800 dark:hover:text-zinc-200">
                      View LangGraph Execution Logs ({exec.agent_trace.length} entries)
                    </summary>
                    <div className="mt-2 space-y-1 p-3 bg-zinc-950 text-zinc-300 rounded-lg font-mono text-[11px] max-h-52 overflow-y-auto">
                      {exec.agent_trace.map((tr, i) => (
                        <div key={i} className="flex items-start gap-2 border-b border-zinc-800/60 pb-1 mb-1">
                          <span className="text-zinc-500 shrink-0">[{tr.timestamp?.split("T")[1]?.slice(0, 8)}]</span>
                          <span className="text-indigo-400 shrink-0 font-bold">{tr.node}:</span>
                          <span className="text-zinc-200">{tr.message}</span>
                        </div>
                      ))}
                    </div>
                  </details>
                )}
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
