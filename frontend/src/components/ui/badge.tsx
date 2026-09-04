import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "destructive" | "outline" | "glow";
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const variantStyles = {
    default: "border-transparent bg-blue-600 text-white shadow hover:bg-blue-500",
    secondary: "border-zinc-800 bg-zinc-800/80 text-zinc-300",
    destructive: "border-transparent bg-red-900/30 text-red-400 border border-red-800/50",
    outline: "border-zinc-800 text-zinc-400 bg-zinc-900/30",
    glow: "border-blue-500/30 bg-blue-500/10 text-blue-400 shadow-sm shadow-blue-500/20",
  };

  return (
    <div
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors select-none",
        variantStyles[variant],
        className
      )}
      {...props}
    />
  );
}

export { Badge };

