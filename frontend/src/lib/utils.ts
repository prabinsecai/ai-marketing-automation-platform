import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateStr: string): string {
  if (!dateStr) return "-";
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return dateStr;
  }
}

export function getStatusBadgeVariant(status: string) {
  switch (status) {
    case "APPROVED":
      return "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20";
    case "IN_REVIEW":
      return "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20";
    case "STRATEGY_GENERATED":
      return "bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20";
    case "CONTENT_GENERATED":
      return "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/20";
    case "REJECTED":
      return "bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20";
    case "DRAFT":
    default:
      return "bg-zinc-500/10 text-zinc-600 dark:text-zinc-400 border-zinc-500/20";
  }
}
