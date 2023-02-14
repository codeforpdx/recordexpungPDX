import React from "react";
import { panelClass, mainWrapper, singlePanelClass } from "../Layout";
import { headingLargeClass } from ".";

interface Props extends React.PropsWithChildren {
  heading?: string;
  className?: string;
}

export default function SingleSection({
  heading,
  className = "",
  children,
}: Props) {
  return (
    <section
      className={mainWrapper + panelClass + singlePanelClass + className}
    >
      {heading && <h2 className={headingLargeClass}>{heading}</h2>}
      {children}
    </section>
  );
}
