interface Props {
  disclosureIsExpanded: boolean;
}

export default function DisclosureIcon({ disclosureIsExpanded }: Props) {
  return (
    <span
      aria-hidden="true"
      className={`pt1 pl1 fas fa-angle-${disclosureIsExpanded ? "up" : "down"}`}
    ></span>
  );
}
