import React from "react";
import "@testing-library/jest-dom";
import { render, screen, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Accordion from "./Accordion";

afterEach(() => {
  window.location.hash = "";
});

test("renders with title and children hidden by default", () => {
  render(<Accordion title="Test Section">Content here</Accordion>);

  expect(screen.getByLabelText("Test Section")).toBeInTheDocument();
  expect(screen.queryByText("Content here")).not.toBeVisible();
});

test("opens and closes on click", async () => {
  const user = userEvent.setup();
  render(<Accordion title="Toggle Me">Inner content</Accordion>);

  const summary = screen.getByLabelText("Toggle Me");

  await user.click(summary);
  expect(screen.getByText("Inner content")).toBeVisible();

  await user.click(summary);
  expect(screen.queryByText("Inner content")).not.toBeVisible();
});

test("renders open when defaultOpen is set", () => {
  render(
    <Accordion title="Open Section" defaultOpen>
      Visible content
    </Accordion>,
  );

  expect(screen.getByText("Visible content")).toBeVisible();
});

test("renders with qna type", () => {
  render(
    <Accordion title="Is this a question?" type="qna">
      Answer here
    </Accordion>,
  );

  expect(screen.getByText(/Q:/)).toBeInTheDocument();
  expect(screen.getByLabelText("Is this a question?")).toBeInTheDocument();
});

test("opens when URL hash matches id", () => {
  window.location.hash = "#my-section";

  render(
    <Accordion title="My Section" id="my-section">
      Hash content
    </Accordion>,
  );

  expect(screen.getByText("Hash content")).toBeVisible();
});

test("does not open when URL hash does not match id", () => {
  window.location.hash = "#other-section";

  render(
    <Accordion title="My Section" id="my-section">
      Hash content
    </Accordion>,
  );

  expect(screen.queryByText("Hash content")).not.toBeVisible();
});

test("opens on hashchange event", () => {
  render(
    <Accordion title="My Section" id="my-section">
      Hash content
    </Accordion>,
  );

  expect(screen.queryByText("Hash content")).not.toBeVisible();

  act(() => {
    window.location.hash = "#my-section";
    window.dispatchEvent(new HashChangeEvent("hashchange"));
  });

  expect(screen.getByText("Hash content")).toBeVisible();
});

test("hash match opens ancestor details elements", () => {
  window.location.hash = "#child";

  render(
    <Accordion title="Parent" id="parent">
      <Accordion title="Child" id="child">
        Nested content
      </Accordion>
    </Accordion>,
  );

  const parent = screen.getByLabelText("Parent").closest("details")!;
  expect(parent).toHaveAttribute("open");
  expect(screen.getByText("Nested content")).toBeVisible();
});
