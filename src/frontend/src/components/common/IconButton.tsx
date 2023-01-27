interface ButtonProps {
  buttonClassName?: string;
  iconClassName?: string;
  displayText?: string;
  hiddenText?: string;
  onClick?: () => void;
  children?: React.ReactNode;
}

export function IconButton(
  {
    buttonClassName,
    iconClassName,
    displayText,
    hiddenText,
    onClick,
    children = undefined,
  }: ButtonProps = { onClick: () => {} }
) {
  const baseButtonClass = "ma2 nowrap mid-gray link hover-blue fw6 br3 pv1 ph2";

  return (
    <button
      className={`${baseButtonClass}${
        buttonClassName ? " " + baseButtonClass : ""
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
