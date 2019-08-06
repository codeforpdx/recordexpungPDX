import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { logIn } from '../../redux/system/actions';
import { SystemState } from '../../redux/system/types';
import Logo from '../Logo';
import { Redirect } from 'react-router';

interface Props {
  system: SystemState;
  logIn: typeof logIn;
}
interface State {
  password: string;
  missingPasswordInput: null | boolean;
  passwordIsValid: null | boolean;
  redirect: boolean;
}

class PasswordReset extends React.Component<Props, State> {
  state: State = {
    password: '',
    missingPasswordInput: null,
    passwordIsValid: null,
    redirect: false
  };

  handleChange = (e: React.BaseSyntheticEvent) => {
    // See https://github.com/DefinitelyTyped/DefinitelyTyped/issues/26635 for why we're
    // using the "any" type.
    this.setState<any>({
      [e.target.id]: e.target.value
    });
  };

  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.validateForm();
    if (
      this.state.passwordIsValid === true &&
      this.state.missingPasswordInput === false
    ) {
      this.setState({
        redirect: true
      });
    }
  };

  validateForm = () => {
    this.setState({
      missingPasswordInput: this.state.password.trim().length === 0,
      passwordIsValid: this.state.password.trim().length >= 10 // Need to implement a more robust password check.
    });
  };

  public render() {
    const { redirect } = this.state;
    if (redirect) {
      return <Redirect to="/record-search" />;
    }
    return (
      <main className="mw8 center ph2">
        <section className="mw6 center cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
          <Logo />
          <form
            onSubmit={this.handleSubmit}
            noValidate
            aria-label="Password Reset"
          >
            <fieldset>
              <legend className="f4 fw7 pt4 pb3">Set your password</legend>
              <p>Your password must have at least ten characters.</p>
              <label htmlFor="password" className="db mt4 mb1 fw6">
                Password
              </label>
              <input
                id="password"
                className="w-100 mb4 pa3 br2 b--black-20"
                type="password"
                required
                aria-describedby={
                  this.state.missingPasswordInput ? 'pw_msg' : undefined
                }
                onChange={this.handleChange}
              />
              <button
                className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 mb4 tc"
                type="submit"
              >
                Set password and log in
              </button>
            </fieldset>
            <div role="alert">
              {this.state.missingPasswordInput === true ||
              this.state.passwordIsValid === false ? (
                <p id="pw_msg" className="bg-washed-red mb3 pa3 br3 fw6">
                  Your password must have at least ten characters.
                </p>
              ) : null}
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
)(PasswordReset);
