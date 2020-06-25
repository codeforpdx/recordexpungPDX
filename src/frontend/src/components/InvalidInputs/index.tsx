import React from "react";

interface Props {
  conditions: boolean[];
  contents: JSX.Element[];
}

export default class InvalidInputs extends React.Component<Props> {
  render() {
    return (
      <div role="alert" className="black-70 w-100">
        {this.props.contents.map((content: JSX.Element, i: number) => {
          return (
            this.props.conditions[i] && (
              <p className="bg-washed-red mv3 pa3 br3 fw6">{content}</p>
            )
          );
        })}
      </div>
    );
  }
}
