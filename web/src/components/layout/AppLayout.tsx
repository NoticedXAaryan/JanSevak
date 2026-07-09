"use client";

import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Toaster } from "@/components/ui/sonner";
import { DotPattern } from "@/components/ui/dot-pattern";
import { useState } from "react";

interface AppLayoutProps {
  children: React.ReactNode;
  role?: "citizen" | "department" | "admin";
}

export function AppLayout({ children, role = "citizen" }: AppLayoutProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className="flex min-h-screen w-full bg-background relative overflow-hidden">
      <DotPattern className="absolute inset-0 opacity-40 dark:opacity-20 text-border pointer-events-none" />
      
      <div className={`hidden md:block shrink-0 z-10 relative transition-all duration-300 ${isCollapsed ? "w-20" : "w-64"}`}>
        <Sidebar role={role} className={`fixed transition-all duration-300 ${isCollapsed ? "w-20" : "w-64"}`} isCollapsed={isCollapsed} setIsCollapsed={setIsCollapsed} />
      </div>
      
      <div className="flex flex-col flex-1 min-w-0 z-10 relative">
        <Header role={role} />
        <ScrollArea className="flex-1">
          <main className="flex-1 p-4 md:p-6 lg:p-8">
            {children}
          </main>
        </ScrollArea>
      </div>
      <Toaster />
    </div>
  );
}
