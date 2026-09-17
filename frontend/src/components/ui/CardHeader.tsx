import React from "react";
import { cn } from "@/lib/utils";

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
  children: React.ReactNode;
}

export const CardHeader: React.FC<CardHeaderProps> = ({ className, children, ...props }) => (
  <div className={cn("flex flex-row items-center justify-between space-y-0 pb-2", className)} {...props}>
    {children}
  </div>
);
