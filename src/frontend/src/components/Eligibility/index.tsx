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
        Possibly Eligible {date} (review)
      </h2>
    );

    const ineligible = (
      <h2 className="fw6 red bg-washed-red pv2 ph3 ma2 mb3 dib br3">
        Ineligible
      </h2>
    );

    const handleWhenTypeEligibile = () => {
      if (time_eligibility) {
        if (time_eligibility.status === 'Eligible') {
          return eligibleNow;
        } else if (time_eligibility.date_will_be_eligible !== null) {
          return eligibleOn(time_eligibility.date_will_be_eligible);
        } else {
          return  <h2 className="fw6 purple bg-washed-purple pv2 ph3 ma2 mb3 dib br3">Eligible but no date on time analysis - please report</h2>;
        }
      } else {
        return <h2 className="fw6 purple bg-washed-purple pv2 ph3 ma2 mb3 dib br3">Eligible but no time analysis - please report</h2>;
      }
    };

    const eligibility = () => {

      // Time ineligibility without a date (meaning "never eligible") beats all other rules for eligibility
      // Currently this only occurs on Class B felonies, but the rule theoretically applies always, so it is checked first.
      if (time_eligibility && time_eligibility.status === 'Ineligible' && time_eligibility.date_will_be_eligible == null) {
        return ineligible;
      }

      switch (type_eligibility.status) {
        case 'Eligible':
          return handleWhenTypeEligibile();
        case 'Needs more analysis':
          if (time_eligibility) {
            return eligibleWithReview(time_eligibility.date_will_be_eligible);
          } else {
            return <h2 className="fw6 purple bg-washed-purple pv2 ph3 ma2 mb3 dib br3">Possibly eligible but no time analysis - please report</h2>;
          }
        case 'Ineligible':
          return ineligible;
        default:
          return <h2 className="fw6 purple bg-washed-purple pv2 ph3 ma2 mb3 dib br3">Unknown type eligibility - please report</h2>;
      }
    };

    return eligibility();
  }
}
