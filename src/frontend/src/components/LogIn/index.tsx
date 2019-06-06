import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { get } from 'lodash';
import { logIn } from '../../redux/system/actions';
import Logo from '../Logo';

class LogIn extends React.Component {
  constructor() {
    super(arguments[0]);
    this.logInNow = this.logInNow.bind(this);
  }

  public logInNow() {
    // TODO: clean this up. Not sure how to appease Typescript here.
    get(this, 'props.logIn')();
    arguments[0].preventDefault();
    arguments[0].stopPropagation();
  }

  public render() {
    return (
      <main className="mw6 ph2 center">
        <section className="cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
          <Logo />
          <form noValidate>
            <legend className="visually-hidden">Log in</legend>
            <label htmlFor="email" className="db mt4 mb1 fw6">
              Email
            </label>
            <input
              id="email"
              type="email"
              className="w-100 mb4 pa3 br2 b--black-20"
            />
            <label htmlFor="password" className="db mb1 fw6">
              Password
            </label>
            <input
              id="input1"
              type="text"
              className="w-100 mb4 pa3 br2 b--black-20"
            />
            <button
              className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 mb4 tc"
              onClick={this.logInNow}
            >
              Log In
            </button>
            <div role="alert" />
            <div className="tc">
              <a className="link underline hover-blue" href="/">
                Forgot your password?
              </a>
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
