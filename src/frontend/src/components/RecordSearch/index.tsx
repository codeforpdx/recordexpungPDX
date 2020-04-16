import React, { Component } from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { RecordData } from './Record/types';
import {
  searchRecord,
  clearRecord
} from '../../redux/search/actions';
import SearchPanel from './SearchPanel';
import Record from './Record';
import Status from './Status';
import Header from '../Header';
import { checkOeciRedirect } from '../../service/cookie-service';

type Props = {
  searchRecord: Function;
  clearRecord: Function;
  record?: RecordData;
};

class RecordSearch extends Component<Props> {
  componentDidMount() {
    checkOeciRedirect();
  }

  componentWillUnmount() {
    this.props.clearRecord();
  }

  render() {
    return (
      <>
      <Header/>
      <main className="mw8 center ph2">
        <SearchPanel searchRecord={this.props.searchRecord} />
        {this.props.record &&
        ((this.props.record.cases &&
        this.props.record.cases.length > 0) || this.props.record.errors) ? (
          <Record record={this.props.record} />
        ) : (
          <Status />
        )}
        <div className="bg-white shadow mv4 pa4 br3">
          <h2 className="fw6 mb3">Assumptions</h2>
          <p className="mb3">We are only able to access your public Oregon records.</p>
          <p className="mb2">Your analysis may be different if you have had cases which were:</p>
          <ul className="lh-copy pl4 mw6">
            <li className="mb2">Previously expunged</li>
            <li className="mb2">From States besides Oregon within the last ten years</li>
            <li className="mb2">From Federal Court within the last ten years</li>
            <li className="mb2">From local District Courts, e.g. Medford Municipal Court (not Jackson County Circuit Court) from within the last ten years</li>
          </ul>
        </div>
      </main>
      </>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    record: state.search.record
  };
};

export default connect(
  mapStateToProps,
  {
    searchRecord: searchRecord,
    clearRecord: clearRecord
  }
)(RecordSearch);
