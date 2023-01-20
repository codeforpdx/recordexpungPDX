import React from "react";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ChargeTypeRule, { TypeRuleData } from "./ChargeTypeRule";

const rule: TypeRuleData = {
  charge_type_class_name: "class_name",
  charge_type_name: "type_name",
  expungement_rules: "rules\n",
};

it("can be opened and closed", async () => {
  const user = userEvent.setup();

  render(<ChargeTypeRule open={false} rule={rule} />);

  expect(screen.queryByText(/rules/i)).not.toBeVisible();

  await user.click(screen.getByRole("button"));

  expect(screen.queryByText(/rules/i)).toBeVisible();

  await user.click(screen.getByRole("button"));

  expect(screen.queryByText(/rules/i)).not.toBeVisible();
});

it("can be opened by default", () => {
  render(<ChargeTypeRule open={true} rule={rule} />);
  expect(screen.queryByText(/rules/i)).toBeVisible();
});
