import React from 'react';

interface Props {
  user: {
    name: string;
    role: string;
    group: string;
  };
}

interface State {}

class User extends React.Component<Props, State> {
  public render() {
    return (
      <tr>
        <td className="pa3 bb b--black-20">
          <a href="#" className="underline">
            {this.props.user.name}
          </a>
        </td>
        <td className="pa3 bb b--black-20">{this.props.user.role}</td>
        <td className="pa3 bb b--black-20">{this.props.user.group}</td>
      </tr>
    );
  }
}

export default User;
