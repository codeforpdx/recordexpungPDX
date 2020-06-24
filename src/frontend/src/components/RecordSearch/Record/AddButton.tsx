import React from "react";

interface Props {
  onClick: Function;
  actionName: string;
  text?: string;
  ariaControls: string;
}

export default class AddButton extends React.Component<Props> {
  render() {
    return (
      <button
        id={this.props.ariaControls + "-add-button"}
        aria-expanded="false" // This never needs to be true because the button disappears when clicked.
        aria-controls={this.props.ariaControls}
        className="tr mid-gray link hover-blue fw6"
        onClick={() => {
          this.props.onClick();
        }}
      >
        <span className="fas fa-plus-circle" aria-hidden="true"></span>
        <span className="visually-hidden">{this.props.actionName}</span>{" "}
        {this.props.text || ""}
      </button>
    );
  }
}
