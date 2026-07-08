"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button, buttonVariants } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Home, 
  MessageSquare, 
  FileText, 
  AlertTriangle, 
  ShieldAlert, 
  Activity, 
  Settings,
  LayoutDashboard,
  Users
} from "lucide-react";

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  role?: "citizen" | "department" | "admin";
}

export function Sidebar({ className, role = "citizen" }: SidebarProps) {
  const pathname = usePathname();

  const citizenRoutes = [
    { name: "Home", path: "/", icon: Home },
    { name: "Ask JanSeva", path: "/chat", icon: MessageSquare },
    { name: "My Documents", path: "/documents", icon: FileText },
    { name: "Report Issue", path: "/complaints/new", icon: AlertTriangle },
    { name: "Whistleblower", path: "/report/anonymous", icon: ShieldAlert },
    { name: "Healthcare", path: "/healthcare", icon: Activity },
  ];

  const departmentRoutes = [
    { name: "Dashboard", path: "/dept/dashboard", icon: LayoutDashboard },
    { name: "Complaints", path: "/dept/complaints", icon: AlertTriangle },
    { name: "Reports (Sealed)", path: "/dept/reports", icon: ShieldAlert },
    { name: "Policies", path: "/dept/policies", icon: FileText },
    { name: "Settings", path: "/dept/settings", icon: Settings },
  ];
  
  const adminRoutes = [
    { name: "Admin Dashboard", path: "/admin/dashboard", icon: LayoutDashboard },
    { name: "Organizations", path: "/admin/orgs", icon: Users },
  ];

  const routes = role === "admin" ? adminRoutes : role === "department" ? departmentRoutes : citizenRoutes;

  return (
    <div className={cn("pb-12 border-r border-border liquid-glass h-screen flex flex-col", className)}>
      <div className="space-y-4 py-4 flex-1">
        <div className="px-3 py-2">
          <div className="flex items-center gap-3 mb-2 px-4 mt-2">
            <div className="relative w-8 h-8 rounded-xl overflow-hidden flex items-center justify-center bg-black">
              <Image src="/logo.png" alt="JanSevak Logo" width={32} height={32} className="object-contain p-1" />
            </div>
            <h2 className="text-2xl font-bold tracking-tight">JanSevak</h2>
          </div>
          <p className="px-4 text-xs text-muted-foreground mb-6">
            {role === "citizen" ? "Citizen Portal" : role === "department" ? "Department Portal" : "Admin Portal"}
          </p>
          <div className="space-y-1">
            {routes.map((route) => (
              <Link
                key={route.path}
                href={route.path}
                className={cn(
                  buttonVariants({
                    variant: pathname === route.path ? "default" : "ghost",
                  }),
                  "w-full justify-start",
                  pathname === route.path && "bg-foreground text-background hover:bg-foreground/90 shadow-md"
                )}
              >
                <route.icon className="mr-2 h-4 w-4" />
                {route.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
