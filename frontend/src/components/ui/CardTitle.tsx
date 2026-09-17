import React from "react";
import { cn } from "@/lib/utils";

interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  className?: string;
  children: React.ReactNode;
}

export const CardTitle: React.FC<CardTitleProps> = ({ className, children, ...props }) => (
  <h3 className={cn("text-sm font-medium", className)} {...props}>
    {children}
  </h3>
);
