import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import { Provider } from "react-redux";

import store from "../../redux/store";
import PartnerInterest from ".";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <Provider store={store}>
        <BrowserRouter>
          <PartnerInterest email="" invalidEmail={false} />
        </BrowserRouter>
      </Provider>
    )
    .toJSON();
  expect(tree).toBeTruthy();
});
