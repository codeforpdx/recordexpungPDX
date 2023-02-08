import React, { useState } from "react";
import { useAppSelector } from "../../../redux/hooks";
import { selectStats } from "../../../redux/statsSlice";
import useRadioGroup from "../../../hooks/useRadioGroup";
import SearchPanel from "../SearchPanel";
import Status from "../Status";
import RecordSummary from "../Record/RecordSummary";
import Record from "../Record";
import Assumptions from "../Assumptions";
import { convertCaseNumberIntoLinks } from "../Record/util";
import ViewOptions from "../expandedView/ViewOptions";
import CasesSummary from "../expandedView/CasesSummary";
import Stats from "../expandedView/SummaryStats";

function ErrorMessage({ message, idx }: { message: string; idx: number }) {
  const id = "record_error_" + idx;
  return (
    <p role="status" id={id} key={id} className="bg-washed-red mv3 pa3 br3 fw6">
      {convertCaseNumberIntoLinks(message)}
    </p>
  );
}

export default function Layout({
  topSection,
}: {
  topSection?: React.ReactElement;
}) {
  const record = useAppSelector((state) => state.search.record);
  const stats = useAppSelector(selectStats);
  const [showColor, setShowColor] = useState(true);
  const { selectedRadioValue, ...radioGroupProps } = useRadioGroup({
    label: "Summary overview sort options",
    initialValue: "Default",
  });
  const radioGroupOptions = ["Default", "Expanded"];
  const isExpandedView = selectedRadioValue === "Expanded";
  const panelClass = "bg-white shadow br3 ";
  const panelHeading = "f5 fw7 tc mt2 mb3";

  return (
    <main>
      <div className="mw8 center f6 f5-l ph2">
        {topSection}
        {!topSection && <h1 className="visually-hidden">Record Search</h1>}

        <section className={panelClass + "pa4 mt3"}>
          <SearchPanel />
        </section>

        <section className={panelClass + "mv2 ph3 pv1"}>
          <div className="flex flex-wrap items-center">
            <div className="f5 fw7 mr4">View Options</div>

            <ViewOptions
              optionLabels={radioGroupOptions}
              radioGroupProps={radioGroupProps}
              showColor={showColor}
              isExpandedView={isExpandedView}
              handleShowColorChange={() => setShowColor(!showColor)}
            />
          </div>
        </section>

        <Status />

        {record?.errors?.map((message: string, idx: number) => (
          <ErrorMessage key={idx} message={message} idx={idx} />
        ))}

        {!isExpandedView && (
          <>
            <section>
              <RecordSummary />
              <Record />
            </section>

            <Assumptions />
          </>
        )}
      </div>

      {isExpandedView && stats.totalCases > 0 && (
        <section className="flex-l mh2">
          <div className={panelClass + "w-70-l f6 ph4 "}>
            <h2 className={panelHeading}>Summary</h2>
            <CasesSummary showColor={showColor} />
          </div>

          <div className={panelClass + "w-30-l ml2-l pl3 pb2"}>
            <h2 className={panelHeading}>Counts</h2>
            <Stats showColor={showColor} />
          </div>
        </section>
      )}
    </main>
  );
}
