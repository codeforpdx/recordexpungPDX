import React from "react";
import { panelClass } from "../Layout";

interface Props {
  leftHeading: JSX.Element | string;
  leftComponent: JSX.Element;
  rightHeading: JSX.Element | string;
  rightComponent: JSX.Element;
  rightClassName?: string;
}

export default function SplitSection({
  leftHeading,
  leftComponent,
  rightHeading,
  rightComponent,
  rightClassName = "",
}: Props) {
  const panelHeadingClass = "f5 fw7 tc pv3 ";
  const leftHeadingElem = React.createElement(
    typeof leftHeading === "string" ? "h2" : "div",
    { className: panelHeadingClass },
    leftHeading
  );
  const rightHeadingElem = React.createElement(
    typeof rightHeading === "string" ? "h3" : "div",
    { className: panelHeadingClass },
    rightHeading
  );

  return (
    <section className="flex-l mh2 mt3">
      <div className={panelClass + "w-70-l f6 ph4 mr3"}>
        {leftHeadingElem}
        {leftComponent}
      </div>

      <div className={panelClass + "w-30-l pl3 pb2 " + rightClassName}>
        {rightHeadingElem}
        {rightComponent}
      </div>
    </section>
  );
}
