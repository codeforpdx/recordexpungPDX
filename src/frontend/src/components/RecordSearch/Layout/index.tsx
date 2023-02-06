import React from "react";
import { useAppSelector } from "../../../redux/hooks";
import SearchPanel from "../SearchPanel";
import Status from "../Status";
import RecordSummary from "../Record/RecordSummary";
import Record from "../Record";
import Assumptions from "../Assumptions";
import { convertCaseNumberIntoLinks } from "../Record/util";

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

  return (
    <main className="mw8 center f6 f5-l ph2">
      {topSection}
      {!topSection && <h1 className="visually-hidden">Record Search</h1>}

      <section className="cf mt4 mb3 pa4 bg-white shadow br3">
        <SearchPanel />
      </section>

      <Status />

      {record?.errors?.map((message: string, idx: number) => (
        <ErrorMessage key={idx} message={message} idx={idx} />
      ))}

      <section>
        <RecordSummary />
        <Record />
      </section>

      <Assumptions />
    </main>
  );
}
