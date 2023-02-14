import React from "react";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import useRadioGroup from ".";

function RadioGroup({
  label,
  optionLabels,
  initialValue,
}: {
  label: string;
  optionLabels: string[];
  initialValue?: string;
}) {
  const { selectedRadioValue, radioGroupWrapperProps, makeRadioButtonProps } =
    useRadioGroup({
      label,
      initialValue,
    });

  return (
    <fieldset {...radioGroupWrapperProps}>
      {selectedRadioValue && (
        <legend>{selectedRadioValue + " in legend"}</legend>
      )}

      {optionLabels.map((label) => {
        const { radioButtonProps, radioLabelProps } =
          makeRadioButtonProps(label);
        return (
          <p key={label}>
            <input {...radioButtonProps} />
            <label {...radioLabelProps}>{label}</label>
          </p>
        );
      })}
    </fieldset>
  );
}

function setup(initialValue?: string) {
  const groupLabel = "Summary overview options";
  const optionLabels = ["Charges", "Cases"];
  const { container } = render(
    <RadioGroup
      label={groupLabel}
      optionLabels={optionLabels}
      initialValue={initialValue}
    />
  );

  const fieldset = container.querySelector("fieldset");
  const inputs = container.querySelectorAll("input");
  const labels = container.querySelectorAll("label");
  const legend = container.querySelector("legend");

  return { legend, groupLabel, optionLabels, fieldset, inputs, labels };
}

describe("default state", () => {
  test("group props are correct", () => {
    const { groupLabel, fieldset } = setup();

    expect(fieldset).toHaveAttribute("aria-label", groupLabel);
    expect(fieldset).toHaveAttribute("role", "radiogroup");
    expect(fieldset).toHaveAttribute("dir", "ltr");
  });

  test("makeRadioButtonProps provides the correct input and label props", () => {
    const { groupLabel, optionLabels, inputs, labels } = setup();
    const prefix = "summary-overview-options-";

    optionLabels.forEach((optionLabel, idx) => {
      const input = inputs[idx];
      const label = labels[idx];
      const id = prefix + optionLabel.toLowerCase();

      expect(input).toHaveAttribute("id", id);
      expect(input).toHaveAttribute("name", groupLabel.toLowerCase());
      expect(input).toHaveAttribute("type", "radio");
      expect(input).toHaveAttribute("aria-checked", "false");

      expect(label).toHaveAttribute("for", id);
    });
  });

  test("the selected value is blank", () => {
    const { legend } = setup();
    expect(legend).toBeNull();
  });
});

describe("when given an initial value", () => {
  beforeEach(() => {
    setup("Cases");
  });

  test("selectedRadioValue is correct", () => {
    expect(screen.queryByText("Cases in legend")).toBeInTheDocument();
  });

  test("the appropriate input has aria-check = true", () => {
    const casesRadio = screen.queryByLabelText("Cases");
    const chargesRadio = screen.queryByLabelText("Charges");

    expect(casesRadio).toHaveAttribute("checked", "");
    expect(casesRadio).toHaveAttribute("aria-checked", "true");
    expect(chargesRadio).toHaveAttribute("aria-checked", "false");
  });

  test("the other option can be selected and the correct changes are made", async () => {
    const user = userEvent.setup();
    const casesRadio = screen.getByLabelText("Cases");
    const chargesRadio = screen.getByLabelText("Charges");

    await user.click(chargesRadio);

    expect(screen.queryByText("Charges in legend")).toBeInTheDocument();
    expect(screen.queryByText("Cases in legend")).not.toBeInTheDocument();

    expect(casesRadio).not.toBeChecked();
    expect(chargesRadio).toBeChecked();
  });
});
