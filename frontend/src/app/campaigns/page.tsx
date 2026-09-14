"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import {
  Megaphone,
  Search,
  ArrowRight,
  Calendar,
  DollarSign,
} from "lucide-react";
import { api } from "@/lib/api";
import { Campaign } from "@/lib/types";
import { Card, Badge } from "@/lib/ui";
import { formatDate } from "@/lib/utils";

const statusTabs = [
  { key: "ALL", label: "All Campaigns" },
  { key: "DRAFT", label: "Draft" },
  { key: "STRATEGY_GENERATED", label: "Strategy" },
  { key: "CONTENT_GENERATED", label: "Content" },
  { key: "IN_REVIEW", label: "In Review" },
  { key: "APPROVED", label: "Approved" },
];

export default function CampaignsListPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedStatus, setSelectedStatus] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState("");

  const loadCampaigns = useCallback(async () => {
    try {
      setLoading(true);
      const statusParam = selectedStatus === "ALL" ? undefined : selectedStatus;
      const data = await api.listCampaigns(undefined, statusParam);
      setCampaigns(data);
    } catch (err) {
      console.error("Failed to load campaigns", err);
    } finally {
      setLoading(false);
    }
  }, [selectedStatus]);

  useEffect(() => {
    loadCampaigns();
  }, [loadCampaigns]);

  const filteredCampaigns = campaigns.filter(
    (c) =>
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.objective.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 tracking-tight">
            Marketing Campaigns
          </h1>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
            Orchestrate B2B campaigns from strategic positioning to multi-channel copy approvals.
          </p>
        </div>
      </div>

      {/* Filter Tabs & Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-2 sm:pb-0">
          {statusTabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setSelectedStatus(tab.key)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors whitespace-nowrap ${
                selectedStatus === tab.key
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "bg-white dark:bg-zinc-900 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-zinc-400" />
          <input
            type="text"
            placeholder="Search campaigns..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full text-xs pl-8 pr-3 py-1.5 rounded-lg border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Campaign Cards Grid */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-6 h-6 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin" />
        </div>
      ) : filteredCampaigns.length === 0 ? (
        <Card className="text-center py-12 border-dashed">
          <Megaphone className="w-8 h-8 text-zinc-400 mx-auto mb-2" />
          <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
            No campaigns found
          </p>
          <p className="text-xs text-zinc-500 mt-1">
            {searchQuery
              ? "Try adjusting your search filters."
              : "Create your first campaign or seed demo data using the navbar button."}
          </p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredCampaigns.map((camp) => (
            <Link
              key={camp.id}
              href={`/campaigns/${camp.id}`}
              className="block group focus:outline-none"
            >
              <Card className="h-full flex flex-col justify-between hover:border-indigo-500/50 hover:shadow-md transition-all">
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors line-clamp-1">
                      {camp.name}
                    </h3>
                    <Badge variant="status" status={camp.status} dot>
                      {camp.status.replace("_", " ")}
                    </Badge>
                  </div>

                  <p className="text-xs text-zinc-600 dark:text-zinc-400 line-clamp-2 leading-relaxed">
                    {camp.objective}
                  </p>
                </div>

                <div className="pt-4 mt-4 border-t border-zinc-100 dark:border-zinc-800/80 space-y-2 text-[11px] text-zinc-500 dark:text-zinc-400">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1">
                      <DollarSign className="w-3.5 h-3.5 text-zinc-400" /> {camp.budget || "Flexible"}
                    </span>
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5 text-zinc-400" /> {camp.target_timeline || "Standard"}
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-[10px] text-zinc-400 pt-1">
                    <span>Created {formatDate(camp.created_at)}</span>
                    <span className="text-indigo-600 dark:text-indigo-400 font-medium flex items-center gap-0.5 group-hover:translate-x-0.5 transition-transform">
                      Open Campaign <ArrowRight className="w-3 h-3" />
                    </span>
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
