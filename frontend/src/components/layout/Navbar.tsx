"use client";

import React, { useState } from "react";
import { Sparkles, Database, Plus, Check } from "lucide-react";
import { Button } from "@/lib/ui";
import { api } from "@/lib/api";

interface NavbarProps {
  workspaceName?: string;
  onRefresh?: () => void;
  onOpenCreateCampaign?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  workspaceName = "AuraFlow Commerce AI",
  onRefresh,
  onOpenCreateCampaign,
}) => {
  const [seeding, setSeeding] = useState(false);
  const [seeded, setSeeded] = useState(false);

  const handleSeed = async () => {
    try {
      setSeeding(true);
      await api.seedDemoData();
      setSeeded(true);
      setTimeout(() => setSeeded(false), 3000);
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error("Failed to seed demo data:", err);
    } finally {
      setSeeding(false);
    }
  };

  return (
    <header className="h-16 bg-white dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800 px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 px-3 py-1 bg-zinc-100 dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700">
          <span className="w-2 h-2 rounded-full bg-emerald-500" />
          <span className="text-xs font-semibold text-zinc-800 dark:text-zinc-200">
            {workspaceName}
          </span>
          <span className="text-[10px] text-zinc-400 font-medium">B2B E-Commerce</span>
        </div>

        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 bg-indigo-50 dark:bg-indigo-950/40 text-indigo-700 dark:text-indigo-300 rounded-md border border-indigo-200 dark:border-indigo-800 text-[11px] font-medium">
          <Sparkles className="w-3 h-3" />
          <span>Phase 1 Strategy & Content Engine</span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <Button
          variant="outline"
          size="sm"
          onClick={handleSeed}
          loading={seeding}
          icon={seeded ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Database className="w-3.5 h-3.5" />}
          title="Seed realistic fictional e-commerce products, audiences, and campaigns"
        >
          {seeded ? "Demo Data Seeded!" : "Seed Demo Data"}
        </Button>

        {onOpenCreateCampaign && (
          <Button
            variant="primary"
            size="sm"
            onClick={onOpenCreateCampaign}
            icon={<Plus className="w-3.5 h-3.5" />}
          >
            New Campaign
          </Button>
        )}
      </div>
    </header>
  );
};
