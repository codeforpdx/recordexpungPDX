import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";

import AccessibilityStatement from ".";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <AccessibilityStatement />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toBeTruthy();
});
