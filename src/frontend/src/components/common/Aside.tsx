import React from "react";

interface ElementProps extends React.PropsWithChildren {
  className?: string;
  text?: string;
}

export default function Aside({
  className = "",
  text = "",
  children,
}: ElementProps) {
  return (
    <aside className={`fw4 pb3 i ${className}`}>
      {text}
      {children}
    </aside>
  );
}
