"use client";

import { motion } from 'framer-motion';
import { ShieldCheck } from 'lucide-react';
import URLForm from '@/components/checker/URLForm';
import ResultCard from '@/components/checker/ResultCard';
import LoadingState from '@/components/checker/LoadingState';
import { usePhishingCheck } from '../../hooks/usePhishingCheck';

export default function Home() {
  const { handleCheck, isLoading, result, clearResult, error } = usePhishingCheck();

  return (
    <div className="flex-1 flex flex-col items-center py-16 px-4 md:px-8 w-full">
      <div className="max-w-6xl w-full mx-auto flex flex-col items-center">
        
        {!result && !isLoading && (
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="flex flex-col items-center text-center mb-16"
          >
            <div className="p-4 bg-[#00D4FF]/10 rounded-full mb-6">
              <ShieldCheck className="w-16 h-16 text-[#00D4FF]" />
            </div>
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-gradient-to-r from-white via-[#E2E8F0] to-[#00D4FF] text-transparent bg-clip-text">
              PhishGuard
            </h1>
            <p className="text-xl md:text-2xl text-gray-400 font-light max-w-2xl">
              Check any URL for phishing using advanced AI, computer vision, and visual similarity detection.
            </p>
          </motion.div>
        )}

        {!result && (
          <div className="w-full">
            <URLForm onSubmit={handleCheck} isLoading={isLoading} />
            {error && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-6 p-4 bg-[#FF4444]/10 border border-[#FF4444]/20 rounded-xl text-[#FF4444] max-w-3xl mx-auto text-center font-medium"
              >
                {error}
              </motion.div>
            )}
          </div>
        )}

        {isLoading && (
          <div className="mt-16 w-full">
            <LoadingState />
          </div>
        )}

        {result && !isLoading && (
          <div className="w-full pt-8">
            <ResultCard result={result} onCheckAnother={clearResult} />
          </div>
        )}
      </div>
    </div>
  );
}
