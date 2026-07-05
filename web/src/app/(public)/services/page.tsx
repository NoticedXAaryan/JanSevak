import React from "react";
import Link from "next/link";
import { Search, ChevronRight, FileText } from "lucide-react";
import { DotPattern } from "@/components/ui/dot-pattern";
import { cn } from "@/lib/utils";

export default function ServicesPage() {
  const categories = [
    "Certificates & Licenses", "Healthcare", "Agriculture", 
    "Education", "Municipal", "Police & Security", "Welfare"
  ];

  return (
    <div className="w-full relative min-h-screen bg-background overflow-hidden">
      <DotPattern className="opacity-40 dark:opacity-20 text-border" />
      
      <div className="max-w-7xl mx-auto px-6 py-12 md:py-20 relative z-10">
        <div className="flex flex-col items-center text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-heading font-bold mb-6 tracking-tight">Government Services</h1>
          <p className="text-xl text-muted-foreground max-w-2xl">
            Find and apply for government services across all departments. Search below or browse by category.
          </p>
          
          <div className="w-full max-w-2xl mt-8">
            <div className="relative group">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search className="h-6 w-6 text-muted-foreground group-focus-within:text-primary transition-colors" />
              </div>
              <input
                type="text"
                className="block w-full pl-12 pr-4 py-4 text-lg border border-border rounded-xl bg-card/80 backdrop-blur-md text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all shadow-lg"
                placeholder="Search for 'Income Certificate', 'Driving License', etc..."
              />
            </div>
          </div>
        </div>

        <div className="flex flex-col md:flex-row gap-8">
          <aside className="w-full md:w-64 shrink-0">
            <div className="liquid-glass p-6 rounded-2xl sticky top-24">
              <h3 className="font-heading font-bold text-lg mb-4">Categories</h3>
              <ul className="space-y-2">
                <li>
                  <button className="w-full text-left px-3 py-2 text-sm font-semibold bg-primary/10 text-primary rounded-md">
                    All Services
                  </button>
                </li>
                {categories.map((cat) => (
                  <li key={cat}>
                    <button className="w-full text-left px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-foreground rounded-md transition-colors">
                      {cat}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </aside>

          <main className="flex-1">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                { id: 1, title: "Income Certificate", desc: "Apply for an income certificate issued by the Revenue Department, required for various subsidies and admissions.", dept: "Revenue Dept", icon: FileText },
                { id: 2, title: "Driving License", desc: "Apply for a new driving license, renew an existing one, or book a driving test slot online.", dept: "Transport Dept", icon: FileText },
                { id: 3, title: "Birth Certificate", desc: "Register a new birth or apply for a duplicate birth certificate from the municipal corporation.", dept: "Municipal Corp", icon: FileText },
                { id: 4, title: "Property Tax Payment", desc: "Pay your annual property tax online, view past receipts, and calculate tax dues.", dept: "Municipal Corp", icon: FileText },
                { id: 5, title: "Police Clearance", desc: "Apply for a PCC required for passport, visa, or employment purposes.", dept: "Police Dept", icon: FileText },
                { id: 6, title: "Trade License", desc: "Apply for or renew a municipal trade license to operate a business legally.", dept: "Municipal Corp", icon: FileText },
              ].map((service) => (
                <Link key={service.id} href={`/services/service-${service.id}`} className="group block">
                  <div className="p-6 rounded-2xl liquid-glass hover:bg-accent/50 border-transparent hover:border-border hover:shadow-2xl transition-all duration-300 h-full flex flex-col group-hover:-translate-y-1">
                    <div className="w-12 h-12 rounded-xl bg-foreground/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                      <service.icon className="w-6 h-6 text-foreground" />
                    </div>
                    <h3 className="text-xl font-bold mb-3 group-hover:text-foreground transition-colors">
                      {service.title}
                    </h3>
                    <p className="text-sm text-muted-foreground mb-6 flex-1 leading-relaxed">
                      {service.desc}
                    </p>
                    <div className="flex items-center justify-between text-sm mt-auto pt-4 border-t border-border/50">
                      <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-accent text-foreground">
                        {service.dept}
                      </span>
                      <span className="flex items-center text-foreground font-bold opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all">
                        View details <ChevronRight className="w-4 h-4 ml-1" />
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
