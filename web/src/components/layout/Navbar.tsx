"use client";
import React from "react";
import Link from "next/link";
import Image from "next/image";
import { Search, Menu, X, Bot } from "lucide-react";
import { cn } from "@/lib/utils";

export default function Navbar() {
  const [isOpen, setIsOpen] = React.useState(false);
  const [isScrolled, setIsScrolled] = React.useState(false);

  React.useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav className={cn(
      "fixed top-0 inset-x-0 z-50 w-full transition-all duration-300",
      isScrolled 
        ? "bg-background/40 liquid-glass border-b border-border shadow-sm" 
        : "bg-transparent"
    )}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20 items-center">
          <div className="flex items-center gap-3">
            <Link href="/" className="flex items-center gap-2 group">
              <div className="relative w-10 h-10 rounded-xl bg-foreground flex items-center justify-center shadow-lg overflow-hidden border border-border">
                <Image src="/jansevak-logo.png" alt="JanSevak Logo" fill className="object-cover" />
              </div>
              <span className="font-heading font-bold text-xl text-foreground group-hover:text-primary transition-colors">JanSevak</span>
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-1 liquid-glass px-4 py-2 rounded-full">
            {[
              { name: "Services", href: "/services" },
              { name: "Schemes", href: "/schemes" },
              { name: "Institutions", href: "/institutions" },
              { name: "Track Status", href: "/track" },
            ].map((link) => (
              <Link 
                key={link.name} 
                href={link.href} 
                className="px-4 py-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-all duration-300 relative after:absolute after:bottom-0 after:left-1/2 after:-translate-x-1/2 after:w-0 after:h-[2px] after:bg-foreground hover:after:w-1/2 after:transition-all after:duration-300"
              >
                {link.name}
              </Link>
            ))}
          </div>

          <div className="hidden md:flex items-center space-x-3">
            <button className="p-2.5 text-muted-foreground hover:text-foreground rounded-full transition-colors">
              <Search className="w-5 h-5" />
            </button>
            <Link href="/login" className="px-5 py-2.5 text-sm font-medium text-foreground transition-all">
              Log In
            </Link>
            <Link href="/chat" className="px-5 py-2.5 text-sm font-bold bg-foreground text-background rounded-full hover:bg-foreground/90 transition-all active:scale-95 flex items-center gap-2 group">
              <Bot className="w-4 h-4 group-hover:animate-bounce" />
              Ask AI
            </Link>
          </div>

          <div className="md:hidden flex items-center">
            <button 
              onClick={() => setIsOpen(!isOpen)} 
              className="p-2 text-foreground liquid-glass rounded-xl"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile menu */}
      <div className={cn(
        "md:hidden overflow-hidden transition-all duration-300 ease-in-out liquid-glass border-x-0 border-t-0 rounded-none",
        isOpen ? "max-h-[400px] border-b border-border shadow-xl" : "max-h-0 opacity-0"
      )}>
        <div className="px-4 pt-2 pb-6 space-y-2">
          {[
            { name: "Services", href: "/services" },
            { name: "Schemes", href: "/schemes" },
            { name: "Institutions", href: "/institutions" },
            { name: "Track Status", href: "/track" },
          ].map((link) => (
            <Link 
              key={link.name} 
              href={link.href} 
              className="block px-4 py-3 text-base font-medium text-foreground hover:bg-accent rounded-xl transition-colors"
            >
              {link.name}
            </Link>
          ))}
          <div className="pt-4 mt-4 flex flex-col gap-3 border-t border-border">
            <Link href="/login" className="block px-4 py-3 text-center text-base font-medium text-foreground border border-border rounded-xl hover:bg-accent transition-colors">
              Log In
            </Link>
            <Link href="/chat" className="flex items-center justify-center gap-2 px-4 py-3 text-center text-base font-bold bg-foreground text-background rounded-xl">
              <Bot className="w-5 h-5" />
              Ask AI
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
