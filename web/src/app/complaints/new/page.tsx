"use client";

import { useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Camera, MapPin, Send, UploadCloud, AlertTriangle } from "lucide-react";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

export default function NewComplaint() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      toast.success("Complaint filed successfully! Tracking ID: CMP-2026-X7Y8Z");
      setIsSubmitting(false);
      router.push("/");
    }, 1500);
  };

  return (
    <AppLayout role="citizen">
      <div className="max-w-3xl mx-auto">
        <Card className="border-t-4 border-t-amber-500">
          <CardHeader>
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="w-5 h-5 text-amber-500" />
              <CardTitle className="text-2xl">Report a Civic Issue</CardTitle>
            </div>
            <CardDescription>
              File a public complaint for issues like potholes, streetlights, or sanitation. 
              This will be publicly visible and assigned to the relevant department.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form id="complaint-form" onSubmit={handleSubmit} className="space-y-6">
              
              <div className="space-y-2">
                <Label htmlFor="category">Issue Category</Label>
                <Select required>
                  <SelectTrigger id="category">
                    <SelectValue placeholder="Select a category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="infrastructure">Infrastructure (Potholes, Roads)</SelectItem>
                    <SelectItem value="sanitation">Sanitation & Garbage</SelectItem>
                    <SelectItem value="water">Water Supply</SelectItem>
                    <SelectItem value="electricity">Electricity & Streetlights</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="desc">Description of the Issue</Label>
                <Textarea 
                  id="desc" 
                  placeholder="Please describe the issue in detail..." 
                  className="min-h-[120px]"
                  required
                />
              </div>

              <div className="space-y-4 border p-4 rounded-lg bg-muted/20">
                <h3 className="font-medium flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-primary" /> Location Details
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="district">District / City</Label>
                    <Input id="district" placeholder="e.g. Lucknow" required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="landmark">Landmark / Street</Label>
                    <Input id="landmark" placeholder="Near post office..." required />
                  </div>
                </div>
                <Button type="button" variant="outline" className="w-full sm:w-auto mt-2">
                  <MapPin className="w-4 h-4 mr-2" /> Detect My Location
                </Button>
              </div>

              <div className="space-y-4 border p-4 rounded-lg bg-muted/20">
                <h3 className="font-medium flex items-center gap-2">
                  <Camera className="w-4 h-4 text-primary" /> Photo Evidence
                </h3>
                <div className="border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center text-center cursor-pointer hover:bg-muted/50 transition-colors">
                  <UploadCloud className="w-8 h-8 text-muted-foreground mb-2" />
                  <p className="text-sm font-medium">Click to upload or drag and drop</p>
                  <p className="text-xs text-muted-foreground mt-1">SVG, PNG, JPG or GIF (max. 5MB)</p>
                  <Input type="file" className="hidden" accept="image/*" />
                </div>
              </div>

            </form>
          </CardContent>
          <CardFooter className="flex justify-between border-t p-6">
            <Button variant="ghost" onClick={() => router.back()}>Cancel</Button>
            <Button type="submit" form="complaint-form" disabled={isSubmitting} className="min-w-[150px]">
              {isSubmitting ? "Submitting..." : "Submit Report"}
              {!isSubmitting && <Send className="w-4 h-4 ml-2" />}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </AppLayout>
  );
}
