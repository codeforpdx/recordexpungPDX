import React from "react";
import { HashLink as Link } from "react-router-hash-link";

class AccessibilityStatement extends React.Component {

  componentDidMount(){
    document.title = "Accessibility Statement - RecordSponge"
  }

  render() {
    return (
      <>
        <div>
          <title>Accessibility Statement - RecordSponge Oregon</title>
        </div>
        <div className="mw7 center lh-copy ph4 mt5 mb6">
          <main>

            <h1 className="f3 f2-ns fw9 mt0 mb3">
              Accessibility Statement
            </h1>
            <p className="mb3">
              RecordSponge is committed to ensuring digital accessibility 
              for all people. We strive to meet level AA standards from the 
              {" "}
              <a 
                className="bb hover-blue" 
                href="https://www.w3.org/TR/WCAG21/#requirements-for-wcag-2-1"
              >
                Web Content Accessibility Guidelines (WCAG) 2.1
              </a>
              . We are continually improving the user experience for 
              everyone, and applying the relevant accessibility standards.
            </p>

            <h2 className="f4 f3-ns fw9 mb2 mt4">
              Conformance Status
            </h2>
            <p className="mb3">
              The Web Content Accessibility Guidelines (WCAG) defines 
              requirements for designers and developers to improve 
              accessibility for people with disabilities. It defines 
              three levels of conformance: Level A, Level AA, and Level 
              AAA. RecordSponge is largely conformant with WCAG 2.1 
              level AA. We’re working to bridge the remaining gaps.
            </p>
            <h2 className="f4 f3-ns fw9 mb2 mt4">
              Technical Specifications
            </h2>
            <p className="mb3">
              Accessibility of RecordSponge relies on the following 
              technologies to work with the particular combination of 
              web browser and any assistive technologies or plugins 
              installed on your computer:
            </p>
            <ul className="mb3 ml4">
              <li>
                HTML
              </li>
              <li>
                WAI-ARIA
              </li>
              <li>
                CSS
              </li>
              <li>
                JavaScript
              </li>
            </ul>
            <p className="mb3">
              These technologies are relied upon for conformance with 
              the accessibility standards used.
            </p>
            <h2 className="f4 f3-ns fw9 mb2 mt4">
              How We Test
            </h2>
            <p className="mb3">
              We test in most modern browsers, we use toolkits like 
              {" "}
              <a 
                className="bb hover-blue" 
                href="https://www.deque.com/axe"
              >
                axe
              </a>
              , and we use VoiceOver in Safari to review our site.
            </p>
            <h2 className="f4 f3-ns fw9 mb2 mt4">
              Limitations
            </h2>
            <p className="mb5">
              Despite our best efforts to ensure accessibility of 
              RecordSponge, there may be some limitations. Please 
              contact us if you observe an issue: contact@recordsponge.com
            </p>
          </main>
          <aside className="mb3">
            This statement was created on August 12, 2020 with guidance 
            from the 
            {" "}
            <a 
              className="bb hover-blue" 
              href="https://www.w3.org/WAI/planning/statements"
            >
              W3C Accessibility Statement Generator
            </a>
            .
          </aside>
        </div>
      </>
    );
  }
}

export default AccessibilityStatement;