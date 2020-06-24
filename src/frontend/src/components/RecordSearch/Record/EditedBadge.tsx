import React from "react";

interface Props {
  editStatus: string;
  onClick: Function;
  editingRecord: boolean;
}

export default class EditedBadge extends React.Component<Props> {
  render() {
    return (
      <div className="inline-flex bs2-inset-gray bg-white fw6 br3 ma2  ">
        <span className="mid-gray bs2-r-gray pa2">
          {this.props.editStatus === "UPDATE"
            ? "Edited"
            : this.props.editStatus === "ADD"
            ? "Manual"
            : this.props.editStatus === "DELETE"
            ? "Removed"
            : null}
        </span>
        {this.props.editingRecord ? (
          <div className="ph3" />
        ) : (
          <button
            className="mid-gray link hover-blue pa2"
            onClick={() => {
              this.props.onClick();
            }}
          >
            <span className="visually-hidden">Undo edits</span>
            <span className="fas fa-undo f6" aria-hidden="true"></span>
          </button>
        )}
      </div>
    );
  }
}
