import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import { Provider } from 'react-redux'
import store from "../../redux/store";
import FillForms from ".";
import { MemoryRouter } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

const mockDownloadExpungementPacketFunc = jest.fn();
jest.mock("../../redux/search/actions", () => ({
  ...jest.requireActual("../../redux/search/actions"),
  downloadExpungementPacket: () => mockDownloadExpungementPacketFunc,
}));

it("renders correctly", () => {
  const tree = renderer
    .create(
      <Provider store={store}>
        <BrowserRouter>
          <FillForms />
        </BrowserRouter>
      </Provider>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it("will not submit a blank form", async () => {
  const user = userEvent.setup();
  const downloadButton = screen.getByRole("button", {
    name: /download expungement packet/i,
  });
  await user.click(downloadButton);
  expect(mockDownloadExpungementPacketFunc).not.toHaveBeenCalled();
});
test("with a valid zip code, the form can be submitted", async () => {
  const user = userEvent.setup();
  const downloadButton = screen.getByRole("button", {
    name: /download expungement packet/i,
  });
  const zipCodeField = screen.getByLabelText(/zip code/i);
  await user.click(zipCodeField);
  await user.keyboard("12345");
  await user.click(downloadButton);
  expect(mockDownloadExpungementPacketFunc).toHaveBeenCalled();
});
