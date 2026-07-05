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

  const handleSendOtp = (e: React.FormEvent) => {
    e.preventDefault();
    if (phone.length < 10) {
      toast.error("Please enter a valid 10-digit phone number");
      return;
    }
    toast.success("OTP sent successfully to " + phone);
    setOtpSent(true);
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (otp.length < 4) {
      toast.error("Please enter a valid OTP");
      return;
    }
    toast.success("Logged in successfully!");
    router.push("/");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4 relative overflow-hidden">
      <DotPattern className="absolute inset-0 opacity-40 dark:opacity-20 text-border pointer-events-none" />
      <Card className="w-full max-w-md liquid-glass border-border shadow-2xl relative z-10 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-[2px] tricolor-glow"></div>
        <CardHeader className="space-y-2 text-center pt-8">
          <div className="flex justify-center mb-4">
            <div className="relative w-16 h-16 rounded-xl bg-foreground flex items-center justify-center shadow-lg overflow-hidden border border-border">
              <Image src="/jansevak-logo.png" alt="JanSevak Logo" fill className="object-cover" />
            </div>
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
              <Button type="submit" className="w-full">
                Send OTP
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
                  Hint: You can enter any 4 digits for this demo.
                </p>
              </div>
              <Button type="submit" className="w-full">
                Verify & Sign In
              </Button>
              <Button variant="ghost" className="w-full" onClick={() => setOtpSent(false)}>
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
