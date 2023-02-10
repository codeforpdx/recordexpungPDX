interface ButtonProps {
  type?: "link" | "button";
  buttonClassName?: string;
  iconClassName?: string;
  displayText?: string;
  hiddenText?: string;
  onClick?: () => void;
  children?: React.ReactNode;
}

export function IconButton(
  {
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
  }[type];

  return (
    <button
      className={`${baseButtonClass}${
        buttonClassName ? " " + buttonClassName : ""
      }`}
      onClick={onClick}
    >
      <i aria-hidden="true" className={`fas ${iconClassName}`}></i>
      {hiddenText && <span className="visually-hidden">{hiddenText}</span>}
      {displayText}
      {children}
    </button>
  );
}
