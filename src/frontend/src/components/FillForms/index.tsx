import React from "react";
import UserDataForm from "./UserDataForm";
import { HashLink as Link } from "react-router-hash-link";
import setupPage from "../../service/setupPage";
import { useAppSelector } from "../../redux/hooks";
import {
  countyFilingData,
  CountyFilingInfo,
} from "../../data/countyFilingData";

function CountyFilingNotes({ county }: { county: string }) {
  const info: CountyFilingInfo | undefined = countyFilingData[county];
  const waitMonths = info?.waitMonths ?? 4;
  const notes = info?.notes ?? [];

  if (notes.length === 0) {
    return (
      <li className="mb2">
        <strong>{county}</strong> estimated response time: {waitMonths} months
      </li>
    );
  }

  return (
    <li className="mb2">
      <strong>{county}:</strong>
      <ul className="pl3 mt1">
        <li>Estimated response time: {waitMonths} months</li>
        {notes.map((note, idx) => (
          <li key={idx}>{note}</li>
        ))}
      </ul>
    </li>
  );
}

function PerCountyFilingNotes() {
  const record = useAppSelector((state) => state.search.record);
  const cases = record?.cases || [];

  // Get unique counties from cases with eligible charges
  const countiesWithEligibleCharges = new Set<string>();
  cases.forEach((c) => {
    const hasEligibleCharge = c.charges.some((charge) => {
      const status = charge.expungement_result?.charge_eligibility?.status;
      return status === "Eligible Now" || status === "Will Be Eligible";
    });
    if (hasEligibleCharge && c.location) {
      // Strip " County" suffix for consistent lookup
      const countyName = c.location.replace(/ County$/, "");
      countiesWithEligibleCharges.add(countyName);
    }
  });

  const counties = Array.from(countiesWithEligibleCharges).sort();

  if (counties.length === 0) {
    return null;
  }

  // Separate counties with custom info from those with defaults
  const countiesWithCustomInfo: string[] = [];
  const countiesWithDefaults: string[] = [];

  counties.forEach((county) => {
    const info = countyFilingData[county];
    const hasCustomWaitTime = info?.waitMonths !== undefined && info.waitMonths !== 4;
    const hasNotes = info?.notes && info.notes.length > 0;
    if (hasCustomWaitTime || hasNotes) {
      countiesWithCustomInfo.push(county);
    } else {
      countiesWithDefaults.push(county);
    }
  });

  return (
    <section className="mw6 lh-copy mb4">
      <h2 className="f4 fw7 mb3">Notes</h2>
      <ul className="pl3">
        {countiesWithCustomInfo.map((county) => (
          <CountyFilingNotes key={county} county={county} />
        ))}
        {countiesWithDefaults.length > 0 && (
          <li className="mb2">
            <strong>All other counties</strong> estimated response time: 4 months
          </li>
        )}
        <li className="mb2">
          See more at{" "}
          <Link to="/community" className="link hover-dark-blue bb">
            Community Page
          </Link>
        </li>
      </ul>
    </section>
  );
}

export default function FillFormsIndex() {
  setupPage("Generate Expungement Forms");

  return (
    <main className="mw8 center f6 f5-l ph3 pt4 pb6">
      <h1 className="f3 f2-l fw9 mb4">Generate Expungement Forms</h1>
      <div className="flex-l pt2">
        <div className="w-50-l pr4-l mb4">
          <PerCountyFilingNotes />

          <section className="mw6 lh-copy">
            <h2 className="f4 fw7 mb3">Filing Instructions</h2>
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
