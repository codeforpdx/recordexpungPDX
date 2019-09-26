import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { AppState } from '../../redux/store';
import { logIn } from '../../redux/system/actions';
import { SystemState } from '../../redux/system/types';
import validateEmail from '../../service/email-validation';
import Logo from '../Logo';

interface Props {
  system: SystemState;
  logIn: typeof logIn;
}

interface State {
  email: string;
  password: string;
  invalidCredentials: boolean;
  invalidResponse: boolean;
  invalidEmail: boolean;
  missingPassword: boolean;
}

class LogIn extends React.Component<Props, State> {
  public state: State = {
    email: '',
    password: '',
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
    event.stopPropagation();

    // Standardize email-lowerCase and trim both form inputs
    this.setState(
      {
        email: this.state.email.toLowerCase().trim(),
        password: this.state.password.trim()
      },
      () => {
        this.validateLogIn();
      }
    );
  };

  public validateLogIn() {
    // validate email returns true for email input of: "_@_._" empty returns false
    this.setState(
      {
        invalidEmail: !validateEmail(this.state.email),
        missingPassword: this.state.password.length === 0
      },
      () => {
        // If no errors are present, attempt to log in.
        if (!this.state.invalidEmail && !this.state.missingPassword) {
          this.props
            .logIn(this.state.email, this.state.password)
            .catch((error: any) => {
              error.response.status === 401
                ? // error: email and password do not match
                  this.setState({ invalidCredentials: true })
                : // error: technical difficulties
                  this.setState({ invalidResponse: true });
            });
        }
      }
    );
  }

  public render() {
    return (
      <main className="mw6 ph2 center">
        <section className="cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
          <Logo />
          <form onSubmit={this.handleSubmit} noValidate={true}>
            <legend className="visually-hidden">Log in</legend>
            <label htmlFor="email" className="db mt4 mb1 fw6">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              className="w-100 mb4 pa3 br2 b--black-20"
              required={true}
              aria-describedby={
                this.state.invalidEmail
                  ? 'email_msg'
                  : this.state.invalidCredentials
                  ? 'no_match_msg'
                  : undefined
              }
              aria-invalid={
                this.state.invalidEmail || this.state.invalidCredentials
                  ? true
                  : false
              }
              onChange={this.handleChange}
            />
            <label htmlFor="password" className="db mb1 fw6">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              className="w-100 mb4 pa3 br2 b--black-20"
              required={true}
              aria-describedby={
                this.state.invalidCredentials
                  ? 'no_match_msg'
                  : this.state.missingPassword
                  ? 'input_msg'
                  : undefined
              }
              aria-invalid={
                this.state.invalidCredentials || this.state.missingPassword
                  ? true
                  : false
              }
              onChange={this.handleChange}
            />
            <button className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 mb4 tc">
              Log In
            </button>
            <div role="alert" className="w-100">
              {this.state.invalidEmail === true ? (
                <p id="email_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  Invalid email address.
                </p>
              ) : null}
              {this.state.missingPassword === true ? (
                <p id="input_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  Both fields are required.
                </p>
              ) : null}
              {this.state.invalidCredentials === true ? (
                <p id="no_match_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  Email and password do not match.
                </p>
              ) : null}
              {this.state.invalidResponse === true ? (
                <p id="no_match_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  Technical difficulties try again later.
                </p>
              ) : null}
            </div>
            <div className="tc">
              <Link
                to="/forgot-password"
                className="link underline hover-blue"
                href="/"
              >
                Forgot your password?
              </Link>
            </div>
          </form>
        </section>
      </main>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  system: state.system
});

export default connect(
  mapStateToProps,
  { logIn }
)(LogIn);
