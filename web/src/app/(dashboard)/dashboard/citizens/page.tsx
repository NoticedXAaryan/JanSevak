"use client";
import React from "react";
import DataTable from "@/components/dashboard/DataTable";
import { UserCheck, Users } from "lucide-react";

export default function CitizensManagement() {
  const columns = [
    { key: "id", header: "Citizen ID" },
    { key: "name", header: "Name" },
    { key: "kyc", header: "KYC Status", render: (val: string) => (
      <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
        val === "Verified" ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-500" :
        "bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-500"
      }`}>
        {val}
      </span>
    )},
    { key: "joined", header: "Joined Date" },
  ];

  const mockData = [
    { id: "CIT-001", name: "Aarav Sharma", kyc: "Verified", joined: "Jul 1, 2026" },
    { id: "CIT-002", name: "Priya Patel", kyc: "Pending", joined: "Jul 3, 2026" },
    { id: "CIT-003", name: "Rahul Verma", kyc: "Verified", joined: "Jun 28, 2026" },
    { id: "CIT-004", name: "Ananya Gupta", kyc: "Verified", joined: "Jun 15, 2026" },
    { id: "CIT-005", name: "Vikram Singh", kyc: "Pending", joined: "Jul 8, 2026" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-heading font-semibold text-foreground">Citizens Management</h1>
          <p className="text-muted-foreground text-sm">View and manage registered citizens in your jurisdiction.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
        <div className="p-6 bg-card border border-border rounded-xl flex items-center gap-4 shadow-sm">
          <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
            <Users className="w-6 h-6 text-primary" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">Total Citizens</p>
            <p className="text-2xl font-bold">8,590</p>
          </div>
        </div>
        <div className="p-6 bg-card border border-border rounded-xl flex items-center gap-4 shadow-sm">
          <div className="w-12 h-12 rounded-full bg-emerald-500/10 flex items-center justify-center shrink-0">
            <UserCheck className="w-6 h-6 text-emerald-500" />
          </div>
          <div>
            <p className="text-sm text-muted-foreground">KYC Verified</p>
            <p className="text-2xl font-bold">7,241</p>
          </div>
        </div>
      </div>

      <div className="bg-card border border-border rounded-xl shadow-sm">
        <DataTable 
          title="Citizen Directory" 
          columns={columns} 
          data={mockData} 
        />
      </div>
    </div>
  );
}
