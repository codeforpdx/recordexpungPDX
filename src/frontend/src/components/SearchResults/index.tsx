import React from 'react';
import Cases from '../Cases';
import RecordSummary from '../RecordSummary';
import { Record } from './types';

interface Props {
  record: Record;
}

export default class SearchResults extends React.Component<Props> {
  render() {
    const errors = ( this.props.record.errors ?
      this.props.record.errors.map(((errorMessage: string, errorIndex: number) => {
        const id= "record_error_" + errorIndex;
        return <p id={id} className="bg-washed-red mv4 pa3 br3 fw6">
                  {errorMessage}
               </p>
        }
        )
      )
      : null
    );

    return (
      <>
      {errors}
      <section className="bg-gray-blue-2 shadow br3 overflow-auto">
        {this.props.record.summary ? (
          <RecordSummary summary={this.props.record.summary}/>
          ) : null }
        {this.props.record.cases ? (
          <Cases cases={this.props.record.cases} />
        ) : null}
      </section>
      </>
    );
  }
}
