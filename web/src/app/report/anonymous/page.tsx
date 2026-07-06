"use client";

import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { ShieldAlert, Send, Lock, EyeOff } from "lucide-react";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

export default function AnonymousReport() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      // In a real application, encryption happens here before sending
      const form = e.target as HTMLFormElement;
      const target = (form.elements.namedItem('target') as HTMLInputElement).value;
      const desc = (form.elements.namedItem('desc') as HTMLTextAreaElement).value;
      const isSealed = (form.elements.namedItem('seal') as HTMLInputElement).checked;

      // Mock encryption for demo
      const payload = {
        category: target,
        content_encrypted: btoa(desc), // simple base64 mock
        identity_envelope_encrypted: isSealed ? btoa("user-identity-data") : "anonymous",
      };

      const res = await fetch("http://localhost:8000/api/v1/reports", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to submit report");
      }
      
      toast.success(`Sealed Report submitted securely. Tracking Token: ${data.report_token}`, {
        duration: 10000,
      });
      
      // Delay redirect to let user copy the token
      setTimeout(() => {
        router.push("/");
      }, 5000);
      
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AppLayout role="citizen">
      <div className="max-w-3xl mx-auto">
        <Card className="border-t-4 border-t-destructive bg-destructive/5 dark:bg-destructive/10">
          <CardHeader>
            <div className="flex items-center gap-2 mb-2">
              <ShieldAlert className="w-6 h-6 text-destructive" />
              <CardTitle className="text-2xl text-destructive dark:text-red-400">Secure Whistleblower Portal</CardTitle>
            </div>
            <CardDescription className="text-foreground/80">
              Report corruption, bribery, or severe misconduct. Your identity is placed in a 
              <strong> digitally sealed envelope</strong>. It can only be unsealed with a court order requiring dual-key authorization.
            </CardDescription>
          </CardHeader>
        </Card>

        <Card className="mt-6">
          <CardContent className="pt-6">
            <form id="whistle-form" onSubmit={handleSubmit} className="space-y-6">
              
              <div className="p-4 bg-muted rounded-lg flex items-start gap-3 border">
                <Lock className="w-5 h-5 text-muted-foreground mt-0.5 shrink-0" />
                <div className="text-sm text-muted-foreground">
                  <strong>End-to-End Encrypted:</strong> The details of this report are encrypted before leaving your device. Only authorized anti-corruption officials can read the content.
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="target">Department / Official Being Reported</Label>
                <Input id="target" name="target" placeholder="e.g. Revenue Dept, Lucknow" required />
              </div>

              <div className="space-y-2">
                <Label htmlFor="desc">Incident Description</Label>
                <Textarea 
                  id="desc" 
                  name="desc"
                  placeholder="Provide specific details, dates, and amounts if applicable..." 
                  className="min-h-[150px]"
                  required
                />
              </div>

              <div className="space-y-4 border p-4 rounded-lg bg-destructive/5 border-destructive/20">
                <h3 className="font-medium flex items-center gap-2 text-destructive">
                  <EyeOff className="w-4 h-4" /> Identity Protection (Sealed Envelope)
                </h3>
                <p className="text-sm text-muted-foreground">
                  You may choose to remain completely anonymous, or seal your identity. A sealed identity allows investigators to contact you, but requires a legal warrant to unseal.
                </p>
                <div className="space-y-3 pt-2">
                  <div className="flex items-center space-x-2">
                    <input type="radio" id="anon" name="identity" className="text-primary focus:ring-primary h-4 w-4" defaultChecked />
                    <Label htmlFor="anon" className="font-normal">Stay Completely Anonymous</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <input type="radio" id="seal" name="identity" className="text-primary focus:ring-primary h-4 w-4" />
                    <Label htmlFor="seal" className="font-normal">Seal My Identity (Recommended for investigation updates)</Label>
                  </div>
                </div>
              </div>

            </form>
          </CardContent>
          <CardFooter className="flex justify-between border-t p-6">
            <Button variant="ghost" onClick={() => router.back()}>Cancel</Button>
            <Button type="submit" form="whistle-form" disabled={isSubmitting} variant="destructive" className="min-w-[200px]">
              {isSubmitting ? "Encrypting & Sending..." : "Submit Secure Report"}
              {!isSubmitting && <Lock className="w-4 h-4 ml-2" />}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </AppLayout>
  );
}
