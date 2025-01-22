import React, { useState } from "react";
import { useAppSelector, useAppDispatch } from "../../../redux/hooks";
import {
  startEditing,
  doneEditing,
  selectIsEditing,
} from "../../../redux/editingSlice";
import Cases from "./Cases";
import Case from "./Case";
import AddButton from "./AddButton";
import Link from "../../common/Link";

export default function Record() {
  const dispatch = useAppDispatch();
  const record = useAppSelector((state) => state.search.record);
  const isEditing = useAppSelector(selectIsEditing);
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
      restitution: false,
      edit_status: "ADD",
    };
  };

  return (
    <>
      {addingNewCase && (
        <div className="bg-gray-blue-2 shadow br3 overflow-auto mb3">
          <Case
            whenEditing={() => {
              dispatch(startEditing());
            }}
            whenDoneEditing={() => {
              dispatch(doneEditing());
              setAddingNewCase(false);
              setNextNewCaseNum(nextNewCaseNum + 1);
            }}
            case={createNextBlankCase()}
            editing={true}
            isNewCase={true}
            showEditButtons={!isEditing && enableEditing}
            customElementId="new-case"
          />
        </div>
      )}
      <div className="tr">
        {enableEditing ? (
          !isEditing && (
            <>
              <AddButton
                onClick={() => {
                  dispatch(startEditing());
                  setAddingNewCase(true);
                }}
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
              iconClassName="fas fa-question-circle"
              hiddenText="Editing Help"
            />
          </>
        )}
      </div>

      {record?.cases && (
        <Cases
          cases={record.cases}
          showEditButtons={!isEditing && enableEditing}
          whenEditing={() => {
            dispatch(startEditing());
          }}
          whenDoneEditing={() => {
            dispatch(doneEditing());
          }}
        />
      )}
    </>
  );
}
