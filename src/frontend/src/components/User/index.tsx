import React from 'react';
import { connect } from 'react-redux';
import history from '../../service/history';
import { AppState } from '../../redux/store';
import { UserState } from '../../redux/users/types';
import { User as UserTypes } from '../../redux/users/types';
import { toEditUser } from '../../redux/users/actions';

interface Props {
  users: UserState;
  user: UserTypes;
  toEditUser: Function;
}
interface ownProps {
  user: UserTypes;
}

class User extends React.Component<Props> {
  public render() {
    return (
      <tr className="bt b--black-20">
        <td className="pa3">{this.props.user.name}</td>
        <td className="pa3">{this.props.user.admin ? 'Admin' : 'Search'}</td>
        <td className="pa3">{this.props.user.group}</td>
        <td className="pa3 flex justify-end">
          <button
            onClick={() => {
              this.props.toEditUser(
                this.props.user.id,
                this.props.user.name,
                this.props.user.email,
                this.props.user.group,
                this.props.user.admin
              );
            }}
            aria-label={`edit user: ${this.props.user.name}`}
            className="navy hover-dark-blue"
          >
            <i aria-hidden="true" className="fa fa-pen pr3" />
          </button>
        </td>
      </tr>
    );
  }
}

function mapStateToProps(state: AppState, ownProps: ownProps) {
  return {
    users: state.users,
    user: ownProps.user
  }
}

export default connect(
  mapStateToProps,
  { toEditUser }
)(User);
