import React, { useEffect, useState } from "react";
import moment from "moment";
import { AliasData, AliasFieldNames } from "./types";
import { useAppSelector, useAppDispatch } from "../../../redux/hooks";
import {
  selectSearchFormAliases,
  selectSearchFormDate,
  setSearchFormDate,
  updateSearchFormAlias,
  addSearchFormAlias,
  removeSearchFormAlias,
} from "../../../redux/searchFormSlice";
import {
  isValidOptionalWildcard,
  areAnyBlank,
  isValidOptionalDate,
} from "./validators";
import { searchRecord } from "../../../redux/search/actions";
import Alias from "./Alias";
import Field from "./Field";
import IconButton from "../../common/IconButton";
import InvalidInputs from "../../InvalidInputs";

export default function SearchPanel() {
  const dispatch = useAppDispatch();
  const aliases = useAppSelector(selectSearchFormAliases);
  const date = useAppSelector(selectSearchFormDate);
  const [errorMessages, setErorrMessages] = useState<string[]>([]);

  useEffect(() => {
    if (date === "") dispatch(setSearchFormDate(moment().format("M/D/YYYY")));
  }, [date, dispatch]);

  // A map of error messages and validators that return true if messages should be shown
  const validators = {
    "First and last name are required.": (alias: AliasData) =>
      areAnyBlank(alias.first_name, alias.last_name),

    "The date format must be MM/DD/YYYY.": (alias: AliasData) =>
      !isValidOptionalDate(alias.birth_date),

    "A wildcard in First Name field must be at the end and follow at least one letter.":
      (alias: AliasData) => !isValidOptionalWildcard(alias.first_name, 2),

    "A wildcard in the Last Name field must be at the end and follow at least two letters.":
      (alias: AliasData) => !isValidOptionalWildcard(alias.last_name, 3),
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    let messages = Object.entries(validators).reduce(
      (errors, [message, isInvalid]) => {
        if (aliases.some(isInvalid)) errors.push(message);
        return errors;
      },
      [] as string[]
    );

    setErorrMessages(messages);

    if (messages.length === 0) dispatch(searchRecord());
  };

  return (
    <form className="mw7 center" onSubmit={handleSubmit} noValidate>
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
