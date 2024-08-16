import React, { useState } from "react";
import { AliasData, AliasFieldNames } from "./types";
import { useAppSelector, useAppDispatch } from "../../../redux/hooks";
import { clearAllData } from "../../../redux/store";
import {
  selectSearchFormValues,
  setSearchFormDate,
  updateSearchFormAlias,
  addSearchFormAlias,
  removeSearchFormAlias,
} from "../../../redux/searchFormSlice";
import {
  isPresent,
  isValidOptionalDate,
  isValidOptionalWildcard,
  validate,
} from "../../../service/validators";
import { searchRecord } from "../../../redux/search/actions";
import Alias from "./Alias";
import Field from "./Field";
import IconButton from "../../common/IconButton";
import InvalidInputs from "../../InvalidInputs";

export default function SearchPanel() {
  const dispatch = useAppDispatch();
  const { aliases, date } = useAppSelector(selectSearchFormValues);
  const [errorMessages, setErrorMessages] = useState<string[]>([]);
  const validators = [
    isPresent("first_name", "First name is required."),
    isPresent("last_name", "Last name is required."),
    isValidOptionalDate("birth_date", "The date format must be MM/DD/YYYY.", {
      indexes: [0],
    }),
    isValidOptionalWildcard(
      "first_name",
      "A wildcard in First Name field must be at the end and follow at least one letter."
    ),
    isValidOptionalWildcard(
      "last_name",
      "A wildcard in the Last Name field must be at the end and follow at least two letters.",
      { minLength: 3 }
    ),
  ];

  const handleStartOverClick = () => {
    dispatch(clearAllData());
    window.scrollTo(0, 0);
  };

  return (
    <form
      className="mw7 center"
      onSubmit={(e: React.FormEvent) => {
        e.preventDefault();

        validate(aliases, validators, setErrorMessages, () =>
          dispatch(searchRecord())
        );
      }}
      noValidate
    >
      <div className="flex">
        <Field
          coda="mm/dd/yyyy"
          name="today"
          label="Expunge Date"
          content={date}
          divMarkup="pl2-r"
          onChange={(newDate: string) => {
            dispatch(setSearchFormDate(newDate));
          }}
          required={true}
          errorMessage="today_msg"
        />
      </div>

      {aliases.map((alias: AliasData, index: number) => {
        console.log(index);
        return (
          <React.Fragment key={index}>
            {index > 0 && (
              <hr className="bb b--black-05 mt2 mt3-ns mb3 mb4-ns" />
            )}
            <Alias
              ind={index}
              aliasData={alias}
              onChange={(attribute: AliasFieldNames, value: string) => {
                dispatch(updateSearchFormAlias({ index, attribute, value }));
              }}
              onRemoveClick={() => {
                dispatch(removeSearchFormAlias(index));
              }}
              hideRemoveButton={aliases.length === 1}
            />
          </React.Fragment>
        );
      })}

      <div className="flex">
        <IconButton
          styling="blank"
          displayText="Alias"
          buttonClassName="w4 tc br2 bg-gray-blue-2 link hover-dark-blue mid-gray w-20 tc fw5 pv3 ph3 mr2"
          iconClassName="fa-plus-circle pr1"
          onClick={() => dispatch(addSearchFormAlias())}
        />

        <IconButton
          styling="blank"
          type="submit"
          displayText="Search"
          buttonClassName="fw7 br2 bg-blue white bg-animate hover-bg-dark-blue db w-90 tc fw5 pv3 ph3 btn--search mr2"
          iconClassName="fa-search pr2"
        />

        <IconButton
          styling="button"
          buttonClassName="w4 tc br2 bg-gray-blue-2 hover-dark-blue mid-gray w-30 tc fw5 pv3 ph3"
          iconClassName="fa-arrow-up pr2"
          displayText="Clear Data"
          onClick={handleStartOverClick}
        />

      </div>

      <InvalidInputs contents={errorMessages} />
    </form>
  );
}
