export default function Footer() {
  return (
    <footer className="border-t border-white/10 bg-[#0D1627] py-6">
      <div className="container mx-auto flex flex-col items-center justify-center gap-4 px-4 md:px-8 md:flex-row md:justify-between text-sm text-muted-foreground">
        <p>© {new Date().getFullYear()} PhishGuard. All rights reserved.</p>
        <div className="flex gap-4 cursor-pointer hover:text-[#00D4FF] transition-colors">
          <span>Terms of Service</span>
          <span>Privacy Policy</span>
        </div>
      </div>
    </footer>
  );
}
