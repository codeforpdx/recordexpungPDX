import React from "react";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ExpungementRules from "./ExpungementRules";

it("can be opened and closed", async () => {
  const user = userEvent.setup();

  render(<ExpungementRules expungement_rules="rules\n" />);

  expect(screen.queryByText(/rules/i)).not.toBeVisible();

  await user.click(screen.getByRole("button"));

  expect(screen.queryByText(/rules/i)).toBeVisible();

  await user.click(screen.getByRole("button"));

  expect(screen.queryByText(/rules/i)).not.toBeVisible();
});
