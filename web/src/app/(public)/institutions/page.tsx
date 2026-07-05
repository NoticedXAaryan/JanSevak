import React from "react";
import Link from "next/link";
import { Search, MapPin, Building2, ExternalLink } from "lucide-react";
import { DotPattern } from "@/components/ui/dot-pattern";

export default function InstitutionsPage() {
  const types = [
    "Hospitals", "Police Stations", "Schools", 
    "Revenue Offices", "Municipal", "UIDAI Centers", "Agriculture Offices"
  ];

  return (
    <div className="w-full relative min-h-screen bg-background overflow-hidden">
      <DotPattern className="opacity-40 dark:opacity-20 text-border" />
      
      <div className="max-w-7xl mx-auto px-6 py-12 md:py-20 relative z-10">
        <div className="flex flex-col items-center text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-heading font-bold mb-6 tracking-tight">Public Institutions</h1>
          <p className="text-xl text-muted-foreground max-w-2xl">
            Locate and connect with government offices, hospitals, and police stations near you.
          </p>
          
          <div className="w-full max-w-3xl mt-8 flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1 group">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-muted-foreground group-focus-within:text-primary transition-colors" />
              </div>
              <input
                type="text"
                className="block w-full pl-11 pr-4 py-3 text-lg border border-border rounded-xl bg-card/80 backdrop-blur-md text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all shadow-lg"
                placeholder="Search institutions by name..."
              />
            </div>
            <div className="relative sm:w-56 group">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <MapPin className="h-5 w-5 text-muted-foreground group-focus-within:text-primary transition-colors" />
              </div>
              <select className="block w-full pl-11 pr-4 py-3 text-lg border border-border rounded-xl bg-card/80 backdrop-blur-md text-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 appearance-none transition-all shadow-lg cursor-pointer">
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
            <div className="liquid-glass p-6 rounded-2xl sticky top-24">
              <h3 className="font-heading font-bold text-lg mb-4">Institution Type</h3>
              <ul className="space-y-2">
                <li>
                  <button className="w-full text-left px-3 py-2 text-sm font-semibold bg-primary/10 text-primary rounded-md">
                    All Types
                  </button>
                </li>
                {types.map((type) => (
                  <li key={type}>
                    <button className="w-full text-left px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-foreground rounded-md transition-colors">
                      {type}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </aside>

          <main className="flex-1">
            <div className="grid grid-cols-1 gap-4">
              {[
                { id: 1, title: "District General Hospital", addr: "Sector 14, Main Road", type: "Healthcare", desc: "Primary referral hospital providing 24/7 emergency services, OPD, and specialized care." },
                { id: 2, title: "Central Police Station", addr: "M.G. Road, Civil Lines", type: "Police", desc: "Main district police station handling FIRs, verifications, and law enforcement." },
                { id: 3, title: "Municipal Corporation Office", addr: "Town Hall Square", type: "Municipal", desc: "Head office for property tax, trade licenses, birth/death registration." },
                { id: 4, title: "Regional Transport Office (RTO)", addr: "Transport Nagar", type: "Transport", desc: "Handles driving licenses, vehicle registration, and road tax collection." },
                { id: 5, title: "Government Girls High School", addr: "Vidya Mandir Road", type: "Education", desc: "State-run senior secondary school offering education from classes 6 to 12." },
              ].map((inst) => (
                <div key={inst.id} className="p-6 rounded-2xl liquid-glass border-transparent hover:border-border hover:shadow-xl transition-all duration-300 flex flex-col sm:flex-row sm:items-center justify-between gap-6 group hover:-translate-y-1">
                  <div className="flex items-start gap-5">
                    <div className="w-14 h-14 rounded-xl bg-foreground/5 flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform">
                      <Building2 className="w-7 h-7 text-foreground" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold mb-1 group-hover:text-foreground transition-colors">
                        {inst.title}
                      </h3>
                      <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground mb-3">
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3.5 h-3.5" /> {inst.addr}
                        </span>
                        <span className="px-2.5 py-1 rounded-full bg-accent text-foreground text-xs font-semibold">
                          {inst.type}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground line-clamp-2 max-w-2xl leading-relaxed">
                        {inst.desc}
                      </p>
                    </div>
                  </div>
                  <div className="shrink-0 flex flex-col gap-3 sm:min-w-[140px]">
                    <Link href={`/institutions/${inst.id}`} className="inline-flex items-center justify-center px-4 py-2.5 text-sm font-bold bg-foreground text-background hover:bg-foreground/90 rounded-xl transition-all shadow-md">
                      View Profile
                    </Link>
                    <a href="#" className="inline-flex items-center justify-center px-4 py-2 text-sm font-semibold text-foreground hover:bg-accent rounded-xl transition-colors border border-border hover:border-foreground/50">
                      Directions <ExternalLink className="w-4 h-4 ml-1.5" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
