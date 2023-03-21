import React, { useEffect } from "react";
import UserDataForm from "./UserDataForm";
import { HashLink as Link } from "react-router-hash-link";
import setupPage from "../../service/setupPage";

export default function FillFormsIndex() {
  setupPage("Generate Expungement Forms");

  return (
    <main className="mw8 center f6 f5-l ph3 pt4 pb6">
      <h1 className="f3 f2-l fw9 mb4">Generate Expungement Forms</h1>
      <div className="flex-l pt2">
        <div className="w-50-l pr4-l mb4">
          <section className="mw6 lh-copy">
            <p className="mb3">
              This will fill and download the required paperwork forms as PDF
              files for all cases that have charges eligible for expungement.
            </p>

            <p className="mb3">
              On this page, you may optionally provide the person's name,
              address, and other information and it will be used to populate the
              forms. It is not required if you would prefer to fill out the
              information later, and we do not save any of this information.
            </p>

            <p className="mb2">
              The following required information is obtained from OECI and will
              be provided in the form:
            </p>
            <ol className="pl4 mb3">
              <li>Case number</li>
              <li>Names of charges</li>
              <li>Dates of arrest</li>
              <li>Dates of conviction or dismissal</li>
            </ol>

            <p className="mb2">
              The following information might be missing from OECI. If it's
              available, it will be provided in the form. If it is not present
              in OECI, some of the information may or may not be required in the
              application; please consult the{" "}
              <Link to="/manual#file" className="link hover-dark-blue bb">
                Manual
              </Link>
              .
            </p>
            <ol className="pl4 mb3">
              <li>Arresting Agency</li>
              <li>DA Number</li>
            </ol>

            <p className="mb3">
              The form that is filled out for each case is selected based on the{" "}
              <strong>County</strong> information for that case.
            </p>

            <p className="mb3">
              RecordSponge supports automatic form-filling for all the counties
              in our{" "}
              <Link to="/appendix" className="link hover-dark-blue bb">
                appendix
              </Link>
              , and will use the Stock Form for those not listed.
            </p>

            <p className="mb3">
              Please read the complete instructions in the{" "}
              <Link to="/manual#file" className="link hover-dark-blue bb">
                Manual
              </Link>{" "}
              for filing the required forms for expungement. After downloading
              the PDFs, review their contents to verify that all the required
              information is present and correct.
            </p>
          </section>
        </div>

        <div className="w-50-l pl4-l">
          <div className="mw6">
            <section className="lh-copy">
              <UserDataForm />
            </section>
          </div>
        </div>
      </div>
    </main>
  );
}
