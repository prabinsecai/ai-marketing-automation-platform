"use client";

import React, { useState, useEffect } from "react";
import { Modal, Button } from "@/lib/ui";
import { ContentAsset } from "@/lib/types";

interface ContentEditModalProps {
  isOpen: boolean;
  onClose: () => void;
  asset: ContentAsset | null;
  onSave: (assetId: string, updatedData: Partial<ContentAsset> & { edit_summary?: string }) => Promise<void>;
}

export const ContentEditModal: React.FC<ContentEditModalProps> = ({
  isOpen,
  onClose,
  asset,
  onSave,
}) => {
  const [title, setTitle] = useState("");
  const [previewText, setPreviewText] = useState("");
  const [hook, setHook] = useState("");
  const [body, setBody] = useState("");
  const [cta, setCta] = useState("");
  const [editSummary, setEditSummary] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (asset) {
      setTitle(asset.title || "");
      setPreviewText(asset.preview_text || "");
      setHook(asset.hook || "");
      setBody(asset.body || "");
      setCta(asset.cta || "");
      setEditSummary("");
    }
  }, [asset]);

  if (!asset) return null;

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      await onSave(asset.id, {
        title: title.trim() || undefined,
        preview_text: previewText.trim() || undefined,
        hook: hook.trim() || undefined,
        body: body.trim(),
        cta: cta.trim() || undefined,
        edit_summary: editSummary.trim() || "Manual copy edit",
      });
      onClose();
    } catch (err) {
      alert(`Failed to save edit: ${err}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Edit ${asset.channel} Variation #${asset.variation_number}`}
      description="Make precise manual adjustments to the generated copy. All changes are tracked in the version history."
      maxWidth="2xl"
    >
      <form onSubmit={handleFormSubmit} className="space-y-4">
        {asset.channel === "EMAIL" && (
          <>
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Subject Line
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Preview Text / Preheader
              </label>
              <input
                type="text"
                value={previewText}
                onChange={(e) => setPreviewText(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </>
        )}

        {asset.channel === "SOCIAL" && (
          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Opening Hook Line
            </label>
            <input
              type="text"
              value={hook}
              onChange={(e) => setHook(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        )}

        {asset.channel === "ADVERTISEMENT" && (
          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Headline
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        )}

        <div>
          <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
            {asset.channel === "EMAIL"
              ? "Email Body Copy"
              : asset.channel === "SOCIAL"
              ? "Social Caption Copy"
              : "Ad Primary Text"}
          </label>
          <textarea
            rows={8}
            required
            value={body}
            onChange={(e) => setBody(e.target.value)}
            className="w-full text-xs font-mono px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
            Call to Action (CTA)
          </label>
          <input
            type="text"
            value={cta}
            onChange={(e) => setCta(e.target.value)}
            className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
            Edit Reason / Summary (for audit history)
          </label>
          <input
            type="text"
            placeholder="e.g. Adjusted tone for mid-market personas, shortened paragraphs"
            value={editSummary}
            onChange={(e) => setEditSummary(e.target.value)}
            className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="flex justify-end gap-2 pt-3 border-t border-zinc-200 dark:border-zinc-800">
          <Button type="button" variant="outline" size="sm" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" size="sm" loading={saving}>
            Save Changes
          </Button>
        </div>
      </form>
    </Modal>
  );
};
