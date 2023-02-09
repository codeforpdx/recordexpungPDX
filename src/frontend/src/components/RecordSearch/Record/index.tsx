import React from "react";
import { connect } from "react-redux";
import { HashLink as Link } from "react-router-hash-link";
import Cases from "./Cases";
import Case from "./Case";
import RecordSummary from "./RecordSummary";
import { RecordData, CaseData } from "./types";
import AddButton from "./AddButton";
import { startEditing, doneEditing } from "../../../redux/search/actions";
import { AppState } from "../../../redux/store";
import { convertCaseNumberIntoLinks } from "./util";

interface Props {
  record?: RecordData;
  editingRecord: boolean;
  startEditing: Function;
  doneEditing: Function;
}

interface State {
  enableEditing: boolean;
  addingNewCase: boolean;
  blankCase?: CaseData;
  nextNewCaseNum: number;
}

class Record extends React.Component<Props, State> {
  state: State = {
    enableEditing: false,
    addingNewCase: false,
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
      district_attorney_number: "",
      edit_status: "ADD",
    };
  }

  handleAddCaseClick = () => {
    this.props.startEditing();
    this.setState({
      addingNewCase: true,
    });
  };

  render() {
    const errors =
      this.props.record && this.props.record.errors
        ? this.props.record.errors.map(
            (errorMessage: string, errorIndex: number) => {
              const id = "record_error_" + errorIndex;
              const errorMessageHTML = convertCaseNumberIntoLinks(errorMessage);
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
                  this.props.startEditing();
                }}
                whenDoneEditing={() => {
                  this.props.doneEditing();
                  this.setState({
                    addingNewCase: false,
                    nextNewCaseNum: this.state.nextNewCaseNum + 1,
                  });
                }}
                case={this.createNextBlankCase()}
                editing={true}
                isNewCase={true}
                showEditButtons={
                  !this.props.editingRecord && this.state.enableEditing
                }
                customElementId="new-case"
              />
            </div>
          )}
          <div className="tr">
            {this.state.enableEditing ? (
              !this.props.editingRecord && (
                <>
                  <AddButton
                    onClick={this.handleAddCaseClick}
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
                    this.setState({ enableEditing: true });
                  }}
                >
                  Enable Editing
                </button>{" "}
                <Link
                  to="/manual#editing"
                  className=" gray link hover-blue underline"
                >
                  <i
                    aria-hidden="true"
                    className="fas fa-question-circle link hover-dark-blue gray"
                  ></i>
                  <span className="visually-hidden">Editing Help</span>
                </Link>
              </>
            )}
          </div>

          {this.props.record && this.props.record.cases && (
            <Cases
              cases={this.props.record.cases}
              showEditButtons={
                !this.props.editingRecord && this.state.enableEditing
              }
              whenEditing={() => {
                this.props.startEditing();
              }}
              whenDoneEditing={() => {
                this.props.doneEditing();
              }}
            />
          )}
        </section>
      </>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    editingRecord: state.search.editingRecord,
  };
};

export default connect(mapStateToProps, {
  startEditing,
  doneEditing,
})(Record);
