import React, { useState } from "react";
import { AliasData, AliasFieldNames } from "./types";
import { useAppSelector, useAppDispatch } from "../../../redux/hooks";
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
          buttonClassName="w4 tc br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pv3 ph3 mr2"
          iconClassName="fa-plus-circle pr1"
          onClick={() => dispatch(addSearchFormAlias())}
        />

        <IconButton
          styling="blank"
          type="submit"
          displayText="Search"
          buttonClassName="fw7 br2 bg-blue white bg-animate hover-bg-dark-blue db w-100 tc pv3 btn--search"
          iconClassName="fa-search pr2"
        />
      </div>

      <InvalidInputs contents={errorMessages} />
    </form>
  );
}
