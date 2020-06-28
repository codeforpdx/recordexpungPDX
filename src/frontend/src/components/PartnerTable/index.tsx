import React from "react";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@reach/disclosure";

class PartnerTable extends React.Component {
  render() {
    return (
      <React.Fragment>
        <div className="bg-navy pv6">
          <div className="mw7 center">
            <div className="mh4">
              <h2 className="white tc f3 f2-ns fw9 mb3">
                Are you looking to clear your record?
              </h2>
              <p className="white tc center mw6 mb4">
                Select a partner below near you. They can provide your analysis
                and help you file for expungement.
              </p>
            </div>
            <div className="ba bw3 br3 b--lightest-blue1 bg-white mb6">
              <h3 className="f3 fw9 pa4">Partners</h3>
              <ul className="list">
                <li className="bt bw2 b--lightest-blue1">
                  <Disclosure>
                    <DisclosureButton className="flex-ns w-100 relative navy hover-blue pv3 ph3 ph4-ns">
                      <span className="w-70 db fw7 pr3 mb2 mb0-ns">
                        Portland Community College
                      </span>
                      <span className="w-30 pr3">Northeast Portland</span>
                      <span className="absolute top-0 right-0 pt3 ph3">
                        <span
                          aria-hidden="true"
                          className="fas fa-angle-down"
                        ></span>
                      </span>
                    </DisclosureButton>
                    <DisclosurePanel>
                      <div className="bl bw2 f5 b--blue pb3 ph3 ml3 ml4-ns">
                        Here I am! I am the buried treasure!
                      </div>
                    </DisclosurePanel>
                  </Disclosure>{" "}
                </li>

                <li className="bt bw2 b--lightest-blue1">
                  <Disclosure>
                    <DisclosureButton className="flex-ns w-100 relative navy hover-blue pv3 ph3 ph4-ns">
                      <span className="w-70 db fw7 pr3 mb2 mb0-ns">
                        Qiu-qiu Law
                      </span>
                      <span className="w-30 pr3">Portland</span>
                      <span className="absolute top-0 right-0 pt3 ph3">
                        <span
                          aria-hidden="true"
                          className="fas fa-angle-up"
                        ></span>
                      </span>
                    </DisclosureButton>
                    <DisclosurePanel>
                      <div className="bl bw2 f5 b--blue pb3 ph3 ml3 ml4-ns">
                        <ul className="list mb3">
                          <li className="flex-ns mb3">
                            <span className="w4-ns db fw6 mr3">
                              Analysis Cost
                            </span>
                            <span>Free</span>
                          </li>
                          <li className="flex-ns mb3">
                            <span className="w4-ns db fw6 mr3">
                              Filing Cost
                            </span>
                            <span>NA</span>
                          </li>
                          <li className="flex-ns mb3">
                            <span className="w4-ns db fw6 mr3">Court Fees</span>
                            <span>Not Included</span>
                          </li>
                          <li className="flex-ns mb3">
                            <span className="w4-ns db fw6 mr3">
                              Income Restrictions
                            </span>
                            <span>Under 45k Annual</span>
                          </li>
                          <li className="flex-ns mb3">
                            <span className="w4-ns db fw6 mr3">Locations</span>
                            <span>Portland Metro</span>
                          </li>
                        </ul>
                        <p className="mw6 bt b--black-10 pv3">
                          Send an email with your full name, previous names
                          (including aliases and maiden names), and date of
                          birth.
                        </p>
                        <ul className="list mb3">
                          <li className="fw6 mb3">email@domain.com</li>
                          <li className="fw6 mb2">555-555-5555</li>
                        </ul>
                      </div>
                    </DisclosurePanel>
                  </Disclosure>
                </li>

                <li className="bt bw2 b--lightest-blue1">
                  <Disclosure>
                    <DisclosureButton className="flex-ns w-100 relative navy hover-blue pv3 ph3 ph4-ns">
                      <span className="w-70 db fw7 pr3 mb2 mb0-ns">
                        Criminals Anonymous
                      </span>
                      <span className="w-30 pr3">East Portland</span>
                      <span className="absolute top-0 right-0 pt3 ph3">
                        <span
                          aria-hidden="true"
                          className="fas fa-angle-down"
                        ></span>
                      </span>
                    </DisclosureButton>
                    <DisclosurePanel>
                      <div className="bl bw2 f5 b--blue pb3 ph3 ml3 ml4-ns">
                        Here I am! I am the buried treasure!
                      </div>
                    </DisclosurePanel>
                  </Disclosure>
                </li>

                <li className="bt bw2 b--lightest-blue1">
                  <Disclosure>
                    <DisclosureButton className="flex-ns w-100 relative navy hover-blue pv3 ph3 ph4-ns">
                      <span className="w-70 db fw7 pr3 mb2 mb0-ns">
                        Probation and Parole, Community Justice Center
                      </span>
                      <span className="w-30 pr3">Medford</span>
                      <span className="absolute top-0 right-0 pt3 ph3">
                        <span
                          aria-hidden="true"
                          className="fas fa-angle-down"
                        ></span>
                      </span>
                    </DisclosureButton>
                    <DisclosurePanel>
                      <div className="bl bw2 f5 b--blue pb3 ph3 ml3 ml4-ns">
                        Here I am! I am the buried treasure!
                      </div>
                    </DisclosurePanel>
                  </Disclosure>
                </li>
              </ul>
            </div>

            <span className="db w4 center bb bw2 b--blue mb3"></span>
            <p className="tc white mw7 mh4">
              Over 1,060 analyses delivered as of June 11, 2020
            </p>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default PartnerTable;
