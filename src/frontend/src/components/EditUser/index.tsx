import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { AppState } from '../../redux/store';
import { UserState } from '../../redux/users/types';
import validateEmail from '../../service/email-validation';
import Logo from '../Logo';

interface Props {
  users: UserState;
}

interface State {
  email: string;
  password: string;
  name: string;
  group: string;
  role: string;
  invalidCredentials: boolean;
  invalidResponse: boolean;
  invalidEmail: boolean;
  missingPassword: boolean;
}

class EditUser extends React.Component<Props, State> {
  public state: State = {
    email: '',
    password: '',
    name: '',
    group: '',
    role: '',
    invalidCredentials: false,
    invalidResponse: false,
    invalidEmail: false,
    missingPassword: false
  };

  public handleChange = (e: React.BaseSyntheticEvent) => {
    // See https://github.com/DefinitelyTyped/DefinitelyTyped/issues/26635 for why we're
    // using the "any" type.
    this.setState<any>({
      [e.target.id]: e.target.value
    });
  };

  public handleSubmit = (event: React.BaseSyntheticEvent) => {
    event.preventDefault();

    // Standardize email-lowerCase and trim both form inputs
    this.setState(
      {
        email: this.state.email.toLowerCase().trim(),
        password: this.state.password.trim()
      },
      () => {
        // TODO: Pre-populate form fields with user to be edited
        return
      }
    );
  };

  public render() {
    return (
      <main className="mw6 center ph2">

        <section className="cf mt4 mb3 pa3 pa4-l bg-white shadow br3">
          <h1 className="mb4 f4 fw6">Account: Jaire Alexander</h1>
          <form>
            <div className="mb4">
              <label htmlFor="name" className="db mb2 fw6">
                Name *
              </label>
              <input id="name" required type="text" value="Jaire Alexander" className="w-100 pa3 br2 b--black-20" />
            </div>

            <div className="mb4">
              <label htmlFor="email" className="db mb2 fw6">
                Email *
              </label>
              <input id="email" required type="email" value="jalexander@example.com" className="w-100 pa3 br2 b--black-20" />
            </div>

            <div className="mb4">
              <label htmlFor="role" className="db mb2 fw6">
                Role
              </label>
              <div className="pl0 ml0 center ba bw1 b--black-20 br2">
                <div className="ph3 bb bw1 b--black-20">
                  <div className="radio">
                    <input
                      type="radio"
                      id="search"
                      name="role"
                      value="search"
                      className="v-top"
                      checked
                    />
                    <label htmlFor="search" className="fw6">Search</label>
                  </div>
                  <div className="radio">
                    <p className="mt3 ml4 mb4">&bull;&nbsp;Can search records</p>
                  </div>
                </div>
                <div className="ph3">
                  <div className="radio">
                    <input
                      type="radio"
                      id="admin"
                      name="role"
                      value="admin"
                      className="v-top"
                    />
                    <label htmlFor="admin" className="fw6">Admin</label>
                  </div>
                  <ul className="list mt3 ml4 mb4">
                    <li className="mb1">&bull;&nbsp;Can search records</li>
                    <li className="mb1">&bull;&nbsp;Can manage users and groups</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="mb4">
              <label htmlFor="group" className="db mb2 fw6">
                Group
              </label>
              <div className="relative">
                <select
                  id="group"
                  className="w-100 pa3 br2 bw1 b--black-20 input-reset bg-white black-60"
                >
                  <option value="">Please select a group</option>
                  <option value="option1">Option 1</option>
                  <option value="option2">Option 2</option>
                  <option value="option3">Option 3</option>
                </select>
                <div className="absolute pa3 right-0 top-0 bottom-0 pointer-events-none">
                  <i aria-hidden="true" className="fas fa-angle-down"></i>
                </div>
              </div>
            </div>

            <div className="mb5">
              <button className="bg-blue white bg-animate hover-bg-dark-blue fw6 br2 pv3 ph4 db w-100 tc">
                Update Account
              </button>
            </div>

            <div className="bt b--black-20 pt5 mb5">
              <div className="mb2 fw7">Forgot your password or want to change it?</div>
              <button
                className="bg-navy white bg-animate hover-bg-dark-blue fw6 br2 pv3 ph4 tc w-100">
                Send an email to reset your password
              </button>
            </div>

            <div className="mb4">
              <button className="bg-navy white bg-animate hover-bg-dark-red fw6 br2 pv3 ph4 tc w-100">
                Delete Account
              </button>
            </div>
          </form>
        </section>
      </main>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  users: state.users
});

export default connect(
  mapStateToProps,
)(EditUser);
