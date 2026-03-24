import { CheckResult } from '../../../lib/types';
import { format } from 'date-fns'; // We might need to install this or just use native dates
import { ArrowRight, ShieldAlert, ShieldCheck } from 'lucide-react';

interface HistoryTableProps {
  data: CheckResult[];
}

export default function HistoryTable({ data }: HistoryTableProps) {
  if (data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-12 bg-[#0D1627] rounded-2xl border border-white/5">
        <p className="text-gray-400">No history found.</p>
      </div>
    );
  }

  return (
    <div className="w-full bg-[#0D1627] rounded-2xl border border-white/5 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#0A0F1E] border-b border-white/5 text-xs uppercase tracking-wider text-gray-400 font-semibold">
              <th className="p-5 font-medium">URL</th>
              <th className="p-5 font-medium">Status</th>
              <th className="p-5 font-medium">Confidence</th>
              <th className="p-5 font-medium">Similar To</th>
              <th className="p-5 font-medium hidden md:table-cell">Date</th>
              <th className="p-5 font-medium"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {data.map((item, i) => (
              <tr key={i} className="hover:bg-white/[0.02] transition-colors">
                <td className="p-5 text-gray-200 font-medium truncate max-w-[200px] sm:max-w-xs block sm:table-cell">
                  {item.url}
                </td>
                <td className="p-5">
                  <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${item.is_phishing ? 'bg-[#FF4444]/10 text-[#FF4444]' : 'bg-[#00FF88]/10 text-[#00FF88]'}`}>
                    {item.is_phishing ? <ShieldAlert className="w-3.5 h-3.5" /> : <ShieldCheck className="w-3.5 h-3.5" />}
                    {item.is_phishing ? 'PHISHING' : 'SAFE'}
                  </div>
                </td>
                <td className="p-5">
                  <span className="text-white font-medium">{Math.round(item.confidence * 100)}%</span>
                </td>
                <td className="p-5 text-gray-400 text-sm">
                  {item.similar_to || '-'}
                </td>
                <td className="p-5 text-gray-500 text-sm hidden md:table-cell">
                  {new Date(item.checked_at).toLocaleString()}
                </td>
                <td className="p-5 text-right">
                  <button className="text-[#00D4FF] hover:text-white transition-colors">
                    <ArrowRight className="w-5 h-5 ml-auto" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
