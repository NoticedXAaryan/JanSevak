"use client";

import React, { use } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { ArrowLeft, MapPin, Phone, Mail, Clock, ExternalLink, Building2, ShieldAlert } from "lucide-react";
import Link from "next/link";

// Mock data
const MOCK_INSTS: Record<string, any> = {
  "1": {
    name: "Civil Hospital, Central",
    type: "Healthcare",
    address: "Medical Road, Central District, 110001",
    phone: "+91 11-2345-6789",
    email: "contact@civilhospital.gov.in",
    hours: "24x7 Emergency Services",
    services: ["Emergency Trauma", "OPD", "Vaccination", "PM-JAY Registration"]
  }
};

export default function InstitutionDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const inst = MOCK_INSTS[resolvedParams.id] || {
    name: "Government Institution " + resolvedParams.id,
    type: "Public Service",
    address: "Main Government Block, Sector 4",
    phone: "1800-XXX-XXXX",
    email: "info@gov.in",
    hours: "9:00 AM - 5:00 PM (Mon-Fri)",
    services: ["Public Grievance", "Document Verification", "General Info"]
  };

  return (
    <AppLayout role="citizen">
      <div className="max-w-6xl mx-auto py-8 px-4">
        <Link href="/institutions" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-6 transition-colors">
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to Directory
        </Link>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            {/* Header Card */}
            <div className="bg-card border border-border rounded-3xl p-8 shadow-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 p-8 opacity-5">
                <Building2 className="w-48 h-48" />
              </div>
              <span className="inline-block px-3 py-1 bg-primary/10 text-primary text-xs font-bold rounded-full mb-4">
                {inst.type}
              </span>
              <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-4 relative z-10">{inst.name}</h1>
              <div className="flex items-center text-muted-foreground mb-6 relative z-10">
                <MapPin className="w-4 h-4 mr-2 shrink-0" />
                <p>{inst.address}</p>
              </div>
              
              <div className="flex flex-wrap gap-3 relative z-10">
                <Button className="rounded-xl"><MapPin className="w-4 h-4 mr-2"/> Get Directions</Button>
                <Button variant="outline" className="rounded-xl"><Phone className="w-4 h-4 mr-2"/> Call Now</Button>
                <Button variant="secondary" className="rounded-xl asChild">
                  <Link href={`/complaints/new?inst=${resolvedParams.id}`}><ShieldAlert className="w-4 h-4 mr-2 text-amber-500"/> Report Issue</Link>
                </Button>
              </div>
            </div>

            {/* Services Available */}
            <div className="bg-card border border-border rounded-3xl p-8 shadow-sm">
              <h2 className="text-2xl font-bold mb-6">Services Available</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {inst.services.map((service: string, i: number) => (
                  <div key={i} className="p-4 rounded-xl border border-border bg-muted/20 flex items-center justify-between group cursor-pointer hover:bg-muted/50 transition-colors">
                    <span className="font-medium">{service}</span>
                    <ExternalLink className="w-4 h-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            {/* Contact Info Card */}
            <div className="bg-card border border-border rounded-3xl p-6 shadow-sm">
              <h3 className="font-bold text-lg mb-4">Contact Information</h3>
              <div className="space-y-4">
                <div className="flex gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                    <Phone className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Phone</p>
                    <p className="font-medium">{inst.phone}</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                    <Mail className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Email</p>
                    <p className="font-medium break-all">{inst.email}</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                    <Clock className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Working Hours</p>
                    <p className="font-medium">{inst.hours}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Map Placeholder */}
            <div className="bg-card border border-border rounded-3xl p-2 shadow-sm aspect-square relative overflow-hidden flex items-center justify-center bg-muted/50">
               <div className="text-center p-6">
                 <MapPin className="w-8 h-8 text-muted-foreground mx-auto mb-2 opacity-50" />
                 <p className="text-sm font-medium text-muted-foreground">Map Integration</p>
                 <p className="text-xs text-muted-foreground/70">Google Maps / MapMyIndia API goes here</p>
               </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
