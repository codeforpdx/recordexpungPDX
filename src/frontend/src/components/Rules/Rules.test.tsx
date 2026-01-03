import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";

import Rules from ".";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <Rules />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toBeTruthy();
});
