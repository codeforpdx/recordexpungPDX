import React, { useState } from "react";
import { useAppSelector } from "../../../redux/hooks";
import { useStartEditing, useDoneEditing } from "../../../redux/search/actions";
import { convertCaseNumberIntoLinks } from "./util";
import RecordSummary from "./RecordSummary";
import Cases from "./Cases";
import Case from "./Case";
import AddButton from "./AddButton";
import Link from "../../common/Link";

function ErrorMessage({ message, idx }: { message: string; idx: number }) {
  const id = "record_error_" + idx;
  return (
    <p role="status" id={id} key={id} className="bg-washed-red mv3 pa3 br3 fw6">
      {convertCaseNumberIntoLinks(message)}
    </p>
  );
}

export default function Record() {
  const startEditing = useStartEditing();
  const doneEditing = useDoneEditing();
  const record = useAppSelector((state) => state.search.record);
  const editingRecord = useAppSelector((state) => state.search.editingRecord);
  const [enableEditing, setEnableEditing] = useState(false);
  const [addingNewCase, setAddingNewCase] = useState(false);
  const [nextNewCaseNum, setNextNewCaseNum] = useState(1);

  const createNextBlankCase = () => {
    return {
      balance_due: 0,
      birth_year: 0,
      case_detail_link: "",
      case_number: "CASE-" + ("000" + nextNewCaseNum).slice(-4),
      charges: [],
      citation_number: "",
      current_status: "",
      date: "",
      location: "",
      name: "",
      violation_type: "",
      district_attorney_number: "",
      edit_status: "ADD",
    };
  };

  const handleAddCaseClick = () => {
    startEditing();
    setAddingNewCase(true);
  };

  return (
    <>
      {record?.errors?.map((message: string, idx: number) => (
        <ErrorMessage key={idx} message={message} idx={idx} />
      ))}

      <section>
        <RecordSummary />

        {addingNewCase && (
          <div className="bg-gray-blue-2 shadow br3 overflow-auto mb3">
            <Case
              whenEditing={() => {
                startEditing();
              }}
              whenDoneEditing={() => {
                doneEditing();
                setAddingNewCase(false);
                setNextNewCaseNum(nextNewCaseNum + 1);
              }}
              case={createNextBlankCase()}
              editing={true}
              isNewCase={true}
              showEditButtons={!editingRecord && enableEditing}
              customElementId="new-case"
            />
          </div>
        )}
        <div className="tr">
          {enableEditing ? (
            !editingRecord && (
              <>
                <AddButton
                  onClick={handleAddCaseClick}
                  actionName={"Add"}
                  text={"Case"}
                />
                <div className="pb3" />
              </>
            )
          ) : (
            <>
              <button
                className="inline-flex bg-white f6 fw5 br2 ba b--black-10 mid-gray link hover-blue pv1 ph2 mb3"
                onClick={() => {
                  setEnableEditing(true);
                }}
              >
                Enable Editing
              </button>{" "}
              <Link
                to="/manual#editing"
                className=" gray link hover-blue underline"
                iconClassName="fas fa-question-circle link hover-dark-blue gray"
                hiddenText="Editing Help"
              />
            </>
          )}
        </div>

        {record?.cases && (
          <Cases
            cases={record.cases}
            showEditButtons={!editingRecord && enableEditing}
            whenEditing={() => {
              startEditing();
            }}
            whenDoneEditing={() => {
              doneEditing();
            }}
          />
        )}
      </section>
    </>
  );
}
