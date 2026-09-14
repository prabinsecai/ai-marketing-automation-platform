"use client";

import React, { useState } from "react";
import { Modal, Button } from "@/lib/ui";
import { ContentAsset } from "@/lib/types";
import { RefreshCw } from "lucide-react";

interface RegenerateModalProps {
  isOpen: boolean;
  onClose: () => void;
  asset: ContentAsset | null;
  onRegenerate: (assetId: string, instructions?: string) => Promise<void>;
}

export const RegenerateModal: React.FC<RegenerateModalProps> = ({
  isOpen,
  onClose,
  asset,
  onRegenerate,
}) => {
  const [instructions, setInstructions] = useState("");
  const [loading, setLoading] = useState(false);

  if (!asset) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      await onRegenerate(asset.id, instructions.trim() || undefined);
      setInstructions("");
      onClose();
    } catch (err) {
      alert(`Regeneration failed: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Regenerate ${asset.channel} Variation #${asset.variation_number}`}
      description="Instruct the AI Content Agent on specific tone adjustments, hooks, or focus areas for this variation."
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
            Revision Instructions (Optional)
          </label>
          <textarea
            rows={4}
            placeholder="e.g., Emphasize the 70% reduction in setup time more aggressively, make the opening hook punchier, or use a more consultative tone..."
            value={instructions}
            onChange={(e) => setInstructions(e.target.value)}
            className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="flex justify-end gap-2 pt-3 border-t border-zinc-200 dark:border-zinc-800">
          <Button type="button" variant="outline" size="sm" onClick={onClose}>
            Cancel
          </Button>
          <Button
            type="submit"
            variant="primary"
            size="sm"
            loading={loading}
            icon={<RefreshCw className="w-3.5 h-3.5" />}
          >
            Regenerate Variation
          </Button>
        </div>
      </form>
    </Modal>
  );
};
