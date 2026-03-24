import { motion } from 'framer-motion';
import { ShieldAlert } from 'lucide-react';

export default function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-6">
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.5, 1, 0.5],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      >
        <ShieldAlert className="w-24 h-24 text-[#00D4FF]" />
      </motion.div>
      
      <div className="flex flex-col items-center gap-2">
        <h3 className="text-xl font-semibold text-white animate-pulse">Scanning URL...</h3>
        <p className="text-gray-400 text-sm max-w-sm text-center">
          Analyzing UI similarities, domain reputation, and visual markers in real-time.
        </p>
      </div>

      <div className="w-64 h-1 bg-white/10 rounded-full overflow-hidden mt-4">
        <motion.div
          className="h-full bg-gradient-to-r from-transparent via-[#00D4FF] to-transparent"
          animate={{
            x: ['-100%', '100%'],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: "linear",
          }}
          style={{ width: '100%' }}
        />
      </div>
    </div>
  );
}
