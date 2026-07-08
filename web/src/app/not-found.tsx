"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Wrench, ArrowLeft, Construction } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-md w-full bg-white rounded-2xl shadow-sm border border-gray-100 p-8 text-center"
      >
        <div className="flex justify-center mb-6">
          <div className="relative">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
              className="absolute -inset-4 bg-orange-50 rounded-full z-0"
            />
            <div className="relative z-10 bg-orange-100 p-4 rounded-full text-orange-600">
              <Construction size={40} />
            </div>
          </div>
        </div>

        <h1 className="text-2xl font-bold text-gray-900 mb-3">
          Under Maintenance
        </h1>
        <p className="text-gray-500 mb-8 leading-relaxed">
          This feature is currently under active development. We're working hard to 
          bring you a better experience. Please check back later!
        </p>

        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Link
            href="/"
            className="inline-flex items-center justify-center px-6 py-2.5 rounded-lg bg-orange-600 text-white font-medium hover:bg-orange-700 transition-colors gap-2"
          >
            <ArrowLeft size={18} />
            Back to Home
          </Link>
        </div>
      </motion.div>

      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.5 }}
        className="mt-8 text-sm text-gray-400 flex items-center gap-2"
      >
        <Wrench size={14} />
        JanSevak Core Product
      </motion.div>
    </div>
  );
}
