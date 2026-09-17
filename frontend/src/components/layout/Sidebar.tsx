"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Megaphone,
  Package,
  Users,
  FileText,
  CheckSquare,
  Settings,
  Sparkles,
  Bot,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Campaigns", href: "/campaigns", icon: Megaphone },
  { name: "Executions", href: "/executions", icon: Zap },
  { name: "Products & Services", href: "/products", icon: Package },
  { name: "Target Audiences", href: "/audiences", icon: Users },
  { name: "AI Content Library", href: "/content", icon: FileText },
  { name: "Approvals Queue", href: "/approvals", icon: CheckSquare },
  { name: "AI Logs & Settings", href: "/settings", icon: Settings },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-zinc-900 text-zinc-300 flex flex-col border-r border-zinc-800 shrink-0 h-screen sticky top-0">
      {/* Brand Header */}
      <div className="h-16 flex items-center gap-3 px-6 border-b border-zinc-800">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-indigo-700 flex items-center justify-center text-white font-bold shadow-md shadow-indigo-500/20">
          <Sparkles className="w-4 h-4" />
        </div>
        <div>
          <span className="font-semibold text-white tracking-tight text-sm">AuraFlow AI</span>
          <span className="block text-[10px] text-zinc-400 font-medium uppercase tracking-wider">
            Campaign Intelligence
          </span>
        </div>
      </div>

      {/* Main Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">
          Platform
        </div>
        {navigation.map((item) => {
          const isActive =
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(item.href);

          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 text-xs font-medium rounded-lg transition-colors group",
                isActive
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/60"
              )}
            >
              <item.icon
                className={cn(
                  "w-4 h-4 transition-colors",
                  isActive ? "text-white" : "text-zinc-400 group-hover:text-zinc-200"
                )}
              />
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* AI Strategist Status card in sidebar */}
      <div className="p-3 m-3 bg-zinc-800/70 border border-zinc-700/60 rounded-xl">
        <div className="flex items-center gap-2 mb-1.5">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-[11px] font-semibold text-zinc-200 flex items-center gap-1">
            <Bot className="w-3 h-3 text-indigo-400" /> AI Engine Ready
          </span>
        </div>
        <p className="text-[10px] text-zinc-400 leading-relaxed">
          Marketing Strategist & Multi-Channel Copy Agent are active (Mock Mode enabled).
        </p>
      </div>

      {/* User Footer */}
      <div className="p-4 border-t border-zinc-800 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-full bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-xs font-bold text-indigo-300">
            SJ
          </div>
          <div className="text-left">
            <p className="text-xs font-medium text-zinc-200">Sarah Jenkins</p>
            <p className="text-[10px] text-zinc-400">Marketing Director</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
