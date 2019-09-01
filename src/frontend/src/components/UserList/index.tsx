import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { loadUsers } from '../../redux/users/actions';
import { SystemState } from '../../redux/system/types';
import { UserState } from '../../redux/users/types';
import User from '../User';

// Data for loadUsers action to populate the store with user data
const placeholderUserData: UserTypes[] = [
  {
    name: 'Jane Dolby',
    role: 'Search',
    group: 'Metropolitan Public Defender'
  },
  {
    name: 'Michael Zhang',
    role: 'Admin',
    group: 'Metropolitan Public Defender'
  },
  {
    name: 'Melissa Jennings',
    role: 'Search',
    group: 'Royce, Jennings & Coldwater'
  },
  {
    name: 'Terri Royce',
    role: 'Search',
    group: 'Royce, Jennings & Coldwater'
  }
];

interface Props {
  system: SystemState;
  users: UserState;
  loadUsers: Function;
}

interface UserTypes {
  name: string;
  role: string;
  group: string;
}

class UserList extends React.Component<Props, UserState> {
  state: UserState = {
    userList: []
  };

  componentWillMount() {
    // This is just a placeholder to mock how the component will look with user data
    this.props.loadUsers(placeholderUserData);
  }

  displayUsers = (inputUsers: UserTypes[]) => {
    if (inputUsers) {
      let returnList = inputUsers.map(user => {
        return <User user={user} />;
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
  system: state.system,
  users: state.users
});

export default connect(
  mapStateToProps,
  { loadUsers }
)(UserList);
