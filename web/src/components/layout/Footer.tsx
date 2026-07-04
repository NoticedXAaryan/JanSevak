import React from "react";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-border bg-background pt-12 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          <div className="md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <div className="relative w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                <span className="font-heading font-bold text-lg text-primary-foreground">JS</span>
              </div>
              <span className="font-heading font-semibold text-xl text-foreground">JanSevak</span>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Empowering Indian citizens with AI-driven access to public services, schemes, and grievance redressal.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold text-foreground mb-4">Citizens</h3>
            <ul className="space-y-3 text-sm text-muted-foreground">
              <li><Link href="/services" className="hover:text-primary transition-colors">Find a Service</Link></li>
              <li><Link href="/schemes" className="hover:text-primary transition-colors">Government Schemes</Link></li>
              <li><Link href="/track" className="hover:text-primary transition-colors">Track Grievance</Link></li>
              <li><Link href="/institutions" className="hover:text-primary transition-colors">Institution Directory</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-foreground mb-4">Government</h3>
            <ul className="space-y-3 text-sm text-muted-foreground">
              <li><Link href="/login" className="hover:text-primary transition-colors">Official Login</Link></li>
              <li><Link href="/register/institution" className="hover:text-primary transition-colors">Register Institution</Link></li>
              <li><Link href="/about" className="hover:text-primary transition-colors">About the Platform</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-foreground mb-4">Legal</h3>
            <ul className="space-y-3 text-sm text-muted-foreground">
              <li><Link href="/privacy" className="hover:text-primary transition-colors">Privacy Policy</Link></li>
              <li><Link href="/terms" className="hover:text-primary transition-colors">Terms of Service</Link></li>
              <li><Link href="/accessibility" className="hover:text-primary transition-colors">Accessibility Statement</Link></li>
              <li><Link href="/contact" className="hover:text-primary transition-colors">Contact Us</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-border pt-8 flex flex-col md:flex-row items-center justify-between text-xs text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} JanSevak Initiative. Open Source Digital Public Good.</p>
          <div className="mt-4 md:mt-0 space-x-4">
            <Link href="/" className="hover:text-foreground">National Portal</Link>
            <Link href="/" className="hover:text-foreground">Digital India</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
