"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
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
    <div className={cn("pb-12 border-r bg-card h-screen flex flex-col", className)}>
      <div className="space-y-4 py-4 flex-1">
        <div className="px-3 py-2">
          <div className="flex items-center mb-2 px-4">
            <ShieldAlert className="w-6 h-6 mr-2 text-primary" />
            <h2 className="text-xl font-bold tracking-tight">JanSevak</h2>
          </div>
          <p className="px-4 text-xs text-muted-foreground mb-4">
            {role === "citizen" ? "Citizen Portal" : role === "department" ? "Department Portal" : "Admin Portal"}
          </p>
          <div className="space-y-1">
            {routes.map((route) => (
              <Button
                key={route.path}
                variant={pathname === route.path ? "secondary" : "ghost"}
                className="w-full justify-start"
                asChild
              >
                <Link href={route.path}>
                  <route.icon className="mr-2 h-4 w-4" />
                  {route.name}
                </Link>
              </Button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
