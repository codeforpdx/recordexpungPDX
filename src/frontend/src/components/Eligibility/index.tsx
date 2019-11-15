import React from 'react';
import { ExpungementResultType } from '../SearchResults/types';

interface Props {
  expungement_result: ExpungementResultType;
}

export default class Eligibility extends React.Component<Props> {
  render() {
    const {
      type_eligibility,
      time_eligibility
    } = this.props.expungement_result;

    const eligibleNow = (
      <h2 className="fw6 green bg-washed-green pv2 ph3 ma2 mb3 dib br3">
        Eligible now
      </h2>
    );

    const eligibleOn = (date: string) => (
      <h2 className="fw6 dark-blue bg-washed-blue pv2 ph3 ma2 mb3 dib br3">
        Eligible {date}
      </h2>
    );

    const eligibleWithReview = (date: string) => (
      <h2 className="fw6 purple bg-washed-purple pv2 ph3 ma2 mb3 dib br3">
        Eligible {date} (review)
      </h2>
    );

    const ineligible = (
      <h2 className="fw6 red bg-washed-red pv2 ph3 ma2 mb3 dib br3">
        Ineligible
      </h2>
    );

    const eligibility = () => {
      if (
        type_eligibility.status === 'Eligible' &&
        time_eligibility &&
        time_eligibility.status === 'Eligible'
      ) {
        return eligibleNow;
      } else if (
        type_eligibility.status === 'Eligible' &&
        time_eligibility &&
        time_eligibility.date_of_eligibility !== null
      ) {
        return eligibleOn(time_eligibility.date_of_eligibility);
      } else if (
        type_eligibility.status === 'Needs more analysis' &&
        time_eligibility
      ) {
        return eligibleWithReview(time_eligibility.date_of_eligibility);
      } else if (type_eligibility.status === 'Ineligible') {
        return ineligible;
      } else {
        return 'Unknown type or time eligibility';
      }
    };

    return eligibility();
  }
}
