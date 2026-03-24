import { motion } from 'framer-motion';

interface ScreenshotViewProps {
  screenshotUrl: string;
  originalScreenshotUrl: string | null;
  similarTo: string | null;
}

export default function ScreenshotView({ screenshotUrl, originalScreenshotUrl, similarTo }: ScreenshotViewProps) {
  return (
    <div className="mt-8">
      <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
        Visual Analysis
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="flex flex-col gap-3"
        >
          <span className="text-sm font-medium text-gray-400 uppercase tracking-wider">Checked Target</span>
          <div className="rounded-lg overflow-hidden border border-white/10 bg-black/40 aspect-video relative flex items-center justify-center">
            {screenshotUrl ? (
              <img src={screenshotUrl} alt="Checked website" className="w-full h-full object-cover" />
            ) : (
              <span className="text-gray-600">No screenshot available</span>
            )}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="flex flex-col gap-3"
        >
          <span className="text-sm font-medium text-gray-400 uppercase tracking-wider">
            Original Brand {similarTo && <span className="text-[#00D4FF]">({similarTo})</span>}
          </span>
          <div className="rounded-lg overflow-hidden border border-white/10 bg-black/40 aspect-video relative flex items-center justify-center">
            {originalScreenshotUrl ? (
              <img src={originalScreenshotUrl} alt="Original brand" className="w-full h-full object-cover opacity-80" />
            ) : (
              <span className="text-gray-600">N/A (No visual match)</span>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
