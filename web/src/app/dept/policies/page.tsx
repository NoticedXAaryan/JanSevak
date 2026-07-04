"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { useState } from "react";
import { FileText, Plus, Save } from "lucide-react";

export default function DeptPolicies() {
  const [policies, setPolicies] = useState([
    { id: 1, title: "Pothole Repair SLA", description: "All reported potholes on main roads must be inspected within 48 hours and repaired within 7 days." },
    { id: 2, title: "Garbage Collection Timings", description: "Residential garbage collection occurs between 6 AM and 10 AM daily." },
  ]);

  const [newTitle, setNewTitle] = useState("");
  const [newDesc, setNewDesc] = useState("");

  const handleAdd = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle || !newDesc) return;
    
    setPolicies([...policies, { id: Date.now(), title: newTitle, description: newDesc }]);
    setNewTitle("");
    setNewDesc("");
    toast.success("Policy added successfully");
  };

  const handleSaveAll = () => {
    toast.success("All policies synced to AI Knowledge Base");
  };

  return (
    <AppLayout role="department">
      <div className="space-y-6 max-w-5xl mx-auto">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Department Policies</h1>
            <p className="text-muted-foreground mt-2">
              Manage local rules and SLAs. This data is fed directly into the JanSevak AI.
            </p>
          </div>
          <Button onClick={handleSaveAll} className="gap-2">
            <Save className="w-4 h-4" /> Sync to AI
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {/* Add New Policy Form */}
          <Card>
            <CardHeader>
              <CardTitle>Add New Policy</CardTitle>
              <CardDescription>Enter a new local rule or procedure.</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleAdd} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="title">Policy Title</Label>
                  <Input 
                    id="title" 
                    placeholder="e.g. Water Supply Timings" 
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="desc">Description / Rules</Label>
                  <Textarea 
                    id="desc" 
                    placeholder="Describe the policy, SLAs, or timings in detail..." 
                    className="min-h-[120px]"
                    value={newDesc}
                    onChange={(e) => setNewDesc(e.target.value)}
                    required
                  />
                </div>
                <Button type="submit" className="w-full gap-2">
                  <Plus className="w-4 h-4" /> Add Policy
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Existing Policies */}
          <div className="space-y-4">
            <h3 className="font-semibold text-lg flex items-center gap-2">
              <FileText className="w-5 h-5 text-primary" /> Active Policies
            </h3>
            {policies.map(p => (
              <Card key={p.id}>
                <CardHeader className="pb-2">
                  <CardTitle className="text-base">{p.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{p.description}</p>
                  <div className="mt-4 flex justify-end">
                    <Button variant="ghost" size="sm" className="text-destructive">Delete</Button>
                  </div>
                </CardContent>
              </Card>
            ))}
            {policies.length === 0 && (
              <div className="text-center p-8 border border-dashed rounded-lg text-muted-foreground">
                No policies defined yet.
              </div>
            )}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
