export const metadata = { title: "Dropship Automator" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 0 }}>
        <div style={{ display: "flex", gap: 16, padding: 12, background: "#111", color: "#fff" }}>
          <a href="/" style={{ color: "#fff" }}>Dashboard</a>
          <a href="/import" style={{ color: "#fff" }}>Import</a>
          <a href="/affiliate" style={{ color: "#fff" }}>Affiliate</a>
          <a href="/jobs" style={{ color: "#fff" }}>Jobs</a>
        </div>
        <main style={{ padding: 16 }}>{children}</main>
      </body>
    </html>
  );
}
