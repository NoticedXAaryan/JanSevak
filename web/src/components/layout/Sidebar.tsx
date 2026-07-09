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
  Users,
  ChevronLeft,
  ChevronRight
} from "lucide-react";

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  role?: "citizen" | "department" | "admin";
  isCollapsed?: boolean;
  setIsCollapsed?: (collapsed: boolean) => void;
}

export function Sidebar({ className, role = "citizen", isCollapsed = false, setIsCollapsed }: SidebarProps) {
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
    <div className={cn("pb-12 border-r border-border liquid-glass h-screen flex flex-col relative", className)}>
      <div className="space-y-4 py-4 flex-1">
        <div className="px-3 py-2">
          <div className={`flex items-center ${isCollapsed ? 'justify-center' : 'gap-3 px-4'} mb-2 mt-2`}>
            <div className="relative w-8 h-8 rounded-xl overflow-hidden flex items-center justify-center bg-black shrink-0">
              <Image src="/logo.png" alt="JanSevak Logo" width={32} height={32} className="object-contain p-1" />
            </div>
            {!isCollapsed && <h2 className="text-2xl font-bold tracking-tight whitespace-nowrap">JanSevak</h2>}
          </div>
          {!isCollapsed && (
            <p className="px-4 text-xs text-muted-foreground mb-6 whitespace-nowrap">
              {role === "citizen" ? "Citizen Portal" : role === "department" ? "Department Portal" : "Admin Portal"}
            </p>
          )}
          {isCollapsed && <div className="h-6 mb-6"></div>}
          <div className="space-y-1 mt-2">
            {routes.map((route) => (
              <Link
                key={route.path}
                href={route.path}
                title={isCollapsed ? route.name : undefined}
                className={cn(
                  buttonVariants({
                    variant: pathname === route.path ? "default" : "ghost",
                  }),
                  isCollapsed ? "w-full justify-center px-0" : "w-full justify-start",
                  pathname === route.path && "bg-foreground text-background hover:bg-foreground/90 shadow-md"
                )}
              >
                <route.icon className={cn("h-4 w-4", !isCollapsed && "mr-2")} />
                {!isCollapsed && <span className="whitespace-nowrap">{route.name}</span>}
              </Link>
            ))}
          </div>
        </div>
      </div>
      
      {setIsCollapsed && (
        <Button
          variant="ghost"
          size="icon"
          className="absolute -right-3 top-6 h-6 w-6 rounded-full border border-border bg-background shadow-md z-20 hover:bg-accent flex items-center justify-center"
          onClick={() => setIsCollapsed(!isCollapsed)}
        >
          {isCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      )}
    </div>
  );
}
