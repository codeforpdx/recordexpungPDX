import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";

import Appendix from ".";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <BrowserRouter>
        <Appendix />
      </BrowserRouter>
    )
    .toJSON();
  expect(tree).toBeTruthy();
});
