"use client";

import Link from 'next/link';
import { Shield } from 'lucide-react';
import { useCheckerStore } from '../../../store/useCheckerStore';

export default function Navbar() {
  const clearResult = useCheckerStore((state) => state.clearResult);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/10 bg-[#0A0F1E]/80 backdrop-blur supports-[backdrop-filter]:bg-[#0A0F1E]/60">
      <div className="container mx-auto flex h-16 items-center px-4 md:px-8">
        <div className="flex items-center gap-2 mr-8">
          <Shield className="h-6 w-6 text-[#00D4FF]" />
          <Link href="/" onClick={clearResult} className="font-bold text-xl tracking-tight text-white hover:text-white/90">
            PhishGuard
          </Link>
        </div>
        <nav className="flex items-center gap-6 text-sm font-medium">
          <Link href="/" onClick={clearResult} className="transition-colors hover:text-[#00D4FF] text-foreground/80">
            Checker
          </Link>
          <Link href="/history" className="transition-colors hover:text-[#00D4FF] text-foreground/80">
            History
          </Link>
          <Link href="/stats" className="transition-colors hover:text-[#00D4FF] text-foreground/80">
            Stats
          </Link>
        </nav>
      </div>
    </header>
  );
}
