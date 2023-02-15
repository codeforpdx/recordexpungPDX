import React from "react";

interface Props extends React.HTMLAttributes<HTMLElement> {
  id: string;
  labelText: string;
  showAllCharges: boolean;
  setShowAllCharges: (val: boolean) => void;
}

export default function HideTrafficChargesCheckbox({
  id,
  labelText,
  showAllCharges,
  setShowAllCharges,
  ...props
}: Props) {
  return (
    <div {...props}>
      <input
        type="checkbox"
        id={"hide-traffic-charges-" + id}
        data-testid={"hide-traffic-charges-" + id}
        checked={showAllCharges}
        onChange={() => {
          setShowAllCharges(!showAllCharges);
        }}
      />
      <label className="pointer pl2" htmlFor={"hide-traffic-charges-" + id}>
        {labelText}
      </label>
    </div>
  );
}
