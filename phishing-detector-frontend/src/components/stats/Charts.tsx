"use client";

import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as LineTooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Tooltip as PieTooltip, Legend,
  BarChart, Bar, XAxis as BarX, YAxis as BarY, Tooltip as BarTooltip
} from 'recharts';

interface ChartsProps {
  trendData: any[];
  ratioData: any[];
  brandsData: any[];
}

const COLORS = ['#00FF88', '#FF4444'];

export default function Charts({ trendData, ratioData, brandsData }: ChartsProps) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full">
      {/* Trend Chart */}
      <div className="bg-[#0D1627] p-6 rounded-2xl border border-white/5 lg:col-span-2 shadow-sm">
        <h3 className="text-lg font-semibold text-white mb-6">Daily Scans Trend</h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2D3748" vertical={false} />
              <XAxis dataKey="date" stroke="#A0AEC0" axisLine={false} tickLine={false} />
              <YAxis stroke="#A0AEC0" axisLine={false} tickLine={false} />
              <LineTooltip 
                contentStyle={{ backgroundColor: '#0A0F1E', border: '1px solid #2D3748', borderRadius: '8px' }}
                itemStyle={{ color: '#E2E8F0' }}
              />
              <Line type="monotone" dataKey="scans" stroke="#00D4FF" strokeWidth={3} dot={{ r: 4, fill: '#0A0F1E', stroke: '#00D4FF', strokeWidth: 2 }} activeDot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Pie Chart */}
      <div className="bg-[#0D1627] p-6 rounded-2xl border border-white/5 shadow-sm">
        <h3 className="text-lg font-semibold text-white mb-6">Safe vs Phishing Ratio</h3>
        <div className="h-64 w-full flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={ratioData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
                stroke="none"
              >
                {ratioData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <PieTooltip contentStyle={{ backgroundColor: '#0A0F1E', border: 'none', borderRadius: '8px' }} />
              <Legend verticalAlign="bottom" height={36} iconType="circle" />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Bar Chart */}
      <div className="bg-[#0D1627] p-6 rounded-2xl border border-white/5 shadow-sm">
        <h3 className="text-lg font-semibold text-white mb-6">Top Targeted Brands</h3>
        <div className="h-64 w-full flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={brandsData} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2D3748" horizontal={false} />
              <BarX type="number" stroke="#A0AEC0" axisLine={false} tickLine={false} />
              <BarY type="category" dataKey="name" stroke="#A0AEC0" axisLine={false} tickLine={false} />
              <BarTooltip cursor={{ fill: 'rgba(255,255,255,0.05)' }} contentStyle={{ backgroundColor: '#0A0F1E', border: 'none', borderRadius: '8px' }} />
              <Bar dataKey="count" fill="#00D4FF" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
