import React, { useState } from "react";
import { useAppSelector } from "../../../../redux/hooks";
import { useAppDispatch } from "../../../../redux/hooks";
import {
  startLoadingSummary,
  selectSummaryIsLoading,
} from "../../../../redux/summarySlice";
import { buildAndSendDownloadPdfRequest } from "../../../../redux/search/actions";
import history from "../../../../service/history";
import ChargesList from "./ChargesList";
import CountyFines from "./CountyFines";
import IconButton from "../../../common/IconButton";

export default function RecordSummary() {
  const dispatch = useAppDispatch();
  const record = useAppSelector((state) => state.search.record);
  const summaryIsLoading = useAppSelector(selectSummaryIsLoading);
  const [canGenerateForms, setCanGenerateForms] = useState(true);

  if (!record || !record.summary) return <></>;

  const summary = record.summary;

  const {
    total_cases: totalCases,
    total_charges: totalCharges,
    charges_grouped_by_eligibility_and_case: groupedCharges,
    ...fines
  } = summary;

  const handleGenerateFormsClick = () => {
    if (
      groupedCharges?.some(
        (x) =>
          x[0] === "Eligible Now" ||
          x[0] === "Eligible on case with Ineligible charge"
      )
    ) {
      history.push("/fill-expungement-forms");
    } else {
      setCanGenerateForms(false);
    }
  };

  const handleDownloadSummaryClick = () => {
    dispatch(startLoadingSummary());
    dispatch(buildAndSendDownloadPdfRequest);
  };

  return (
    <div className="bg-white shadow br3 mb3 ph3 pb3">
      <div className="flex flex-wrap justify-end mb1">
        <h2 className="f5 fw7 mv3 mr-auto">Search Summary</h2>

        {!canGenerateForms && (
          <span className="bg-washed-red mv2 pa2 br3 fw6" role="alert">
            There must be eligible charges to generate paperwork.{" "}
            <IconButton
              styling="link"
              iconClassName="fa-circle-xmark gray"
              hiddenText="Close"
              onClick={() => {
                setCanGenerateForms(true);
              }}
            />
          </span>
        )}

        <IconButton
          styling="link"
          buttonClassName="hover-blue"
          iconClassName="fa-bolt pr2"
          displayText="Generate Paperwork"
          onClick={handleGenerateFormsClick}
        />

        <IconButton
          styling="link"
          buttonClassName={
            "hover-blue " + (summaryIsLoading ? "loading-btn" : "")
          }
          iconClassName="fa-download pr2"
          displayText="Summary PDF"
          onClick={handleDownloadSummaryClick}
        />
      </div>

      <div className="flex-ns flex-wrap">
        <div className="w-100 w-two-thirds-l">
          <h3 className="bt b--light-gray pt2 mb3">
            <span className="fw7">Cases</span> ({totalCases})
          </h3>

          <ChargesList
            chargesGroupedByEligibilityAndCase={groupedCharges}
            totalCharges={totalCharges}
          />
        </div>

        <div className="w-100 w-33-l ph3-l mb3">
          <CountyFines {...fines} />
        </div>
      </div>
    </div>
  );
}
