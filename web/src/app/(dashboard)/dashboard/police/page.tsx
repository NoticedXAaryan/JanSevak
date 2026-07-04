"use client";
import React from "react";
import StatsCard from "@/components/dashboard/StatsCard";
import DataTable from "@/components/dashboard/DataTable";
import { Users, FileText, Activity, AlertTriangle, ArrowLeft, ShieldAlert, Car, PhoneCall } from "lucide-react";
import Link from "next/link";

export default function PoliceDashboard() {
  const stats = [
    { title: "Active FIRs", value: "128", icon: FileText, trend: { value: 4, isPositive: false }, description: "This month" },
    { title: "Emergency Calls (112)", value: "45", icon: PhoneCall, trend: { value: 12, isPositive: true }, description: "Today" },
    { title: "Patrol Units Active", value: "8/12", icon: Car, description: "4 in maintenance" },
    { title: "Citizen Verifications", value: "62", icon: Users, trend: { value: 20, isPositive: true }, description: "Pending approval" },
  ];

  const firColumns = [
    { key: "id", header: "FIR No." },
    { key: "type", header: "Offense Type" },
    { key: "officer", header: "Investigating Officer" },
    { key: "status", header: "Status", render: (val: string) => (
      <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
        val === "Under Investigation" ? "bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-500" :
        val === "Closed" ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-500" :
        "bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-500"
      }`}>
        {val}
      </span>
    )},
    { key: "date", header: "Registered On" },
  ];

  const firData = [
    { id: "FIR-24-0891", type: "Theft", officer: "Insp. R. Sharma", status: "Under Investigation", date: "Today, 08:30 AM" },
    { id: "FIR-24-0890", type: "Cyber Fraud", officer: "SI M. Patel", status: "Under Investigation", date: "Yesterday" },
    { id: "FIR-24-0889", type: "Assault", officer: "Insp. V. Singh", status: "Charge Sheet Filed", date: "Jul 1, 2026" },
    { id: "FIR-24-0885", type: "Missing Person", officer: "SI A. Kumar", status: "Closed", date: "Jun 28, 2026" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <Link href="/dashboard" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-2">
            <ArrowLeft className="w-4 h-4 mr-1" /> Back to Overview
          </Link>
          <h1 className="text-2xl font-heading font-semibold text-foreground">Police Station Dashboard</h1>
          <p className="text-muted-foreground text-sm">Law enforcement and public safety metrics.</p>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 text-sm font-medium bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
            Dispatch Unit
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <StatsCard key={i} {...stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <DataTable 
            title="Recent FIRs" 
            columns={firColumns} 
            data={firData} 
            action={
              <button className="text-sm font-medium text-primary hover:underline">View All</button>
            }
          />
        </div>
        
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
            <h3 className="text-lg font-heading font-semibold text-foreground mb-4">AI Predictive Alerts</h3>
            <div className="space-y-4">
              <div className="p-4 rounded-lg bg-rose-500/10 border border-rose-500/20">
                <div className="flex gap-3">
                  <div className="w-2 h-2 rounded-full bg-rose-500 mt-1.5 shrink-0" />
                  <p className="text-sm text-foreground">High probability of traffic congestion near Market Square due to upcoming festival.</p>
                </div>
              </div>
              <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/20">
                <div className="flex gap-3">
                  <div className="w-2 h-2 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                  <p className="text-sm text-foreground">Spike in cyber fraud reports targeting elderly citizens in Sector 4.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
