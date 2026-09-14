"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import {
  ShieldCheck,
  CheckCircle2,
  Clock,
  ArrowRight,
} from "lucide-react";
import { api } from "@/lib/api";
import { ContentAsset, Approval } from "@/lib/types";
import { Card, Badge, Button } from "@/lib/ui";
import { formatDate } from "@/lib/utils";
import { ApprovalModal } from "@/components/campaigns/ApprovalModal";

export default function ApprovalsQueuePage() {
  const [inReviewAssets, setInReviewAssets] = useState<ContentAsset[]>([]);
  const [approvalsLog, setApprovalsLog] = useState<Approval[]>([]);
  const [loading, setLoading] = useState(true);
  const [reviewingAsset, setReviewingAsset] = useState<ContentAsset | null>(null);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [assets, logs] = await Promise.all([
        api.listContentAssets(undefined, undefined, "IN_REVIEW"),
        api.listApprovals(),
      ]);
      setInReviewAssets(assets);
      setApprovalsLog(logs);
    } catch (err) {
      console.error("Failed to load approvals queue data", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleDecision = async (
    assetId: string,
    action: "APPROVE" | "REJECT" | "REQUEST_CHANGES",
    feedback?: string
  ) => {
    await api.approveContentAsset(assetId, action, feedback);
    await loadData();
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 tracking-tight">
          Governance & Approvals Queue
        </h1>
        <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
          Enterprise review gates ensuring all AI generated copy aligns with brand guidelines before live deployment.
        </p>
      </div>

      {/* Pending Items Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
            <Clock className="w-4 h-4 text-amber-500" /> Pending Review Items ({inReviewAssets.length})
          </h2>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="w-6 h-6 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin" />
          </div>
        ) : inReviewAssets.length === 0 ? (
          <Card className="text-center py-10 border-dashed">
            <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
            <p className="text-sm font-semibold text-zinc-800 dark:text-zinc-200">
              Inbox Zero: All Items Reviewed
            </p>
            <p className="text-xs text-zinc-500 mt-0.5">
              No content assets are currently pending stakeholder review.
            </p>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {inReviewAssets.map((asset) => (
              <Card key={asset.id} className="flex flex-col justify-between space-y-4">
                <div className="space-y-2.5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">
                      {asset.channel} Var #{asset.variation_number}
                    </span>
                    <Badge variant="status" status="IN_REVIEW" dot>
                      In Review
                    </Badge>
                  </div>

                  {asset.title && (
                    <p className="text-xs font-semibold text-zinc-900 dark:text-zinc-100">
                      {asset.title}
                    </p>
                  )}

                  <div className="p-3 bg-zinc-50 dark:bg-zinc-800/40 rounded-lg text-xs text-zinc-700 dark:text-zinc-300 line-clamp-4 leading-relaxed">
                    {asset.body}
                  </div>

                  {asset.cta && (
                    <p className="text-[11px] text-zinc-500">
                      <strong className="text-zinc-700 dark:text-zinc-300">CTA:</strong> {asset.cta}
                    </p>
                  )}
                </div>

                <div className="pt-3 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between gap-2">
                  <Link
                    href={`/campaigns/${asset.campaign_id}`}
                    className="text-[11px] text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-0.5"
                  >
                    View Campaign <ArrowRight className="w-3 h-3" />
                  </Link>

                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => setReviewingAsset(asset)}
                    icon={<ShieldCheck className="w-3.5 h-3.5" />}
                  >
                    Review & Decide
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Decision Audit Log Table */}
      <Card className="space-y-4">
        <div className="flex items-center justify-between pb-2 border-b border-zinc-100 dark:border-zinc-800">
          <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-indigo-500" /> Historical Audit Trail
          </h2>
          <span className="text-xs text-zinc-400">{approvalsLog.length} recorded decisions</span>
        </div>

        {approvalsLog.length === 0 ? (
          <div className="text-center py-8 text-xs text-zinc-500">No review decisions logged yet.</div>
        ) : (
          <div className="space-y-2.5">
            {approvalsLog.map((log) => (
              <div
                key={log.id}
                className="p-3 rounded-lg border border-zinc-100 dark:border-zinc-800 text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-2"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant="status" status={log.action}>
                      {log.action}
                    </Badge>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200">
                      {log.user_id ? "Marcus Vance (Reviewer)" : "Authorized Stakeholder"}
                    </span>
                  </div>
                  {log.feedback && (
                    <p className="text-zinc-600 dark:text-zinc-400 italic">
                      &quot;{log.feedback}&quot;
                    </p>
                  )}
                </div>

                <div className="text-[10px] text-zinc-400 whitespace-nowrap">
                  {formatDate(log.created_at)}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Modal */}
      <ApprovalModal
        isOpen={!!reviewingAsset}
        onClose={() => setReviewingAsset(null)}
        asset={reviewingAsset}
        onApprove={handleDecision}
      />
    </div>
  );
}
