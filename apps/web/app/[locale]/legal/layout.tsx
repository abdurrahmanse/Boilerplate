import type { ReactNode } from "react";

interface LegalLayoutProperties {
  readonly children: ReactNode;
}

const LegalLayout = ({ children }: LegalLayoutProperties) => (
  <div className="prose prose-sm prose-zinc dark:prose-invert mx-auto py-24">
    {children}
  </div>
);

export default LegalLayout;
