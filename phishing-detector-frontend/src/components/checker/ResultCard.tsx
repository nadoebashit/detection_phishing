import { motion } from 'framer-motion';
import { AlertTriangle, CheckCircle2, RefreshCw } from 'lucide-react';
import { CheckResult } from '../../../lib/types';
import ScoreBar from './ScoreBar';
import ScreenshotView from './ScreenshotView';

interface ResultCardProps {
  result: CheckResult;
  onCheckAnother: () => void;
}

export default function ResultCard({ result, onCheckAnother }: ResultCardProps) {
  const isPhishing = result.is_phishing;
  const confidence = Math.round(result.confidence * 100);
  
  const statusColor = isPhishing ? 'text-[#FF4444]' : 'text-[#00FF88]';
  const bgColor = isPhishing ? 'bg-[#FF4444]/10' : 'bg-[#00FF88]/10';
  const borderColor = isPhishing ? 'border-[#FF4444]/30' : 'border-[#00FF88]/30';

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className={`w-full max-w-4xl mx-auto rounded-3xl border ${borderColor} ${bgColor} backdrop-blur-md p-8 sm:p-12 shadow-2xl relative overflow-hidden`}
    >
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 mb-10">
        <div className="flex items-center gap-6">
          <div className="shrink-0">
            {isPhishing ? (
              <AlertTriangle className={`w-20 h-20 ${statusColor}`} />
            ) : (
              <CheckCircle2 className={`w-20 h-20 ${statusColor}`} />
            )}
          </div>
          <div className="flex flex-col">
            <h2 className={`text-4xl sm:text-5xl font-bold tracking-tight mb-2 ${statusColor}`}>
              {isPhishing ? 'PHISHING' : 'SAFE'}
            </h2>
            <p className="text-gray-300 text-lg break-all">
              {result.url}
            </p>
            {isPhishing && result.similar_to && (
              <span className="inline-flex items-center px-3 py-1 rounded-full bg-[#FF4444]/20 text-[#FF4444] text-sm font-medium mt-3 max-w-max">
                Similar to: {result.similar_to}
              </span>
            )}
          </div>
        </div>

        <div className="flex flex-col items-center bg-black/40 rounded-2xl p-6 border border-white/5 min-w-[160px]">
          <span className="text-gray-400 text-sm font-medium mb-1 uppercase tracking-wider">Confidence</span>
          <span className="text-5xl font-bold text-white">
            {confidence}<span className="text-2xl text-gray-500 ml-1">%</span>
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="bg-[#0A0F1E]/50 rounded-xl p-5 border border-white/5">
          <ScoreBar label="pHash Score" score={result.scores?.phash || 0.0} />
        </div>
        <div className="bg-[#0A0F1E]/50 rounded-xl p-5 border border-white/5">
          <ScoreBar label="SSIM Score" score={result.scores?.ssim || 0.0} />
        </div>
        <div className="bg-[#0A0F1E]/50 rounded-xl p-5 border border-white/5">
          <ScoreBar label="CNN Concept" score={result.scores?.cnn || 0.0} />
        </div>
      </div>

      <ScreenshotView
        screenshotUrl={result.screenshot_url}
        originalScreenshotUrl={result.original_screenshot_url}
        similarTo={result.similar_to}
      />

      <div className="mt-12 flex justify-center">
        <button
          onClick={onCheckAnother}
          className="flex items-center gap-2 px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full transition-colors text-white font-medium"
        >
          <RefreshCw className="w-5 h-5" />
          Check Another URL
        </button>
      </div>
    </motion.div>
  );
}
