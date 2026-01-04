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
                <h3 className="fw7 mb2">Baker</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Benton</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Clackamas</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Coos</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Curry</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Jackson</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Josephine</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Lane</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Lincoln</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Linn</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Marion</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Morrow</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Multnomah</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Multnomah-Conviction-Form.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Multnomah-Arrest-Form.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Multnomah-marijuana.pdf"
                    >
                      Marijuana <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Polk</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Tillamook</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Umatilla</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Washington</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h3 className="fw7 mb2">Yamhill</h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Blank-County-Expungement-Form.pdf"
                    >
                      Expungement Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3" id="stockforms">
                <h3 className="fw7 mb2">
                  Stock Forms
                </h3>
                <ul className="list ml2">
                  <li className="mb3">
                    <a className="bb hover-blue" href="/docs/osp-criminal-history-request-form.pdf">
                      Criminal History Request Form <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a className="bb hover-blue" href="/docs/Blank-MUNICIPAL-Expungement-Form.pdf">
                      Municipal Courts <span className="f7 fw7">PDF</span>
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
