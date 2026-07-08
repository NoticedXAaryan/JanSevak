"use client";
import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function SettingsManagement() {
  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-heading font-semibold text-foreground">Institution Settings</h1>
          <p className="text-muted-foreground text-sm">Manage your public profile and platform integrations.</p>
        </div>
        <Button>Save Changes</Button>
      </div>

      <div className="bg-card border border-border rounded-xl shadow-sm p-6 space-y-6">
        <h2 className="text-lg font-semibold">Public Profile</h2>
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Institution Name</Label>
              <Input defaultValue="Civil Hospital, Central" />
            </div>
            <div className="space-y-2">
              <Label>Contact Email</Label>
              <Input defaultValue="contact@civilhospital.gov.in" />
            </div>
          </div>
          <div className="space-y-2">
            <Label>Address</Label>
            <Input defaultValue="Medical Road, Central District, 110001" />
          </div>
        </div>
      </div>

      <div className="bg-card border border-border rounded-xl shadow-sm p-6 space-y-6">
        <h2 className="text-lg font-semibold">API Integrations</h2>
        <p className="text-sm text-muted-foreground mb-4">Integrate your internal systems with JanSevak.</p>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label>Webhook URL</Label>
            <Input defaultValue="https://api.civilhospital.gov.in/jansevak/webhook" />
          </div>
          <div className="space-y-2">
            <Label>JanSevak API Key</Label>
            <Input type="password" defaultValue="jsk_live_9a8b7c6d5e4f3g2h1" />
          </div>
          <Button variant="outline">Regenerate Key</Button>
        </div>
      </div>
    </div>
  );
}
