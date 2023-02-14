import React from "react";

interface Props extends React.HTMLAttributes<HTMLElement> {
  id: string;
  labelText: string;
  showAllCharges: boolean;
  setShowAllCharges: (val: boolean) => void;
}

export default function ShowAllChargesCheckbox({
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
        id={"show-excluded-charges-" + id}
        checked={showAllCharges}
        onChange={() => {
          setShowAllCharges(!showAllCharges);
        }}
      />
      <label className="pointer pl2" htmlFor={"show-excluded-charges-" + id}>
        {labelText}
      </label>
    </div>
  );
}
