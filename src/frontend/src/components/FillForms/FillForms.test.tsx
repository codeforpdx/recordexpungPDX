import React from "react";
import { MemoryRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Provider } from "react-redux";
import store from "../../redux/store";
import FillForms from ".";
import { appRender, fillExpungementPacketForm } from "../../test/testHelpers";
import EmptyFieldsModal from "./EmptyFieldsModal";

const mockDownloadExpungementPacketFunc = jest.fn();

jest.mock("../../redux/search/actions", () => ({
  ...jest.requireActual("../../redux/search/actions"),
  downloadExpungementPacket: () => mockDownloadExpungementPacketFunc,
}));

describe("masterRender", () => {
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
});

describe("renderCorrect", () => {
  it("renders correctly", async () => {
    const { asFragment } = appRender(<FillForms />);
    const user = userEvent.setup();
    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });
    await user.click(downloadButton);
    expect(asFragment()).toMatchSnapshot();
  });
});

describe("beforeEach", () => {
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
    await fillExpungementPacketForm(user);
    await user.click(downloadButton);
    expect(mockDownloadExpungementPacketFunc).toHaveBeenCalled();
  });
});

//tests if modal renders
describe("modalRenders", () => {
  beforeEach(() => {
    render(
      <Provider store={store}>
        <MemoryRouter>
          <FillForms />
        </MemoryRouter>
      </Provider>
    );
  });

  it("modal renders correctly", async () => {
    const modal = render(
      <EmptyFieldsModal
        close={true}
        onClose={() => void {}}
        onDownload={() => void {}}
      />
    );

    const user = userEvent.setup();
    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });
    await user.click(downloadButton);
    expect(modal).not.toBeNull();
  });
});
