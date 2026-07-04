"use client";
import React from "react";
import StatsCard from "@/components/dashboard/StatsCard";
import DataTable from "@/components/dashboard/DataTable";
import { Users, FileText, Activity, AlertTriangle, ArrowLeft, Bed, Stethoscope, Clock } from "lucide-react";
import Link from "next/link";

export default function HospitalDashboard() {
  const stats = [
    { title: "Total Beds Available", value: "32/150", icon: Bed, trend: { value: 5, isPositive: false }, description: "ICU: 2, General: 30" },
    { title: "OPD Registrations (Today)", value: "245", icon: Users, trend: { value: 12, isPositive: true }, description: "Peak hours: 10AM-12PM" },
    { title: "Ayushman Approvals", value: "18", icon: FileText, trend: { value: 2, isPositive: false }, description: "Average delay: 2.5 days" },
    { title: "Avg Wait Time (OPD)", value: "45 mins", icon: Clock, trend: { value: 10, isPositive: false }, description: "Target: 30 mins" },
  ];

  const queueColumns = [
    { key: "id", header: "Patient ID" },
    { key: "name", header: "Patient Name" },
    { key: "department", header: "Department" },
    { key: "status", header: "Status", render: (val: string) => (
      <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
        val === "Waiting" ? "bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-500" :
        val === "In Consultation" ? "bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-500" :
        "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-500"
      }`}>
        {val}
      </span>
    )},
    { key: "time", header: "Wait Time" },
  ];

  const queueData = [
    { id: "PAT-001", name: "Ramesh Kumar", department: "General Medicine", status: "In Consultation", time: "10 mins" },
    { id: "PAT-002", name: "Sita Devi", department: "Orthopedics", status: "Waiting", time: "45 mins" },
    { id: "PAT-003", name: "Amit Singh", department: "Cardiology", status: "Waiting", time: "30 mins" },
    { id: "PAT-004", name: "Priya Sharma", department: "Pediatrics", status: "Waiting", time: "15 mins" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <Link href="/dashboard" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-2">
            <ArrowLeft className="w-4 h-4 mr-1" /> Back to Overview
          </Link>
          <h1 className="text-2xl font-heading font-semibold text-foreground">Hospital Management</h1>
          <p className="text-muted-foreground text-sm">Real-time capacity and patient flow for District Hospital.</p>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 text-sm font-medium bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
            Update Bed Count
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
            title="Live OPD Queue" 
            columns={queueColumns} 
            data={queueData} 
            action={
              <button className="text-sm font-medium text-primary hover:underline">Manage Queue</button>
            }
          />
        </div>
        
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-card border border-border rounded-xl p-6 shadow-sm">
            <h3 className="text-lg font-heading font-semibold text-foreground mb-4">Inventory Alerts</h3>
            <div className="space-y-4">
              <div className="p-4 rounded-lg bg-rose-500/10 border border-rose-500/20">
                <div className="flex gap-3">
                  <div className="w-2 h-2 rounded-full bg-rose-500 mt-1.5 shrink-0" />
                  <p className="text-sm text-foreground">Critical Shortage: O-Negative Blood (2 units remaining).</p>
                </div>
              </div>
              <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/20">
                <div className="flex gap-3">
                  <div className="w-2 h-2 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                  <p className="text-sm text-foreground">Anti-Rabies Vaccine stock dropping below threshold.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
