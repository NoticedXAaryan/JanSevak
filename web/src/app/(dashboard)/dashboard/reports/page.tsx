"use client";
import React from "react";
import DataTable from "@/components/dashboard/DataTable";
import { AlertTriangle, TrendingDown } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function ReportsManagement() {
  const columns = [
    { key: "id", header: "Report ID" },
    { key: "category", header: "Category" },
    { key: "severity", header: "Severity", render: (val: string) => (
      <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
        val === "High" ? "bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-500" :
        val === "Medium" ? "bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-500" :
        "bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-500"
      }`}>
        {val}
      </span>
    )},
    { key: "date", header: "Date Reported" },
  ];

  const mockData = [
    { id: "REP-991", category: "Infrastructure", severity: "High", date: "Today" },
    { id: "REP-992", category: "Sanitation", severity: "Medium", date: "Yesterday" },
    { id: "REP-993", category: "Water Supply", severity: "High", date: "Jul 6, 2026" },
    { id: "REP-994", category: "Electricity", severity: "Low", date: "Jul 5, 2026" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-heading font-semibold text-foreground">Grievance Reports</h1>
          <p className="text-muted-foreground text-sm">Monitor public complaints and analytics.</p>
        </div>
        <Button>Export CSV</Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
        <div className="p-6 bg-card border border-border rounded-xl shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <div>
              <p className="text-sm text-muted-foreground">Pending Issues</p>
              <p className="text-3xl font-bold mt-1">156</p>
            </div>
            <div className="p-3 bg-amber-500/10 rounded-lg">
              <AlertTriangle className="w-6 h-6 text-amber-500" />
            </div>
          </div>
          <div className="flex items-center text-sm text-red-500 font-medium">
             <TrendingDown className="w-4 h-4 mr-1" /> +12% from last week
          </div>
        </div>
      </div>

      <div className="bg-card border border-border rounded-xl shadow-sm">
        <DataTable 
          title="Active Reports" 
          columns={columns} 
          data={mockData} 
        />
      </div>
    </div>
  );
}
