"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, AlertTriangle, ShieldAlert, MessageSquare, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function CitizenDashboard() {
  return (
    <AppLayout role="citizen">
      <div className="space-y-6 max-w-5xl mx-auto">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Citizen Dashboard</h1>
          <p className="text-muted-foreground mt-2">
            Welcome back. Here's an overview of your government services and reports.
          </p>
        </div>

        {/* Quick Actions */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card className="hover:bg-muted/50 transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium">Ask JanSeva</CardTitle>
              <MessageSquare className="w-4 h-4 text-primary" />
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground mb-4">
                Chat with our AI to find services or schemes
              </p>
              <Button size="sm" className="w-full" asChild>
                <Link href="/chat">Chat Now</Link>
              </Button>
            </CardContent>
          </Card>
          
          <Card className="hover:bg-muted/50 transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium">Report Issue</CardTitle>
              <AlertTriangle className="w-4 h-4 text-amber-500" />
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground mb-4">
                File a civic complaint with your local authority
              </p>
              <Button size="sm" variant="outline" className="w-full" asChild>
                <Link href="/complaints/new">File Report</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:bg-muted/50 transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium">Whistleblower</CardTitle>
              <ShieldAlert className="w-4 h-4 text-destructive" />
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground mb-4">
                Submit a sealed anonymous report securely
              </p>
              <Button size="sm" variant="outline" className="w-full" asChild>
                <Link href="/report/anonymous">Submit Securely</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:bg-muted/50 transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium">My Documents</CardTitle>
              <FileText className="w-4 h-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground mb-4">
                View your saved certificates and applications
              </p>
              <Button size="sm" variant="outline" className="w-full" asChild>
                <Link href="/documents">View Files</Link>
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity & Stats */}
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>Your latest interactions and updates</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="rounded-full bg-amber-500/10 p-2">
                    <AlertTriangle className="h-4 w-4 text-amber-500" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <p className="text-sm font-medium leading-none">Pothole reported in Sector 4</p>
                    <p className="text-sm text-muted-foreground">Status: In Progress</p>
                  </div>
                  <div className="text-sm text-muted-foreground">2d ago</div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="rounded-full bg-blue-500/10 p-2">
                    <MessageSquare className="h-4 w-4 text-blue-500" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <p className="text-sm font-medium leading-none">Asked about Income Certificate</p>
                    <p className="text-sm text-muted-foreground">Chat completed</p>
                  </div>
                  <div className="text-sm text-muted-foreground">5d ago</div>
                </div>
              </div>
              <Button variant="ghost" className="w-full mt-4 justify-between" asChild>
                <Link href="/history">
                  View full history
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recommended Schemes</CardTitle>
              <CardDescription>Based on your profile and location</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="rounded-lg border p-3 flex flex-col space-y-2">
                  <div className="flex justify-between items-start">
                    <h4 className="font-semibold text-sm">PM Kisan Samman Nidhi</h4>
                    <span className="text-xs bg-green-500/10 text-green-600 px-2 py-1 rounded-full font-medium">High Match</span>
                  </div>
                  <p className="text-xs text-muted-foreground">₹6000/year income support for landholding farmers.</p>
                  <Link href="/chat?q=PM+Kisan" className="text-xs text-primary font-medium hover:underline inline-flex items-center">
                    Check Eligibility <ArrowRight className="ml-1 w-3 h-3" />
                  </Link>
                </div>
                <div className="rounded-lg border p-3 flex flex-col space-y-2">
                  <div className="flex justify-between items-start">
                    <h4 className="font-semibold text-sm">Ayushman Bharat</h4>
                    <span className="text-xs bg-blue-500/10 text-blue-600 px-2 py-1 rounded-full font-medium">Eligible</span>
                  </div>
                  <p className="text-xs text-muted-foreground">Health insurance coverage up to ₹5 Lakhs per family.</p>
                  <Link href="/chat?q=Ayushman+Bharat" className="text-xs text-primary font-medium hover:underline inline-flex items-center">
                    Apply Now <ArrowRight className="ml-1 w-3 h-3" />
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  );
}
