import React from "react";
import Link from "next/link";
import { Bot, Mail, Shield, ShieldCheck } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-background text-muted-foreground pt-20 pb-10 border-t border-border relative overflow-hidden">
      {/* Decorative Glow */}
      <div className="absolute top-0 left-0 w-full h-1 tricolor-glow opacity-50"></div>
      
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 mb-16">
          <div className="md:col-span-4">
            <div className="flex items-center gap-3 mb-6">
              <div className="relative w-12 h-12 rounded-xl bg-foreground flex items-center justify-center shadow-lg">
                <span className="font-heading font-bold text-xl text-background">JS</span>
              </div>
              <span className="font-heading font-bold text-2xl text-foreground">JanSevak</span>
            </div>
            <p className="text-muted-foreground leading-relaxed mb-6">
              Empowering Indian citizens with AI-driven access to public services, schemes, and grievance redressal. A modern unified interface for GovTech.
            </p>
            <div className="flex items-center gap-4">
              <a href="#" className="w-10 h-10 rounded-full bg-accent border border-border flex items-center justify-center hover:bg-foreground hover:text-background transition-colors">
                <Bot className="w-5 h-5" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full bg-accent border border-border flex items-center justify-center hover:bg-foreground hover:text-background transition-colors">
                <Mail className="w-5 h-5" />
              </a>
            </div>
          </div>
          
          <div className="md:col-span-2 md:col-start-6">
            <h3 className="font-bold text-foreground mb-6 uppercase tracking-wider text-sm">Citizens</h3>
            <ul className="space-y-4 text-sm">
              <li><Link href="/services" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>Find a Service</Link></li>
              <li><Link href="/schemes" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>Government Schemes</Link></li>
              <li><Link href="/track" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>Track Grievance</Link></li>
              <li><Link href="/institutions" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>Institution Directory</Link></li>
            </ul>
          </div>

          <div className="md:col-span-2">
            <h3 className="font-bold text-foreground mb-6 uppercase tracking-wider text-sm">Government</h3>
            <ul className="space-y-4 text-sm">
              <li><Link href="/login" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>Official Login</Link></li>
              <li><Link href="/register/institution" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>Register Institution</Link></li>
              <li><Link href="/about" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>About the Platform</Link></li>
            </ul>
          </div>

          <div className="md:col-span-2">
            <h3 className="font-bold text-foreground mb-6 uppercase tracking-wider text-sm">Legal</h3>
            <ul className="space-y-4 text-sm">
              <li><Link href="/privacy" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>Privacy Policy</Link></li>
              <li><Link href="/terms" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>Terms of Service</Link></li>
              <li><Link href="/accessibility" className="hover:text-foreground transition-colors flex items-center gap-2"><span className="w-1 h-1 rounded-full bg-border"></span>Accessibility</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-border pt-8 flex flex-col md:flex-row items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <ShieldCheck className="w-5 h-5 text-green-500" />
            <p>&copy; {new Date().getFullYear()} JanSevak Initiative. Built for Bharat.</p>
          </div>
          <div className="flex space-x-6">
            <Link href="/" className="hover:text-foreground transition-colors">National Portal</Link>
            <Link href="/" className="hover:text-foreground transition-colors">Digital India</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
