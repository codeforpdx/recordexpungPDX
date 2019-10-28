import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { oeciLogIn } from '../../redux/system/actions';
import { SystemState } from '../../redux/system/types';

interface Props {
  system: SystemState;
  oeciLogIn: typeof oeciLogIn;
}
interface State {
  userId: string;
  password: string;
  missingUserId: boolean;
  missingPassword: boolean;
  invalidCredentials: null | boolean;
  invalidResponse: null | boolean;
  missingInputs: null | boolean;
}

class OeciLogin extends React.Component<Props, State> {
  state: State = {
    userId: '',
    password: '',
    missingUserId: false, // Initially set to false for aria-invalid
    missingPassword: false, // Initially set to false for aria-invalid
    invalidCredentials: null,
    invalidResponse: null,
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
    // validate form
    this.setState(
      {
        missingUserId: this.state.userId.trim().length === 0,
        missingPassword: this.state.password.trim().length === 0,
        missingInputs:
          this.state.userId.trim().length === 0 ||
          this.state.password.trim().length === 0
      },
      () => {
        if (this.state.missingInputs === false) {
          this.props
            .oeciLogIn(this.state.userId, this.state.password)
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
  };

  public render() {
    return (
      <main className="mw8 center ph2">
        <section className="mw6 center cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
          <form
            onSubmit={this.handleSubmit}
            noValidate
            className="oeci-login-form"
            id="OeciLoginForm"
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
                    this.state.missingUserId ? 'inputs_msg' : undefined
                  }
                  aria-invalid={this.state.missingUserId}
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
                  this.state.missingPassword ? 'inputs_msg' : undefined
                }
                aria-invalid={this.state.missingPassword}
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
              {this.state.invalidResponse === true ? (
                <p id="no_match_msg" className="bg-washed-red mv4 pa3 br3 fw6">
                  Technical difficulties try again later.
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
  { oeciLogIn }
)(OeciLogin);
