import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { logIn } from '../../redux/system/actions';
import { SystemState } from '../../redux/system/types';
import history from '../History';

interface Props {
  system: SystemState;
  logIn: typeof logIn;
}
interface State {
  userId: string;
  password: string;
  userIdHasInput: boolean;
  passwordHasInput: boolean;
  invalidCredentials: null | boolean;
  missingInputs: null | boolean;
}

class OECIlogin extends React.Component<Props, State> {
  state: State = {
    userId: '',
    password: '',
    userIdHasInput: false,
    passwordHasInput: false,
    invalidCredentials: null,
    missingInputs: null
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
  };

  validateForm = () => {
    this.setState({
      userIdHasInput: this.state.userId.trim().length === 0
    });
    this.setState({
      passwordHasInput: this.state.password.trim().length === 0
    });
    this.setState(
      {
        missingInputs:
          this.state.userId.trim().length === 0 ||
          this.state.password.trim().length === 0
      },
      () =>
        this.state.missingInputs === false
          ? history.push('/recordsearch')
          : null // Using setState(updater, callback) because setState doesn't immediately update component
    );
    //need validation for userId & PW
  };

  public render() {
    return (
      <main className="mw8 center ph2">
        <section className="mw6 center cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
          <form
            onSubmit={this.handleSubmit}
            noValidate
            className="oeci-login-form"
            id="OECILoginForm"
            aria-label="OECI Login Form"
          >
            <fieldset>
              <legend className="f4 fw6 dib pb3">
                Oregon eCourt Case Information
              </legend>
              <p className="mb4">
                Log in to OECI to search and analyse criminal records for
                expungement.
              </p>
              <div className="mt4">
                <label htmlFor="name" className="db mb1 fw6">
                  User ID
                </label>
                <input
                  id="userId"
                  className="w-100 mb4 pa3 br2 b--black-20"
                  type="text"
                  required
                  aria-describedby={
                    this.state.userIdHasInput ? 'inputs_msg' : undefined
                  }
                  aria-invalid={this.state.userIdHasInput}
                  onChange={this.handleChange}
                />
              </div>
              <label htmlFor="password" className="db mb1 fw6">
                Password
              </label>
              <input
                className="w-100 mb4 pa3 br2 b--black-20"
                type="password"
                id="password"
                required
                aria-describedby={
                  this.state.passwordHasInput ? 'inputs_msg' : undefined
                }
                aria-invalid={this.state.passwordHasInput}
                onChange={this.handleChange}
              />
              <button
                className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 mb4 tc"
                type="submit"
              >
                Log In
              </button>
            </fieldset>
            <div role="alert" className="mb4">
              {this.state.missingInputs === true ? (
                <p id="inputs_msg" className="bg-washed-red mb3 pa3 br3 fw6">
                  All fields are required.
                </p>
              ) : null}
              {this.state.invalidCredentials === true ? (
                <p className="bg-washed-red mb3 pa3 br3 fw6">
                  User ID and password do not match.
                </p>
              ) : null}
            </div>
            <a
              className="db tc link underline hover-blue"
              href="https://publicaccess.courts.oregon.gov/PublicAccessLogin/Login.aspx"
            >
              Oregon eCourt Case Information website
            </a>
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
)(OECIlogin);
