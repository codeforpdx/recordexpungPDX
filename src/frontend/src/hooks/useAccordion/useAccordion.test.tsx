import React from "react";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import useAccordion from ".";

const sections = [
  { header: "header0", panel: "panel0" },
  { header: "header1", panel: "panel1" },
  { header: "header2", panel: "panel2" },
];

function TestComponent() {
  const { useAccordionSection } = useAccordion();

  return (
    <ul>
      {sections.map(({ header, panel }) => {
        const { isExpanded, headerProps, panelProps } = useAccordionSection({
          id: header,
        });

        return (
          <li key={header}>
            <button {...headerProps}>{header}</button>
            <div {...panelProps}>{panel}</div>
            <p>{(isExpanded ? "expanded" : "collapsed") + panel}</p>
          </li>
        );
      })}
    </ul>
  );
}

describe("default state", () => {
  beforeEach(() => {
    render(<TestComponent />);
  });

  sections.forEach(({ header, panel }) => {
    test(`the initial state is closed (${header})`, () => {
      const button = screen.queryByRole("button", { name: header });
      const content = screen.queryByText(panel);

      expect(button).toHaveAttribute("aria-expanded", "false");
      expect(button).toHaveAttribute(
        "aria-controls",
        "accordion-panel-" + header
      );

      expect(content).toHaveAttribute("id", "accordion-panel-" + header);
      expect(content).not.toBeVisible();

      expect(screen.queryByText("expanded" + panel)).not.toBeInTheDocument();
      expect(screen.queryByText("collapsed" + panel)).toBeInTheDocument();
    });
  });
});

describe("when the first header is clicked", () => {
  beforeEach(async () => {
    render(<TestComponent />);

    const user = userEvent.setup();
    await user.click(screen.getByRole("button", { name: sections[0].header }));
  });

  it("shows the first panel's content", () => {
    const panel = sections[0].panel;
    expect(screen.queryByText(panel)).toBeVisible();
    expect(screen.queryByText("expanded" + panel)).toBeInTheDocument();
    expect(screen.queryByText("collapsed" + panel)).not.toBeInTheDocument();
  });

  [1, 2].forEach((idx) => {
    it(`doesn't show the index = ${idx} panel's content`, () => {
      const panel = sections[idx].panel;
      expect(screen.queryByText(panel)).not.toBeVisible();
      expect(screen.queryByText("expanded" + panel)).not.toBeInTheDocument();
      expect(screen.queryByText("collapsed" + panel)).toBeInTheDocument();
    });
  });
});

describe("when the second header is clicked after the first is clicked", () => {
  beforeEach(async () => {
    render(<TestComponent />);

    const user = userEvent.setup();
    await user.click(screen.getByRole("button", { name: sections[0].header }));
    await user.click(screen.getByRole("button", { name: sections[1].header }));
  });

  it("shows the second panel's content", () => {
    const panel = sections[1].panel;

    expect(screen.queryByText(panel)).toBeVisible();
    expect(screen.queryByText("expanded" + panel)).toBeInTheDocument();
    expect(screen.queryByText("collapsed" + panel)).not.toBeInTheDocument();
  });

  [0, 2].forEach((idx) => {
    it(`doesn't show the index = ${idx} panel's content`, () => {
      const panel = sections[idx].panel;
      expect(screen.queryByText(panel)).not.toBeVisible();
      expect(screen.queryByText("expanded" + panel)).not.toBeInTheDocument();
      expect(screen.queryByText("collapsed" + panel)).toBeInTheDocument();
    });
  });
});
