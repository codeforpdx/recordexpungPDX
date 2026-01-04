import React from "react";
import axios from "axios";
import { BrowserRouter, MemoryRouter } from "react-router-dom";
import { Provider } from "react-redux";
import renderer from "react-test-renderer";
import { render, screen, waitFor } from "@testing-library/react";
import { createStore } from "../../test/testHelpers";
import App from ".";

function renderAtRoute(route: string) {
  // "/rules" requires a server fetch in order to display content
  jest
    .spyOn(axios, "request")
    .mockResolvedValue({ data: { charge_types: [] } });

  render(
    <Provider store={createStore()}>
      <MemoryRouter initialEntries={[route]}>
        <App />
      </MemoryRouter>
    </Provider>
  );
}

it("renders correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toBeTruthy();
});

describe("App routing", () => {
  // "/record-search" requires being logged in and is tested elsewhere
  const routeText = [
    ["/", "winner"],
    ["/oeci", "ecourt"],
    ["/demo-record-search", "app demo"],
    ["/manual", "introduction"],
    ["/rules", "type eligibility rules"],
    ["/faq", "myth"],
    ["/appendix", "forms to file"],
    ["/privacy-policy", "what we collect and why"],
    ["/fill-expungement-forms", "this will fill and download"],
    ["/partner-interest", "made for organizations to become expungement"],
    ["/accessibility-statement", "committed to ensuring digital"],
    ["/about", "collaboration between Code PDX"],
    ["/foo", "winner"],
  ];

  test.each(routeText)(
    "Route '%s' renders component with content '%s'",
    async (route, containedText) => {
      const regex = new RegExp(containedText, "i");

      renderAtRoute(route);
      await waitFor(() =>
        expect(screen.getAllByText(regex).length).toBeGreaterThan(0)
      );
    }
  );
});
