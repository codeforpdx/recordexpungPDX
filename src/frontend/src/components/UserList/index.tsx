import React from 'react';
import history from '../../service/history';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { loadUsers, clearUsers } from '../../redux/users/actions';
import { UserState } from '../../redux/users/types';
import User from '../User';
import LoadingSpinner from '../LoadingSpinner';
import NotAuthorized from '../NotAuthorized';
import TechnicalDifficulties from '../TechnicalDifficulties';

interface Props {
  users: UserState;
  loadUsers: () => Promise<void>;
  clearUsers: Function;
}

interface State {
  errorType: string;
  addUser: boolean;
}

class UserList extends React.Component<Props> {
  state: State = {
    errorType: 'none',
    addUser: false,
    };
  componentDidMount() {
    // this will call the axios request to populate the component with userList
    this.props.loadUsers().catch(error => {
      if (error.response.status === 403) {
        // error if user is not admin
        this.setState({ errorType: 'unauthorized' });
      } else {
        this.setState({ errorType: 'technical' });
      }
    });
  }

  componentWillUnmount() {
    this.props.clearUsers();
  }

  displayNoUsers = () => {
    if (this.state.errorType === 'none') {
      return <LoadingSpinner inputString={'Users'} />;
    } else if (this.state.errorType === 'unauthorized') {
      return <NotAuthorized />;
    } else {
      return <TechnicalDifficulties />;
    }
  };

  displayUserList = () => {
    const returnList = this.props.users.userList.map(user => {
      return <User key={user.id} user={user} />;
    });

    return returnList;
  };

  displayUsers = () => (
    <section className="cf bg-white shadow br3 mb5">
      <div className="pv4 ph3">
        <h1 className="f3 fw6 dib">Users</h1>
        <button
          onClick={() => history.push('add-user')}
          className="bg-navy white bg-animate hover-bg-dark-blue fw6 br2 pv2 ph3 fr">
          New User
        </button>
      </div>

      <div className="overflow-auto">
        <table className="f6 w-100 mw8 center collapse">
          <thead className="bb b--black-20">
            <tr>
              <th className="fw6 tl pb3 ph3 bg-white">Name</th>
              <th className="fw6 tl pb3 ph3 bg-white">Role</th>
              <th className="fw6 tl pb3 ph3 bg-white">Group</th>
            </tr>
          </thead>

          <tbody className="lh-copy">{this.displayUserList()}</tbody>
        </table>
      </div>
    </section>
  );

  render() {
    return this.props.users.userList.length > 0
      ? this.displayUsers()
      : this.displayNoUsers();
  }
}

const mapStateToProps = (state: AppState) => ({
  users: state.users
});

export default connect(
  mapStateToProps,
  { loadUsers, clearUsers }
)(UserList);
