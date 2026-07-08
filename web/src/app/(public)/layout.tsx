import React from "react";
import Navbar from "@/components/layout/Navbar";
import { FlickeringFooter } from "@/components/ui/flickering-footer";

export default function PublicLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="dark min-h-screen bg-background text-foreground flex flex-col selection:bg-primary/30 selection:text-primary-foreground">
      <Navbar />
      <main className="flex-1 relative z-10 flex flex-col">
        {children}
      </main>
      <FlickeringFooter />
    </div>
  );
}
