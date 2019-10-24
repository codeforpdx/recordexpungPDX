import React from 'react';
import Cases from '../Cases';
import { Record } from '../../redux/records/types';

interface Props {
  records: Record;
}

export default class SearchResults extends React.Component<Props> {
  render() {
    console.log('hiiiiii', this.props.records);

    return (
      <section className="bg-gray-blue-2 shadow br3 overflow-auto">
        {this.props.records.cases ? (
          <Cases cases={this.props.records.cases} />
        ) : null}
      </section>
    );
  }
}
