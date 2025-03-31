import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Manual from ".";

it("renders", () => {
  renderer
    .create(
      <BrowserRouter>
        <Manual />
      </BrowserRouter>
    )
    .toJSON();
});

test("the editing guide can be opened and closed", async () => {
  const user = userEvent.setup();

  render(
    <BrowserRouter>
      <Manual />
    </BrowserRouter>
  );

  expect(screen.queryByText(/why edit/i)).not.toBeVisible();

  await user.click(screen.getByRole("button"));

  expect(screen.queryByText(/why edit/i)).toBeVisible();

  await user.click(screen.getByRole("button", { name: /editing guide/i }));

  expect(screen.queryByText(/why edit/i)).not.toBeVisible();
});
