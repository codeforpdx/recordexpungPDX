import React, { useState } from "react";
import { RecordData } from "../types";
import { useAppSelector } from "../../../../redux/hooks";
import { downloadPdf } from "../../../../redux/search/actions";
import history from "../../../../service/history";
import useRadioGroup from "../../../../hooks/useRadioGroup";
import RadioGroup from "../../../common/RadioGroup";
import ChargesList from "./ChargesList";
import CasesList from "./CasesList";
import CountyFines from "./CountyFines";
import { IconButton } from "../../../common/IconButton";

interface Props {
  record: RecordData;
}

export default function RecordSummary({ record }: Props) {
  const loadingPdf = useAppSelector((state) => state.search.loadingPdf);
  const [canGenerateForms, setCanGenerateForms] = useState(true);
  const { selectedRadioValue, ...radioGroupProps } = useRadioGroup({
    label: "Summary overview sort options",
    initialValue: "Charges",
  });
  const cases = record.cases;
  const summary = record.summary;

  if (!summary) return <></>;

  const {
    total_cases: totalCases,
    total_charges: totalCharges,
    charges_grouped_by_eligibility_and_case: groupedCharges,
    ...fines
  } = summary;

  const handleGenerateFormsClick = () => {
    if (groupedCharges["Eligible Now"]?.length > 0) {
      history.push("/fill-expungement-forms");
    } else {
      setCanGenerateForms(false);
    }
  };

  return (
    <div className="bg-white shadow br3 mb3 ph3 pb3">
      <div className="flex flex-wrap justify-end mb1">
        <div className="flex flex-wrap items-center mv1 mr-auto">
          <h2 className="f5 fw7 mr3">Search Summary</h2>

          <RadioGroup
            className="flex flex-wrap radio radio-sm ml1"
            optionLabels={["Charges", "Cases"]}
            radioGroupProps={radioGroupProps}
          />
        </div>

        {!canGenerateForms && (
          <span className="bg-washed-red mv2 pa2 br3 fw6" role="alert">
            There must be eligible charges to generate paperwork.{" "}
            <IconButton
              iconClassName="fa-circle-xmark gray"
              hiddenText="Close"
              onClick={() => {
                setCanGenerateForms(true);
              }}
            />
          </span>
        )}

        <IconButton
          iconClassName="fa-bolt pr2"
          displayText="Generate Paperwork"
          onClick={handleGenerateFormsClick}
        />

        <IconButton
          buttonClassName={loadingPdf ? "loading-btn" : ""}
          iconClassName="fa-download pr2"
          displayText="Summary PDF"
          onClick={() => {
            downloadPdf();
          }}
        />
      </div>

      <div className="flex-ns flex-wrap">
        <div className="w-100 w-two-thirds-l">
          <h3 className="bt b--light-gray pt2 mb3">
            <span className="fw7">Cases</span> ({totalCases})
          </h3>

          {selectedRadioValue === "Charges" ? (
            <ChargesList
              chargesGroupedByEligibilityAndCase={groupedCharges}
              totalCharges={totalCharges}
            />
          ) : (
            <CasesList cases={cases} />
          )}
        </div>

        <div className="w-100 w-33-l ph3-l mb3">
          <CountyFines {...fines} />
        </div>
      </div>
    </div>
  );
}
