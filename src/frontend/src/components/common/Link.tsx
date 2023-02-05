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
    <HashLink to={to} className={className}>
      {text}
      {children}
      {iconClassName && <i aria-hidden="true" className={iconClassName}></i>}
      {hiddenText && <span className="visually-hidden">{hiddenText}</span>}
    </HashLink>
  );
}
