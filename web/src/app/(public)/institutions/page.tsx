import React from "react";
import Link from "next/link";
import { Search, MapPin, Building2, ExternalLink } from "lucide-react";

export default function InstitutionsPage() {
  const types = [
    "Hospitals", "Police Stations", "Schools", 
    "Revenue Offices", "Municipal", "UIDAI Centers", "Agriculture Offices"
  ];

  return (
    <div className="w-full max-w-7xl mx-auto px-6 py-12 md:py-20">
      <div className="flex flex-col items-center text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-heading font-semibold mb-6">Public Institutions Directory</h1>
        <p className="text-xl text-muted-foreground max-w-2xl">
          Locate and connect with government offices, hospitals, and police stations near you.
        </p>
        
        <div className="w-full max-w-2xl mt-8 flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1 group">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-muted-foreground group-focus-within:text-primary transition-colors" />
            </div>
            <input
              type="text"
              className="block w-full pl-11 pr-4 py-3 text-base border border-border rounded-xl bg-card text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all shadow-sm"
              placeholder="Search institutions by name..."
            />
          </div>
          <div className="relative sm:w-48 group">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <MapPin className="h-5 w-5 text-muted-foreground group-focus-within:text-primary transition-colors" />
            </div>
            <select className="block w-full pl-11 pr-4 py-3 text-base border border-border rounded-xl bg-card text-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 appearance-none transition-all shadow-sm">
              <option>All Districts</option>
              <option>Delhi</option>
              <option>Mumbai</option>
              <option>Bangalore</option>
            </select>
          </div>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        <aside className="w-full md:w-64 shrink-0">
          <h3 className="font-heading font-semibold text-lg mb-4">Institution Type</h3>
          <ul className="space-y-2">
            <li>
              <button className="w-full text-left px-3 py-2 text-sm font-medium bg-primary/10 text-primary rounded-md">
                All Types
              </button>
            </li>
            {types.map((type) => (
              <li key={type}>
                <button className="w-full text-left px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground rounded-md transition-colors">
                  {type}
                </button>
              </li>
            ))}
          </ul>
        </aside>

        <main className="flex-1">
          <div className="grid grid-cols-1 gap-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="p-6 rounded-2xl bg-card border border-border hover:border-primary/50 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                    <Building2 className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-1">
                      District General Hospital, Example City
                    </h3>
                    <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground mb-3">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5" /> Sector 14, Main Road
                      </span>
                      <span className="px-2 py-0.5 rounded bg-secondary text-secondary-foreground text-xs font-medium">
                        Healthcare
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground line-clamp-2">
                      Primary referral hospital providing 24/7 emergency services, OPD, and specialized care.
                    </p>
                  </div>
                </div>
                <div className="shrink-0 flex flex-col gap-2">
                  <Link href={`/institutions/${i}`} className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium bg-secondary hover:bg-secondary/80 text-secondary-foreground rounded-lg transition-colors">
                    View Profile
                  </Link>
                  <a href="#" className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-primary hover:bg-primary/10 rounded-lg transition-colors">
                    Get Directions <ExternalLink className="w-4 h-4 ml-2" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
