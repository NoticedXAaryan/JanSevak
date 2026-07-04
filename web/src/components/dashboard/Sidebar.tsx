"use client";
import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Users, 
  FileText, 
  Settings, 
  HelpCircle,
  Building2
} from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    { name: "Overview", href: "/dashboard", icon: LayoutDashboard },
    { name: "Citizens", href: "/dashboard/citizens", icon: Users },
    { name: "Reports", href: "/dashboard/reports", icon: FileText },
    { name: "My Institution", href: "/dashboard/settings", icon: Building2 },
    { name: "Support", href: "/dashboard/support", icon: HelpCircle },
  ];

  return (
    <aside className="w-64 bg-card border-r border-border hidden md:flex flex-col">
      <div className="h-16 flex items-center px-6 border-b border-border">
        <div className="flex items-center gap-2">
          <div className="relative w-8 h-8 rounded-full bg-primary flex items-center justify-center">
            <span className="font-heading font-bold text-lg text-primary-foreground">JS</span>
          </div>
          <span className="font-heading font-semibold text-xl text-foreground">JanSevak</span>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto py-6">
        <nav className="space-y-1 px-3">
          {links.map((link) => {
            const isActive = pathname === link.href;
            const Icon = link.icon;
            return (
              <Link
                key={link.name}
                href={link.href}
                className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-md transition-colors ${
                  isActive 
                    ? "bg-primary/10 text-primary" 
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <Icon className={`w-5 h-5 mr-3 ${isActive ? "text-primary" : "text-muted-foreground"}`} />
                {link.name}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="p-4 border-t border-border">
        <div className="bg-muted rounded-lg p-4">
          <p className="text-xs font-semibold text-foreground mb-1">Need AI Help?</p>
          <p className="text-xs text-muted-foreground mb-3">Ask JanSevak about your data</p>
          <button className="w-full py-2 bg-primary text-primary-foreground text-xs font-semibold rounded-md hover:bg-primary/90 transition-colors">
            Open Chat
          </button>
        </div>
      </div>
    </aside>
  );
}
