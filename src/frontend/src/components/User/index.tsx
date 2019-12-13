import React from 'react';
import { User as UserTypes } from '../../redux/users/types';

interface Props {
  user: UserTypes;
}

class User extends React.Component<Props> {
  public render() {
    return (
      <tr className="bt b--black-20">
        <td className="pa3">
          <a href="/admin" className="underline">
            {this.props.user.name}
          </a>
        </td>
        <td className="pa3">{this.props.user.admin ? 'Admin' : 'Search'}</td>
        <td className="pa3">{this.props.user.group}</td>
        <td className="pa3 flex justify-end">
          <button
            aria-label={`edit user: ${this.props.user.name}`}
            className="navy hover-dark-blue"
          >
            <i aria-hidden="true" className="fa fa-pen pr3" />
          </button>
          <button
            aria-label={`delete user: ${this.props.user.name}`}
            className="navy hover-dark-blue"
          >
            <i aria-hidden="true" className="fa fa-trash" />
          </button>
        </td>
      </tr>
    );
  }
}

export default User;
