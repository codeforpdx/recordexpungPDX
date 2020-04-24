import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { oeciLogIn } from '../../redux/system/actions';
import { SystemState } from '../../redux/system/types';
import Header from '../Header';

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
      <>
      <Header/>
      <main className="mw8 center ph2">
        <section className="mw6 center cf white bg-dark-blue shadow br3 mt4 mb3 pa4 pa5-ns pt4-ns">
          <form
            onSubmit={this.handleSubmit}
            noValidate
            className="oeci-login-form"
            id="OeciLoginForm"
            aria-label="OECI Login Form"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="db center mb4"
              width="66"
              height="66"
              viewBox="0 0 66 66"
            >
              <g fill="none" fillRule="evenodd">
                <circle cx="33" cy="33" r="33" fill="#FFF"></circle>
                <path
                  fill="#A2C8FA"
                  fillRule="nonzero"
                  d="M33 5c15.464 0 28 12.536 28 28S48.464 61 33 61 5 48.464 5 33 17.536 5 33 5zm0 3.2C19.303 8.2 8.2 19.303 8.2 33c0 13.697 11.103 24.8 24.8 24.8 13.697 0 24.8-11.103 24.8-24.8C57.8 19.303 46.697 8.2 33 8.2zm.315 12.8c1.254 0 2.366.564 3.114 1.44l.136.167h10.411c.417 0 .76.306.811.702l.006.101v1.607c0 .41-.311.747-.714.797l-.066.004.157.115c.254.204.473.465.637.783 4.113 7.977 4.375 8.282 4.391 8.916l.001.173c.001 2.212-2.958 4.006-6.609 4.006-3.561 0-6.465-1.707-6.604-3.845l-.006-.161.001-.175c.014-.602.263-.905 4.392-8.914.196-.38.47-.68.79-.896h-6.845a4.028 4.028 0 01-2.16 2.778l-.21.097v12.291h2.908c.417 0 .76.307.81.703l.007.1v1.608c0 .41-.312.747-.715.797l-.102.006h-9.082a.812.812 0 01-.811-.703l-.006-.1V41.79c0-.41.311-.748.714-.797l.103-.007h2.907V28.695a4.044 4.044 0 01-2.316-2.649l-.053-.226h-7.476c.32.217.594.515.79.896 4.176 8.098 4.383 8.29 4.392 8.945v.03l.002.114c0 2.212-2.96 4.006-6.61 4.006-3.65 0-6.61-1.794-6.609-4.006 0-.785-.107-.363 4.391-9.09.24-.465.598-.808 1.012-1.028a.797.797 0 01-.36-.552l-.008-.118V23.41c0-.41.312-.747.715-.797l.102-.006h10.412A4.088 4.088 0 0133.315 21zm12.59 6.897l-3.777 7.525h7.554l-3.777-7.525zm-25.81 0l-3.777 7.525h7.554l-3.777-7.525z"
                ></path>
              </g>
            </svg>
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
                className="bg-blue white bg-animate hover-bg-dark-blue ba b--blue fw6 db w-100 br2 pv3 ph4 mb4 tc"
                type="submit"
              >
                Log in to OECI
              </button>
            </fieldset>
            <div className="black-70" role="alert">
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
                  Technical difficulties, please contact system administrator.
                </p>
              ) : null}
            </div>
            <a
              className="db tc link underline hover-light-blue"
              href="https://publicaccess.courts.oregon.gov/PublicAccessLogin/Login.aspx"
            >
              Oregon eCourt Case Information website
            </a>
            <p className="lh-copy mt4">The eCourt site is offline during the 4th weekend of each month between
            6 PM PST on Friday until noon on Sunday. During this time, record search will not&nbsp;function.</p>
          </form>
        </section>
      </main>
      </>
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
