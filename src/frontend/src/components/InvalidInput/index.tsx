import React from 'react';

interface Props {
  message: string;
  condition: boolean;
}

export default class InvalidInput extends React.Component<Props> {
  render() {
    return (
        this.props.condition ?
      <div role="alert" className="w-100">
        <p className="bg-washed-red mv4 pa3 br3 fw6">
          {this.props.message}
        </p>
      </div> : <></>
    );
  }
}
