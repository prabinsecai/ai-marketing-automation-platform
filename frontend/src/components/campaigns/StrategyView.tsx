"use client";

import React from "react";
import {
  Sparkles,
  Target,
  Layers,
  Calendar,
  AlertTriangle,
  TrendingUp,
  Lightbulb,
  Radio,
} from "lucide-react";
import { CampaignStrategy } from "@/lib/types";
import { Button, Card, Badge } from "@/lib/ui";

interface StrategyViewProps {
  strategy?: CampaignStrategy | null;
  onGenerate: () => void;
  loading: boolean;
}

export const StrategyView: React.FC<StrategyViewProps> = ({
  strategy,
  onGenerate,
  loading,
}) => {
  if (!strategy) {
    return (
      <Card className="text-center py-12 px-4 border-dashed border-2">
        <div className="w-12 h-12 rounded-full bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center mx-auto mb-4">
          <Sparkles className="w-6 h-6" />
        </div>
        <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
          No Campaign Strategy Generated Yet
        </h3>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 max-w-md mx-auto mt-1 mb-6">
          Trigger the AI Marketing Strategist to analyze your product positioning, audience pain
          points, and campaign objectives to craft a verified go-to-market plan.
        </p>
        <Button
          variant="primary"
          onClick={onGenerate}
          loading={loading}
          icon={<Sparkles className="w-4 h-4" />}
        >
          Generate AI Campaign Strategy
        </Button>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Strategy Header & Action Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900/50 rounded-xl p-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-indigo-600 text-white flex items-center justify-center">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
              AI Marketing Strategist Brief
            </h3>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              Model: {strategy.model_used || "mock-marketing-agent-v1"} • Verified Grounding
            </p>
          </div>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={onGenerate}
          loading={loading}
          icon={<Sparkles className="w-3.5 h-3.5" />}
        >
          Regenerate Strategy
        </Button>
      </div>

      {/* Summary & Audience Reasoning */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="space-y-2">
          <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            <Target className="w-4 h-4" /> Executive Summary
          </div>
          <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed">
            {strategy.summary}
          </p>
        </Card>

        <Card className="space-y-2">
          <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            <Lightbulb className="w-4 h-4" /> Audience Reasoning & Psychology
          </div>
          <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed">
            {strategy.audience_reasoning}
          </p>
        </Card>
      </div>

      {/* Positioning & Key Message */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="space-y-2 bg-gradient-to-br from-white to-zinc-50 dark:from-zinc-900 dark:to-zinc-900/50">
          <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">
            Market Positioning
          </span>
          <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100 leading-snug">
            &quot;{strategy.positioning}&quot;
          </p>
        </Card>

        <Card className="space-y-2 bg-gradient-to-br from-white to-zinc-50 dark:from-zinc-900 dark:to-zinc-900/50">
          <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">
            Core Memorable Message
          </span>
          <p className="text-sm font-medium text-indigo-600 dark:text-indigo-400 leading-snug">
            &quot;{strategy.key_message}&quot;
          </p>
        </Card>
      </div>

      {/* Channel Strategy Breakdown */}
      <div>
        <h4 className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider mb-3 flex items-center gap-2">
          <Radio className="w-4 h-4 text-indigo-500" /> Channel Strategy & Tactics
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {strategy.channel_strategy.map((item, idx) => (
            <Card key={idx} className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-xs text-zinc-900 dark:text-zinc-100">
                  {item.channel}
                </span>
                <Badge
                  variant={item.priority === "Primary" ? "brand" : "outline"}
                >
                  {item.priority}
                </Badge>
              </div>
              <p className="text-xs text-zinc-600 dark:text-zinc-400">{item.rationale}</p>
              {item.tactics && item.tactics.length > 0 && (
                <ul className="space-y-1 pt-2 border-t border-zinc-100 dark:border-zinc-800">
                  {item.tactics.map((t, tIdx) => (
                    <li key={tIdx} className="text-[11px] text-zinc-500 dark:text-zinc-400 flex items-start gap-1.5">
                      <span className="text-indigo-500 font-bold">•</span>
                      <span>{t}</span>
                    </li>
                  ))}
                </ul>
              )}
            </Card>
          ))}
        </div>
      </div>

      {/* Campaign Themes */}
      <div>
        <h4 className="text-xs font-semibold text-zinc-900 dark:text-zinc-100 uppercase tracking-wider mb-3 flex items-center gap-2">
          <Layers className="w-4 h-4 text-indigo-500" /> Core Campaign Themes
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {strategy.campaign_themes.map((theme, idx) => (
            <Card key={idx} className="space-y-2">
              <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400">
                Theme {idx + 1}: {theme.theme}
              </span>
              <p className="text-xs font-medium text-zinc-900 dark:text-zinc-100 italic">
                &ldquo;{theme.hook}&rdquo;
              </p>
              <p className="text-[11px] text-zinc-500 dark:text-zinc-400">{theme.description}</p>
            </Card>
          ))}
        </div>
      </div>

      {/* CTA Strategy & Timeline */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="space-y-2">
          <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            <Target className="w-4 h-4" /> CTA Strategy & Ladder
          </div>
          <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed">
            {strategy.cta_strategy}
          </p>
        </Card>

        <Card className="space-y-2">
          <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            <Calendar className="w-4 h-4" /> Rollout Timeline Suggestion
          </div>
          <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed">
            {strategy.timeline_suggestion}
          </p>
        </Card>
      </div>

      {/* Future Success Metrics & Risks */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="space-y-3">
          <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 text-xs font-semibold uppercase tracking-wider">
            <TrendingUp className="w-4 h-4" /> Target Success Metrics & Benchmarks
          </div>
          <div className="space-y-2">
            {strategy.future_success_metrics.map((m, idx) => (
              <div
                key={idx}
                className="p-2.5 bg-zinc-50 dark:bg-zinc-800/60 rounded-lg border border-zinc-100 dark:border-zinc-800 text-xs space-y-1"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-zinc-900 dark:text-zinc-100">
                    {m.metric}
                  </span>
                  <span className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400">
                    {m.target_benchmark}
                  </span>
                </div>
                <p className="text-[11px] text-zinc-500 dark:text-zinc-400">{m.rationale}</p>
              </div>
            ))}
          </div>
        </Card>

        <Card className="space-y-3">
          <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400 text-xs font-semibold uppercase tracking-wider">
            <AlertTriangle className="w-4 h-4" /> Risks & Mitigations
          </div>
          <div className="space-y-2">
            {strategy.risks_assumptions.map((r, idx) => (
              <div
                key={idx}
                className="p-2.5 bg-zinc-50 dark:bg-zinc-800/60 rounded-lg border border-zinc-100 dark:border-zinc-800 text-xs space-y-1"
              >
                <p className="font-semibold text-zinc-900 dark:text-zinc-100">{r.risk}</p>
                <p className="text-[11px] text-zinc-500 dark:text-zinc-400">
                  <strong className="text-zinc-700 dark:text-zinc-300">Mitigation:</strong> {r.mitigation}
                </p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
