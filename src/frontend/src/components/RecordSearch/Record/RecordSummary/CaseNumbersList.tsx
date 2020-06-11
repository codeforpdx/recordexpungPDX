import React from 'react';

interface Props {
  cases: string[];
  title: string;
  subheading: string;
  color: string;
}

export default class CaseNumbersList extends React.Component<Props> {
  render() {
    const listItems = this.props.cases.map(
      (caseNumber: string, index: number) => {
        const id = 'summary_li_' + caseNumber;
        return (
          <li className="mb2" id={id} key={id}>
            <a href={'#' + caseNumber} className="underline">
              {caseNumber}
            </a>
          </li>
        );
      }
    );

    return (
      <>
        <h3 className={'fw7 mb1 ' + this.props.color}>{this.props.title}</h3>
        <p className="f6 mb2">{this.props.subheading}</p>
        <ul className="list mb3">
          {listItems.length > 0 ? listItems : 'None'}
        </ul>
      </>
    );
  }
}
