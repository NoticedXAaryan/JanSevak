"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ShieldAlert } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { DotPattern } from "@/components/ui/dot-pattern";
import { toast } from "sonner";
import Image from "next/image";

export default function CitizenLogin() {
  const router = useRouter();
  const [phone, setPhone] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState("");

  const [isLoading, setIsLoading] = useState(false);

  const handleSendOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (phone.length < 10) {
      toast.error("Please enter a valid 10-digit phone number");
      return;
    }
    
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/auth/otp/request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone_number: phone })
      });
      
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to send OTP");
      }
      
      toast.success(data.message || `OTP sent successfully to ${phone} via Telegram`);
      setOtpSent(true);
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (otp.length < 4) {
      toast.error("Please enter a valid OTP");
      return;
    }
    
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone_number: phone, otp })
      });
      
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Invalid OTP");
      }
      
      toast.success("Logged in successfully!");
      localStorage.setItem("jansevak_isLoggedIn", "true");
      // Store token if needed: localStorage.setItem("token", data.access_token);
      router.push("/chat");
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4 relative overflow-hidden">
      <DotPattern className="absolute inset-0 opacity-40 dark:opacity-20 text-border pointer-events-none" />
      <Card className="w-full max-w-md liquid-glass border-border shadow-2xl relative z-10 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-[2px] tricolor-glow"></div>
        <CardHeader className="space-y-2 text-center pt-8">
          <div className="flex justify-center mb-4">
            <h2 className="text-3xl font-bold tracking-tight">JanSevak</h2>
          </div>
          <CardTitle className="text-2xl font-bold tracking-tight">Welcome to JanSevak</CardTitle>
          <CardDescription>Enter your phone number to sign in or create an account</CardDescription>
        </CardHeader>
        <CardContent>
          {!otpSent ? (
            <form onSubmit={handleSendOtp} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="phone">Phone Number</Label>
                <div className="flex">
                  <div className="flex items-center justify-center rounded-l-md border border-r-0 border-border bg-muted/20 px-3 text-sm text-muted-foreground">
                    +91
                  </div>
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="9876543210"
                    className="rounded-l-none"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                  />
                </div>
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "Sending..." : "Send OTP"}
              </Button>
            </form>
          ) : (
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="otp">One-Time Password</Label>
                <Input
                  id="otp"
                  type="text"
                  placeholder="Enter 4-digit OTP"
                  maxLength={4}
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  required
                />
                <p className="text-xs text-muted-foreground">
                  Hint: Check the JanSevak Telegram bot for your OTP.
                </p>
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? "Verifying..." : "Verify & Sign In"}
              </Button>
              <Button variant="ghost" className="w-full" onClick={() => setOtpSent(false)} disabled={isLoading}>
                Use a different number
              </Button>
            </form>
          )}
        </CardContent>
        <CardFooter className="flex flex-col space-y-4 border-t border-border/50 px-6 py-4 bg-muted/10">
          <div className="text-sm text-center text-muted-foreground">
            Department Official? <Link href="/dept/login" className="text-foreground hover:underline font-medium">Sign in here</Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
