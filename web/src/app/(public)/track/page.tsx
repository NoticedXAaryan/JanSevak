"use client";
import React, { useState } from "react";
import { Search, MapPin, Clock, CheckCircle2, AlertCircle, FileText } from "lucide-react";

export default function TrackPage() {
  const [ticketId, setTicketId] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (ticketId.trim()) {
      setHasSearched(true);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-6 py-12 md:py-20">
      <div className="flex flex-col items-center text-center mb-12">
        <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mb-6">
          <Search className="w-8 h-8 text-primary" />
        </div>
        <h1 className="text-4xl md:text-5xl font-heading font-semibold mb-4">Track Status</h1>
        <p className="text-xl text-muted-foreground max-w-2xl">
          Enter your Application ID or Grievance Ticket Number to check real-time progress.
        </p>
      </div>

      <div className="bg-card border border-border rounded-2xl p-6 md:p-8 shadow-sm mb-12">
        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <input
              type="text"
              value={ticketId}
              onChange={(e) => setTicketId(e.target.value)}
              className="block w-full pl-4 pr-4 py-4 text-lg border border-border rounded-xl bg-background text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all font-mono"
              placeholder="e.g. GRV-2026-89A4B2"
              required
            />
          </div>
          <button 
            type="submit"
            className="px-8 py-4 bg-primary text-primary-foreground text-lg font-semibold rounded-xl hover:bg-primary/90 transition-colors shrink-0"
          >
            Track Now
          </button>
        </form>
      </div>

      {hasSearched && (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="bg-card border border-border rounded-2xl p-6 md:p-8 shadow-sm">
            <div className="flex flex-col md:flex-row justify-between md:items-center gap-4 mb-8 pb-8 border-b border-border">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <h2 className="text-2xl font-semibold font-mono">{ticketId.toUpperCase()}</h2>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-amber-500/20 text-amber-500">
                    In Progress
                  </span>
                </div>
                <p className="text-muted-foreground">Pothole repair request on Main Street</p>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground bg-muted px-4 py-2 rounded-lg">
                <MapPin className="w-4 h-4" />
                Municipal Corporation, Ward 12
              </div>
            </div>

            <div className="relative pl-8 space-y-8 before:absolute before:inset-0 before:ml-10 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
              
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div className="flex items-center justify-center w-6 h-6 rounded-full bg-primary text-primary-foreground shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <Clock className="w-3 h-3" />
                </div>
                <div className="w-[calc(100%-3rem)] md:w-[calc(50%-2rem)] p-4 rounded-xl border border-border bg-background shadow-sm">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="font-semibold">Assigned to Field Engineer</h3>
                    <time className="text-xs text-muted-foreground">Today, 10:30 AM</time>
                  </div>
                  <p className="text-sm text-muted-foreground">Engineer Rajesh Kumar has been assigned and is scheduled to inspect the site tomorrow.</p>
                </div>
              </div>

              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                <div className="flex items-center justify-center w-6 h-6 rounded-full bg-secondary text-secondary-foreground shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <CheckCircle2 className="w-4 h-4" />
                </div>
                <div className="w-[calc(100%-3rem)] md:w-[calc(50%-2rem)] p-4 rounded-xl border border-border bg-background shadow-sm">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="font-semibold text-muted-foreground">Forwarded to PWD</h3>
                    <time className="text-xs text-muted-foreground">Jul 2, 2:15 PM</time>
                  </div>
                </div>
              </div>

              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                <div className="flex items-center justify-center w-6 h-6 rounded-full bg-secondary text-secondary-foreground shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <CheckCircle2 className="w-4 h-4" />
                </div>
                <div className="w-[calc(100%-3rem)] md:w-[calc(50%-2rem)] p-4 rounded-xl border border-border bg-background shadow-sm">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="font-semibold text-muted-foreground">Request Verified</h3>
                    <time className="text-xs text-muted-foreground">Jul 2, 10:00 AM</time>
                  </div>
                </div>
              </div>

              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
                <div className="flex items-center justify-center w-6 h-6 rounded-full bg-secondary text-secondary-foreground shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <FileText className="w-3 h-3" />
                </div>
                <div className="w-[calc(100%-3rem)] md:w-[calc(50%-2rem)] p-4 rounded-xl border border-border bg-background shadow-sm">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="font-semibold text-muted-foreground">Grievance Submitted</h3>
                    <time className="text-xs text-muted-foreground">Jul 1, 4:45 PM</time>
                  </div>
                  <p className="text-sm text-muted-foreground">Reported via JanSevak AI Chatbot.</p>
                </div>
              </div>

            </div>
          </div>

          <div className="bg-primary/10 border border-primary/20 rounded-2xl p-6 flex items-start gap-4">
            <AlertCircle className="w-6 h-6 text-primary shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-primary mb-1">Need to escalate?</h3>
              <p className="text-sm text-muted-foreground mb-3">If this grievance has crossed the SLA of 7 days, you can escalate it to the Nodal Officer.</p>
              <button className="text-sm font-medium text-primary hover:underline" disabled>
                Escalate Request (Available in 4 days)
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
