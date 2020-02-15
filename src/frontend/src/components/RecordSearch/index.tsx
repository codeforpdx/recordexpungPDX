import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { SystemState } from '../../redux/system/types';
import { AliasType, AliasFieldNames } from './types';
import moment from 'moment';
import Alias from './Alias';

interface Props {
  system: SystemState;
  fetchRecords: Function;
}

interface State {
  aliases: AliasType[];
  missingInputs: null | boolean;
  invalidDate: boolean;
}

class RecordSearch extends React.Component<Props, State> {
  state: State = {
    aliases: [
      {
        first_name: '',
        middle_name: '',
        last_name: '',
        birth_date: '',
      },
    ],
    missingInputs: null,
    invalidDate: false
  };

  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.validateForm().then(() => {
      if (
        !this.state.missingInputs &&
        !this.state.invalidDate
      ) {
        this.props.fetchRecords( this.state.aliases);
      }
    });
  };

  validateForm = () => {
    return new Promise(resolve => {
      let missingInputs : boolean = false;
        for (let i : number = 0; i < this.state.aliases.length; i++) {
          if (this.state.aliases[i].first_name.trim().length === 0 ||
              this.state.aliases[i].last_name.trim().length === 0 ) {
            missingInputs = true;
            break;
          }
        }
      this.setState(
        {
          missingInputs: missingInputs,
          invalidDate:
            moment(this.state.aliases[0].birth_date, 'M/D/YYYY', true).isValid() ===
              false && this.state.aliases[0].birth_date.length !== 0
        },
        resolve
      );
    });
  };

  handleAliasContentChange = (ind: number, fieldName: AliasFieldNames, fieldValue: string) => {
    let updated_aliases: AliasType[] = this.state.aliases;
    updated_aliases[ind][fieldName] = fieldValue;

    this.setState<any>({
      aliases: updated_aliases
    });

  }

  addAlias = () => {
    let updatedAliases = this.state.aliases;
    updatedAliases.push({
        first_name: '',
        middle_name: '',
        last_name: '',
        birth_date: ''
      })
    this.setState({aliases: updatedAliases})
  }

  handleAliasRemoveClick = (aliasIndex : number) => {
    let updated_aliases: AliasType[] = this.state.aliases;
    updated_aliases.splice(aliasIndex, 1);

    this.setState<any>({
      aliases: updated_aliases
    });
  }

  public render() {
    const aliasComponents = this.state.aliases.map((alias: AliasType, i) => {
      const separator = ( i > 0 ? <hr className="bb b--black-05 mt2 mt3-ns mb3 mb4-ns" /> : null );
      return (
        <>
        {separator}
        <Alias
          ind={i}
          aliasData={alias}
          onChange={
            (fieldName: AliasFieldNames, fieldValue: string) => {
              this.handleAliasContentChange(i, fieldName, fieldValue)
            }
          }
          onRemoveClick={
            () => {
              this.handleAliasRemoveClick(i)
            }
          }
          hideRemoveButton={this.state.aliases.length === 1}
          key={"alias" + i}
        />
        </>
      );
    });
    return (
      <div>
        <h1 className="f4 fw6 tc mv4">Record Search</h1>
        <section className="cf mt4 mb3 pa4 bg-white shadow br3">
          <form className="mw7 center" onSubmit={this.handleSubmit} noValidate>
              {aliasComponents}
              <div className="flex">
              {  // Row containing The +Alias and Search buttons.
              }
                <button
                  className="w4 tc br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pv3 ph3 mr2"
                  onClick={() => {this.addAlias()}}
                  type="button">
                  <i aria-hidden={"true"} className="fas fa-plus-circle pr1"></i>Alias
                </button>
                <button className="br2 bg-blue white bg-animate hover-bg-dark-blue db w-100 tc pv3 btn--search"  type="submit">
                  <i aria-hidden="true" className="fas fa-search pr2"></i>
                  <span className="fw7">Search</span>
                </button>
              </div>

            <div role="alert" className="w-100">
              {this.state.missingInputs === true ? (
                <p id="name_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  First and last name are required.
                </p>
              ) : null}
              {this.state.invalidDate === true ? (
                <p id="dob_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  The date format must be MM/DD/YYYY.
                </p>
              ) : null}
            </div>
          </form>
        </section>
      </div>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system
});

export default connect(mapStateToProps)(RecordSearch);
