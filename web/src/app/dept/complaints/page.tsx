"use client";
import React from "react";
import { Button } from "@/components/ui/button";
import { Inbox, CheckCircle, Clock } from "lucide-react";

export default function DepartmentComplaints() {
  const complaints = [
    { id: "CMP-001", title: "Pothole on Main Street", status: "Open", urgency: "High", date: "2 hours ago" },
    { id: "CMP-002", title: "Streetlight not working", status: "In Progress", urgency: "Medium", date: "Yesterday" },
    { id: "CMP-003", title: "Garbage pile up near school", status: "Resolved", urgency: "High", date: "3 days ago" },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Complaints Inbox</h1>
          <p className="text-sm text-gray-500">Manage and resolve civic issues.</p>
        </div>
        <Button variant="outline">Refresh</Button>
      </div>

      <div className="flex-1 p-6 max-w-5xl mx-auto w-full">
        <div className="grid grid-cols-1 gap-4">
          {complaints.map((comp) => (
            <div key={comp.id} className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:border-gray-300 transition-colors cursor-pointer">
              <div className="flex items-start gap-4">
                <div className={`mt-1 w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
                  comp.status === 'Resolved' ? 'bg-green-100 text-green-600' :
                  comp.status === 'In Progress' ? 'bg-amber-100 text-amber-600' :
                  'bg-red-100 text-red-600'
                }`}>
                  {comp.status === 'Resolved' ? <CheckCircle className="w-5 h-5" /> : 
                   comp.status === 'In Progress' ? <Clock className="w-5 h-5" /> : 
                   <Inbox className="w-5 h-5" />}
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-medium text-gray-500">{comp.id}</span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      comp.urgency === 'High' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'
                    }`}>
                      {comp.urgency} URGENCY
                    </span>
                  </div>
                  <h3 className="font-semibold text-lg">{comp.title}</h3>
                  <p className="text-sm text-gray-500">Reported {comp.date}</p>
                </div>
              </div>
              
              <div className="w-full sm:w-auto">
                <Button variant={comp.status === 'Resolved' ? "outline" : "default"} className="w-full sm:w-auto">
                  {comp.status === 'Resolved' ? "View Details" : "Take Action"}
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
