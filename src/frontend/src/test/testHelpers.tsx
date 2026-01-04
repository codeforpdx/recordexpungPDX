// https://redux.js.org/usage/writing-tests
import React, { PropsWithChildren } from "react";
import axios from "axios";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import { render, screen, RenderOptions } from "@testing-library/react";
import { UserEvent } from "@testing-library/user-event/dist/types/setup/setup";
import userEvent from "@testing-library/user-event";
import { PreloadedState } from "@reduxjs/toolkit";
import {
  getResponseFromRecordName,
  FakeResponseName,
} from "./hooks/useInjectSearchResponse";
import store, {
  setupStore,
  clearAllData,
  AppStore,
  RootState,
} from "../redux/store";
import { default as initialSearchState } from "../redux/search/initialState";
import {
  initialState as initialSearchFormState,
  setSearchFormDate,
} from "../redux/searchFormSlice";
import { processCharges } from "../redux/search/actions";
import App from "../components/App";

interface ExtendedRenderOptions extends Omit<RenderOptions, "queries"> {
  preloadedState?: PreloadedState<RootState>;
  store?: AppStore;
}

// setup helpers
export function createStore(fakeResponseName?: FakeResponseName) {
  let search = initialSearchState;

  if (fakeResponseName) {
    const record = getResponseFromRecordName(fakeResponseName).record;

    processCharges(record);
    search = {
      ...initialSearchState,
      record,
    };
  }

  return setupStore({
    search,
    searchForm: { ...initialSearchFormState, date: "1/2/2023" },
  });
}

export function appRender(
  ui: React.ReactElement,
  fakeResponseName?: FakeResponseName,
  { store, ...renderOptions }: ExtendedRenderOptions = {}
) {
  if (!store) {
    store = createStore(fakeResponseName);
  }

  function AllProviders({ children }: PropsWithChildren<{}>) {
    return (
      <Provider store={store!}>
        <MemoryRouter>{children}</MemoryRouter>
      </Provider>
    );
  }
  return { store, ...render(ui, { wrapper: AllProviders, ...renderOptions }) };
}

export function setupUserAndRender(
  ui: React.ReactElement,
  fakeResponseName?: FakeResponseName,
  opts: ExtendedRenderOptions = {}
) {
  const user = userEvent.setup();
  return { user, ...appRender(ui, fakeResponseName, opts) };
}

export function setupIntegrationTests(component = <App />) {
  store.dispatch(clearAllData());
  store.dispatch(setSearchFormDate("1/2/2023"));

  const user = userEvent.setup();
  const requestSpy = jest.spyOn(axios, "request").mockResolvedValue({});

  appRender(component, undefined, {
    store,
  });
  return { user, requestSpy };
}

// assertion helpers
export function assertRequest(spy: jest.SpyInstance, obj: Object) {
  expect(spy).toHaveBeenCalledWith(obj);
  spy.mockClear();
}

// user helpers
export async function goToSearchPage(user: UserEvent) {
  await user.click(screen.getAllByRole("link", { name: /search/i })[0]);
}

type ButtonName =
  | "login"
  | "search"
  | "alias"
  | "remove"
  | "enable editing"
  | "add case"
  | "create case"
  | "edit case"
  | "remove case"
  | "update case"
  | "add charge"
  | "edit charge"
  | "update charge"
  | "remove charge"
  | "summary"
  | "generate paperwork"
  | "download packet"
  | "start over";

export async function clickButton(
  user: UserEvent,
  name: ButtonName,
  index?: number
) {
  const nameMap = {
    login: /log in/i,
    search: /search/i,
    alias: /alias/i,
    "enable editing": /enable editing/i,
    "add case": /add case/i,
    "create case": /create case/i,
    "edit case": /edit case/i,
    "remove case": /remove case/i,
    "update case": /update case/i,
    "add charge": /add charge/i,
    "edit charge": /edit charge/i,
    "update charge": /update charge/i,
    "remove charge": /remove charge/i,
    remove: /remove/i,
    summary: /summary/i,
    "generate paperwork": /generate paperwork/i,
    "download packet": /download expungement packet/i,
    "start over": /start over/i,
  } as Record<string, RegExp>;

  await user.click(
    screen.getAllByRole("button", { name: nameMap[name] })[index ?? 0]
  );
}

export async function fillLoginForm(user: UserEvent) {
  await user.click(screen.getByLabelText(/user id/i));
  await user.keyboard("username");
  await user.click(screen.getByLabelText(/password/i));
  await user.keyboard("secret");
}

export async function fillSearchFormNames(
  user: UserEvent,
  firstName = true,
  lastName = true
) {
  if (firstName) {
    await user.click(screen.getByLabelText(/first name/i));
    await user.keyboard("foo");
  }
  if (lastName) {
    await user.click(screen.getByLabelText(/last name/i));
    await user.keyboard("bar");
  }
}

export async function fillNewCaseForm(user: UserEvent) {
  await user.click(screen.getByLabelText(/open/i));
  await user.selectOptions(
    screen.getByRole("combobox"),
    screen.getByRole("option", { name: /benton/i })
  );
  await user.click(screen.getByLabelText(/balance/i));
  // Balance already has a value of 0.00, so need to backspace first.
  await user.keyboard("{Backspace}1");
  await user.click(screen.getByLabelText(/birth year/i));
  await user.keyboard("1999");
}

export async function fillExpungementPacketForm(user: UserEvent, dobIndex = 0) {
  await user.click(screen.getAllByLabelText(/birth/i)[dobIndex]);
  await user.keyboard("12/12/1999");

  await user.click(screen.getByLabelText(/mailing street address/i));
  await user.keyboard("1111 NE anywhere");

  await user.click(screen.getByLabelText(/city/i));
  await user.keyboard("Portland");

  await user.selectOptions(
    screen.getByRole("combobox"),
    screen.getByRole("option", { name: /oregon/i })
  );

  await user.click(screen.getByLabelText(/zip code/i));
  await user.keyboard("12345");

  await user.click(screen.getByLabelText(/phone/i));
  await user.keyboard("123-456-7890");
}
