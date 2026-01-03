import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";

import PrivacyPolicy from ".";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <PrivacyPolicy />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toBeTruthy();
});
