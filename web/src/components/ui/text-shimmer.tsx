import { cn } from "@/lib/utils";
import React from "react";

interface TextShimmerProps extends React.HTMLAttributes<HTMLHeadingElement> {
  children: React.ReactNode;
  duration?: number;
}

export function TextShimmer({
  children,
  className,
  duration = 3,
  ...props
}: TextShimmerProps) {
  return (
    <span
      className={cn(
        "inline-flex bg-clip-text text-transparent bg-[linear-gradient(110deg,#a1a1aa,45%,#0f172a,55%,#a1a1aa)] dark:bg-[linear-gradient(110deg,#94a3b8,45%,#fff,55%,#94a3b8)] bg-[length:250%_100%] animate-shimmer",
        className
      )}
      style={{
        animationDuration: `${duration}s`,
      }}
      {...props}
    >
      {children}
    </span>
  );
}
