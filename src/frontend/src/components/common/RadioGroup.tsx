interface RadioGroupProps {
  className?: string;
  optionLabels: string[];
  radioGroupProps: any;
}

export default function RadioGroup({
  className = "",
  optionLabels,
  radioGroupProps,
}: RadioGroupProps) {
  const { groupProps, makeRadioButtonProps } = radioGroupProps;

  return (
    <fieldset {...groupProps} className={className}>
      {optionLabels.map((label) => {
        const { inputProps, labelProps } = makeRadioButtonProps(label);

        return (
          <p key={label}>
            <input {...inputProps} />
            <label {...labelProps}>{label}</label>
          </p>
        );
      })}
    </fieldset>
  );
}
