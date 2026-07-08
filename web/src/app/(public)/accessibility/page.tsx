"use client";

import React from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Accessibility } from "lucide-react";

export default function AccessibilityPage() {
  return (
    <AppLayout role="citizen">
      <div className="max-w-4xl mx-auto py-12 px-4">
        <div className="flex items-center gap-3 mb-8">
          <Accessibility className="w-8 h-8 text-primary" />
          <h1 className="text-4xl font-bold tracking-tight">Accessibility Statement</h1>
        </div>
        
        <ScrollArea className="h-[65vh] pr-6">
          <div className="prose prose-slate dark:prose-invert max-w-none">
            <p className="text-muted-foreground mb-6">
              JanSevak is committed to ensuring digital accessibility for people with disabilities. We are continually improving the user experience for everyone and applying the relevant accessibility standards.
            </p>
            
            <h2 className="text-2xl font-semibold mt-8 mb-4">Conformance Status</h2>
            <p className="mb-4 text-muted-foreground leading-relaxed">
              The Web Content Accessibility Guidelines (WCAG) defines requirements for designers and developers to improve accessibility for people with disabilities. It defines three levels of conformance: Level A, Level AA, and Level AAA. JanSevak is partially conformant with WCAG 2.1 level AA.
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">Multilingual and Voice Access</h2>
            <p className="mb-4 text-muted-foreground leading-relaxed">
              To accommodate users with varying levels of literacy, JanSevak natively supports Voice-to-Text interaction across both the Web platform and Telegram bots. The AI assistant processes queries in multiple regional languages without requiring manual keyboard input.
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">Feedback</h2>
            <p className="mb-4 text-muted-foreground leading-relaxed">
              We welcome your feedback on the accessibility of JanSevak. If you encounter accessibility barriers, please file a grievance through the platform or contact the support desk.
            </p>
          </div>
        </ScrollArea>
      </div>
    </AppLayout>
  );
}
