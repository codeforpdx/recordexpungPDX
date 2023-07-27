import React from "react";
import { Navigate } from "react-router-dom";
import InvalidInputs from "../InvalidInputs";
import oeciLogIn from "../../service/oeci";
import { Link } from "react-router-dom";

interface State {
  userId: string;
  password: string;
  missingUserId: boolean;
  missingPassword: boolean;
  expectedFailure: boolean;
  expectedFailureMessage: string;
  invalidResponse: boolean;
  missingInputs: boolean;
  isLoggedIn: boolean;
}

class OeciLogin extends React.Component<State> {
  componentDidMount() {
    document.title = "Log In - RecordSponge";
  }

  state: State = {
    userId: "",
    password: "",
    missingUserId: false,
    missingPassword: false,
    expectedFailure: false,
    expectedFailureMessage: "",
    invalidResponse: false,
    missingInputs: false,
    isLoggedIn: false,
  };

  handleChange = (e: React.BaseSyntheticEvent) => {
    // See https://github.com/DefinitelyTyped/DefinitelyTyped/issues/26635 for why we're
    // using the "any" type.
    this.setState({
      [e.target.id]: e.target.value,
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
          this.state.password.trim().length === 0,
      },
      () => {
        if (this.state.missingInputs === false) {
          oeciLogIn(this.state.userId, this.state.password)
            .then((isLoggedIn: boolean) => {
              this.setState({ isLoggedIn });
            })
            .catch((error: any) => {
              error.response.status === 401 || error.response.status === 404
                ? // error: 40x
                  this.setState({
                    expectedFailure: true,
                    expectedFailureMessage: error.response.data.message,
                  })
                : // error: technical difficulties
                  this.setState({ invalidResponse: true });
            });
        }
      }
    );
  };

  public render() {
    if (this.state.isLoggedIn) {
      return <Navigate to="/record-search" />;
    }

    return (
      <>
        <main className="flex-l f6 f5-l">
          <div className="w-50-l bg-navy pt5 pb5 pb7-l ph4 pr5-l">
            <div className="mw6 center mr0-l ml-auto-l">
              <section className="ph3-l ph5-l">
                <h1 className="visually-hidden">
                  Log in to OECI to search records
                </h1>
                <div className="white">
                  <form
                    onSubmit={this.handleSubmit}
                    noValidate
                    className="oeci-login-form"
                    id="OeciLoginForm"
                    aria-label="OECI Login Form"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="db center mb3"
                      width="50"
                      height="50"
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
                      <legend className="f4 fw6 db center tc pb3">
                        Oregon eCourt Case Information
                      </legend>
                      <p className="tc mb4">
                        Log in to OECI to search and analyse criminal records
                        for expungement.
                      </p>
                      <div className="mt4">
                        <label htmlFor="userId" className="db mb1 fw6">
                          User ID
                        </label>
                        <input
                          id="userId"
                          name="oecilogin"
                          type="text"
                          autoComplete="username"
                          className="w-100 mb4 pa3 br2 b--black-20"
                          required
                          aria-describedby={
                            this.state.missingUserId ? "inputs_msg" : undefined
                          }
                          aria-invalid={this.state.missingUserId}
                          onChange={this.handleChange}
                        />
                      </div>
                      <label htmlFor="password" className="db mb1 fw6">
                        Password (WARNING: we have temporarily disabled security
                        - we are working hard to get it restored - proceed at
                        your own risk of getting your password stolen)
                      </label>
                      <input
                        id="password"
                        name="oecilogin"
                        type="password"
                        autoComplete="current-password"
                        className="w-100 mb4 pa3 br2 b--black-20"
                        required
                        aria-describedby={
                          this.state.missingPassword ? "inputs_msg" : undefined
                        }
                        aria-invalid={this.state.missingPassword}
                        onChange={this.handleChange}
                      />
                      <button
                        className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 tc"
                        type="submit"
                      >
                        Log in to OECI
                      </button>
                    </fieldset>
                    <InvalidInputs
                      conditions={[
                        this.state.missingInputs,
                        this.state.invalidResponse,
                        this.state.expectedFailure,
                      ]}
                      contents={[
                        <span>All fields are required.</span>,
                        <>
                          We're experiencing technical difficulties, please
                          contact{" "}
                          <a
                            className="link underline hover-blue"
                            href="mailto:help@recordsponge.com"
                          >
                            help@recordsponge.com
                          </a>
                        </>,
                        <span>{this.state.expectedFailureMessage}</span>,
                      ]}
                    />
                    <p className="lh-copy moon-gray mt5">
                      The{" "}
                      <a
                        className="link hover-light-blue bb"
                        href="https://publicaccess.courts.oregon.gov/PublicAccessLogin/Login.aspx"
                      >
                        eCourt site
                      </a>{" "}
                      is offline during the 4th weekend of each month between 6
                      PM PST on Friday until noon on Sunday. During this time,
                      record search will not&nbsp;function.
                    </p>
                  </form>
                </div>
              </section>
            </div>
          </div>
          <div className="w-50-l pt4 pt5-l pb5 ph4 ph6-l">
            <div className="mw6">
              <section className="lh-copy">
                <span className="db w3 bb bw2 b--blue pt3 mt2 mb2"></span>
                <h2 className="f4 fw9 mb4">New here?</h2>
                <p className="mb4">
                  <Link
                    to="/partner-interest"
                    className="link hover-dark-blue bb"
                    onClick={() => window.scrollTo(0, 0)}
                  >
                    Learn more about providing expungement help
                  </Link>
                  .
                </p>
                <p className="mb4">
                  <Link
                    to="/demo-record-search"
                    className="link hover-dark-blue bb"
                    onClick={() => window.scrollTo(0, 0)}
                  >
                    {" "}
                    Check out the demo version
                  </Link>
                  .
                </p>
                <p className="mb1">
                  We ask anyone using the software to be in touch so that we can
                  better maintain, scale, and improve our work and community.
                </p>
                <p className="mb4">
                  <Link
                    to="/partner-interest"
                    className="link hover-dark-blue bb"
                    onClick={() => window.scrollTo(0, 0)}
                  >
                    Please complete this contact form if you haven’t already
                  </Link>
                  .
                </p>
              </section>
            </div>
          </div>
        </main>
      </>
    );
  }
}

export default OeciLogin;
