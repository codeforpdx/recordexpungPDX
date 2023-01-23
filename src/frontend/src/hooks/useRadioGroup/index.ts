import React, { useState } from "react";

interface RadioButtonProps {
  id: string;
  name: string;
  type: string;
  value: string;
  "aria-checked": boolean;
  checked: boolean;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

interface RadioLabelProps {
  htmlFor: string;
}

interface UseRadioGroupProps {
  label: string;
  initialValue?: string;
}

export default function useRadioGroup({
  label,
  initialValue = "",
}: UseRadioGroupProps) {
  const [selectedRadioValue, setSelectedRadioValue] = useState(initialValue);
  const groupLabel = label.toLowerCase();
  const prefix = groupLabel.replaceAll(" ", "-") + "-";
  const groupProps = {
    dir: "ltr",
    role: "radiogroup",
    "aria-label": label,
  };

  const makeRadioButtonProps = (label: string) => {
    const id = prefix + label.toLowerCase();
    const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setSelectedRadioValue(event.target.value);
    };

    const inputProps: RadioButtonProps = {
      id,
      name: groupLabel,
      type: "radio",
      value: label,
      "aria-checked": label === selectedRadioValue,
      checked: label === selectedRadioValue,
      onChange,
    };

    const labelProps: RadioLabelProps = {
      htmlFor: id,
    };

    return {
      inputProps,
      labelProps,
    };
  };

  return {
    selectedRadioValue,
    groupProps,
    makeRadioButtonProps,
  };
}
