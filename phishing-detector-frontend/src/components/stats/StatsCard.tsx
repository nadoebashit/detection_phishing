import { ReactNode } from 'react';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: ReactNode;
  trend?: string;
  trendUp?: boolean;
}

export default function StatsCard({ title, value, icon, trend, trendUp }: StatsCardProps) {
  return (
    <div className="bg-[#0D1627] p-6 rounded-2xl border border-white/5 flex flex-col justify-between hover:border-[#00D4FF]/20 transition-colors">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-gray-400 font-medium text-sm lg:text-base">{title}</h3>
        <div className="p-3 bg-[#0A0F1E] rounded-xl border border-white/5 text-[#00D4FF]">
          {icon}
        </div>
      </div>
      <div>
        <span className="text-3xl md:text-4xl font-bold text-white">{value}</span>
        {trend && (
          <div className={`mt-2 text-sm font-medium flex items-center gap-1 ${trendUp ? 'text-[#00FF88]' : 'text-[#FF4444]'}`}>
            {trendUp ? '↑' : '↓'} {trend}
          </div>
        )}
      </div>
    </div>
  );
}
