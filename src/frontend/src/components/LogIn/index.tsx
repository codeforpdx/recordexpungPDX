import React from 'react';
import { connect } from "react-redux";
import { AppState } from "../../redux/store";
import './styles.scss';
import { get } from 'lodash';
import { logIn } from "../../redux/system/actions";
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
    return(
      <section className="cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
        <form
          className="login-form"
          id="LoginForm"
          aria-label="Record Expunge Login Form">
          <Logo/>
          <div className="form-group mt4">
            <label htmlFor="name"
                   className="db mb1 fw6">
                Email
            </label>
            <input id="name"
                   className="w-100 mb4 pa3 br2 b--black-10"
                   type="text"
                   aria-describedby="name-desc"/>
          </div>
          <div className="form-group">
            <label htmlFor="password"
                   className="db mb1 fw6">
                Password
            </label>
            <input className="w-100 mb4 pa3 br2 b--black-10"
                   type="password"
                   id="password"
                   aria-describedby="password-desc"/>
          </div>
          <div className="form-group">
            <button
                onClick={this.logInNow}
                className="br2 bg-blue white db w-100 fw6 tc mb4 pv3">
                Log In
            </button>
            <button className="db tc link underline hover-blue">
                Forgot your password?
            </button>
          </div>
        </form>
      </section>
    )
  }

}

const mapStateToProps = (state: AppState) => ({
  system: state.system,
});

export default connect(
  mapStateToProps,
  { logIn }
)(LogIn);
