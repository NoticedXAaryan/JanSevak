"use client";
import React from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { HelpCircle, Phone, BookOpen } from "lucide-react";

export default function SupportManagement() {
  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-heading font-semibold text-foreground">Support & Help Desk</h1>
          <p className="text-muted-foreground text-sm">Need help with the platform? Contact JanSevak admin.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-card border border-border rounded-xl shadow-sm text-center">
          <Phone className="w-8 h-8 text-primary mx-auto mb-4" />
          <h3 className="font-semibold mb-2">Technical Support</h3>
          <p className="text-sm text-muted-foreground mb-4">Call our dedicated IT helpline for immediate assistance.</p>
          <Button variant="outline" className="w-full">Call 1800-XXX-XXXX</Button>
        </div>
        
        <div className="p-6 bg-card border border-border rounded-xl shadow-sm text-center">
          <BookOpen className="w-8 h-8 text-primary mx-auto mb-4" />
          <h3 className="font-semibold mb-2">Documentation</h3>
          <p className="text-sm text-muted-foreground mb-4">Read our guides on API integration and dashboard usage.</p>
          <Button variant="outline" className="w-full">Read Docs</Button>
        </div>

        <div className="p-6 bg-card border border-border rounded-xl shadow-sm text-center">
          <HelpCircle className="w-8 h-8 text-primary mx-auto mb-4" />
          <h3 className="font-semibold mb-2">FAQs</h3>
          <p className="text-sm text-muted-foreground mb-4">Find answers to commonly asked questions.</p>
          <Button variant="outline" className="w-full">View FAQs</Button>
        </div>
      </div>

      <div className="bg-card border border-border rounded-xl shadow-sm p-6 mt-8">
        <h2 className="text-lg font-semibold mb-4">Open a Support Ticket</h2>
        <form className="space-y-4">
          <Textarea 
            placeholder="Describe your issue with the JanSevak platform..." 
            className="min-h-[120px]"
          />
          <Button type="button">Submit Ticket</Button>
        </form>
      </div>
    </div>
  );
}
