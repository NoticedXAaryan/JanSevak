import React from "react";

export default function StaticDocPage({ title }: { title?: string }) {
  return (
    <div className="w-full max-w-4xl mx-auto px-6 py-12 md:py-20">
      <h1 className="text-4xl md:text-5xl font-heading font-semibold mb-12">Placeholder Page</h1>
      <div className="prose prose-invert max-w-none">
        <p>This is a placeholder for static content such as Privacy Policy, Terms of Service, Accessibility Statement, or FAQ.</p>
        <p>In a production application, this content would be managed via a CMS or MDX files.</p>
      </div>
    </div>
  );
}
