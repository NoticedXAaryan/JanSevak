"use client";
import React, { useEffect, useState } from "react";
import StatsCard from "@/components/dashboard/StatsCard";
import DataTable from "@/components/dashboard/DataTable";
import { Users, FileText, Activity, AlertTriangle, ArrowRight } from "lucide-react";
import Link from "next/link";
import { getSession } from "@/lib/auth";

export default function DashboardOverview() {
  const [orgType, setOrgType] = useState<string>("generic");

  useEffect(() => {
    // In a real app, we fetch the org type from the user's session
    const session = getSession();
    if (session?.orgType) {
      setOrgType(session.orgType);
    }
  }, []);

  const getStats = () => {
    switch (orgType) {
      case "hospital":
        return [
          { title: "OPD Patients Today", value: "245", icon: Users, trend: { value: 12, isPositive: true }, description: "vs yesterday" },
          { title: "Beds Available", value: "32/150", icon: Activity, trend: { value: 5, isPositive: false }, description: "Critical shortage in ICU" },
          { title: "Pending Ayushman Approvals", value: "18", icon: FileText, trend: { value: 2, isPositive: false }, description: "Average delay: 2.5 days" },
          { title: "Grievances", value: "4", icon: AlertTriangle, trend: { value: 10, isPositive: true }, description: "2 high priority" },
        ];
      case "police":
        return [
          { title: "Active FIRs", value: "128", icon: FileText, trend: { value: 4, isPositive: false }, description: "This month" },
          { title: "Patrols Active", value: "12", icon: Activity, description: "All beats covered" },
          { title: "Anonymous Tips", value: "34", icon: AlertTriangle, trend: { value: 15, isPositive: true }, description: "Action taken on 8" },
          { title: "Citizen Verifications", value: "45", icon: Users, trend: { value: 20, isPositive: true }, description: "Pending approval" },
        ];
      default: // generic revenue/municipal
        return [
          { title: "Total Applications", value: "1,245", icon: FileText, trend: { value: 18, isPositive: true }, description: "Past 30 days" },
          { title: "Citizens Served", value: "8,590", icon: Users, trend: { value: 5, isPositive: true }, description: "Total registered" },
          { title: "Avg. Resolution Time", value: "4.2 days", icon: Activity, trend: { value: 12, isPositive: true }, description: "Target: 5 days" },
          { title: "Pending Grievances", value: "156", icon: AlertTriangle, trend: { value: 2, isPositive: false }, description: "12 breached SLA" },
        ];
    }
  };

  const recentActivityColumns = [
    { key: "id", header: "ID" },
    { key: "type", header: "Request Type" },
    { key: "status", header: "Status", render: (val: string) => (
      <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
        val === "Pending" ? "bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-500" :
        val === "Completed" ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-500" :
        "bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-500"
      }`}>
        {val}
      </span>
    )},
    { key: "date", header: "Date" },
  ];

  const recentActivityData = [
    { id: "REQ-001", type: "Income Certificate", status: "Pending", date: "Today, 10:45 AM" },
    { id: "REQ-002", type: "Grievance: Water Supply", status: "In Progress", date: "Yesterday, 2:30 PM" },
    { id: "REQ-003", type: "Domicile Certificate", status: "Completed", date: "Jul 2, 2026" },
    { id: "REQ-004", type: "RTI Application", status: "Pending", date: "Jul 1, 2026" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-heading font-semibold text-foreground">Dashboard Overview</h1>
          <p className="text-muted-foreground text-sm">Welcome back. Here is what's happening today.</p>
        </div>
        <div className="flex gap-3">
          <Link href={`/dashboard/${orgType === 'generic' ? 'municipal' : orgType}`} className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium bg-secondary hover:bg-secondary/80 text-secondary-foreground rounded-lg transition-colors">
            View Sector Dashboard <ArrowRight className="w-4 h-4 ml-2" />
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {getStats().map((stat, i) => (
          <StatsCard key={i} {...stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <DataTable 
            title="Recent Citizen Requests" 
            columns={recentActivityColumns} 
            data={recentActivityData} 
            action={
              <button className="text-sm font-medium text-primary hover:underline">View All</button>
            }
          />
        </div>
        
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
            <h3 className="text-lg font-heading font-semibold text-foreground mb-4">AI Insights</h3>
            <div className="space-y-4">
              <div className="p-4 rounded-lg bg-primary/10 border border-primary/20">
                <div className="flex gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary mt-1.5 shrink-0" />
                  <p className="text-sm text-foreground">Grievances related to <span className="font-semibold">street lighting</span> have increased by 40% in Ward 12 this week.</p>
                </div>
              </div>
              <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/20">
                <div className="flex gap-3">
                  <div className="w-2 h-2 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                  <p className="text-sm text-foreground">3 applications for Income Certificates are nearing their 7-day SLA breach limit.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
