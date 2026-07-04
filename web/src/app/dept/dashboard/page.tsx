"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Users, FileText, AlertTriangle, ShieldAlert, BarChart3, TrendingUp, TrendingDown } from "lucide-react";
import Link from "next/link";

export default function DeptDashboard() {
  return (
    <AppLayout role="department">
      <div className="space-y-6 max-w-6xl mx-auto">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Department Overview</h1>
            <p className="text-muted-foreground mt-2">
              Uttar Pradesh Revenue Department - Lucknow District
            </p>
          </div>
          <Button>Generate Report</Button>
        </div>

        {/* Key Metrics */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium">Active Complaints</CardTitle>
              <AlertTriangle className="w-4 h-4 text-amber-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">142</div>
              <p className="text-xs text-muted-foreground flex items-center mt-1">
                <TrendingUp className="w-3 h-3 text-red-500 mr-1" />
                <span className="text-red-500 font-medium">+12%</span> from last month
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium">Resolution Rate</CardTitle>
              <BarChart3 className="w-4 h-4 text-emerald-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">87.4%</div>
              <p className="text-xs text-muted-foreground flex items-center mt-1">
                <TrendingUp className="w-3 h-3 text-emerald-500 mr-1" />
                <span className="text-emerald-500 font-medium">+2.1%</span> from last month
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium">Sealed Reports</CardTitle>
              <ShieldAlert className="w-4 h-4 text-destructive" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">3</div>
              <p className="text-xs text-muted-foreground flex items-center mt-1 text-destructive font-medium">
                Requires immediate attention
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium">Citizens Assisted</CardTitle>
              <Users className="w-4 h-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1,409</div>
              <p className="text-xs text-muted-foreground flex items-center mt-1">
                <TrendingDown className="w-3 h-3 text-red-500 mr-1" />
                <span className="text-red-500 font-medium">-4%</span> from last month
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
          {/* Recent Complaints */}
          <Card className="col-span-1 lg:col-span-4">
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle>Recent Complaints</CardTitle>
                  <CardDescription>Latest civic issues assigned to your department.</CardDescription>
                </div>
                <Button variant="outline" size="sm" asChild>
                  <Link href="/dept/complaints">View All</Link>
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {[
                  { id: "CMP-2026-A8B9C", type: "Infrastructure", desc: "Pothole on Main Street", status: "Pending", time: "2 hours ago" },
                  { id: "CMP-2026-F4D2E", type: "Sanitation", desc: "Garbage collection missed", status: "In Progress", time: "5 hours ago" },
                  { id: "CMP-2026-9X1Y2", type: "Water Supply", desc: "No water in Sector 4", status: "Resolved", time: "1 day ago" },
                ].map((complaint) => (
                  <div key={complaint.id} className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{complaint.desc}</span>
                        <span className="text-xs bg-muted px-2 py-0.5 rounded-full">{complaint.id}</span>
                      </div>
                      <div className="flex items-center text-sm text-muted-foreground gap-2">
                        <span>{complaint.type}</span>
                        <span>•</span>
                        <span>{complaint.time}</span>
                      </div>
                    </div>
                    <div className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                      complaint.status === "Pending" ? "bg-amber-100 text-amber-700 dark:bg-amber-500/20 dark:text-amber-500" :
                      complaint.status === "In Progress" ? "bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-500" :
                      "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-500"
                    }`}>
                      {complaint.status}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions & AI Insights */}
          <div className="col-span-1 lg:col-span-3 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>AI Insights</CardTitle>
                <CardDescription>Automated analysis of recent data</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-primary/10 border border-primary/20 rounded-lg p-4">
                  <h4 className="font-semibold text-primary text-sm flex items-center mb-2">
                    <TrendingUp className="w-4 h-4 mr-2" /> Surge Detected
                  </h4>
                  <p className="text-sm">24% increase in "Water Supply" complaints in Sector 4 over the last 48 hours. Consider dispatching an inspection team.</p>
                </div>
                <div className="bg-amber-500/10 border border-amber-500/20 rounded-lg p-4">
                  <h4 className="font-semibold text-amber-600 dark:text-amber-500 text-sm flex items-center mb-2">
                    <AlertTriangle className="w-4 h-4 mr-2" /> Policy Gap
                  </h4>
                  <p className="text-sm">Many citizens are asking the AI about "Solar Subsidy" but your local policy data is outdated.</p>
                  <Button variant="link" className="px-0 h-auto text-amber-600 dark:text-amber-500" asChild>
                    <Link href="/dept/policies">Update Policy Now →</Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
