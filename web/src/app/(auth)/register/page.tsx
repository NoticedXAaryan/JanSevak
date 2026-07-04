"use client";
import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { setSession } from "@/lib/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [phone, setPhone] = useState("");
  const [step, setStep] = useState(1);

  const handleSendOTP = (e: React.FormEvent) => {
    e.preventDefault();
    setStep(2);
  };

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    // Mock citizen login
    setSession({
      id: "cit_123",
      name: "Demo Citizen",
      phone,
      role: "citizen",
    });
    // Redirect to public dashboard or back to what they were doing
    router.push("/");
  };

  return (
    <div className="w-full bg-card border border-border rounded-2xl shadow-xl p-8">
      <div className="flex flex-col items-center mb-8">
        <h1 className="text-2xl font-heading font-semibold text-foreground">Citizen Registration</h1>
        <p className="text-sm text-muted-foreground mt-1">Access services securely via OTP</p>
      </div>

      {step === 1 ? (
        <form onSubmit={handleSendOTP} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Mobile Number</label>
            <div className="flex">
              <span className="inline-flex items-center px-4 rounded-l-lg border border-r-0 border-border bg-muted text-muted-foreground text-sm">
                +91
              </span>
              <input
                type="tel"
                required
                pattern="[0-9]{10}"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full px-4 py-2 bg-background border border-border rounded-r-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
                placeholder="9876543210"
              />
            </div>
          </div>
          <button type="submit" className="w-full py-2.5 bg-primary text-primary-foreground font-semibold rounded-lg hover:bg-primary/90 transition-colors mt-6">
            Send OTP
          </button>
        </form>
      ) : (
        <form onSubmit={handleVerify} className="space-y-4 animate-in fade-in zoom-in duration-300">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Enter OTP sent to +91 {phone}</label>
            <input
              type="text"
              required
              className="w-full px-4 py-2 bg-background border border-border rounded-lg text-foreground text-center tracking-widest text-lg focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="••••"
              maxLength={4}
            />
          </div>
          <button type="submit" className="w-full py-2.5 bg-primary text-primary-foreground font-semibold rounded-lg hover:bg-primary/90 transition-colors mt-6">
            Verify & Continue
          </button>
          <button 
            type="button" 
            onClick={() => setStep(1)}
            className="w-full py-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            Wrong number? Change it
          </button>
        </form>
      )}

      <div className="mt-6 text-center text-sm text-muted-foreground">
        Are you a government official?{" "}
        <Link href="/register/institution" className="text-primary hover:underline font-medium">Register your institution</Link>
      </div>
    </div>
  );
}
