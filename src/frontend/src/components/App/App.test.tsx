import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";

import App from ".";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
