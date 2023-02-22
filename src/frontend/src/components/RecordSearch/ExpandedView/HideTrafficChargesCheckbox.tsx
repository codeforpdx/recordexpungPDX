import React from "react";

interface Props extends React.HTMLAttributes<HTMLElement> {
  id: string;
  labelText: string;
  checked: boolean;
  onChange: (val: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function HideTrafficChargesCheckbox({
  id,
  labelText,
  checked,
  onChange,
  ...props
}: Props) {
  return (
    <div {...props}>
      <input
        type="checkbox"
        id={"hide-traffic-charges-" + id}
        data-testid={"hide-traffic-charges-" + id}
        checked={checked}
        onChange={onChange}
      />
      <label className="pointer pl2" htmlFor={"hide-traffic-charges-" + id}>
        {labelText}
      </label>
    </div>
  );
}
