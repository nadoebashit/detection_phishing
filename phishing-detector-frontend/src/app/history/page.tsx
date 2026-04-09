"use client";

import { useEffect, useState } from "react";
import { useCheckerStore } from "../../../store/useCheckerStore";
import HistoryTable from "@/components/history/HistoryTable";
import { Search } from "lucide-react";

export default function HistoryPage() {
  const { history, fetchHistory } = useCheckerStore();
  const [filter, setFilter] = useState<'all' | 'phishing' | 'safe'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const filteredHistory = history.filter(item => {
    const matchesFilter = 
      filter === 'all' ? true : 
      filter === 'phishing' ? item.is_phishing : 
      !item.is_phishing;
      
    const matchesSearch = item.url.toLowerCase().includes(searchQuery.toLowerCase());
    
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="flex-1 w-full max-w-6xl mx-auto py-12 px-4 md:px-8">
      <div className="mb-10">
        <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">Check History</h1>
        <p className="text-gray-400">Review all previously scanned URLs and their analysis results.</p>
      </div>

      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <div className="flex bg-[#0D1627] p-1 rounded-xl border border-white/5">
          <button 
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'all' ? 'bg-[#00D4FF]/20 text-[#00D4FF]' : 'text-gray-400 hover:text-white'}`}
          >
            All
          </button>
          <button 
            onClick={() => setFilter('phishing')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'phishing' ? 'bg-[#FF4444]/20 text-[#FF4444]' : 'text-gray-400 hover:text-white'}`}
          >
            Phishing
          </button>
          <button 
            onClick={() => setFilter('safe')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'safe' ? 'bg-[#00FF88]/20 text-[#00FF88]' : 'text-gray-400 hover:text-white'}`}
          >
            Safe
          </button>
        </div>

        <div className="relative w-full md:w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input 
            type="text" 
            placeholder="Search URLs..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-[#0D1627] border border-white/5 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder:text-gray-600 focus:outline-none focus:border-[#00D4FF]/50 transition-colors"
          />
        </div>
      </div>

      <HistoryTable data={filteredHistory} />
    </div>
  );
}
