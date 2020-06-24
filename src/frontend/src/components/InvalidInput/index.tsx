import React from "react";

interface Props {
  message: any;
  condition: boolean;
}

export default class InvalidInput extends React.Component<Props> {
  render() {
    return (
      <div role="alert" className="black-70 w-100">
        {this.props.condition && (
          <p className="bg-washed-red mv4 pa3 br3 fw6">
            {this.props.message}
            {this.props.children}
          </p>
        )}
      </div>
    );
  }
}
