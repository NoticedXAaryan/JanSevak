"use client";
import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { setSession } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Mock login
    setSession({
      id: "usr_123",
      name: "Demo Admin",
      email,
      role: "org_admin",
      orgType: "generic"
    });
    router.push("/dashboard");
  };

  return (
    <div className="w-full bg-card border border-border rounded-2xl shadow-xl p-8">
      <div className="flex flex-col items-center mb-8">
        <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center mb-4">
          <span className="font-heading font-bold text-xl text-primary-foreground">JS</span>
        </div>
        <h1 className="text-2xl font-heading font-semibold text-foreground">Sign in to JanSevak</h1>
        <p className="text-sm text-muted-foreground mt-1">For citizens and officials</p>
      </div>

      <form onSubmit={handleLogin} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-foreground mb-1">Email or Phone</label>
          <input
            type="text"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
            placeholder="demo@gov.in"
          />
        </div>
        <div>
          <div className="flex items-center justify-between mb-1">
            <label className="block text-sm font-medium text-foreground">Password</label>
            <Link href="#" className="text-xs text-primary hover:underline">Forgot password?</Link>
          </div>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
            placeholder="••••••••"
          />
        </div>
        
        <button type="submit" className="w-full py-2.5 bg-primary text-primary-foreground font-semibold rounded-lg hover:bg-primary/90 transition-colors mt-6">
          Sign In
        </button>
      </form>

      <div className="mt-6 text-center text-sm text-muted-foreground">
        Don't have an account?{" "}
        <Link href="/register" className="text-primary hover:underline font-medium">Create one</Link>
      </div>
      
      <div className="mt-8 pt-6 border-t border-border">
        <div className="text-xs text-center text-muted-foreground bg-muted p-3 rounded-md">
          <strong>Demo Note:</strong> Any credentials will work. This will log you in as an Organization Admin.
        </div>
      </div>
    </div>
  );
}
