"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Search, MapPin, FileText, ShieldAlert, HeartPulse, MessageSquare, Languages, FileCheck, ArrowRight, Bot, User } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function LandingPage() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [placeholderText, setPlaceholderText] = useState("Ask anything...");

  // Typing effect for placeholders
  React.useEffect(() => {
    const examples = [
      "How do I get my PM Kisan money?",
      "Mera ration card gum ho gaya hai...",
      "Where is the nearest govt hospital?",
      "Report a pothole in my area",
      "Ayushman Bharat card apply kaise karein?"
    ];
    let timeout: NodeJS.Timeout;
    let currentExampleIndex = 0;
    let currentCharIndex = 0;
    let isDeleting = false;

    const type = () => {
      const currentExample = examples[currentExampleIndex];
      
      if (isDeleting) {
        setPlaceholderText(currentExample.substring(0, currentCharIndex - 1));
        currentCharIndex--;
      } else {
        setPlaceholderText(currentExample.substring(0, currentCharIndex + 1));
        currentCharIndex++;
      }

      let nextSpeed = isDeleting ? 30 : 60;

      if (!isDeleting && currentCharIndex === currentExample.length) {
        isDeleting = true;
        nextSpeed = 2500;
      } else if (isDeleting && currentCharIndex === 0) {
        isDeleting = false;
        currentExampleIndex = (currentExampleIndex + 1) % examples.length;
        nextSpeed = 500;
      }
      timeout = setTimeout(type, nextSpeed);
    };

    timeout = setTimeout(type, 800);
    return () => clearTimeout(timeout);
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    router.push(`/chat?q=${encodeURIComponent(query)}`);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col items-center">
      
      {/* 
        HERO SECTION 
        "Brainless" usage: A massive search bar right in the center. 
        Subtle Indian aesthetic: A soft tricolor glow behind the main text.
      */}
      <section className="w-full flex flex-col items-center justify-center px-4 pt-32 pb-20 relative overflow-hidden">
        
        {/* Subtle Tricolor Glow Behind Text */}
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-gradient-to-r from-[#FF9933]/10 via-white/5 to-[#138808]/10 blur-[100px] rounded-full pointer-events-none"></div>

        <div className="w-full max-w-3xl flex flex-col items-center relative z-10">
          <h1 className="text-5xl md:text-6xl font-heading font-bold text-foreground mb-4 text-center tracking-tight">
            JanSevak
          </h1>
          <p className="text-muted-foreground text-center mb-12 text-xl md:text-2xl max-w-2xl">
            Your simplified gateway to Indian Government Services. Ask a question, find a scheme, or report an issue.
          </p>

          {/* Central Search/Chat Box */}
          <form onSubmit={handleSearch} className="w-full relative shadow-sm rounded-2xl group mb-8">
            <div className="absolute inset-y-0 left-5 flex items-center pointer-events-none">
              <Search className="h-6 w-6 text-muted-foreground group-focus-within:text-foreground transition-colors" />
            </div>
            <Input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={placeholderText}
              className="w-full h-20 pl-16 pr-36 text-xl rounded-2xl bg-background border-2 border-border focus-visible:ring-0 focus-visible:border-primary transition-all shadow-md"
            />
            <div className="absolute inset-y-3 right-3 flex items-center">
              <Button type="submit" size="lg" className="h-full rounded-xl px-8 font-semibold text-lg">
                Ask JanSevak
              </Button>
            </div>
          </form>

          {/* Trust Anchor */}
          <div className="flex items-center justify-center gap-2 mb-8 text-xs font-medium text-muted-foreground bg-muted/30 px-4 py-2 rounded-full border border-border/50 shadow-sm backdrop-blur-sm">
            <ShieldAlert className="w-4 h-4 text-emerald-500" />
            <span>100% Free & Private. We never store your personal IDs or Aadhaar.</span>
          </div>

          {/* Suggestion Chips */}
          <div className="flex flex-wrap justify-center gap-3">
            <SuggestionChip 
              icon={<FileText className="w-4 h-4" />} 
              label="PM KISAN Scheme" 
              onClick={() => router.push("/chat?q=PM+KISAN+Scheme")}
            />
            <SuggestionChip 
              icon={<MapPin className="w-4 h-4" />} 
              label="Local Police Station" 
              onClick={() => router.push("/chat?q=Find+Local+Police+Station")}
            />
            <SuggestionChip 
              icon={<HeartPulse className="w-4 h-4" />} 
              label="Ayushman Bharat" 
              onClick={() => router.push("/chat?q=Ayushman+Bharat+Card")}
            />
            <SuggestionChip 
              icon={<ShieldAlert className="w-4 h-4" />} 
              label="Report Pothole" 
              onClick={() => router.push("/chat?q=Report+a+pothole+in+my+area")}
            />
          </div>
        </div>
      </section>

      {/* 
        FEATURES SECTION 
        Grounded copy, no fake SaaS jargon.
      */}
      <section className="w-full max-w-6xl px-4 py-24 border-t border-border/50">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight mb-4">Everything you need, in one place</h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            We've combined hundreds of separate government portals into a single, easy-to-use assistant that understands you.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard 
            icon={<MessageSquare className="w-8 h-8 text-foreground" />}
            title="Chat in Your Language"
            description="Don't know English? No problem. JanSevak understands Hindi, Marathi, Tamil, and many other regional languages fluently."
          />
          <FeatureCard 
            icon={<FileCheck className="w-8 h-8 text-foreground" />}
            title="Find Schemes Easily"
            description="Stop searching through confusing PDFs. Just tell us about yourself, and we'll tell you exactly which government benefits you qualify for."
          />
          <FeatureCard 
            icon={<MapPin className="w-8 h-8 text-foreground" />}
            title="Local Help & Reporting"
            description="Find the nearest government hospital, police station, or anonymously report civic issues like broken streetlights in seconds."
          />
        </div>
      </section>

      {/* 
        HOW IT WORKS
        Simple 3 step process
      */}
      <section className="w-full max-w-6xl px-4 py-24 border-t border-border/50 mb-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight mb-4">How it works</h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            No manuals needed. If you know how to use WhatsApp, you know how to use JanSevak.
          </p>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-center gap-6 md:gap-12">
          <Step 
            number="1"
            title="Ask a Question"
            description="Type your problem in the search bar above in your own words."
          />
          <ArrowRight className="w-8 h-8 text-muted-foreground hidden md:block" />
          <Step 
            number="2"
            title="Get Instant Answers"
            description="JanSevak instantly reads through official government data to give you the exact answer."
          />
          <ArrowRight className="w-8 h-8 text-muted-foreground hidden md:block" />
          <Step 
            number="3"
            title="Take Action"
            description="Apply for the scheme or find the location directly from the chat."
          />
        </div>
      </section>      {/* 
        MOCK CHAT PREVIEW (Added UX enhancement)
      */}
      <section className="w-full max-w-4xl px-4 py-12 mb-12 flex flex-col items-center">
        <div className="w-full rounded-3xl border border-border/50 bg-muted/10 shadow-xl overflow-hidden backdrop-blur-sm">
          <div className="px-6 py-4 border-b border-border/50 bg-background/50 flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
              <Bot className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h4 className="font-bold text-sm">JanSevak Assistant</h4>
              <p className="text-xs text-muted-foreground">Online • Official Govt Data</p>
            </div>
          </div>
          <div className="p-6 md:p-8 flex flex-col gap-6">
            {/* User Bubble */}
            <div className="flex items-start gap-4 self-end flex-row-reverse max-w-[85%] md:max-w-[70%]">
              <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center shrink-0">
                <User className="w-5 h-5 text-foreground" />
              </div>
              <div className="bg-primary text-primary-foreground px-5 py-3.5 rounded-2xl rounded-tr-none text-sm md:text-base shadow-sm">
                My street light has been broken for 3 weeks and the local office is ignoring me.
              </div>
            </div>
            
            {/* Bot Bubble */}
            <div className="flex items-start gap-4 max-w-[85%] md:max-w-[70%]">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0 border border-primary/20">
                <Bot className="w-5 h-5 text-primary" />
              </div>
              <div className="bg-background border border-border/50 px-5 py-4 rounded-2xl rounded-tl-none shadow-sm flex flex-col gap-3">
                <p className="text-sm md:text-base text-foreground leading-relaxed">
                  I can help you escalate this directly to the Municipal Corporation's grievance portal. 
                </p>
                <p className="text-sm md:text-base text-foreground leading-relaxed">
                  What is your <strong>Pin Code</strong> so I can locate the correct ward office?
                </p>
                <div className="flex gap-2 mt-2">
                  <button className="text-xs bg-muted/50 hover:bg-muted border border-border px-3 py-1.5 rounded-full transition-colors font-medium">Use my location</button>
                  <button className="text-xs bg-muted/50 hover:bg-muted border border-border px-3 py-1.5 rounded-full transition-colors font-medium">Type pin code</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}

function SuggestionChip({ icon, label, onClick }: { icon: React.ReactNode, label: string, onClick: () => void }) {
  return (
    <button 
      onClick={onClick}
      className="flex items-center gap-2 px-5 py-2.5 bg-muted/30 hover:bg-muted text-foreground text-sm rounded-full border border-border transition-colors font-medium"
    >
      <span className="text-muted-foreground">{icon}</span>
      {label}
    </button>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <div className="p-8 rounded-3xl bg-muted/20 border border-border/50 hover:bg-muted/40 transition-colors flex flex-col items-center text-center">
      <div className="w-16 h-16 rounded-2xl bg-background flex items-center justify-center border border-border shadow-sm mb-6">
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-muted-foreground leading-relaxed">
        {description}
      </p>
    </div>
  );
}

function Step({ number, title, description }: { number: string, title: string, description: string }) {
  return (
    <div className="flex flex-col items-center text-center max-w-[280px]">
      <div className="w-12 h-12 rounded-full bg-foreground text-background font-bold text-xl flex items-center justify-center mb-6">
        {number}
      </div>
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-muted-foreground">
        {description}
      </p>
    </div>
  );
}
