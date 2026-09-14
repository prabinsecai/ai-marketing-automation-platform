import React from "react";
import { cn, getStatusBadgeVariant } from "@/lib/utils";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "status" | "default" | "brand" | "outline";
  status?: string;
  className?: string;
  dot?: boolean;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "default",
  status,
  className,
  dot = false,
}) => {
  let style = "bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700";

  if (variant === "status" && status) {
    style = getStatusBadgeVariant(status);
  } else if (variant === "brand") {
    style = "bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800";
  } else if (variant === "outline") {
    style = "bg-transparent border-zinc-300 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400";
  }

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border",
        style,
        className
      )}
    >
      {dot && (
        <span
          className={cn(
            "w-1.5 h-1.5 rounded-full",
            status === "APPROVED"
              ? "bg-emerald-500"
              : status === "IN_REVIEW"
              ? "bg-amber-500"
              : status === "REJECTED"
              ? "bg-rose-500"
              : "bg-indigo-500"
          )}
        />
      )}
      {children}
    </span>
  );
};
