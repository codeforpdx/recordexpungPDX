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

export interface RadioGroupWrapperProps {
  dir: string;
  role: "radiogroup";
  "aria-label": string;
}

export type MakeRadioButtonProps = (label: string) => {
  radioButtonProps: RadioButtonProps;
  radioLabelProps: RadioLabelProps;
};

export interface UseRadioGroupReturn {
  selectedRadioValue: string;
  radioGroupWrapperProps: RadioGroupWrapperProps;
  makeRadioButtonProps: MakeRadioButtonProps;
}

interface Props {
  label: string;
  initialValue?: string;
}

export default function useRadioGroup({ label, initialValue = "" }: Props) {
  const [selectedRadioValue, setSelectedRadioValue] = useState(initialValue);
  const groupLabel = label.toLowerCase();
  const prefix = groupLabel.replace(/\s/g, "-") + "-";
  const radioGroupWrapperProps: RadioGroupWrapperProps = {
    dir: "ltr",
    role: "radiogroup",
    "aria-label": label,
  };

  const makeRadioButtonProps: MakeRadioButtonProps = (label: string) => {
    const id = prefix + label.toLowerCase();
    const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setSelectedRadioValue(event.target.value);
    };

    const radioButtonProps: RadioButtonProps = {
      id,
      name: groupLabel,
      type: "radio",
      value: label,
      "aria-checked": label === selectedRadioValue,
      checked: label === selectedRadioValue,
      onChange,
    };

    const radioLabelProps: RadioLabelProps = {
      htmlFor: id,
    };

    return {
      radioButtonProps,
      radioLabelProps,
    };
  };

  return {
    selectedRadioValue,
    radioGroupWrapperProps,
    makeRadioButtonProps,
  } as UseRadioGroupReturn;
}
