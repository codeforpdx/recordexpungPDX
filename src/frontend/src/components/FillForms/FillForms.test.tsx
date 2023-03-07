import React from "react";
import { MemoryRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";
import { Provider } from "react-redux";
import store from "../../redux/store";
import FillForms from ".";
import { appRender, fillExpungementPacketForm } from "../../test/testHelpers";

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

  it("packet will download when all fields are properly filled", async () => {
    const user = userEvent.setup();

    fillExpungementPacketForm(user);

    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });

    await user.click(downloadButton);

    expect(mockDownloadExpungementPacketFunc).not.toHaveBeenCalled();
  });
});

//modal will still render if certain fields are filled in or not
describe("modal with certain fields filled out", () => {
  beforeEach(() => {
    render(
      <Provider store={store}>
        <MemoryRouter>
          <FillForms />
        </MemoryRouter>
      </Provider>
    );
  });

  it("1 modal renders correctly when only name is filled out", async () => {
    const user = userEvent.setup();

    await user.click(screen.getByLabelText(/full name/i));
    await user.keyboard("username");

    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });

    await user.click(downloadButton);
    expect(screen.getByText(/incomplete/i)).toBeInTheDocument();
  });

  it("2 modal renders correctly when only name and DOB are filled out", async () => {
    const user = userEvent.setup();

    await user.click(screen.getByLabelText(/full name/i));
    await user.keyboard("username");
    await user.click(screen.getByLabelText(/birth/i));
    await user.keyboard("12/12/1999");

    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });

    await user.click(downloadButton);
    expect(screen.getByText(/incomplete/i)).toBeInTheDocument();
  });

  it("3 modal renders correctly when only name, DOB, and ZipCode are filled out", async () => {
    const user = userEvent.setup();

    await user.click(screen.getByLabelText(/full name/i));
    await user.keyboard("username");
    await user.click(screen.getByLabelText(/birth/i));
    await user.keyboard("12/12/1999");
    await user.click(screen.getByLabelText(/zip code/i));
    await user.keyboard("12345");

    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });

    await user.click(downloadButton);
    expect(screen.getByText(/incomplete/i)).toBeInTheDocument();
  });

  it("4 modal renders correctly when only name, DOB, ZipCode, and PhoneNumber are filled out", async () => {
    const user = userEvent.setup();

    await user.click(screen.getByLabelText(/full name/i));
    await user.keyboard("username");
    await user.click(screen.getByLabelText(/birth/i));
    await user.keyboard("12/12/1999");
    await user.click(screen.getByLabelText(/zip code/i));
    await user.keyboard("12345");
    await user.click(screen.getByLabelText(/phone/i));
    await user.keyboard("123-456-7890");

    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });

    await user.click(downloadButton);
    expect(screen.getByText(/incomplete/i)).toBeInTheDocument();
  });

  it("5 modal renders correctly when only name, DOB, ZipCode, PhoneNumber, and MailingAddress are filled out", async () => {
    const user = userEvent.setup();

    await user.click(screen.getByLabelText(/full name/i));
    await user.keyboard("username");
    await user.click(screen.getByLabelText(/birth/i));
    await user.keyboard("12/12/1999");
    await user.click(screen.getByLabelText(/zip code/i));
    await user.keyboard("12345");
    await user.click(screen.getByLabelText(/phone/i));
    await user.keyboard("123-456-7890");
    await user.click(screen.getByLabelText(/address/i));
    await user.keyboard("1111 NE anywhere");

    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });

    await user.click(downloadButton);
    expect(screen.getByText(/incomplete/i)).toBeInTheDocument();
  });

  it("6 modal does NOT render when all fields are filled out", async () => {
    const user = userEvent.setup();

    await user.click(screen.getByLabelText(/full name/i));
    await user.keyboard("username");
    await user.click(screen.getByLabelText(/birth/i));
    await user.keyboard("12/12/1999");
    await user.click(screen.getByLabelText(/zip code/i));
    await user.keyboard("12345");
    await user.click(screen.getByLabelText(/phone/i));
    await user.keyboard("123-456-7890");
    await user.click(screen.getByLabelText(/address/i));
    await user.keyboard("1111 NE anywhere");
    await user.click(screen.getByLabelText(/city/i));
    await user.keyboard("Portland");
    await user.selectOptions(
      screen.getByRole("combobox"),
      screen.getByRole("option", { name: /oregon/i })
    );

    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });

    await user.click(downloadButton);

    expect(screen.queryByText(/incomplete/i)).not.toBeInTheDocument();
  });
});

// possible test for modal pop-up and successful download when mailingAddress or City is not filled
describe("test if certain fields left empty will still trigger the modal and a download", () => {
  beforeEach(() => {
    render(
      <Provider store={store}>
        <MemoryRouter>
          <FillForms />
        </MemoryRouter>
      </Provider>
    );
  });

  it("7 modal and download cannot happen at the same time when city field isnt completed", async () => {
    const user = userEvent.setup();

    await user.click(screen.getByLabelText(/full name/i));
    await user.keyboard("username");
    await user.click(screen.getByLabelText(/birth/i));
    await user.keyboard("12/12/1999");
    await user.click(screen.getByLabelText(/zip code/i));
    await user.keyboard("12345");
    await user.click(screen.getByLabelText(/phone/i));
    await user.keyboard("123-456-7890");
    await user.click(screen.getByLabelText(/address/i));
    await user.keyboard("1111 NE anywhere");
    await user.selectOptions(
      screen.getByRole("combobox"),
      screen.getByRole("option", { name: /oregon/i })
    );
    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });

    await user.click(downloadButton);

    expect(mockDownloadExpungementPacketFunc).not.toHaveBeenCalled();
    expect(screen.queryByText(/incomplete/i)).not.toBeNull();
  });

  it("8 modal and downlaod cannot happen at the same time when mailing address field isnt completed", async () => {
    const user = userEvent.setup();

    await user.click(screen.getByLabelText(/full name/i));
    await user.keyboard("username");
    await user.click(screen.getByLabelText(/birth/i));
    await user.keyboard("12/12/1999");
    await user.click(screen.getByLabelText(/zip code/i));
    await user.keyboard("12345");
    await user.click(screen.getByLabelText(/phone/i));
    await user.keyboard("123-456-7890");
    await user.click(screen.getByLabelText(/city/i));
    await user.keyboard("Portland");
    await user.selectOptions(
      screen.getByRole("combobox"),
      screen.getByRole("option", { name: /oregon/i })
    );

    const downloadButton = screen.getByRole("button", {
      name: /download expungement packet/i,
    });

    await user.click(downloadButton);
    expect(mockDownloadExpungementPacketFunc).not.toHaveBeenCalled();
    expect(screen.queryByText(/incomplete/i)).not.toBeNull();
  });
});
