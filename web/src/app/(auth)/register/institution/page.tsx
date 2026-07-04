"use client";
import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { setSession } from "@/lib/auth";

export default function InstitutionRegisterPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: "",
    orgType: "hospital",
    email: "",
    state: "",
    district: ""
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (step === 1) {
      setStep(2);
    } else {
      // Mock registration
      setSession({
        id: "org_admin_123",
        name: formData.name,
        email: formData.email,
        role: "org_admin",
        orgType: formData.orgType
      });
      router.push("/dashboard");
    }
  };

  const orgTypes = [
    { id: "hospital", label: "Hospital / Healthcare Center" },
    { id: "police", label: "Police Station" },
    { id: "school", label: "Government School / Institute" },
    { id: "revenue", label: "Revenue Office / Tehsil" },
    { id: "municipal", label: "Municipal Corporation / Panchayat" },
  ];

  return (
    <div className="w-full bg-card border border-border rounded-2xl shadow-xl p-8">
      <div className="flex flex-col items-center mb-8">
        <h1 className="text-2xl font-heading font-semibold text-foreground">Register Institution</h1>
        <p className="text-sm text-muted-foreground mt-1 text-center">Claim your public dashboard and manage citizen requests</p>
      </div>

      <div className="flex items-center justify-center gap-2 mb-8">
        <div className={`w-3 h-3 rounded-full ${step >= 1 ? 'bg-primary' : 'bg-muted'}`} />
        <div className="w-12 h-1 bg-muted rounded-full overflow-hidden">
          <div className={`h-full bg-primary transition-all duration-300 ${step >= 2 ? 'w-full' : 'w-0'}`} />
        </div>
        <div className={`w-3 h-3 rounded-full ${step >= 2 ? 'bg-primary' : 'bg-muted'}`} />
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {step === 1 ? (
          <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Institution Name</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
                placeholder="e.g., District Hospital South"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Institution Type</label>
              <select
                required
                value={formData.orgType}
                onChange={(e) => setFormData({...formData, orgType: e.target.value})}
                className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 appearance-none"
              >
                {orgTypes.map(type => (
                  <option key={type.id} value={type.id}>{type.label}</option>
                ))}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">State</label>
                <input
                  type="text"
                  required
                  value={formData.state}
                  onChange={(e) => setFormData({...formData, state: e.target.value})}
                  className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
                  placeholder="e.g., Delhi"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-foreground mb-1">District</label>
                <input
                  type="text"
                  required
                  value={formData.district}
                  onChange={(e) => setFormData({...formData, district: e.target.value})}
                  className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
                  placeholder="e.g., South West"
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Official Email Address</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
                placeholder="admin@hospital.gov.in"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Admin Password</label>
              <input
                type="password"
                required
                className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
                placeholder="••••••••"
              />
            </div>
            <div className="bg-muted p-4 rounded-lg mt-4">
              <p className="text-xs text-muted-foreground">
                By registering, you confirm that you are authorized to manage the digital presence for this institution. Your account will require secondary verification by a nodal officer before becoming fully active.
              </p>
            </div>
          </div>
        )}

        <div className="flex gap-3 mt-6">
          {step === 2 && (
            <button 
              type="button" 
              onClick={() => setStep(1)}
              className="px-4 py-2.5 bg-secondary text-secondary-foreground font-medium rounded-lg hover:bg-secondary/80 transition-colors"
            >
              Back
            </button>
          )}
          <button type="submit" className="flex-1 py-2.5 bg-primary text-primary-foreground font-semibold rounded-lg hover:bg-primary/90 transition-colors">
            {step === 1 ? "Next Step" : "Complete Registration"}
          </button>
        </div>
      </form>

      <div className="mt-6 text-center text-sm text-muted-foreground">
        Already have an account?{" "}
        <Link href="/login" className="text-primary hover:underline font-medium">Sign in</Link>
      </div>
    </div>
  );
}
