import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";

import Faq from ".";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <Faq />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toBeTruthy();
});
