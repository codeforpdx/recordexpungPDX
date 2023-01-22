import React from "react";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import renderer from "react-test-renderer";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router";
import store from "../../../../redux/store";
import history from "../../../../service/history";
import johnCommonRecord from "../../../../data/demo/johnCommon";
import multipleChargesRecord from "../../../../data/demo/multipleCharges";
import RecordSummary from ".";

const downloadPdfPath = "../../../../redux/search/actions";
const mockDownloadPdf = jest.fn();
const summary = johnCommonRecord.summary!;

jest.mock(downloadPdfPath, () => ({
  ...jest.requireActual(downloadPdfPath),
  downloadPdf: () => mockDownloadPdf(),
}));

it("correctly renders with the John Common demo data", () => {
  const tree = renderer
    .create(
      <Provider store={store}>
        <MemoryRouter>
          <RecordSummary summary={summary} />
        </MemoryRouter>
      </Provider>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it("correctly renders with the Multiple Charges demo data", () => {
  const tree = renderer
    .create(
      <Provider store={store}>
        <MemoryRouter>
          <RecordSummary summary={multipleChargesRecord.summary!} />
        </MemoryRouter>
      </Provider>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

describe("When rendered with the John Common demo data", () => {
  beforeEach(() => {
    render(
      <>
        <Provider store={store}>
          <MemoryRouter>
            <RecordSummary summary={summary} />
          </MemoryRouter>
        </Provider>
      </>
    );
  });

  test("the generate paperwork button works", async () => {
    const user = userEvent.setup();
    const historySpy = jest.spyOn(history, "push").mockReturnValue();
    const generateButton = screen.getByRole("button", {
      name: /generate paperwork/i,
    });

    await user.click(generateButton);

    expect(historySpy).toHaveBeenCalledWith("/fill-expungement-forms");
  });

  test("the summary pdf button works", async () => {
    const user = userEvent.setup();
    const pdfButton = screen.getByRole("button", {
      name: /summary pdf/i,
    });

    await user.click(pdfButton);

    expect(mockDownloadPdf).toHaveBeenCalled();
  });
});

describe("When rendered with empty results", () => {
  beforeEach(() => {
    const summary = {
      total_charges: 0,
      charges_grouped_by_eligibility_and_case: {},
      county_fines: [],
      total_fines_due: 0,
      total_cases: 0,
    };
    render(
      <Provider store={store}>
        <MemoryRouter>
          <RecordSummary summary={summary} />
        </MemoryRouter>
      </Provider>
    );
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
