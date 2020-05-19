import React from 'react';

interface Props {
  onClick: Function
  }

export default class AddCaseButton extends React.Component<Props> {
  render() {

    return (
      <div className="tr pb3">
        <button className="tr mid-gray link hover-blue fw6" onClick={()=>{this.props.onClick()}}>
          <span className="fas fa-plus-circle" aria-hidden="true"></span>
          <span className="visually-hidden">Add</span> Case
        </button>
      </div>
    );
  }
}
