import { motion } from 'framer-motion';

interface ScoreBarProps {
  label: string;
  score: number;
}

export default function ScoreBar({ label, score }: ScoreBarProps) {
  // Score is expected to be 0-1, convert to percentage
  const percentage = Math.round(score * 100);
  
  return (
    <div className="flex flex-col gap-2 w-full">
      <div className="flex justify-between items-center text-sm">
        <span className="text-gray-400">{label}</span>
        <span className="font-medium text-white">{percentage}%</span>
      </div>
      <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, delay: 0.2, ease: "easeOut" }}
          className="h-full bg-[#00D4FF]"
        />
      </div>
    </div>
  );
}
