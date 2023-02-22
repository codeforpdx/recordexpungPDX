import { UseRadioGroupReturn } from "../../hooks/useRadioGroup";

interface Props {
  className?: string;
  inputGroupClassName?: string;
  optionLabels: string[];
  radioGroupProps: Omit<UseRadioGroupReturn, "selectedRadioValue">;
}

export default function RadioGroup({
  className = "",
  inputGroupClassName = "",
  optionLabels,
  radioGroupProps,
}: Props) {
  const { radioGroupWrapperProps, makeRadioButtonProps } = radioGroupProps;

  return (
    <fieldset {...radioGroupWrapperProps} className={className}>
      {optionLabels.map((label) => {
        const { radioButtonProps, radioLabelProps } =
          makeRadioButtonProps(label);

        return (
          <p key={label} className={inputGroupClassName}>
            <input {...radioButtonProps} />
            <label {...radioLabelProps}>{label}</label>
          </p>
        );
      })}
    </fieldset>
  );
}
