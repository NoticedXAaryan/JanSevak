"use client";
import React from "react";
import Link from "next/link";
import { Search, Menu, X } from "lucide-react";

export default function Navbar() {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <nav className="sticky top-0 z-50 w-full backdrop-blur-md bg-background/80 border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-3">
            <Link href="/" className="flex items-center gap-2">
              <div className="relative w-8 h-8 rounded-full overflow-hidden flex items-center justify-center bg-primary border border-primary/20">
                <span className="font-heading font-bold text-lg tracking-tighter text-primary-foreground">JS</span>
              </div>
              <span className="font-heading font-semibold text-xl tracking-tight text-foreground">JanSevak</span>
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/services" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Services</Link>
            <Link href="/schemes" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Schemes</Link>
            <Link href="/institutions" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Institutions</Link>
            <Link href="/track" className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors">Track Status</Link>
          </div>

          <div className="hidden md:flex items-center space-x-4">
            <button className="p-2 text-muted-foreground hover:text-foreground rounded-full hover:bg-muted transition-colors">
              <Search className="w-5 h-5" />
            </button>
            <Link href="/login" className="px-4 py-2 text-sm font-semibold text-foreground hover:bg-muted rounded-full transition-colors">
              Log In
            </Link>
            <Link href="/register" className="px-4 py-2 text-sm font-semibold bg-primary text-primary-foreground rounded-full hover:bg-primary/90 transition-transform active:scale-95">
              Citizen Portal
            </Link>
          </div>

          <div className="md:hidden flex items-center">
            <button onClick={() => setIsOpen(!isOpen)} className="p-2 text-foreground">
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden bg-background border-b border-border">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link href="/services" className="block px-3 py-2 text-base font-medium text-foreground hover:bg-muted rounded-md">Services</Link>
            <Link href="/schemes" className="block px-3 py-2 text-base font-medium text-foreground hover:bg-muted rounded-md">Schemes</Link>
            <Link href="/institutions" className="block px-3 py-2 text-base font-medium text-foreground hover:bg-muted rounded-md">Institutions</Link>
            <Link href="/track" className="block px-3 py-2 text-base font-medium text-foreground hover:bg-muted rounded-md">Track Status</Link>
            <div className="pt-4 flex flex-col gap-2">
              <Link href="/login" className="block px-3 py-2 text-center text-base font-medium text-foreground border border-border rounded-md">Log In</Link>
              <Link href="/register" className="block px-3 py-2 text-center text-base font-medium bg-primary text-primary-foreground rounded-md">Citizen Portal</Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
