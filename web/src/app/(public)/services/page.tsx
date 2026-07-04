import React from "react";
import Link from "next/link";
import { Search, ChevronRight, FileText } from "lucide-react";

export default function ServicesPage() {
  const categories = [
    "Certificates & Licenses", "Healthcare", "Agriculture", 
    "Education", "Municipal", "Police & Security", "Welfare"
  ];

  return (
    <div className="w-full max-w-7xl mx-auto px-6 py-12 md:py-20">
      <div className="flex flex-col items-center text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-heading font-semibold mb-6">Government Services</h1>
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
              className="block w-full pl-12 pr-4 py-4 text-lg border border-border rounded-xl bg-card text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all shadow-sm"
              placeholder="Search for 'Income Certificate', 'Driving License', etc..."
            />
          </div>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        <aside className="w-full md:w-64 shrink-0">
          <h3 className="font-heading font-semibold text-lg mb-4">Categories</h3>
          <ul className="space-y-2">
            <li>
              <button className="w-full text-left px-3 py-2 text-sm font-medium bg-primary/10 text-primary rounded-md">
                All Services
              </button>
            </li>
            {categories.map((cat) => (
              <li key={cat}>
                <button className="w-full text-left px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground rounded-md transition-colors">
                  {cat}
                </button>
              </li>
            ))}
          </ul>
        </aside>

        <main className="flex-1">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <Link key={i} href={`/services/service-${i}`} className="group block">
                <div className="p-6 rounded-2xl bg-card border border-border hover:border-primary/50 transition-colors h-full flex flex-col">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                    <FileText className="w-5 h-5 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
                    Income Certificate
                  </h3>
                  <p className="text-sm text-muted-foreground mb-4 flex-1">
                    Apply for an income certificate issued by the Revenue Department, required for various subsidies and admissions.
                  </p>
                  <div className="flex items-center justify-between text-sm">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-secondary text-secondary-foreground">
                      Revenue Dept
                    </span>
                    <span className="flex items-center text-primary font-medium opacity-70 group-hover:opacity-100 transition-opacity">
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
  );
}
