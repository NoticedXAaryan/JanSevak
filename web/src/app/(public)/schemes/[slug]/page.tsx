"use client";

import React, { use } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { ArrowLeft, FileText, CheckCircle2, ChevronRight, Share2, Info } from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";

// Mock data since DB is not wired for this view in the demo
const MOCK_SCHEMES: Record<string, any> = {
  "scheme-1": {
    name: "PM KISAN Samman Nidhi",
    ministry: "Ministry of Agriculture and Farmers Welfare",
    amount: "₹6,000 per year",
    description: "An initiative by the government of India in which all farmers will get up to ₹6,000 per year as minimum income support.",
    benefits: [
      "Financial benefit of Rs 6000/- per year",
      "Direct Benefit Transfer (DBT) into bank accounts",
      "Payable in three equal installments of Rs 2000/- every four months"
    ],
    eligibility: [
      "Must be a landholding farmer family",
      "Cultivable land holding in their name",
      "Citizens of India"
    ],
    documents: [
      "Aadhaar Card",
      "Bank Passbook",
      "Land Ownership Documents (Khatauni)",
      "Passport Size Photo"
    ]
  },
  "scheme-2": {
    name: "Ayushman Bharat PM-JAY",
    ministry: "Ministry of Health and Family Welfare",
    amount: "Up to ₹5,00,000",
    description: "The world's largest health insurance/ assurance scheme fully financed by the government providing a cover of Rs. 5 lakhs per family per year for secondary and tertiary care hospitalization.",
    benefits: [
      "Free treatment up to ₹5 lakhs per year",
      "Cashless access to health care services",
      "Covers up to 3 days of pre-hospitalization and 15 days post-hospitalization expenses"
    ],
    eligibility: [
      "Families belonging to poor and vulnerable sections as per SECC database",
      "No cap on family size, age, or gender"
    ],
    documents: [
      "Ration Card",
      "Aadhaar Card",
      "PM-JAY e-Card or Letter"
    ]
  }
};

export default function SchemeDetailsPage({ params }: { params: Promise<{ slug: string }> }) {
  const resolvedParams = use(params);
  const scheme = MOCK_SCHEMES[resolvedParams.slug];

  if (!scheme) {
    // If not found in mock, just show a generic template
    return <GenericSchemeTemplate id={resolvedParams.slug} />;
  }

  return (
    <AppLayout role="citizen">
      <div className="max-w-5xl mx-auto py-8 px-4">
        <Link href="/schemes" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-6 transition-colors">
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to Schemes
        </Link>
        
        <div className="bg-card border border-border rounded-3xl overflow-hidden mb-8 shadow-sm">
          <div className="bg-gradient-to-r from-orange-500/10 via-amber-500/10 to-transparent p-8 md:p-12 border-b border-border">
            <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
              <div>
                <span className="inline-block px-3 py-1 bg-primary/10 text-primary text-xs font-bold rounded-full mb-4">
                  {scheme.ministry}
                </span>
                <h1 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">{scheme.name}</h1>
                <p className="text-lg text-muted-foreground max-w-2xl leading-relaxed">
                  {scheme.description}
                </p>
              </div>
              <div className="shrink-0 flex flex-col gap-3 min-w-[200px]">
                <div className="p-4 bg-background rounded-2xl border border-border text-center shadow-sm">
                  <p className="text-sm text-muted-foreground mb-1">Financial Benefit</p>
                  <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{scheme.amount}</p>
                </div>
                <Button size="lg" className="w-full text-base font-semibold rounded-xl" asChild>
                  <Link href="/chat">Check Eligibility via AI</Link>
                </Button>
                <Button variant="outline" className="w-full rounded-xl">
                  <Share2 className="w-4 h-4 mr-2" /> Share Scheme
                </Button>
              </div>
            </div>
          </div>

          <div className="p-8 md:p-12 grid grid-cols-1 md:grid-cols-2 gap-12">
            <div>
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <CheckCircle2 className="w-6 h-6 text-primary" /> Key Benefits
              </h2>
              <ul className="space-y-4">
                {scheme.benefits.map((benefit: string, i: number) => (
                  <li key={i} className="flex gap-3 text-muted-foreground">
                    <span className="shrink-0 w-6 h-6 rounded-full bg-primary/10 text-primary flex items-center justify-center text-sm font-bold mt-0.5">{i+1}</span>
                    <span className="leading-relaxed">{benefit}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Info className="w-6 h-6 text-primary" /> Eligibility & Documents
              </h2>
              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold text-foreground mb-3">Who is eligible?</h3>
                  <ul className="list-disc pl-5 space-y-2 text-muted-foreground">
                    {scheme.eligibility.map((item: string, i: number) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-3">Required Documents:</h3>
                  <div className="flex flex-wrap gap-2">
                    {scheme.documents.map((doc: string, i: number) => (
                      <div key={i} className="px-3 py-1.5 bg-muted rounded-lg text-sm border border-border/50 text-muted-foreground flex items-center gap-2">
                        <FileText className="w-3.5 h-3.5" /> {doc}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}

// Fallback for non-mocked schemes
function GenericSchemeTemplate({ id }: { id: string }) {
  return (
    <AppLayout role="citizen">
      <div className="max-w-5xl mx-auto py-12 px-4 text-center">
        <h1 className="text-3xl font-bold mb-4">Scheme Details: {id}</h1>
        <p className="text-muted-foreground mb-8">This is a dynamic placeholder for government schemes.</p>
        <Button asChild>
          <Link href="/schemes">Back to Schemes</Link>
        </Button>
      </div>
    </AppLayout>
  );
}
