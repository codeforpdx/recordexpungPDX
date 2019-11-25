import React from 'react';

class NotAuthorized extends React.Component {
  render() {
    return (
      <p className="bg-white mv4 pa4 br3 fw6 tc shadow br3">
        You are not authorized to view this content, please contact system
        administraitor.
      </p>
    );
  }
}

export default NotAuthorized;
