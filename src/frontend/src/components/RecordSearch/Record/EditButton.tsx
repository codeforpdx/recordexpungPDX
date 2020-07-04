import React from "react";

interface Props {
  onClick: Function;
  actionName: string;
}

export default class EditButton extends React.Component<Props> {
  render() {
    return (
      <button
        className="mid-gray hover-blue ph2"
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
