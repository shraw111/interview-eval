import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";
import { FileText } from "lucide-react";

export const metadata: Metadata = {
  title: "Interview Evaluation System",
  description: "AI-powered interview evaluation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <div className="min-h-screen flex flex-col">
            {/* Header */}
            <header className="border-b border-border bg-card sticky top-0 z-50">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 bg-primary rounded-lg flex items-center justify-center">
                      <FileText className="w-5 h-5 text-white" strokeWidth={2} />
                    </div>
                    <div>
                      <h1 className="text-base font-semibold">
                        Interview Evaluator
                      </h1>
                    </div>
                  </div>
                </div>
              </div>
            </header>

            {/* Main Content */}
            <main className="flex-1">{children}</main>

            {/* Footer */}
            <footer className="border-t border-border bg-card mt-auto">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                  <p className="text-xs text-muted-foreground">
                    © {new Date().getFullYear()} Interview Evaluator
                  </p>
                  <p className="text-xs text-muted-foreground">
                    AI-powered evaluation system
                  </p>
                </div>
              </div>
            </footer>
          </div>
        </Providers>
      </body>
    </html>
  );
}
