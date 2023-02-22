interface ButtonProps {
  styling?: "link" | "button" | "blank";
  type?: "button" | "submit" | "reset";
  buttonClassName?: string;
  iconClassName?: string;
  displayText?: string;
  hiddenText?: string;
  onClick?: () => void;
  children?: React.ReactNode;
}

export default function IconButton(
  {
    styling = "button",
    type = "button",
    buttonClassName,
    iconClassName,
    displayText,
    hiddenText,
    onClick,
    children = undefined,
  }: ButtonProps = { onClick: () => {} }
) {
  const baseButtonClass = {
    link: "ma2 nowrap mid-gray link fw6 br3 pv1 ph2",
    button: "fw6 bg-animate br3 pv3 ph4",
    blank: "",
  }[styling];

  return (
    <button
      className={`${baseButtonClass}${
        buttonClassName ? " " + buttonClassName : ""
      }`}
      type={type}
      onClick={onClick}
    >
      <i aria-hidden="true" className={`fas ${iconClassName}`}></i>
      {hiddenText && <span className="visually-hidden">{hiddenText}</span>}
      {displayText}
      {children}
    </button>
  );
}
