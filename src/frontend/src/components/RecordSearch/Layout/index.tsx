import React, { useState, useEffect } from "react";
import { useAppSelector, useAppDispatch } from "../../../redux/hooks";
import { selectStats } from "../../../redux/statsSlice";
import { dismissAllRestitution } from "../../../redux/search/actions";
import useRadioGroup from "../../../hooks/useRadioGroup";
import setUpScrollSpy from "../ExpandedView/setupScrollSpy";
import SearchPanel from "../SearchPanel";
import Status from "../Status";
import RecordSummary from "../Record/RecordSummary";
import Record from "../Record";
import Assumptions from "../Assumptions";
import { convertCaseNumberIntoLinks } from "../Record/util";
import ViewOptions from "../ExpandedView/ViewOptions";
import ExpandedView from "../ExpandedView";

function ErrorMessage({ message, idx }: { message: string; idx: number }) {
  const id = "record_error_" + idx;
  return (
    <p role="status" id={id} key={id} className="bg-washed-red mv3 pa3 br3 fw6">
      {convertCaseNumberIntoLinks(message)}
    </p>
  );
}

function RestitutionBanner() {
  const dispatch = useAppDispatch();
  const record = useAppSelector((state) => state.search.record);
  const cases = record?.cases || [];
  const casesWithRestitution = cases.filter((c) => c.restitution === true);

  if (casesWithRestitution.length === 0) return null;

  return (
    <p role="status" className="bg-washed-red mv3 pa3 br3 fw6">
      OECI records for cases under "Ineligible if Restitution Owed" mention
      Restitution. If no Restitution is owed on any case, you may{" "}
      <button
        className="bg-navy white fw6 br2 pv1 ph2 pointer nowrap"
        onClick={() => dispatch(dismissAllRestitution(casesWithRestitution))}
      >
        Dismiss All
      </button>
    </p>
  );
}

export const mainWrapper = "mw8 center f6 f5-l ";
export const panelClass = "bg-white shadow br3 ";
export const singlePanelClass = "pa4 mt3 ";

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

  useEffect(setUpScrollSpy, [isExpandedView, record]);

  useEffect(() => {
    document.querySelector("html")?.classList.toggle("smooth-scroll");
    return () => {
      document.querySelector("html")?.classList.toggle("smooth-scroll");
    };
  });

  return (
    <main>
      <div className={mainWrapper + "ph2"}>
        {topSection}
        {!topSection && <h1 className="visually-hidden">Record Search</h1>}

        <section className={panelClass + singlePanelClass}>
          <SearchPanel />
        </section>

        <section className={panelClass + "mv3 ph3 pv1"}>
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

        <RestitutionBanner />

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
        <ExpandedView showColor={showColor} />
      )}
    </main>
  );
}
