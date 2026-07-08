"use client";

import React from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ShieldCheck } from "lucide-react";

export default function TermsPage() {
  return (
    <AppLayout role="citizen">
      <div className="max-w-4xl mx-auto py-12 px-4">
        <div className="flex items-center gap-3 mb-8">
          <ShieldCheck className="w-8 h-8 text-primary" />
          <h1 className="text-4xl font-bold tracking-tight">Terms of Service</h1>
        </div>
        
        <ScrollArea className="h-[65vh] pr-6">
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <p className="text-muted-foreground mb-6">Last updated: July 2026</p>
            
            <h2 className="text-2xl font-semibold mt-8 mb-4">1. Acceptance of Terms</h2>
            <p className="mb-4 text-muted-foreground leading-relaxed">
              By accessing and using JanSevak ("the Platform"), you agree to be bound by these Terms of Service. The Platform serves as a digital bridge between citizens and government services, utilizing AI to streamline access to information.
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">2. Use of AI and Information Accuracy</h2>
            <p className="mb-4 text-muted-foreground leading-relaxed">
              JanSevak uses advanced Artificial Intelligence (LLMs) to retrieve and summarize government schemes, policies, and location data. While we strive for high accuracy, the Platform's responses should not be considered legally binding government directives. Users must verify critical information on official `.gov.in` portals.
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">3. User Conduct</h2>
            <p className="mb-4 text-muted-foreground leading-relaxed">
              You agree to use the Platform for lawful civic purposes only. You must not submit false grievances, impersonate officials, or attempt to manipulate the Platform's infrastructure. Anonymous reporting must be used responsibly for valid civic issues.
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">4. Data Privacy</h2>
            <p className="mb-4 text-muted-foreground leading-relaxed">
              Your interactions with the AI assistant are processed securely. Anonymous reports are stripped of personally identifiable information (PII) before being stored. Please refer to our Privacy Policy for detailed information on data handling.
            </p>
          </div>
        </ScrollArea>
      </div>
    </AppLayout>
  );
}
