import React from "react";

interface Props {
  onClick: Function;
  actionName: string;
  text?: string;
}

export default class AddButton extends React.Component<Props> {
  render() {
    return (
      <button
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
