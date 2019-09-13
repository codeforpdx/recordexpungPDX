import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { AppState } from '../../redux/store';
import { logIn } from '../../redux/system/actions';
import { SystemState } from '../../redux/system/types';
import apiService, { Request } from '../../service/api-service';
import history from '../History';
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
  missingInputs: boolean;
}

class LogIn extends React.Component<Props, State> {
  public state: State = {
    email: '',
    password: '',
    invalidCredentials: false,
    invalidResponse: false,
    invalidEmail: false,
    missingInputs: false
  };

  constructor(props: Props) {
    super(props);
    this.logInNow = this.logInNow.bind(this);
  }

  public handleChange = (e: React.BaseSyntheticEvent) => {
    // See https://github.com/DefinitelyTyped/DefinitelyTyped/issues/26635 for why we're
    // using the "any" type.
    this.setState<any>({
      [e.target.id]: e.target.value
    });
  };

  public logInNow(event: React.BaseSyntheticEvent) {
    event.preventDefault();
    event.stopPropagation();

    // checks to see if the form is ready for submission and updates error messages
    this.validateForm();
    if (!this.state.missingInputs && !this.state.invalidEmail) {
      const request: Request = {
        url: '/api/auth_token',
        data: {
          email: this.state.email.toLowerCase().trim(),
          password: this.state.password.trim()
        },
        method: 'post'
      };

      apiService(request)
        .then(response => {
          // attach token to auth headers
          // console.log(response);
          this.props.logIn();
          history.push('/oeci');
        })
        .catch(error => {
          // ERROR: email and password do not match
          this.setState({
            invalidCredentials: true
          });
        });
    } else {
      // ERROR: technical difficulty error
      this.setState({
        invalidResponse: true
      });
    }
  }

  public isEmailValid = (email: string) => {
    // returns true if the email is correct format: https://www.w3resource.com/javascript/form/email-validation.php
    return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email);
  };

  public validateForm = () => {
    this.setState({
      invalidEmail: this.isEmailValid(this.state.email.toLowerCase().trim())
        ? false
        : true
    });
    if (
      this.state.email.trim().length === 0 ||
      this.state.password.trim().length === 0
    ) {
      this.setState({ missingInputs: true });
    }
  };

  public render() {
    return (
      <main className="mw6 ph2 center">
        <section className="cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
          <Logo />
          <form onSubmit={this.logInNow} noValidate={true}>
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
                this.state.invalidEmail && this.state.invalidCredentials
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
                  : this.state.missingInputs
                  ? 'input_msg'
                  : undefined
              }
              aria-invalid={
                this.state.invalidCredentials && this.state.missingInputs
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
              {this.state.missingInputs === true ? (
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
                <p id="tech_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  Technical difficulties, please try again later.
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
