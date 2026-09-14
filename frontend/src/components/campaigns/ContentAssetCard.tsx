"use client";

import React, { useState } from "react";
import {
  Mail,
  Share2,
  Tv,
  Check,
  Edit2,
  RefreshCw,
  History,
  ShieldCheck,
} from "lucide-react";
import { ContentAsset } from "@/lib/types";
import { Card, Badge, Button } from "@/lib/ui";
import { formatDate } from "@/lib/utils";

interface ContentAssetCardProps {
  asset: ContentAsset;
  onEdit: (asset: ContentAsset) => void;
  onRegenerate: (asset: ContentAsset) => void;
  onSelect: (assetId: string) => void;
  onReview: (asset: ContentAsset) => void;
}

export const ContentAssetCard: React.FC<ContentAssetCardProps> = ({
  asset,
  onEdit,
  onRegenerate,
  onSelect,
  onReview,
}) => {
  const [showHistory, setShowHistory] = useState(false);

  const getChannelIcon = () => {
    switch (asset.channel) {
      case "EMAIL":
        return <Mail className="w-4 h-4 text-indigo-500" />;
      case "SOCIAL":
        return <Share2 className="w-4 h-4 text-blue-500" />;
      case "ADVERTISEMENT":
        return <Tv className="w-4 h-4 text-emerald-500" />;
      default:
        return null;
    }
  };

  return (
    <Card className="flex flex-col justify-between space-y-4 relative border-zinc-200 dark:border-zinc-800">
      {/* Top Header */}
      <div>
        <div className="flex items-center justify-between gap-2 mb-2">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-zinc-100 dark:bg-zinc-800">
              {getChannelIcon()}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">
                  Variation #{asset.variation_number}
                </span>
                {asset.platform && (
                  <span className="text-[11px] text-zinc-400 font-medium">
                    • {asset.platform}
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="status" status={asset.status} dot>
              {asset.status.replace("_", " ")}
            </Badge>

            {/* Selection Checkbox */}
            <button
              onClick={() => onSelect(asset.id)}
              className={`p-1.5 rounded-lg border text-xs font-medium transition-all flex items-center gap-1 ${
                asset.is_selected
                  ? "bg-indigo-600 text-white border-indigo-600"
                  : "bg-zinc-50 dark:bg-zinc-800/80 text-zinc-400 border-zinc-200 dark:border-zinc-700 hover:text-zinc-200"
              }`}
              title={asset.is_selected ? "Selected for live campaign" : "Select for campaign"}
            >
              <Check className="w-3.5 h-3.5" />
              <span className="text-[10px] pr-1">{asset.is_selected ? "Selected" : "Select"}</span>
            </button>
          </div>
        </div>

        {/* Content Body Display */}
        <div className="space-y-2 mt-3 pt-3 border-t border-zinc-100 dark:border-zinc-800/80">
          {/* Email Subject / Ad Headline */}
          {asset.title && (
            <div>
              <span className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider block">
                {asset.channel === "EMAIL" ? "Subject Line" : "Headline"}
              </span>
              <p className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">
                {asset.title}
              </p>
            </div>
          )}

          {/* Email Preview */}
          {asset.preview_text && (
            <div>
              <span className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider block">
                Preheader Snippet
              </span>
              <p className="text-xs text-zinc-600 dark:text-zinc-400 italic">
                {asset.preview_text}
              </p>
            </div>
          )}

          {/* Social Hook */}
          {asset.hook && (
            <div>
              <span className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider block">
                Opening Hook
              </span>
              <p className="text-xs font-medium text-indigo-600 dark:text-indigo-400">
                {asset.hook}
              </p>
            </div>
          )}

          {/* Main Body */}
          <div>
            <span className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider block mb-1">
              {asset.channel === "EMAIL"
                ? "Body Copy"
                : asset.channel === "SOCIAL"
                ? "Caption Copy"
                : "Primary Text"}
            </span>
            <div className="bg-zinc-50 dark:bg-zinc-800/40 p-3 rounded-lg border border-zinc-100 dark:border-zinc-800 text-xs text-zinc-800 dark:text-zinc-200 whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">
              {asset.body}
            </div>
          </div>

          {/* CTA Button */}
          {asset.cta && (
            <div className="flex items-center gap-2 pt-1">
              <span className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider">
                Call to Action:
              </span>
              <span className="px-2.5 py-1 rounded bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 text-xs font-medium border border-indigo-100 dark:border-indigo-900/50">
                {asset.cta}
              </span>
            </div>
          )}

          {/* Social Hashtags */}
          {asset.hashtags && asset.hashtags.length > 0 && (
            <div className="flex flex-wrap gap-1 pt-1">
              {asset.hashtags.map((tag, tIdx) => (
                <span
                  key={tIdx}
                  className="text-[10px] text-zinc-500 dark:text-zinc-400 bg-zinc-100 dark:bg-zinc-800 px-1.5 py-0.5 rounded"
                >
                  #{tag.replace(/^#/, "")}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Footer & Actions */}
      <div className="pt-3 border-t border-zinc-100 dark:border-zinc-800 space-y-2">
        <div className="flex items-center justify-between text-[11px] text-zinc-400">
          <span>Model: {asset.model_used || "mock-agent"}</span>
          {asset.edit_history && asset.edit_history.length > 0 && (
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="flex items-center gap-1 text-indigo-500 hover:text-indigo-400 font-medium transition-colors"
            >
              <History className="w-3 h-3" />
              {asset.edit_history.length} {asset.edit_history.length === 1 ? "edit" : "edits"}
            </button>
          )}
        </div>

        {/* Edit History Expander */}
        {showHistory && asset.edit_history && (
          <div className="p-2.5 bg-zinc-100 dark:bg-zinc-800/80 rounded-lg text-[10px] space-y-1.5 border border-zinc-200 dark:border-zinc-700">
            <span className="font-semibold text-zinc-700 dark:text-zinc-300 block">
              Version History Log
            </span>
            {asset.edit_history.map((h, hIdx) => (
              <div key={hIdx} className="text-zinc-500 dark:text-zinc-400 pb-1 border-b border-zinc-200 dark:border-zinc-700/50 last:border-0 last:pb-0">
                <span className="font-medium text-zinc-700 dark:text-zinc-300">
                  {formatDate(h.edited_at)}:
                </span>{" "}
                {h.summary || "Copy edited"}
              </div>
            ))}
          </div>
        )}

        {/* Action Buttons Toolbar */}
        <div className="flex items-center justify-between gap-2 pt-1">
          <div className="flex items-center gap-1.5">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onEdit(asset)}
              icon={<Edit2 className="w-3 h-3" />}
            >
              Edit
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onRegenerate(asset)}
              icon={<RefreshCw className="w-3 h-3" />}
            >
              Regenerate
            </Button>
          </div>

          <Button
            variant="secondary"
            size="sm"
            onClick={() => onReview(asset)}
            icon={<ShieldCheck className="w-3.5 h-3.5 text-indigo-500" />}
          >
            Review
          </Button>
        </div>
      </div>
    </Card>
  );
};
