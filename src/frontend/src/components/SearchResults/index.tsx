import React from 'react';

export default class SearchResults extends React.Component {
  render() {
    return (
      <section className="bg-gray-blue-2 shadow br3 overflow-auto">
        <div className="mb3">
          <div className="cf pv2 br3 br--top shadow-case">
            <div className="fl ph3 pv1">
              <span className="fw7">Case </span>
              <a className="underline" href="#">
                PA0061902
              </a>
            </div>
            <div className="fl ph3 pv1">
              <span className="fw7">Balance </span>
              $200.00
            </div>
            <div className="fl ph3 pv1">
              <span className="fw7">Name </span>
              Mark Monk
            </div>
            <div className="fl ph3 pv1">
              <span className="fw7">DOB </span>
              1/24/2014
            </div>
          </div>
        </div>
      </section>
    );
  }
}
