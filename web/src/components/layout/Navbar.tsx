"use client";
import React from "react";
import Link from "next/link";
import Image from "next/image";
import { Search, Menu, X, Bot, User, Globe } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";

export default function Navbar() {
  const [isOpen, setIsOpen] = React.useState(false);
  const [isScrolled, setIsScrolled] = React.useState(false);
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [lang, setLang] = React.useState("EN");

  React.useEffect(() => {
    if (typeof window !== "undefined") {
      setIsLoggedIn(localStorage.getItem("jansevak_isLoggedIn") === "true");
      setLang(localStorage.getItem("jansevak_lang") || "EN");
    }
    
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const toggleLang = () => {
    const newLang = lang === "EN" ? "HI" : "EN";
    setLang(newLang);
    if (typeof window !== "undefined") {
      localStorage.setItem("jansevak_lang", newLang);
      window.dispatchEvent(new Event("languageChange"));
    }
  };

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
            <Link href="/" className="flex items-center gap-3 group">
              <div className="relative w-10 h-10 rounded-xl overflow-hidden flex items-center justify-center bg-black">
                <Image src="/logo.png" alt="JanSevak Logo" width={40} height={40} className="object-contain p-1" />
              </div>
              <span className="font-heading font-bold text-2xl tracking-tight text-foreground transition-colors group-hover:text-primary">JanSevak</span>
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
            <button onClick={toggleLang} className="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold text-muted-foreground hover:text-foreground liquid-glass rounded-full transition-all">
              <Globe className="w-4 h-4" />
              {lang}
            </button>
            <button className="p-2.5 text-muted-foreground hover:text-foreground rounded-full transition-colors hidden lg:block">
              <Search className="w-5 h-5" />
            </button>
            {isLoggedIn ? (
              <Link href="/chat">
                <Avatar className="h-9 w-9 border-2 border-border cursor-pointer hover:border-foreground transition-colors">
                  <AvatarFallback className="bg-foreground text-background font-bold">U</AvatarFallback>
                </Avatar>
              </Link>
            ) : (
              <Link href="/login" className="px-5 py-2.5 text-sm font-medium text-foreground transition-all">
                Log In
              </Link>
            )}
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
            <button onClick={toggleLang} className="flex items-center justify-center gap-2 px-4 py-3 text-center text-base font-medium text-foreground border border-border rounded-xl hover:bg-accent transition-colors">
              <Globe className="w-5 h-5" />
              Language: {lang === "EN" ? "English" : "हिंदी"}
            </button>
            {!isLoggedIn && (
              <Link href="/login" className="block px-4 py-3 text-center text-base font-medium text-foreground border border-border rounded-xl hover:bg-accent transition-colors">
                Log In
              </Link>
            )}
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
