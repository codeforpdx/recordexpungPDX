import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { UserState } from '../../redux/users/types';
import { editUser } from '../../redux/users/actions';
import validateEmail from '../../service/email-validation';
import Header from '../Header';

interface Props {
  users: UserState;
  isAdmin?: boolean;
  editUser: (id: number, name: string, email: string, password: string, group: string, admin: boolean) => Promise<void>;

}

interface State {
  errorType: string;
  errorMessage: string;
  id: number;
  email: string;
  password: string;
  confirmPassword: string;
  name: string;
  group: string;
  role: string;
  invalidResponse: boolean;
  missingName: boolean;
  invalidEmail: boolean;
  invalidPassword: boolean;
  mismatchPasswords: boolean;
}

class EditUser extends React.Component<Props, State> {
  public state: State = {
    errorType: '',
    errorMessage: '',
    id: 1,
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    group: '',
    role: 'search',
    invalidResponse: false,
    missingName: false,
    invalidEmail: false,
    invalidPassword: false,
    mismatchPasswords: false,
  };

  componentDidMount() {
    this.setState({
      id: this.props.users.editID,
      name: this.props.users.editName,
      email: this.props.users.editEmail,
      group: this.props.users.editGroup,
      role: this.props.users.editAdmin === true ? 'admin' : 'search'

    });
  }

  public handleChange = (e: React.BaseSyntheticEvent) => {
    // See https://github.com/DefinitelyTyped/DefinitelyTyped/issues/26635 for why we're
    // using the "any" type.
    this.setState<any>({
      [e.target.id]: e.target.value
    });
  };

  public handleRadioChange = (e: React.BaseSyntheticEvent) => {
    this.setState<any>({
      [e.target.name]: e.target.value
    });
  };

  public handleSubmit = (event: React.BaseSyntheticEvent) => {
    event.preventDefault();

    // Standardize email-lowerCase and trim both form inputs
    this.setState(
      {
        name: this.state.name.trim(),
        email: this.state.email.toLowerCase().trim(),
        password: this.state.password.trim(),
        confirmPassword: this.state.confirmPassword.trim()
      },
      () => {
        // TODO: Pre-populate form fields with user to be edited
        this.validateFormFields();
      }
    );
  };

  public validateFormFields() {
    this.setState(
      {
        missingName: this.state.name.length === 0,
        invalidEmail: !validateEmail(this.state.email),
        invalidPassword: this.state.password.length > 0 && this.state.password.length < 8,
        mismatchPasswords: this.state.password !== this.state.confirmPassword
      },
      () => {
        if (
          !(this.state.missingName
          || this.state.invalidEmail
          || this.state.invalidPassword
          || this.state.mismatchPasswords)
        ) {
            this.dispatchEditUser();
          }
      }
    );
  }

  public dispatchEditUser() {
    var admin = (this.state.role === 'search') ? false : true;
    this.props.editUser(
      this.state.id,
      this.state.name,
      this.state.email,
      this.state.password,
      this.state.group,
      admin
    ).catch(error => {
      if (error.response.status === 403) {
        // error if user is not admin
        this.setState({ errorType: 'unauthorized' });
      } else if (error.response.status === 422) {
        this.setState({
          errorType: 'endpoint',
          errorMessage: error.response.data.message
        });
      }
      else {
        this.setState({ errorType: 'technical' });
      }
    })
  }

  public render() {
    return (
      <>
      <Header/>
      <main className="mw6 center ph2">

        <section className="cf mt4 mb3 pa3 pa4-l bg-white shadow br3">
          <h1 className="mb4 f4 fw6">Account: </h1>
          <form onSubmit={this.handleSubmit} noValidate={true}>
            <div className="mb4">
              <label htmlFor="name" className="db mb2 fw6">
                Name *
              </label>
              <input
                id="name"
                name="name"
                type="text"
                placeholder={this.state.name}
                required={true}
                className="w-100 pa3 br2 b--black-20"
                aria-describedby={
                  this.state.missingName
                    ? 'name_input_message'
                    : undefined
                }
                aria-invalid={this.state.missingName}
                onChange={this.handleChange}
              />
            </div>
            <div className="mb4">
              <label htmlFor="email" className="db mb2 fw6">
                Email *
              </label>
              <input
                id="email"
                name="email"
                type="email"
                placeholder={this.state.email}
                required={true}
                className="w-100 pa3 br2 b--black-20"
                aria-describedby={
                  this.state.invalidEmail
                    ? 'email_message'
                    : undefined
                }
                aria-invalid={this.state.invalidEmail}
                onChange={this.handleChange}
              />
            </div>
            <div className="mb4">
              <label htmlFor="password" className="db mb2 fw6">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required={true}
                className="w-100 pa3 br2 b--black-20"
                aria-describedby={
                  this.state.invalidPassword
                    ? 'password_message'
                    : undefined
                }
                aria-invalid={this.state.invalidPassword}
                onChange={this.handleChange}
              />
            </div>
            <div className="mb4">
              <label htmlFor="confirm-password" className="db mb2 fw6">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                name="confirm-password"
                type="password"
                className="w-100 pa3 br2 b--black-20"
                aria-describedby={
                  this.state.mismatchPasswords
                    ? 'mismatch_message'
                    : undefined
                }
                aria-invalid={this.state.mismatchPasswords}
                onChange={this.handleChange}
              />
            </div>
            <div className="mb4">
              <label htmlFor="group" className="db mb2 fw6">
                Group
              </label>
              <input
                id="group"
                name="group"
                type="text"
                placeholder={this.state.group}
                className="w-100 pa3 br2 b--black-20"
                onChange={this.handleChange}
              />
            </div>
            {this.props.isAdmin ? (
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
                        checked={this.state.role === "search"}
                        onChange={this.handleRadioChange}
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
                        checked={this.state.role === 'admin'}
                        onChange={this.handleRadioChange}
                      />
                      <label htmlFor="admin" className="fw6">Admin</label>
                    </div>
                    <ul className="list mt3 ml4 mb4">
                      <li className="mb1">&bull;&nbsp;Can search records</li>
                      <li className="mb1">&bull;&nbsp;Can manage users and groups</li>
                    </ul>
                  </div>
                </div>
              </div>) : null}
            <div className="mb5">
              <button className="bg-blue white bg-animate hover-bg-dark-blue fw6 br2 pv3 ph4 db w-100 tc">
                Update Account
              </button>
            </div>

            <div role="alert" className="w-100">
              {this.state.missingName === true ? (
                <p id="name_input_message" className="bg-washed-red mv4 pa3 br3 fw6">
                  Name is required.
                </p>
              ) : null}
              {this.state.invalidEmail === true ? (
                <p id="email_message" className="bg-washed-red mv4 pa3 br3 fw6">
                  Invalid email address.
                </p>
              ) : null}
              {this.state.invalidPassword === true ? (
                <p id="password_message" className="bg-washed-red mv4 pa3 br3 fw6">
                  Passwords must be at least 8 characters.
                </p>
              ) : null}
              {this.state.mismatchPasswords === true ? (
                <p id="mismatch_message" className="bg-washed-red mv4 pa3 br3 fw6">
                  Passwords do not match.
                </p>
              ) : null}
              {this.state.invalidResponse === true ? (
                <p id="no_match_message" className="bg-washed-red mv4 pa3 br3 fw6">
                  Technical difficulties try again later.
                </p>
              ) : null}
              {this.state.errorType === 'endpoint' ? (
                <p id="endpoint_error_message" className="bg-washed-red mv4 pa3 br3 fw6">
                  {this.state.errorMessage}
                </p>
              ) : null}
            </div>

            <div className="visually-hidden bt b--black-20 pt5 mb5">
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
      </>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  users: state.users,
  isAdmin: state.system.isAdmin
});

export default connect(
  mapStateToProps,
  { editUser }
)(EditUser);
