interface Props {
  disclosureIsExpanded: boolean;
  className?: string;
}

export default function DisclosureIcon({
  disclosureIsExpanded,
  className = "",
}: Props) {
  return (
    <span
      aria-hidden="true"
      className={`${className ? className + " " : ""}fas fa-angle-${
        disclosureIsExpanded ? "up" : "down"
      }`}
    ></span>
  );
}
