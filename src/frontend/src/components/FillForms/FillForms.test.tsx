import React from "react";
import { MemoryRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Provider } from "react-redux";
import store from "../../redux/store";
import FillForms from ".";

const mockDownloadExpungementPacketFunc = jest.fn();

jest.mock("../../redux/search/actions", () => ({
  ...jest.requireActual("../../redux/search/actions"),
  downloadExpungementPacket: () => mockDownloadExpungementPacketFunc,
}));

it("renders correctly", () => {
  const tree = renderer
    .create(
      <Provider store={store}>
        <MemoryRouter>
          <FillForms />
        </MemoryRouter>
      </Provider>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

beforeEach(() => {
  render(
    <Provider store={store}>
      <MemoryRouter>
        <FillForms />
      </MemoryRouter>
    </Provider>
  );
});

it("will not submit a blank form", async () => {
  const user = userEvent.setup();
  const downloadButton = screen.getByRole("button", {
    name: /download expungement packet/i,
  });

  await user.click(downloadButton);

  expect(mockDownloadExpungementPacketFunc).not.toHaveBeenCalled();
});

test("with a valid zip code, dob, and phone number the form can be submitted", async () => {
  const user = userEvent.setup();
  const downloadButton = screen.getByRole("button", {
    name: /download expungement packet/i,
  });
  const zipCodeField = screen.getByLabelText(/zip code/i);
  const dobCodeField = screen.getByLabelText(/date of birth/i);
  const phoneCodeField = screen.getByLabelText(/phone number/i);

  await user.click(dobCodeField);
  await user.keyboard("11/13/1995");
  await user.click(phoneCodeField);
  await user.keyboard("1112223333");
  await user.click(zipCodeField);
  await user.keyboard("12345");
  await user.click(downloadButton);
  expect(mockDownloadExpungementPacketFunc).toHaveBeenCalled();
});
