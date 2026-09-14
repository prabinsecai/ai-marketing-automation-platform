"use client";

import React, { useState } from "react";
import { Modal, Button } from "@/lib/ui";
import { ContentAsset } from "@/lib/types";
import { Check, X, AlertCircle } from "lucide-react";

interface ApprovalModalProps {
  isOpen: boolean;
  onClose: () => void;
  asset: ContentAsset | null;
  onApprove: (
    assetId: string,
    action: "APPROVE" | "REJECT" | "REQUEST_CHANGES",
    feedback?: string
  ) => Promise<void>;
}

export const ApprovalModal: React.FC<ApprovalModalProps> = ({
  isOpen,
  onClose,
  asset,
  onApprove,
}) => {
  const [action, setAction] = useState<"APPROVE" | "REJECT" | "REQUEST_CHANGES">("APPROVE");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);

  if (!asset) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      await onApprove(asset.id, action, feedback.trim() || undefined);
      setFeedback("");
      onClose();
    } catch (err) {
      alert(`Approval submission failed: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Review & Decision: ${asset.channel} Variation #${asset.variation_number}`}
      description="Record an official stakeholder review decision in the campaign governance log."
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-2">
            Decision Action
          </label>
          <div className="grid grid-cols-3 gap-2">
            <button
              type="button"
              onClick={() => setAction("APPROVE")}
              className={`flex flex-col items-center gap-1.5 p-3 rounded-lg border text-xs font-medium transition-all ${
                action === "APPROVE"
                  ? "bg-emerald-500/10 border-emerald-500 text-emerald-600 dark:text-emerald-400 font-semibold"
                  : "border-zinc-200 dark:border-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800"
              }`}
            >
              <Check className="w-4 h-4" />
              Approve
            </button>

            <button
              type="button"
              onClick={() => setAction("REQUEST_CHANGES")}
              className={`flex flex-col items-center gap-1.5 p-3 rounded-lg border text-xs font-medium transition-all ${
                action === "REQUEST_CHANGES"
                  ? "bg-amber-500/10 border-amber-500 text-amber-600 dark:text-amber-400 font-semibold"
                  : "border-zinc-200 dark:border-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800"
              }`}
            >
              <AlertCircle className="w-4 h-4" />
              Request Changes
            </button>

            <button
              type="button"
              onClick={() => setAction("REJECT")}
              className={`flex flex-col items-center gap-1.5 p-3 rounded-lg border text-xs font-medium transition-all ${
                action === "REJECT"
                  ? "bg-rose-500/10 border-rose-500 text-rose-600 dark:text-rose-400 font-semibold"
                  : "border-zinc-200 dark:border-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-zinc-800"
              }`}
            >
              <X className="w-4 h-4" />
              Reject
            </button>
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
            Reviewer Feedback / Comments (Optional)
          </label>
          <textarea
            rows={3}
            placeholder="Add any stakeholder remarks or required changes..."
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="flex justify-end gap-2 pt-3 border-t border-zinc-200 dark:border-zinc-800">
          <Button type="button" variant="outline" size="sm" onClick={onClose}>
            Cancel
          </Button>
          <Button
            type="submit"
            variant={action === "REJECT" ? "danger" : "primary"}
            size="sm"
            loading={loading}
          >
            Submit Decision
          </Button>
        </div>
      </form>
    </Modal>
  );
};
