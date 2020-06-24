import React from "react";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@reach/disclosure";


export default class PartnerTable extends React.Component {
  public render() {
    return (
      <Disclosure >
        <DisclosureButton className="mb1 flex-ns bg-white br3 pa3 ba b--white hover-b-blue"> Redmond Housing Works</DisclosureButton>
        <DisclosurePanel>Here I am! I am the buried treasure!</DisclosurePanel>
      </Disclosure>
    );
  }
}

