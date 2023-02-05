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
import initialState from "../redux/search/initialState";

interface ExtendedRenderOptions extends Omit<RenderOptions, "queries"> {
  preloadedState?: PreloadedState<RootState>;
  store?: AppStore;
}

export function appRender(
  ui: React.ReactElement,
  fakeResponseName?: FakeResponseName,
  { store, ...renderOptions }: ExtendedRenderOptions = {}
) {
  const search = fakeResponseName
    ? {
        ...initialState,
        record: getResponseFromRecordName(fakeResponseName).record,
      }
    : initialState;

  if (!store) {
    store = setupStore({ search });
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
