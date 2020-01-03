import React from 'react';
import Cases from '../Cases';
import { Record } from './types';

interface Props {
  records: Record;
}

export default class SearchResults extends React.Component<Props> {
  render() {
    const errors = ( this.props.records.errors ?
      this.props.records.errors.map(((errorMessage: string, errorIndex: number) => {
        let id= "record_error_" + errorIndex;
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
        {this.props.records.cases ? (
          <Cases cases={this.props.records.cases} />
        ) : null}
      </section>
      </>
    );
  }
}
