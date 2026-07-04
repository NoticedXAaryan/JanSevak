import React from "react";

export default function AboutPage() {
  return (
    <div className="w-full max-w-4xl mx-auto px-6 py-12 md:py-20">
      <div className="text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-heading font-semibold mb-6">About JanSevak</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Building the next generation of digital public goods for India, powered by Artificial Intelligence.
        </p>
      </div>

      <div className="prose prose-invert prose-lg max-w-none">
        <h2>Our Mission</h2>
        <p>
          JanSevak aims to bridge the gap between Indian citizens and government services by providing an accessible, multi-lingual, AI-powered platform. We believe that every citizen should have frictionless access to the schemes, services, and institutions designed to serve them.
        </p>
        
        <h2>How It Works</h2>
        <p>
          At its core, JanSevak is a centralized knowledge base connected to multiple institutional endpoints. When a citizen asks a question or submits a request, our AI routing engine (powered by LangGraph) determines the intent and securely interfaces with the relevant department—whether it's checking hospital bed availability, applying for a certificate, or filing a grievance.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 my-12 not-prose">
          <div className="p-6 rounded-2xl bg-card border border-border">
            <h3 className="text-xl font-heading font-semibold mb-3">For Citizens</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li>• Single portal for all government services</li>
              <li>• Conversational AI in multiple languages</li>
              <li>• Transparent grievance tracking</li>
              <li>• Automated scheme eligibility checking</li>
            </ul>
          </div>
          <div className="p-6 rounded-2xl bg-card border border-border">
            <h3 className="text-xl font-heading font-semibold mb-3">For Institutions</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li>• Unified dashboard for managing requests</li>
              <li>• AI-assisted response drafting</li>
              <li>• Cross-departmental analytics</li>
              <li>• Automated escalation protocols</li>
            </ul>
          </div>
        </div>

        <h2>The Hackathon Project</h2>
        <p>
          This version of JanSevak was built as a demonstration of what is possible when modern AI architecture is applied to civic technology. It is a prototype designed to showcase the integration of LLMs, vector databases, and multi-agent workflows in a secure, scalable public sector context.
        </p>
      </div>
    </div>
  );
}
