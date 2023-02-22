import RadioGroup from "../../common/RadioGroup";
import { UseRadioGroupReturn } from "../../../hooks/useRadioGroup";

interface Props {
  optionLabels: string[];
  radioGroupProps: Omit<UseRadioGroupReturn, "selectedRadioValue">;
  showColor: boolean;
  isExpandedView: boolean;
  handleShowColorChange: () => void;
}

export default function ViewOptions({
  optionLabels,
  radioGroupProps,
  showColor,
  isExpandedView,
  handleShowColorChange,
}: Props) {
  return (
    <>
      <RadioGroup
        className="flex flex-wrap radio radio-sm"
        inputGroupClassName="pr3"
        optionLabels={optionLabels}
        radioGroupProps={radioGroupProps}
      />

      {isExpandedView && (
        <fieldset className="checkbox checkbox-sm">
          <input
            type="checkbox"
            id={"show-bg-color"}
            checked={showColor}
            onChange={handleShowColorChange}
          />
          <label className="pointer" htmlFor={"show-bg-color"}>
            Show Colors
          </label>
        </fieldset>
      )}
    </>
  );
}
