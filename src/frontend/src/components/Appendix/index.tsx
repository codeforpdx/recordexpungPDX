import React from "react";

class Landing extends React.Component {
  render() {
    return (
      <>
        <main className="flex-l mw8 center ph4 mt5">
          <article className="order-1 lh-copy">
            <section className="mb5">
              <h1 className="f2 fw9 mb3 mt4" id="appendix">
                Appendix
              </h1>
              <h3 className="fw7 tl mb2">Forms to file for expungement</h3>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Baker</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/courts/baker/help/Pages/forms.aspx"
                    >
                      Conviction
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/courts/baker/help/Pages/forms.aspx"
                    >
                      Arrest
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Benton</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Exp%20Section%20C%20Forms%20and%20Instructions.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Exp%20Section%20A%20Forms%20and%20Instructions.pdf"
                    >
                      Arrest but no charge ever filed in Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Exp%20Section%20B%20Forms%20and%20Instructions.pdf"
                    >
                      Arrested and charged in Court but later dismissed or
                      acquitted of charge(s) <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Clackamas</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Clackamas-Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Clackamas-Arrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Coos</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/COO-ExpungementAffidavitMotionOrderSetAsideConvictionCoos.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/COO-ExpungementAffidavitMotionOrderSetAsideArrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Curry</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/CUR-ExpungementAffidavitMotionOrderSetAsideConviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/CUR-ExpungementAffidavitMotionOrdeSetAsideArrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Jackson</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/JAC-PktC-CrimSetAside-Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/JAC-PktA-CrimSetAside-Arrest.pdf"
                    >
                      Arrest but no charges or cases were filed with the Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/JAC-PktB-CrimSetAside-DismissalAcquittal.pdf"
                    >
                      Arrested and a case filed with the Court but later
                      charge(s) were dismissed or acquitted{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Josephine</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="http://www.co.josephine.or.us/Files/Setting%20Aside%20Conviction%20Form.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="http://www.co.josephine.or.us/Files/Setting%20Aside%20Arrest%20Form.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Lane</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Motion%20and%20Affidavit%20to%20Set%20Aside%20Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Motion%20and%20Affidavit%20to%20Set%20Aside%20Charges.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Lincoln</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Lincoln%20Set%20Aside%20Conviction%20-%20PACKET.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Lincoln%20Set%20Aside%20Arrest%20-%20PACKET.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Linn</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/LIN-Criminal-SetAsideRecordsOfConviction-C.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/LIN-Criminal-SetAsideRecordsOfCharge-B.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Marion</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/MAR-SetAside-PacketC.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/MAR-SetAsidePacketA.pdf"
                    >
                      Arrest but no charges or cases were filed with the Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/MAR-SetAsidePacketB.pdf"
                    >
                      Arrested and a case filed with the Court, but later
                      charge(s) were dismissed or acquitted{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Morrow</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Umatilla-Morrow-Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Umatilla-Morrow-Arrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Multnomah</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.mcda.us/index.php/documents/conviction-motion-and-affidavit-form.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.mcda.us/index.php/documents/arrest-motion-and-affidavit-form.pdf"
                    >
                      Arrest
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Polk</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/PLK-ExpungementPACKETC.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/PLK-ExpungementPACKETA.pdf"
                    >
                      Arrest but no charges or cases were filed with the Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/PLK-ExpungementPACKETB.pdf"
                    >
                      Arrested and a case filed with the court, but later
                      charge(s) were dismissed or acquitted{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Tillamook</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/TIL-ExpungementConviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/TIL-ExpungementArrest.pdf"
                    >
                      Arrest but no charge ever filed in Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/TIL-ExpungementCharge.pdf"
                    >
                      Arrested and charged in Court but later dismissed or
                      acquitted of charge(s) <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Umatilla</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Umatilla-Morrow-Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Umatilla-Morrow-Arrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Washington</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/courts/washington/programs-services/Documents/WSH-ConvictionRecordExpungementPacket.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/courts/washington/programs-services/Documents/WSH-ArrestRecordExpungementPacket.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Yamhill</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/YAM-SetAsidePacketC.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/YAM-SetAsidePacketA.pdf"
                    >
                      Arrest only no charge ever filed in Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/YAM-SetAsidePacketB.pdf"
                    >
                      Arrested and charged in Court but later dismissed or
                      acquitted of charge(s) <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3" id="stockforms">
                <h4 className="fw7 mb2">
                  Stock Form (if county is not listed above)
                </h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Stock-Conviction-HM.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a className="bb hover-blue" href="/docs/Stock-Arrest.pdf">
                      Arrest <span className="f7 fw7">PDF</span>
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
