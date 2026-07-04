import React from "react";
import Link from "next/link";
import { ArrowLeft, Clock, FileCheck, Landmark, MessageSquare } from "lucide-react";

export default function ServiceDetailPage({ params }: { params: { slug: string } }) {
  return (
    <div className="w-full max-w-4xl mx-auto px-6 py-12">
      <Link href="/services" className="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-foreground mb-8 transition-colors">
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back to Services
      </Link>

      <div className="mb-10">
        <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-secondary text-secondary-foreground mb-4">
          Revenue Department
        </div>
        <h1 className="text-4xl md:text-5xl font-heading font-semibold mb-4">Income Certificate</h1>
        <p className="text-xl text-muted-foreground leading-relaxed">
          An official statement provided to the citizen by the state government confirming their annual income.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <div className="p-5 rounded-xl bg-card border border-border flex items-start gap-4">
          <Clock className="w-6 h-6 text-primary shrink-0" />
          <div>
            <h4 className="font-semibold text-sm mb-1">Processing Time</h4>
            <p className="text-sm text-muted-foreground">7-15 Working Days</p>
          </div>
        </div>
        <div className="p-5 rounded-xl bg-card border border-border flex items-start gap-4">
          <Landmark className="w-6 h-6 text-primary shrink-0" />
          <div>
            <h4 className="font-semibold text-sm mb-1">Issuing Authority</h4>
            <p className="text-sm text-muted-foreground">Tehsildar / Revenue Officer</p>
          </div>
        </div>
        <div className="p-5 rounded-xl bg-card border border-border flex items-start gap-4">
          <FileCheck className="w-6 h-6 text-primary shrink-0" />
          <div>
            <h4 className="font-semibold text-sm mb-1">Validity</h4>
            <p className="text-sm text-muted-foreground">1 Year from issuance</p>
          </div>
        </div>
      </div>

      <div className="prose prose-invert max-w-none">
        <h2 className="text-2xl font-heading font-semibold mt-8 mb-4 border-b border-border pb-2">Overview</h2>
        <p className="text-muted-foreground mb-6">
          The Income Certificate is an important document required to avail various subsidies, schemes, and educational benefits provided by the State and Central Government. It serves as proof of your family's annual income from all sources.
        </p>

        <h2 className="text-2xl font-heading font-semibold mt-8 mb-4 border-b border-border pb-2">Documents Required</h2>
        <ul className="list-disc pl-5 space-y-2 text-muted-foreground mb-6">
          <li>Aadhaar Card or Voter ID</li>
          <li>Ration Card or Residential Proof</li>
          <li>Salary Slips (if employed) or Income Affidavit (if self-employed/farmer)</li>
          <li>Recent Passport Size Photograph</li>
          <li>Completed Application Form</li>
        </ul>

        <div className="mt-12 p-8 rounded-2xl bg-primary/10 border border-primary/20 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h3 className="text-xl font-heading font-semibold mb-2">Need help applying?</h3>
            <p className="text-muted-foreground text-sm">Our AI assistant can guide you through the process step-by-step.</p>
          </div>
          <button className="shrink-0 inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full font-semibold hover:bg-primary/90 transition-transform active:scale-95">
            <MessageSquare className="w-5 h-5" />
            Ask JanSevak AI
          </button>
        </div>
      </div>
    </div>
  );
}
