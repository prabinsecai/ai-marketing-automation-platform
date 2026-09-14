import type { Metadata } from "next";
import "./globals.css";
import { Shell } from "@/components/layout/Shell";

export const metadata: Metadata = {
  title: "AuraFlow AI - Campaign Intelligence Platform",
  description: "B2B Marketing Automation, AI Strategy, and Multi-Channel Content Intelligence",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-zinc-950 text-zinc-100 min-h-screen">
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
