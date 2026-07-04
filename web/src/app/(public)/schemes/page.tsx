import React from "react";
import Link from "next/link";
import { Search, ChevronRight, Calculator, IndianRupee } from "lucide-react";

export default function SchemesPage() {
  const categories = [
    "Agriculture & Farmers", "Health & Wellness", "Education & Learning", 
    "Women & Child", "Housing", "Social Welfare", "Business & MSME"
  ];

  return (
    <div className="w-full max-w-7xl mx-auto px-6 py-12 md:py-20">
      <div className="flex flex-col items-center text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-heading font-semibold mb-6">Government Schemes</h1>
        <p className="text-xl text-muted-foreground max-w-2xl">
          Discover central and state government schemes, subsidies, and welfare programs you might be eligible for.
        </p>
        
        <div className="mt-8 flex flex-col sm:flex-row gap-4">
          <div className="relative group w-full sm:w-96">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-muted-foreground group-focus-within:text-primary transition-colors" />
            </div>
            <input
              type="text"
              className="block w-full pl-11 pr-4 py-3 text-base border border-border rounded-xl bg-card text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all shadow-sm"
              placeholder="Search schemes..."
            />
          </div>
          <button className="px-6 py-3 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 transition-colors flex items-center justify-center shrink-0">
            <Calculator className="w-5 h-5 mr-2" />
            Check Eligibility
          </button>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        <aside className="w-full md:w-64 shrink-0">
          <h3 className="font-heading font-semibold text-lg mb-4">Beneficiary</h3>
          <ul className="space-y-2">
            <li>
              <button className="w-full text-left px-3 py-2 text-sm font-medium bg-primary/10 text-primary rounded-md">
                All Schemes
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
              <Link key={i} href={`/schemes/scheme-${i}`} className="group block">
                <div className="p-6 rounded-2xl bg-card border border-border hover:border-primary/50 transition-colors h-full flex flex-col">
                  <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center mb-4">
                    <IndianRupee className="w-5 h-5 text-emerald-500" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition-colors">
                    PM Kisan Samman Nidhi
                  </h3>
                  <p className="text-sm text-muted-foreground mb-4 flex-1">
                    Income support of ₹6,000 per year to all landholding farmer families, provided in three equal installments.
                  </p>
                  <div className="flex items-center justify-between text-sm">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-secondary text-secondary-foreground">
                      Agriculture
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
