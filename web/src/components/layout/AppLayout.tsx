"use client";

import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Toaster } from "@/components/ui/sonner";

interface AppLayoutProps {
  children: React.ReactNode;
  role?: "citizen" | "department" | "admin";
}

export function AppLayout({ children, role = "citizen" }: AppLayoutProps) {
  return (
    <div className="flex min-h-screen w-full bg-muted/40">
      <div className="hidden md:block w-64 shrink-0">
        <Sidebar role={role} className="fixed w-64" />
      </div>
      <div className="flex flex-col flex-1 min-w-0">
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
