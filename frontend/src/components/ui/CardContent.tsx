import React from "react";
import { cn } from "@/lib/utils";

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
  children: React.ReactNode;
}

export const CardContent: React.FC<CardContentProps> = ({ className, children, ...props }) => (
  <div className={cn("p-4 pt-0", className)} {...props}>
    {children}
  </div>
);
