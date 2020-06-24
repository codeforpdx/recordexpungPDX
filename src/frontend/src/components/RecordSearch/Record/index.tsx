import React from "react";
import Cases from "./Cases";
import Case from "./Case";
import RecordSummary from "./RecordSummary";
import { RecordData, CaseData } from "./types";
import AddButton from "./AddButton";

interface Props {
  record?: RecordData;
}

interface State {
  editingRecord: boolean;
  addingNewCase: boolean;
  blankCase?: CaseData;
  nextNewCaseNum: number;
}

export default class Record extends React.Component<Props, State> {
  state: State = {
    addingNewCase: false,
    editingRecord: false,
    nextNewCaseNum: 1,
  };

  createNextBlankCase(): CaseData {
    return {
      balance_due: 0,
      birth_year: 0,
      case_detail_link: "",
      case_number: "CASE-" + ("000" + this.state.nextNewCaseNum).slice(-4),
      charges: [],
      citation_number: "",
      current_status: "",
      date: "",
      location: "",
      name: "",
      violation_type: "",
      edit_status: "ADD",
    };
  }

  handleAddCaseClick = () => {
    this.setState({
      addingNewCase: true,
      editingRecord: true,
    });
  };

  render() {
    const errors =
      this.props.record && this.props.record.errors
        ? this.props.record.errors.map(
            (errorMessage: string, errorIndex: number) => {
              const id = "record_error_" + errorIndex;

              const errorMessageArray = errorMessage.split(/(\[.*?\])/g);
              const errorMessageHTML = errorMessageArray.map(function (
                element
              ) {
                if (element.match(/^\[.*\]$/)) {
                  const caseNumber = element.slice(1, -1);
                  return (
                    <a
                      className="underline"
                      href={"#" + caseNumber}
                      key={caseNumber}
                    >
                      {caseNumber}
                    </a>
                  );
                } else {
                  return element;
                }
              });
              return (
                <p
                  role="status"
                  id={id}
                  key={id}
                  className="bg-washed-red mv3 pa3 br3 fw6"
                >
                  {errorMessageHTML}
                </p>
              );
            }
          )
        : null;

    return (
      <>
        {errors}
        <section>
          {this.props.record && this.props.record.summary && (
            <RecordSummary summary={this.props.record.summary} />
          )}
          {this.state.addingNewCase && (
            <div className="bg-gray-blue-2 shadow br3 overflow-auto mb3">
              <Case
                whenEditing={() => {
                  this.setState({ editingRecord: true });
                }}
                whenDoneEditing={() => {
                  this.setState({
                    addingNewCase: false,
                    editingRecord: false,
                    nextNewCaseNum: this.state.nextNewCaseNum + 1,
                  });
                }}
                case={this.createNextBlankCase()}
                editing={true}
                isNewCase={true}
                editingRecord={this.state.editingRecord}
              />
            </div>
          )}
          {!this.state.editingRecord && (
            <div className="tr pb3">
              <AddButton
                onClick={this.handleAddCaseClick}
                actionName={"Add"}
                text={"Case"}
                ariaControls="" //Can't cleanly get the new case element id atm.
              />
            </div>
          )}
          {this.props.record && this.props.record.cases && (
            <Cases
              cases={this.props.record.cases}
              editingRecord={this.state.editingRecord}
              whenEditing={() => {
                this.setState({ editingRecord: true });
              }}
              whenDoneEditing={() => {
                this.setState({ editingRecord: false });
              }}
            />
          )}
        </section>
      </>
    );
  }
}
