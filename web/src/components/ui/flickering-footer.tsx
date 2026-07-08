"use client";

import { ChevronRightIcon, Bot, Mail, ShieldCheck } from "lucide-react";
import { ClassValue, clsx } from "clsx";
import * as Color from "color-bits";
import { motion } from "framer-motion";
import Link from "next/link";
import Image from "next/image";
import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Helper function to convert any CSS color to rgba
export const getRGBA = (
  cssColor: React.CSSProperties["color"],
  fallback: string = "rgba(180, 180, 180)",
): string => {
  if (typeof window === "undefined") return fallback;
  if (!cssColor) return fallback;

  try {
    if (typeof cssColor === "string" && cssColor.startsWith("var(")) {
      const element = document.createElement("div");
      element.style.color = cssColor;
      document.body.appendChild(element);
      const computedColor = window.getComputedStyle(element).color;
      document.body.removeChild(element);
      return Color.formatRGBA(Color.parse(computedColor));
    }
    return Color.formatRGBA(Color.parse(cssColor as string));
  } catch (e) {
    console.error("Color parsing failed:", e);
    return fallback;
  }
};

export const colorWithOpacity = (color: string, opacity: number): string => {
  if (!color.startsWith("rgb")) return color;
  return Color.formatRGBA(Color.alpha(Color.parse(color), opacity));
};

interface FlickeringGridProps {
  squareSize?: number;
  gridGap?: number;
  flickerChance?: number;
  color?: string;
  width?: number;
  height?: number;
  className?: string;
  maxOpacity?: number;
}

export const FlickeringGrid: React.FC<FlickeringGridProps> = ({
  squareSize = 4,
  gridGap = 6,
  flickerChance = 0.3,
  color = "rgb(150, 150, 150)",
  width,
  height,
  className,
  maxOpacity = 0.3,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [gridSize, setGridSize] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        setGridSize({
          width: width || containerRef.current.clientWidth,
          height: height || containerRef.current.clientHeight,
        });
      }
    };
    updateSize();
    window.addEventListener("resize", updateSize);
    return () => window.removeEventListener("resize", updateSize);
  }, [width, height]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || gridSize.width === 0 || gridSize.height === 0) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = gridSize.width;
    canvas.height = gridSize.height;

    const cols = Math.floor(gridSize.width / (squareSize + gridGap));
    const rows = Math.floor(gridSize.height / (squareSize + gridGap));

    const squares = Array.from({ length: cols * rows }).map(() => ({
      opacity: Math.random() * maxOpacity,
      flicker: Math.random() < flickerChance,
    }));

    let animationFrameId: number;

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      squares.forEach((sq, i) => {
        const x = (i % cols) * (squareSize + gridGap);
        const y = Math.floor(i / cols) * (squareSize + gridGap);

        if (sq.flicker) {
          sq.opacity += (Math.random() - 0.5) * 0.1;
          sq.opacity = Math.max(0, Math.min(maxOpacity, sq.opacity));
        }

        ctx.fillStyle = colorWithOpacity(color, sq.opacity);
        ctx.fillRect(x, y, squareSize, squareSize);
      });

      animationFrameId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [gridSize, squareSize, gridGap, flickerChance, color, maxOpacity]);

  return (
    <div ref={containerRef} className={cn("w-full h-full", className)}>
      <canvas ref={canvasRef} className="block w-full h-full pointer-events-none" />
    </div>
  );
};


export function FlickeringFooter() {
  return (
    <footer className="relative bg-background text-muted-foreground pt-20 pb-10 border-t border-border overflow-hidden">
      {/* Background Effect */}
      <div className="absolute inset-0 z-0">
        <FlickeringGrid
          color="rgb(20, 163, 107)"
          maxOpacity={0.15}
          squareSize={4}
          gridGap={8}
          flickerChance={0.1}
          className="w-full h-full"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background via-background/90 to-background/40"></div>
      </div>
      
      {/* Decorative Glow */}
      <div className="absolute top-0 left-0 w-full h-1 tricolor-glow opacity-50 z-10"></div>
      
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 mb-16">
          <div className="md:col-span-4">
            <div className="flex items-center gap-3 mb-6">
              <div className="relative w-12 h-12 rounded-xl overflow-hidden flex items-center justify-center bg-black">
                <Image src="/logo.png" alt="JanSevak Logo" width={48} height={48} className="object-contain p-1" />
              </div>
              <span className="font-heading font-bold text-2xl text-foreground">JanSevak</span>
            </div>
            <p className="text-muted-foreground leading-relaxed mb-6">
              Empowering Indian citizens with AI-driven access to public services, schemes, and grievance redressal. A modern unified interface for GovTech.
            </p>
            <div className="flex items-center gap-4">
              <a href="#" className="w-10 h-10 rounded-full bg-accent border border-border flex items-center justify-center hover:bg-foreground hover:text-background transition-colors group">
                <Bot className="w-5 h-5 group-hover:scale-110 transition-transform" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full bg-accent border border-border flex items-center justify-center hover:bg-foreground hover:text-background transition-colors group">
                <Mail className="w-5 h-5 group-hover:scale-110 transition-transform" />
              </a>
            </div>
          </div>
          
          <div className="md:col-span-2 md:col-start-6">
            <h3 className="font-bold text-foreground mb-6 uppercase tracking-wider text-sm">Citizens</h3>
            <ul className="space-y-4 text-sm">
              <li><Link href="/services" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />Find a Service</Link></li>
              <li><Link href="/schemes" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />Government Schemes</Link></li>
              <li><Link href="/track" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />Track Grievance</Link></li>
              <li><Link href="/institutions" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />Institution Directory</Link></li>
            </ul>
          </div>

          <div className="md:col-span-2">
            <h3 className="font-bold text-foreground mb-6 uppercase tracking-wider text-sm">Government</h3>
            <ul className="space-y-4 text-sm">
              <li><Link href="/login" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />Official Login</Link></li>
              <li><Link href="/register/institution" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />Register Institution</Link></li>
              <li><Link href="/about" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />About the Platform</Link></li>
            </ul>
          </div>

          <div className="md:col-span-2">
            <h3 className="font-bold text-foreground mb-6 uppercase tracking-wider text-sm">Legal</h3>
            <ul className="space-y-4 text-sm">
              <li><Link href="/privacy" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />Privacy Policy</Link></li>
              <li><Link href="/terms" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />Terms of Service</Link></li>
              <li><Link href="/accessibility" className="hover:text-foreground transition-colors flex items-center gap-2 group"><ChevronRightIcon className="w-3 h-3 text-muted-foreground group-hover:translate-x-1 transition-transform" />Accessibility</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-border pt-8 flex flex-col md:flex-row items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <ShieldCheck className="w-5 h-5 text-green-500" />
            <p>&copy; {new Date().getFullYear()} JanSevak Initiative. Built for Bharat.</p>
          </div>
          <div className="flex space-x-6">
            <Link href="/" className="hover:text-foreground transition-colors">National Portal</Link>
            <Link href="/" className="hover:text-foreground transition-colors">Digital India</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
