import { panelClass } from "../Layout";

interface Props {
  leftHeading: string;
  leftComponent: JSX.Element;
  rightHeading: string;
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

  return (
    <section className="flex-l mh2 mt3">
      <div className={panelClass + "w-70-l f6 ph4 mr3"}>
        <h2 className={panelHeadingClass}>{leftHeading}</h2>
        {leftComponent}
      </div>

      <div className={panelClass + "w-30-l pl3 pb2 " + rightClassName}>
        <h3 className={panelHeadingClass}>{rightHeading}</h3>
        {rightComponent}
      </div>
    </section>
  );
}
