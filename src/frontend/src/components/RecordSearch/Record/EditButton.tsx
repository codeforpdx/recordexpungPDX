import React from "react";

interface Props {
  onClick: Function;
  actionName: string;
  ariaControls: string;
}

export default class EditButton extends React.Component<Props> {
  render() {
    return (
      <button
        className="mid-gray hover-blue ph2"
        aria-expanded="false" // This is never true because the button disappears when clicked, unless we create it anyway and just make it visually-hidden.
        aria-controls={this.props.ariaControls}
        onClick={() => {
          this.props.onClick();
        }}
      >
        <span className="visually-hidden">{this.props.actionName}</span>
        <span aria-hidden="true" className="fas fa-pen"></span>
      </button>
    );
  }
}
