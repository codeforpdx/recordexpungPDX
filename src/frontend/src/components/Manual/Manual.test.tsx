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
      </BrowserRouter>,
    )
    .toJSON();
});

test("the editing guide can be opened and closed", async () => {
  const user = userEvent.setup();

  render(
    <BrowserRouter>
      <Manual />
    </BrowserRouter>,
  );

  const part2 = screen.getByLabelText("Part 2: Search Client Records");
  await user.click(part2);

  const results = screen.getByLabelText("Results");
  await user.click(results);

  const summary = screen.getByLabelText("Editing Guide");

  expect(screen.queryByText(/why edit/i)).not.toBeVisible();

  await user.click(summary);

  expect(screen.getByText(/why edit/i)).toBeVisible();

  await user.click(summary);

  expect(screen.queryByText(/why edit/i)).not.toBeVisible();
});
