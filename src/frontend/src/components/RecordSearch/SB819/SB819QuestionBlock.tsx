import React from "react";

/**
 * The purple-barred block that RecordSponge's own eligibility questions sit in, so the
 * SB-819 questions read as the same kind of thing wherever they appear.
 */
export default function SB819QuestionBlock({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="w-100 relative bl bw3 b--light-purple pa3 pb1">
      {children}
    </div>
  );
}
