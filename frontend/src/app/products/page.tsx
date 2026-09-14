"use client";

import React, { useEffect, useState } from "react";
import { Package, Plus, Trash2, ExternalLink } from "lucide-react";
import { api } from "@/lib/api";
import { Product } from "@/lib/types";
import { Card, Button, Modal } from "@/lib/ui";
import { formatDate } from "@/lib/utils";

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [workspaceId, setWorkspaceId] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Form State
  const [name, setName] = useState("");
  const [category, setCategory] = useState("Commerce Orchestration");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("$999 / mo");
  const [features, setFeatures] = useState("");
  const [benefits, setBenefits] = useState("");
  const [usp, setUsp] = useState("");
  const [url, setUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const workspaces = await api.listWorkspaces();
      if (workspaces.length > 0) {
        setWorkspaceId(workspaces[0].id);
        const data = await api.listProducts(workspaces[0].id);
        setProducts(data);
      }
    } catch (err) {
      console.error("Failed to load products", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !workspaceId) return;

    try {
      setSubmitting(true);
      await api.createProduct({
        workspace_id: workspaceId,
        name,
        category,
        description,
        price,
        features: features.split("\n").filter((f) => f.trim().length > 0),
        target_benefits: benefits.split("\n").filter((b) => b.trim().length > 0),
        usp,
        url: url || undefined,
      });
      setIsModalOpen(false);
      setName("");
      setDescription("");
      setFeatures("");
      setBenefits("");
      setUsp("");
      setUrl("");
      await loadProducts();
    } catch (err) {
      alert(`Failed to create product: ${err}`);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm("Are you sure you want to delete this product?")) {
      try {
        await api.deleteProduct(id);
        await loadProducts();
      } catch (err) {
        alert(`Failed to delete product: ${err}`);
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-zinc-900 dark:text-zinc-100 tracking-tight">
            Products & Services Catalog
          </h1>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
            Verified ground-truth product capabilities that feed the AI Marketing Strategist.
          </p>
        </div>

        <Button
          variant="primary"
          size="sm"
          onClick={() => setIsModalOpen(true)}
          icon={<Plus className="w-3.5 h-3.5" />}
        >
          Add Product
        </Button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-6 h-6 rounded-full border-2 border-indigo-600 border-t-transparent animate-spin" />
        </div>
      ) : products.length === 0 ? (
        <Card className="text-center py-12 border-dashed">
          <Package className="w-8 h-8 text-zinc-400 mx-auto mb-2" />
          <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
            No products in catalog
          </p>
          <p className="text-xs text-zinc-500 mt-1 mb-4">
            Add your verified business products or seed demo data.
          </p>
          <Button variant="primary" size="sm" onClick={() => setIsModalOpen(true)}>
            Add First Product
          </Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((prod) => (
            <Card key={prod.id} className="flex flex-col justify-between space-y-4">
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                      {prod.name}
                    </h3>
                    <span className="text-[11px] text-zinc-400 font-medium">
                      {prod.category} • {prod.price || "Custom Pricing"}
                    </span>
                  </div>
                  <button
                    onClick={() => handleDelete(prod.id)}
                    className="text-zinc-400 hover:text-rose-500 p-1 rounded transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>

                <p className="text-xs text-zinc-600 dark:text-zinc-400 line-clamp-3">
                  {prod.description}
                </p>

                {prod.usp && (
                  <div className="p-2.5 bg-indigo-50/70 dark:bg-indigo-950/30 rounded-lg border border-indigo-100 dark:border-indigo-900/40">
                    <span className="text-[10px] font-bold text-indigo-600 dark:text-indigo-400 uppercase block">
                      USP
                    </span>
                    <p className="text-xs text-indigo-900 dark:text-indigo-200 mt-0.5 line-clamp-2">
                      {prod.usp}
                    </p>
                  </div>
                )}

                {prod.features && prod.features.length > 0 && (
                  <div className="space-y-1">
                    <span className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider block">
                      Key Features
                    </span>
                    <ul className="space-y-1">
                      {prod.features.slice(0, 3).map((f, idx) => (
                        <li key={idx} className="text-[11px] text-zinc-500 dark:text-zinc-400 flex items-center gap-1.5">
                          <span className="text-indigo-500 font-bold">•</span>
                          <span className="truncate">{f}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              <div className="pt-3 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between text-[11px] text-zinc-400">
                <span>Added {formatDate(prod.created_at)}</span>
                {prod.url && (
                  <a
                    href={prod.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-indigo-600 dark:text-indigo-400 flex items-center gap-1 hover:underline"
                  >
                    Product Link <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Add Product Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Add Product / Service"
        description="Provide accurate product specifications so AI copy agents never hallucinate facts."
        maxWidth="2xl"
      >
        <form onSubmit={handleCreateProduct} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Product Name *
              </label>
              <input
                type="text"
                required
                placeholder="e.g. AuraFlow Engine"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Category
              </label>
              <input
                type="text"
                placeholder="e.g. Commerce Orchestration"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Description *
            </label>
            <textarea
              rows={3}
              required
              placeholder="What does this product do and who is it for?"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Pricing Representation
              </label>
              <input
                type="text"
                placeholder="e.g. $1,499 / mo or Custom Enterprise"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Product URL
              </label>
              <input
                type="text"
                placeholder="https://example.com/product"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
              Unique Selling Proposition (USP)
            </label>
            <input
              type="text"
              placeholder="The single standout reason customers choose this product..."
              value={usp}
              onChange={(e) => setUsp(e.target.value)}
              className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Key Features (one per line)
              </label>
              <textarea
                rows={4}
                placeholder="Real-time catalog sync&#10;Automated trigger sequences&#10;Enterprise API connector"
                value={features}
                onChange={(e) => setFeatures(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-1">
                Target Benefits (one per line)
              </label>
              <textarea
                rows={4}
                placeholder="70% faster campaign launch&#10;3.2x repeat customer engagement&#10;Zero inventory sync downtime"
                value={benefits}
                onChange={(e) => setBenefits(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
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
              Save Product
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
