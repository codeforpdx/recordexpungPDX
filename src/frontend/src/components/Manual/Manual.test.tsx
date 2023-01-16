import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";

import Manual from ".";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <Manual />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
