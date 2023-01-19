import React from "react";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import useDisclosure from ".";

function TestComponent() {
  const {
    disclosureIsExpanded,
    disclosureButtonProps,
    disclosureContentProps,
  } = useDisclosure();

  return (
    <div>
      <button {...disclosureButtonProps}> click me </button>
      <div {...disclosureContentProps}>visible</div>;
      <div>{disclosureIsExpanded ? "expanded" : "collapsed"}</div>
    </div>
  );
}

beforeEach(() => {
  render(<TestComponent />);
});

test("the initial state is correct", () => {
  const button = screen.queryByRole("button");
  const content = screen.queryByText(/visible/);

  expect(button).toHaveAttribute("aria-expanded", "false");
  expect(button).toHaveAttribute("aria-controls", "panel--disclosure");

  expect(content).toHaveAttribute("id", "panel--disclosure");
  expect(content).not.toBeVisible();

  expect(screen.queryByText(/expanded/)).not.toBeInTheDocument();
  expect(screen.queryByText(/collapsed/)).toBeInTheDocument();
});

test("the button hides the content when clicked", async () => {
  const user = userEvent.setup();

  await user.click(screen.getByRole("button"));

  expect(screen.queryByText(/visible/)).toBeVisible();
  expect(screen.queryByText(/expanded/)).toBeInTheDocument();
  expect(screen.queryByText(/collapsed/)).not.toBeInTheDocument();
});

test("the button can be activated with an Enter key press", async () => {
  const user = userEvent.setup();
  const button = screen.getByRole("button");

  button.focus();
  await user.keyboard("{enter}");

  expect(screen.queryByText(/visible/)).toBeVisible();
  expect(screen.queryByText(/expanded/)).toBeInTheDocument();
  expect(screen.queryByText(/collapsed/)).not.toBeInTheDocument();
});

test("the button can be activated with an Enter key press", async () => {
  const user = userEvent.setup();
  const button = screen.getByRole("button");

  button.focus();
  await user.keyboard(" ");

  expect(screen.queryByText(/visible/)).toBeVisible();
  expect(screen.queryByText(/expanded/)).toBeInTheDocument();
  expect(screen.queryByText(/collapsed/)).not.toBeInTheDocument();
});

test("the button is not activated by other key presses", async () => {
  const user = userEvent.setup();
  const button = screen.getByRole("button");

  button.focus();
  await user.keyboard("f");

  expect(screen.queryByText(/visible/)).not.toBeVisible();
  expect(screen.queryByText(/expanded/)).not.toBeInTheDocument();
  expect(screen.queryByText(/collapsed/)).toBeInTheDocument();
});
