import React from "react";
import "@testing-library/jest-dom";
import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { appRender } from "../../../../test/testHelpers";
import RecordSummary from ".";

jest.mock("axios", () => {
  return {
    request: () => new Promise(() => {}),
  };
});

const mockUseNavigate = jest.fn();

jest.mock("react-router-dom", () => ({
  ...(jest.requireActual("react-router-dom") as any),
  useNavigate: () => mockUseNavigate,
}));

// snapshot tests for the initial state are accounted
// for in the RecordSearch tests
describe("When rendered with the John Common demo data", () => {
  beforeEach(() => {
    appRender(<RecordSummary />, "common");
  });

  test("the generate paperwork button works", async () => {
    const user = userEvent.setup();
    const generateButton = screen.getByRole("button", {
      name: /generate paperwork/i,
    });
    const mockNavigate = jest.fn();
    mockUseNavigate.mockImplementationOnce(mockNavigate);

    await user.click(generateButton);
    expect(mockNavigate).toHaveBeenCalledWith("/fill-expungement-forms");
  });

  test("the summary pdf button works", async () => {
    const user = userEvent.setup();
    const pdfButton = screen.getByRole("button", {
      name: /summary pdf/i,
    });

    await user.click(pdfButton);
    expect(pdfButton).toHaveClass("loading-btn");
  });
});

describe("When rendered with empty results", () => {
  beforeEach(() => {
    appRender(<RecordSummary />, "blank");
  });

  test("the generate paperwork button will display an error with a dismiss button", async () => {
    const user = userEvent.setup();
    const generateButton = screen.getByRole("button", {
      name: /generate paperwork/i,
    });
    const errorMessage = /must be eligible charges to generate/i;

    await user.click(generateButton);
    expect(screen.queryByText(errorMessage)).toBeInTheDocument();

    const dismissButton = screen.getByRole("button", {
      name: /close/i,
    });

    await user.click(dismissButton);
    expect(screen.queryByText(errorMessage)).not.toBeInTheDocument();
  });
});
