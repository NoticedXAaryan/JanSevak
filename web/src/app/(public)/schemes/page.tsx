import React from "react";
import Link from "next/link";
import { Search, ChevronRight, Calculator, IndianRupee } from "lucide-react";
import { DotPattern } from "@/components/ui/dot-pattern";

export default function SchemesPage() {
  const categories = [
    "Agriculture & Farmers", "Health & Wellness", "Education & Learning", 
    "Women & Child", "Housing", "Social Welfare", "Business & MSME"
  ];

  return (
    <div className="w-full relative min-h-screen bg-background overflow-hidden">
      <DotPattern className="opacity-40 dark:opacity-20 text-border" />
      
      <div className="max-w-7xl mx-auto px-6 py-12 md:py-20 relative z-10">
        <div className="flex flex-col items-center text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-heading font-bold mb-6 tracking-tight">Government Schemes</h1>
          <p className="text-xl text-muted-foreground max-w-2xl">
            Discover central and state government schemes, subsidies, and welfare programs you might be eligible for.
          </p>
          
          <div className="mt-8 flex flex-col sm:flex-row gap-4 w-full max-w-3xl">
            <div className="relative group w-full">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-muted-foreground group-focus-within:text-primary transition-colors" />
              </div>
              <input
                type="text"
                className="block w-full pl-11 pr-4 py-3 text-lg border border-border rounded-xl bg-card/80 backdrop-blur-md text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all shadow-lg"
                placeholder="Search schemes..."
              />
            </div>
            <button className="px-8 py-3 bg-primary text-primary-foreground font-bold text-lg rounded-xl shadow-xl shadow-primary/20 hover:bg-primary/90 hover:scale-105 transition-all flex items-center justify-center shrink-0">
              <Calculator className="w-5 h-5 mr-2" />
              Check Eligibility
            </button>
          </div>
        </div>

        <div className="flex flex-col md:flex-row gap-8">
          <aside className="w-full md:w-64 shrink-0">
            <div className="liquid-glass p-6 rounded-2xl sticky top-24">
              <h3 className="font-heading font-bold text-lg mb-4">Beneficiary</h3>
              <ul className="space-y-2">
                <li>
                  <button className="w-full text-left px-3 py-2 text-sm font-semibold bg-primary/10 text-primary rounded-md">
                    All Schemes
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
                { id: 1, title: "PM Kisan Samman Nidhi", desc: "Income support of ₹6,000 per year to all landholding farmer families, provided in three equal installments.", dept: "Agriculture", icon: IndianRupee },
                { id: 2, title: "Ayushman Bharat", desc: "Health insurance coverage up to ₹5 Lakhs per family per year for secondary and tertiary care hospitalization.", dept: "Health", icon: IndianRupee },
                { id: 3, title: "Sukanya Samriddhi Yojana", desc: "A savings scheme for the parents of a girl child, offering higher interest rates and tax benefits.", dept: "Women & Child", icon: IndianRupee },
                { id: 4, title: "PM Awas Yojana", desc: "Credit linked subsidy scheme to provide affordable housing to the urban poor and weaker sections.", dept: "Housing", icon: IndianRupee },
                { id: 5, title: "Mudra Yojana", desc: "Loans up to ₹10 Lakhs for non-corporate, non-farm small/micro enterprises.", dept: "MSME", icon: IndianRupee },
                { id: 6, title: "Ujjwala Yojana", desc: "Providing clean cooking fuel (LPG) to women of below poverty line households.", dept: "Social Welfare", icon: IndianRupee },
              ].map((scheme) => (
                <Link key={scheme.id} href={`/schemes/scheme-${scheme.id}`} className="group block">
                  <div className="p-6 rounded-2xl liquid-glass hover:bg-accent/50 border-transparent hover:border-border hover:shadow-2xl transition-all duration-300 h-full flex flex-col group-hover:-translate-y-1">
                    <div className="w-12 h-12 rounded-xl bg-foreground/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                      <scheme.icon className="w-6 h-6 text-foreground" />
                    </div>
                    <h3 className="text-xl font-bold mb-3 group-hover:text-foreground transition-colors">
                      {scheme.title}
                    </h3>
                    <p className="text-sm text-muted-foreground mb-6 flex-1 leading-relaxed">
                      {scheme.desc}
                    </p>
                    <div className="flex items-center justify-between text-sm mt-auto pt-4 border-t border-border/50">
                      <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-accent text-foreground">
                        {scheme.dept}
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
