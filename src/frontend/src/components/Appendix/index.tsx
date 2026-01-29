import React from "react";
import { HashLink as Link } from "react-router-hash-link";

class Landing extends React.Component {

  componentDidMount(){
    document.title = "Appendix - RecordSponge";
  }

  render() {
    return (
      <>
        <main className="flex-l mw8 center ph3 mt5">
          <article className="order-1 lh-copy">
            <section className="mb5">
              <h1 className="f2 fw9 mb3 mt4" id="appendix">
                Appendix
              </h1>
              <h2 className="fw7 tl mb2">Forms to file for expungement</h2>
              <p className="mb4 mw7">
                RecordSponge supports automatic form-filling for all the 
                counties listed here, and will use the Stock Form for those 
                not listed. You can also fill out the forms manually if 
                preferred.{" "}
                <Link to="/manual#file" className="link hover-dark-blue bb">
                  Learn more in the Manual
                </Link>
                .
              </p>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Multnomah</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Multnomah-County-Conviction-Form.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Multnomah-County-Arrest-Form.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3" id="stockforms">
                <h3 className="fw7 mb2">
                  All Other Counties
                </h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a className="bb hover-blue" href="/docs/CriminalSetAside_AdultCases2026.pdf">
                      Circuit Court Blank Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a className="bb hover-blue" href="/docs/MUNI_CriminalSetAside_AdultCases2026.pdf">
                      Municipal Court Blank Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a className="bb hover-blue" href="/docs/osp-criminal-history-request-form.pdf">
                      Criminal History Request Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
            </section>
          </article>
        </main>
      </>
    );
  }
}

export default Landing;
