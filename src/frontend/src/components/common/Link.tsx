import { HashLink } from "react-router-hash-link";

interface Props {
  to: string;
  text?: string;
  hiddenText?: string;
  className?: string;
  iconClassName?: string;
  children?: React.ReactNode;
}

export default function Link({
  to = "#",
  text = "",
  iconClassName,
  hiddenText,
  className = "",
  children,
}: Props) {
  return (
    <HashLink to={to} className={"link hover-blue " + className}>
      {(text !== "" || children) && (
        <span className="bb b--moon-gray">
          {text}
          {children}
        </span>
      )}
      {iconClassName && (
        <i
          aria-hidden="true"
          className={"gray hover-dark-blue " + iconClassName}
        ></i>
      )}
      {hiddenText && <span className="visually-hidden">{hiddenText}</span>}
    </HashLink>
  );
}
