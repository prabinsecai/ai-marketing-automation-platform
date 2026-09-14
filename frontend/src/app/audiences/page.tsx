"use client";

import React, { useEffect, useState } from "react";
import { Users, Plus, Trash2, Target, AlertCircle } from "lucide-react";
import { api } from "@/lib/api";
import { Audience } from "@/lib/types";
import { Card, Button, Modal, Badge } from "@/lib/ui";
import { formatDate } from "@/lib/utils";

export default function AudiencesPage() {
  const [audiences, setAudiences] = useState<Audience[]>([]);
  const [loading, setLoading] = useState(true);
  const [workspaceId, setWorkspaceId] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Form State
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [jobTitle, setJobTitle] = useState("VP of Ecommerce, Growth Marketing Director");
  const [companySize, setCompanySize] = useState("50-500 employees ($10M-$50M GMV)");
  const [painPoints, setPainPoints] = useState("");
  const [goals, setGoals] = useState("");
  const [channels, setChannels] = useState("Email, LinkedIn, Google Ads");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadAudiences();
  }, []);

  const loadAudiences = async () => {
    try {
      setLoading(true);
      const workspaces = await api.listWorkspaces();
      if (workspaces.length > 0) {
        setWorkspaceId(workspaces[0].id);
        const data = await api.listAudiences(workspaces[0].id);
        setAudiences(data);
      }
    } catch (err) {
      console.error("Failed to load audiences", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAudience = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !workspaceId) return;

    try {
      setSubmitting(true);
      await api.createAudience({
        workspace_id: workspaceId,
        name,
        description,
        demographics: {
          job_titles: jobTitle.split(",").map((s) => s.trim()),
          company_size: companySize,
        },
        pain_points: painPoints.split("\n").filter((p) => p.trim().length > 0),
        goals: goals.split("\n").filter((g) => g.trim().length > 0),
        preferred_channels: channels.split(",").map((c) => c.trim()),
      });
      setIsModalOpen(false);
      setName("");
      setDescription("");
      setPainPoints("");
      setGoals("");
      await loadAudiences();
    } catch (err) {
      alert(`Failed to create audience: ${err}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm("Are you sure you want to delete this audience persona?")) {
      try {
        await api.deleteAudience(id);
        await loadAudiences();
      } catch (err) {
        alert(`Failed to delete audience: ${err}`);
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 tracking-tight">
            Target Audience Personas
          </h1>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
            Define specific ICP personas, pain points, and preferred channels for personalized AI marketing copy.
          </p>
        </div>

        <Button
          variant="primary"
          size="sm"
          onClick={() => setIsModalOpen(true)}
          icon={<Plus className="w-3.5 h-3.5" />}
        >
          Add Persona
        </Button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-6 h-6 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin" />
        </div>
      ) : audiences.length === 0 ? (
        <Card className="text-center py-12 border-dashed">
          <Users className="w-8 h-8 text-zinc-400 mx-auto mb-2" />
          <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
            No audience personas defined
          </p>
          <p className="text-xs text-zinc-500 mt-1 mb-4">
            Create target buyer personas or seed demo data.
          </p>
          <Button variant="primary" size="sm" onClick={() => setIsModalOpen(true)}>
            Add First Persona
          </Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {audiences.map((aud) => (
            <Card key={aud.id} className="flex flex-col justify-between space-y-4">
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                      {aud.name}
                    </h3>
                    <p className="text-xs text-zinc-500 line-clamp-2 mt-0.5">
                      {aud.description}
                    </p>
                  </div>
                  <button
                    onClick={() => handleDelete(aud.id)}
                    className="text-zinc-400 hover:text-rose-500 p-1 rounded transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* Pain Points */}
                {aud.pain_points && aud.pain_points.length > 0 && (
                  <div className="space-y-1.5 p-2.5 bg-rose-500/5 rounded-lg border border-rose-500/20">
                    <span className="text-[10px] font-bold text-rose-600 dark:text-rose-400 uppercase tracking-wider flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" /> Key Pain Points
                    </span>
                    <ul className="space-y-1">
                      {aud.pain_points.slice(0, 3).map((p, idx) => (
                        <li key={idx} className="text-[11px] text-zinc-600 dark:text-zinc-400 flex items-start gap-1">
                          <span className="text-rose-500">•</span>
                          <span className="truncate">{p}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Goals */}
                {aud.goals && aud.goals.length > 0 && (
                  <div className="space-y-1.5 p-2.5 bg-indigo-500/5 rounded-lg border border-indigo-500/20">
                    <span className="text-[10px] font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider flex items-center gap-1">
                      <Target className="w-3 h-3" /> Core Goals
                    </span>
                    <ul className="space-y-1">
                      {aud.goals.slice(0, 2).map((g, idx) => (
                        <li key={idx} className="text-[11px] text-zinc-600 dark:text-zinc-400 flex items-start gap-1">
                          <span className="text-indigo-500">•</span>
                          <span className="truncate">{g}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Preferred Channels */}
                {aud.preferred_channels && aud.preferred_channels.length > 0 && (
                  <div>
                    <span className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider block mb-1">
                      Preferred Channels
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {aud.preferred_channels.map((ch, idx) => (
                        <Badge key={idx} variant="outline">
                          {ch}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="pt-3 border-t border-zinc-100 dark:border-zinc-800 text-[11px] text-zinc-400">
                Created {formatDate(aud.created_at)}
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Add Persona Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add Target Audience Persona"
        description="Detail buyer demographics and psychological drivers for precision campaign targeting."
        maxWidth="2xl"
      >
        <form onSubmit={handleCreateAudience} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Persona Name *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Mid-Market Ecommerce Directors"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Description
            </label>
            <textarea
              rows={2}
              placeholder="Brief overview of who this persona is..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Target Job Titles (comma separated)
              </label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Company Size / Profile
              </label>
              <input
                type="text"
                value={companySize}
                onChange={(e) => setCompanySize(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Core Pain Points (one per line)
              </label>
              <textarea
                rows={4}
                placeholder="High customer acquisition costs&#10;Disjointed multi-channel attribution&#10;Slow manual campaign setup"
                value={painPoints}
                onChange={(e) => setPainPoints(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Professional Goals (one per line)
              </label>
              <textarea
                rows={4}
                placeholder="Scale revenue without adding headcount&#10;Automate inventory triggers&#10;Improve ROAS by 30%"
                value={goals}
                onChange={(e) => setGoals(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Preferred Marketing Channels (comma separated)
            </label>
            <input
              type="text"
              value={channels}
              onChange={(e) => setChannels(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div className="flex justify-end gap-2 pt-3 border-t border-zinc-200 dark:border-zinc-800">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setIsModalOpen(false)}
            >
              Cancel
            </Button>
            <Button type="submit" variant="primary" size="sm" loading={submitting}>
              Save Persona
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
