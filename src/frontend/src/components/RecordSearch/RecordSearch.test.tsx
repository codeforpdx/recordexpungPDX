import React from "react";
import { BrowserRouter } from "react-router-dom";
import renderer from "react-test-renderer";
import { Provider } from "react-redux";

import store from "../../redux/store";
import RecordSearch from ".";

it("renders correctly", () => {
  const RealDate = Date;
  const mockDate = new Date(2023, 0, 11);
  // @ts-ignore
  const spy = jest.spyOn(global, "Date").mockImplementation(() => mockDate);
  // @ts-ignore
  spy.now = RealDate.now;

  const tree = renderer
    .create(
      <Provider store={store}>
        <BrowserRouter>
          <RecordSearch />
        </BrowserRouter>
      </Provider>
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});
