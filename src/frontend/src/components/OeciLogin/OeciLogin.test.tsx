import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import { Provider } from "react-redux";

import store from "../../redux/store";
import OeciLogin from ".";

it("renders correctly", () => {
  const tree = renderer
    .create(
      <Provider store={store}>
        <BrowserRouter>
          <OeciLogin
            userId=""
            password=""
            missingUserId={false}
            missingPassword={false}
            expectedFailure={false}
            expectedFailureMessage=""
            invalidResponse={false}
            missingInputs={false}
            isLoggedIn={false}
          />
        </BrowserRouter>
      </Provider>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
