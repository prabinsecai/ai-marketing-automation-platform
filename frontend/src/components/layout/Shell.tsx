"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Navbar } from "@/components/layout/Navbar";
import { Modal, Button } from "@/lib/ui";
import { api } from "@/lib/api";
import { Product, Audience } from "@/lib/types";

export const Shell: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [audiences, setAudiences] = useState<Audience[]>([]);
  const [workspaceId, setWorkspaceId] = useState<string>("");
  const [workspaceName, setWorkspaceName] = useState<string>("AuraFlow Commerce AI");

  // Form State
  const [name, setName] = useState("");
  const [objective, setObjective] = useState("Lead Generation & Product Demo Bookings");
  const [productId, setProductId] = useState("");
  const [audienceId, setAudienceId] = useState("");
  const [budget, setBudget] = useState("$20,000");
  const [timeline, setTimeline] = useState("4-Week Campaign Sprint");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const workspaces = await api.listWorkspaces();
      if (workspaces.length > 0) {
        setWorkspaceId(workspaces[0].id);
        setWorkspaceName(workspaces[0].name);
        const [prods, auds] = await Promise.all([
          api.listProducts(workspaces[0].id),
          api.listAudiences(workspaces[0].id),
        ]);
        setProducts(prods);
        setAudiences(auds);
        if (prods.length > 0) setProductId(prods[0].id);
        if (auds.length > 0) setAudienceId(auds[0].id);
      }
    } catch (e) {
      console.error("Failed to load initial workspace data", e);
    }
  };

  const handleCreateCampaign = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !workspaceId) return;

    try {
      setLoading(true);
      const newCamp = await api.createCampaign({
        workspace_id: workspaceId,
        name,
        objective,
        product_id: productId || undefined,
        audience_id: audienceId || undefined,
        budget,
        target_timeline: timeline,
        description,
      });
      setIsCreateOpen(false);
      setName("");
      setDescription("");
      window.location.href = `/campaigns/${newCamp.id}`;
    } catch (err) {
      alert(`Error creating campaign: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-zinc-50 dark:bg-zinc-950">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar
          workspaceName={workspaceName}
          onRefresh={loadData}
          onOpenCreateCampaign={() => setIsCreateOpen(true)}
        />
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">{children}</main>
      </div>

      {/* Global Quick Create Campaign Modal */}
      <Modal
        isOpen={isCreateOpen}
        onClose={() => setIsCreateOpen(false)}
        title="Create New Marketing Campaign"
        description="Set up your campaign parameters to trigger AI Strategy and Multi-Channel Content generation."
      >
        <form onSubmit={handleCreateCampaign} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Campaign Name *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Q3 Omnichannel Growth Sprint"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Core Objective *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Qualified Lead Generation & Product Demo Bookings"
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Target Product / Service
              </label>
              <select
                value={productId}
                onChange={(e) => setProductId(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">-- Select Product --</option>
                {products.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Target Buyer Audience
              </label>
              <select
                value={audienceId}
                onChange={(e) => setAudienceId(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">-- Select Audience --</option>
                {audiences.map((a) => (
                  <option key={a.id} value={a.id}>
                    {a.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Budget Allocation
              </label>
              <input
                type="text"
                placeholder="e.g. $15,000"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Target Timeline
              </label>
              <input
                type="text"
                placeholder="e.g. 4-week sprint"
                value={timeline}
                onChange={(e) => setTimeline(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Campaign Description / Specific Focus
            </label>
            <textarea
              rows={3}
              placeholder="Highlight any specific focus or tactical angle for this campaign..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div className="flex justify-end gap-2 pt-3 border-t border-zinc-200 dark:border-zinc-800">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setIsCreateOpen(false)}
            >
              Cancel
            </Button>
            <Button type="submit" variant="primary" size="sm" loading={loading}>
              Create Campaign
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
