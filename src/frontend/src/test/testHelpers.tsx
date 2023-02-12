// https://redux.js.org/usage/writing-tests
import React, { PropsWithChildren } from "react";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import { render, RenderOptions } from "@testing-library/react";
import { PreloadedState } from "@reduxjs/toolkit";
import { setupStore, AppStore } from "../redux/store";
import { getResponseFromRecordName } from "./hooks/useInjectSearchResponse";
import { RootState } from "../redux/store";
import { FakeResponseName } from "./hooks/useInjectSearchResponse";
import { default as initialSearchState } from "../redux/search/initialState";
import { initialState as initialSearchFormState } from "../redux/searchFormSlice";

interface ExtendedRenderOptions extends Omit<RenderOptions, "queries"> {
  preloadedState?: PreloadedState<RootState>;
  store?: AppStore;
}

export function createStore(fakeResponseName?: FakeResponseName) {
  const search = fakeResponseName
    ? {
        ...initialSearchState,
        record: getResponseFromRecordName(fakeResponseName).record,
      }
    : initialSearchState;

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
