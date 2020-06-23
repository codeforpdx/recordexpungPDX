import React from "react";

interface Props {
  message: any;
  condition: boolean;
}

export default class InvalidInput extends React.Component<Props> {
  render() {
    return this.props.condition ? (
      <div role="alert" className="black-70 w-100">
        <p className="bg-washed-red mb3 pa3 br3 fw6">
          {this.props.message}
          {this.props.children}
        </p>
      </div>
    ) : (
      <></>
    );
  }
}
