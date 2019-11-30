import React from 'react';

interface Props {
  inputString: string;
}

class LoadingSpinner extends React.Component<Props> {
  render() {
    return (
      <p className="bg-white mv4 pa4 br3 fw6 tc">
        <span className="spinner mr2"></span>Loading {this.props.inputString}...
      </p>
    );
  }
}

export default LoadingSpinner;
