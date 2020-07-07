import React from "react";
import { AliasData, AliasFieldNames } from "./types";
import moment from "moment";
import { isValidWildcard } from "./validators";
import Alias from "./Alias";
import InvalidInputs from "../../InvalidInputs";

interface Props {
  searchRecord: Function;
}

interface State {
  aliases: AliasData[];
  missingInputs: boolean;
  invalidDate: boolean;
  invalidFirstNameWildcard: boolean;
  invalidLastNameWildcard: boolean;
}

export default class SearchPanel extends React.Component<Props, State> {
  state: State = {
    aliases: [
      {
        first_name: "",
        middle_name: "",
        last_name: "",
        birth_date: "",
      },
    ],
    missingInputs: false,
    invalidDate: false,
    invalidFirstNameWildcard: false,
    invalidLastNameWildcard: false,
  };

  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.validateForm().then(() => {
      if (
        !this.state.missingInputs &&
        !this.state.invalidDate &&
        !this.state.invalidFirstNameWildcard &&
        !this.state.invalidLastNameWildcard
      ) {
        this.props.searchRecord(this.state.aliases);
      }
    });
  };

  validateForm = () => {
    return new Promise((resolve) => {
      let missingInputs: boolean = false;
      let invalidFirstNameWildcard: boolean = false;
      let invalidLastNameWildcard: boolean = false;
      for (let i: number = 0; i < this.state.aliases.length; i++) {
        if (
          this.state.aliases[i].first_name.trim().length === 0 ||
          this.state.aliases[i].last_name.trim().length === 0
        ) {
          missingInputs = true;
        }
        if (
          this.state.aliases[i].first_name.indexOf("*") > -1 &&
          !isValidWildcard(this.state.aliases[i].first_name, 2)
        ) {
          invalidFirstNameWildcard = true;
        }
        if (
          this.state.aliases[i].last_name.indexOf("*") > -1 &&
          !isValidWildcard(this.state.aliases[i].last_name, 3)
        ) {
          invalidLastNameWildcard = true;
        }
      }
      this.setState(
        {
          missingInputs,
          invalidFirstNameWildcard,
          invalidLastNameWildcard,
          invalidDate:
            moment(
              this.state.aliases[0].birth_date,
              "M/D/YYYY",
              true
            ).isValid() === false &&
            this.state.aliases[0].birth_date.length !== 0,
        },
        resolve
      );
    });
  };

  handleAliasContentChange = (
    ind: number,
    fieldName: AliasFieldNames,
    fieldValue: string
  ) => {
    let updated_aliases: AliasData[] = this.state.aliases;
    updated_aliases[ind][fieldName] = fieldValue;

    this.setState<any>({
      aliases: updated_aliases,
    });
  };

  addAlias = () => {
    const lastAlias: AliasData = this.state.aliases[
      this.state.aliases.length - 1
    ];
    let updatedAliases = this.state.aliases;
    updatedAliases.push({
      first_name: lastAlias.first_name,
      middle_name: lastAlias.middle_name,
      last_name: lastAlias.last_name,
      birth_date: lastAlias.birth_date,
    });
    this.setState({ aliases: updatedAliases });
  };

  handleAliasRemoveClick = (aliasIndex: number) => {
    let updated_aliases: AliasData[] = this.state.aliases;
    updated_aliases.splice(aliasIndex, 1);

    this.setState<any>({
      aliases: updated_aliases,
    });
  };

  public render() {
    const aliasComponents = this.state.aliases.map((alias: AliasData, i) => {
      const separator =
        i > 0 ? <hr className="bb b--black-05 mt2 mt3-ns mb3 mb4-ns" /> : null;
      return (
        <React.Fragment key={i}>
          {separator}
          <Alias
            ind={i}
            aliasData={alias}
            onChange={(fieldName: AliasFieldNames, fieldValue: string) => {
              this.handleAliasContentChange(i, fieldName, fieldValue);
            }}
            onRemoveClick={() => {
              this.handleAliasRemoveClick(i);
            }}
            hideRemoveButton={this.state.aliases.length === 1}
          />
        </React.Fragment>
      );
    });
    return (
      <>
        <h1 className="visually-hidden">Record Search</h1>
        <section className="cf mt4 mb3 pa4 bg-white shadow br3">
          <form className="mw7 center" onSubmit={this.handleSubmit} noValidate>
            {aliasComponents}
            <div className="flex">
              {
                // Row containing The +Alias and Search buttons.
              }
              <button
                className="w4 tc br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pv3 ph3 mr2"
                onClick={this.addAlias}
                type="button"
              >
                <i aria-hidden={"true"} className="fas fa-plus-circle pr1"></i>
                Alias
              </button>
              <button
                className="br2 bg-blue white bg-animate hover-bg-dark-blue db w-100 tc pv3 btn--search"
                type="submit"
              >
                <i aria-hidden="true" className="fas fa-search pr2"></i>
                <span className="fw7">Search</span>
              </button>
            </div>
            <InvalidInputs
              conditions={[
                this.state.missingInputs,
                this.state.invalidDate,
                this.state.invalidFirstNameWildcard,
                this.state.invalidLastNameWildcard,
              ]}
              contents={[
                <span>First and last name are required.</span>,
                <span>The date format must be MM/DD/YYYY.</span>,
                <span>
                  A wildcard in First Name field must be at the end and follow
                  at least one letter.
                </span>,
                <span>
                  A wildcard in the Last Name field must be at the end and
                  follow at least two letters.
                </span>,
              ]}
            />
          </form>
        </section>
      </>
    );
  }
}
