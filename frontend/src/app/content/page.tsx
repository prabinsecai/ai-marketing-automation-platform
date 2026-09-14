"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import {
  FileText,
  Search,
  ArrowRight,
} from "lucide-react";
import { api } from "@/lib/api";
import { ContentAsset } from "@/lib/types";
import { Card, Badge } from "@/lib/ui";
import { formatDate } from "@/lib/utils";

export default function ContentLibraryPage() {
  const [assets, setAssets] = useState<ContentAsset[]>([]);
  const [loading, setLoading] = useState(true);
  const [channelFilter, setChannelFilter] = useState("ALL");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [searchQuery, setSearchQuery] = useState("");

  const loadContent = useCallback(async () => {
    try {
      setLoading(true);
      const ch = channelFilter === "ALL" ? undefined : channelFilter;
      const st = statusFilter === "ALL" ? undefined : statusFilter;
      const data = await api.listContentAssets(undefined, ch, st);
      setAssets(data);
    } catch (err) {
      console.error("Failed to load content assets", err);
    } finally {
      setLoading(false);
    }
  }, [channelFilter, statusFilter]);

  useEffect(() => {
    loadContent();
  }, [loadContent]);

  const filteredAssets = assets.filter(
    (a) =>
      (a.title && a.title.toLowerCase().includes(searchQuery.toLowerCase())) ||
      a.body.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (a.cta && a.cta.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 tracking-tight">
            AI Content Library
          </h1>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
            Centralized repository of generated Email, Social, and Ad variations across all campaigns.
          </p>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
        <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-2 sm:pb-0">
          {["ALL", "EMAIL", "SOCIAL", "ADVERTISEMENT"].map((ch) => (
            <button
              key={ch}
              onClick={() => setChannelFilter(ch)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                channelFilter === ch
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800"
              }`}
            >
              {ch === "ALL" ? "All Channels" : ch}
            </button>
          ))}

          <div className="h-4 w-px bg-zinc-300 dark:bg-zinc-700 mx-1" />

          {["ALL", "DRAFT", "IN_REVIEW", "APPROVED"].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`text-xs px-2.5 py-1.5 rounded-lg font-medium transition-colors ${
                statusFilter === st
                  ? "bg-zinc-800 text-white dark:bg-zinc-700"
                  : "bg-transparent text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
              }`}
            >
              {st === "ALL" ? "All Statuses" : st.replace("_", " ")}
            </button>
          ))}
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-zinc-400" />
          <input
            type="text"
            placeholder="Search copy..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full text-xs pl-8 pr-3 py-1.5 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-6 h-6 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin" />
        </div>
      ) : filteredAssets.length === 0 ? (
        <Card className="text-center py-12 border-dashed">
          <FileText className="w-8 h-8 text-zinc-400 mx-auto mb-2" />
          <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
            No content assets found
          </p>
          <p className="text-xs text-zinc-500 mt-1">
            Generate content within your campaigns or adjust your filter selection.
          </p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAssets.map((asset) => (
            <Card key={asset.id} className="flex flex-col justify-between space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">
                      {asset.channel} Var #{asset.variation_number}
                    </span>
                    {asset.platform && (
                      <span className="text-[11px] text-zinc-400">• {asset.platform}</span>
                    )}
                  </div>
                  <Badge variant="status" status={asset.status} dot>
                    {asset.status.replace("_", " ")}
                  </Badge>
                </div>

                {asset.title && (
                  <p className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">
                    {asset.title}
                  </p>
                )}

                {asset.hook && (
                  <p className="text-xs font-medium text-indigo-600 dark:text-indigo-400 italic">
                    {asset.hook}
                  </p>
                )}

                <div className="p-3 bg-zinc-50 dark:bg-zinc-800/40 rounded-lg border border-zinc-100 dark:border-zinc-800 text-xs text-zinc-700 dark:text-zinc-300 line-clamp-4 whitespace-pre-wrap leading-relaxed">
                  {asset.body}
                </div>

                {asset.cta && (
                  <p className="text-[11px] text-zinc-500 dark:text-zinc-400">
                    <strong className="text-zinc-700 dark:text-zinc-300">CTA:</strong> {asset.cta}
                  </p>
                )}
              </div>

              <div className="pt-3 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between text-[11px]">
                <span className="text-zinc-400">{formatDate(asset.created_at)}</span>
                <Link
                  href={`/campaigns/${asset.campaign_id}`}
                  className="text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1 font-medium"
                >
                  View Campaign <ArrowRight className="w-3 h-3" />
                </Link>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
