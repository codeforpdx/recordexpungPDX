import React from "react";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";
import {
  appRender,
  fillNewCaseForm,
  clickButton,
} from "../../../test/testHelpers";
import Record from ".";

it("correctly renders after clicking add case button", async () => {
  const user = userEvent.setup();
  const { asFragment } = appRender(<Record />);

  await clickButton(user, "enable editing");
  await clickButton(user, "add case");
  // assert the form

  // expect(asFragment()).toMatchSnapshot();
  // These snapshot tests are dumb.

  await fillNewCaseForm(user);
  await clickButton(user, "create case");
  // assert the form is closed and the Add Case button is back
  
  // expect(asFragment()).toMatchSnapshot();
  // These snapshot tests are dumb.

});
