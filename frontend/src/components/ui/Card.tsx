import React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  hoverEffect?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  hoverEffect = false,
  ...props
}) => {
  return (
    <div
      className={cn(
        "bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-5 shadow-sm",
        hoverEffect && "hover:border-zinc-300 dark:hover:border-zinc-700 hover:shadow-md transition-all",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
