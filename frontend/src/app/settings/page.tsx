"use client";

import React, { useEffect, useState } from "react";
import {
  Bot,
  Sliders,
  Shield,
  Clock,
  Building,
} from "lucide-react";
import { api } from "@/lib/api";
import { AILog, Workspace } from "@/lib/types";
import { Card, Badge, Button } from "@/lib/ui";
import { formatDate } from "@/lib/utils";

export default function SettingsPage() {
  const [logs, setLogs] = useState<AILog[]>([]);
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Workspace edit state
  const [brandGuidelines, setBrandGuidelines] = useState("");
  const [savingWs, setSavingWs] = useState(false);

  useEffect(() => {
    loadSettingsData();
  }, []);

  const loadSettingsData = async () => {
    try {
      setLoading(true);
      const [h, wsList, aiLogs] = await Promise.all([
        api.getHealth(),
        api.listWorkspaces(),
        api.listAILogs(),
      ]);
      setHealth(h);
      setLogs(aiLogs);
      if (wsList.length > 0) {
        setWorkspace(wsList[0]);
        setBrandGuidelines(wsList[0].brand_guidelines || "");
      }
    } catch (err) {
      console.error("Failed to load settings data", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateBrandGuidelines = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!workspace) return;
    try {
      setSavingWs(true);
      const updated = await api.updateWorkspace(workspace.id, {
        brand_guidelines: brandGuidelines,
      });
      setWorkspace(updated);
      alert("Brand guidelines updated successfully!");
    } catch (err) {
      alert(`Failed to update workspace: ${err}`);
    } finally {
      setSavingWs(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 tracking-tight">
          AI Architecture & Settings
        </h1>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
          Provider status, brand tone constraints, and AI generation audit logs.
        </p>
      </div>

      {/* AI Provider Config Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <Card className="space-y-2 border-indigo-500/30 bg-indigo-50/20 dark:bg-indigo-950/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-1.5">
              <Bot className="w-4 h-4 text-indigo-500" /> Active LLM Mode
            </span>
            <Badge variant="brand">{health?.llm_mode?.toUpperCase() || "MOCK"}</Badge>
          </div>
          <p className="text-xs text-zinc-600 dark:text-zinc-400">
            {health?.llm_mode === "mock"
              ? "Running in zero-cost deterministic mock provider mode with full domain fidelity."
              : `Connected to live ${health?.llm_mode} provider endpoint.`}
          </p>
        </Card>

        <Card className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-1.5">
              <Shield className="w-4 h-4 text-emerald-500" /> Grounding Compliance
            </span>
            <Badge variant="status" status="APPROVED">
              Enforced
            </Badge>
          </div>
          <p className="text-xs text-zinc-600 dark:text-zinc-400">
            Anti-hallucination prompts strictly anchor copy to verified product specs & guidelines.
          </p>
        </Card>

        <Card className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-1.5">
              <Sliders className="w-4 h-4 text-blue-500" /> API Gateway
            </span>
            <Badge variant="outline">{health?.version || "v1.0.0"}</Badge>
          </div>
          <p className="text-xs text-zinc-600 dark:text-zinc-400">
            FastAPI backend with Pydantic structured output validation and Alembic migrations.
          </p>
        </Card>
      </div>

      {/* Workspace Brand Guidelines Editor */}
      <Card className="space-y-4">
        <div className="flex items-center gap-2 pb-2 border-b border-zinc-100 dark:border-zinc-800">
          <Building className="w-4 h-4 text-indigo-500" />
          <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
            Workspace Brand Guidelines & Constraints
          </h2>
        </div>

        {workspace && (
          <form onSubmit={handleUpdateBrandGuidelines} className="space-y-4">
            <div className="grid grid-cols-2 gap-4 text-xs">
              <div>
                <span className="font-semibold text-zinc-700 dark:text-zinc-300 block">
                  Workspace:
                </span>
                <span className="text-zinc-500">{workspace.name}</span>
              </div>
              <div>
                <span className="font-semibold text-zinc-700 dark:text-zinc-300 block">
                  Industry:
                </span>
                <span className="text-zinc-500">{workspace.industry || "B2B SaaS"}</span>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Tone, Style & Negative Constraints
              </label>
              <textarea
                rows={4}
                value={brandGuidelines}
                onChange={(e) => setBrandGuidelines(e.target.value)}
                placeholder="Specify tone of voice, prohibited terms, and brand positioning rules..."
                className="w-full text-xs font-mono px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div className="flex justify-end">
              <Button type="submit" variant="primary" size="sm" loading={savingWs}>
                Update Brand Guidelines
              </Button>
            </div>
          </form>
        )}
      </Card>

      {/* AI Execution Logs Audit Viewer */}
      <Card className="space-y-4">
        <div className="flex items-center justify-between pb-2 border-b border-zinc-100 dark:border-zinc-800">
          <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
            <Clock className="w-4 h-4 text-indigo-500" /> AI Execution Audit Logs
          </h2>
          <span className="text-xs text-zinc-400">{logs.length} logged generations</span>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="w-6 h-6 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin" />
          </div>
        ) : logs.length === 0 ? (
          <div className="text-center py-8 text-xs text-zinc-500">No AI execution logs recorded yet.</div>
        ) : (
          <div className="space-y-3">
            {logs.map((log) => (
              <div
                key={log.id}
                className="p-3.5 rounded-lg border border-zinc-100 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-800/30 text-xs space-y-2"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-indigo-600 dark:text-indigo-400">
                      {log.agent_name}
                    </span>
                    <Badge variant="outline">
                      {log.provider} ({log.model})
                    </Badge>
                  </div>
                  <Badge variant={log.status === "SUCCESS" ? "status" : "outline"} status={log.status}>
                    {log.status}
                  </Badge>
                </div>

                <p className="text-[11px] text-zinc-600 dark:text-zinc-300 font-mono bg-white dark:bg-zinc-900 p-2 rounded border border-zinc-200 dark:border-zinc-800 truncate">
                  Prompt: {log.prompt_preview}
                </p>

                {log.response_preview && (
                  <p className="text-[11px] text-zinc-500 dark:text-zinc-400 font-mono bg-white dark:bg-zinc-900 p-2 rounded border border-zinc-200 dark:border-zinc-800 truncate">
                    Output: {log.response_preview}
                  </p>
                )}

                <div className="flex items-center justify-between text-[10px] text-zinc-400 pt-1">
                  <span>
                    Latency: {log.latency_ms}ms • Usage: {log.prompt_tokens} in / {log.completion_tokens} out ({log.total_tokens} total)
                  </span>
                  <span>{formatDate(log.created_at)}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
