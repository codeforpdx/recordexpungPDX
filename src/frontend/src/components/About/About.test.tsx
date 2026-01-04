import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";

import About from "./";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <About />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toBeTruthy();
});
