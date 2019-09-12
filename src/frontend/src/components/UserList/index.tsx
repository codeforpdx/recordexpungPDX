import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { loadUsers } from '../../redux/users/actions';
import { User as UserTypes, UserState } from '../../redux/users/types';
import User from '../User';

interface Props {
  users: UserState;
  loadUsers: Function;
}

class UserList extends React.Component<Props> {
  public componentWillMount() {
    // this will call the axios request to populate the component with userList
    this.props.loadUsers();
  }

  public displayUsers = (inputUsers: UserTypes[]) => {
    if (inputUsers) {
      const returnList = inputUsers.map(user => {
        return <User key={user.id} user={user} />;
      });

      return returnList;
    }
  };

  public render() {
    return (
      <section className="cf bg-white shadow br3 mb5">
        <div className="pv4 ph3">
          <h1 className="f3 fw6 dib">Users</h1>
          <button className="bg-navy white bg-animate hover-bg-dark-blue fw6 br2 pv2 ph3 fr">
            New User
          </button>
        </div>

        <div className="overflow-auto">
          <table className="f6 w-100 mw8 center" data-cellspacing="0">
            <thead>
              <tr>
                <th className="fw6 bb b--black-20 tl pb3 ph3 bg-white">Name</th>
                <th className="fw6 bb b--black-20 tl pb3 ph3 bg-white">Role</th>
                <th className="fw6 bb b--black-20 tl pb3 ph3 bg-white">
                  Group
                </th>
              </tr>
            </thead>
            {this.props.users
              ? this.displayUsers(this.props.users.userList)
              : null}
          </table>
        </div>
      </section>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  users: state.users
});

export default connect(
  mapStateToProps,
  { loadUsers }
)(UserList);
