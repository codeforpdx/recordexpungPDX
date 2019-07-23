import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { logIn } from '../../redux/system/actions';
import { SystemState } from '../../redux/system/types';
import Logo from '../Logo';
import history from '../History';
import { Link } from 'react-router-dom';

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

class PasswordReset extends React.Component<Props, State> {
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
          : null // using setState(updater, callback) beccause setState doesn't immediately update component
    );
    //need validation for userId & PW
  };

  public render() {
    return (
      <main className="mw8 center ph2">
        <section className="mw6 center cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
          <Logo />
          <form>
            <fieldset>
              <legend className="f4 fw7 pt4">Forgot your password?</legend>
              <label htmlFor="email" className="db mt4 mb1 fw6">
                Email
              </label>
              <input
                id="email"
                type="email"
                className="w-100 mb4 pa3 br2 b--black-20"
              />
              <button className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 mb4 tc">
                Send email to reset password
              </button>
            </fieldset>
            <div role="alert">
              <p className="bg-washed-red mb3 pa3 br3 fw6">
                Please enter your email.
              </p>
              <p className="bg-washed-red mb3 pa3 br3 fw6">
                Technical difficulties, please try again later.
              </p>
            </div>
            <div role="status">
              <p className="bg-washed-green mb3 pa3 br3 fw6">
                Thanks, we're sending an email that will help you reset your
                password.
              </p>
            </div>
          </form>
          <div className="tc">
            <Link to="/" className="link underline" href="#">
              Return to log in
            </Link>
          </div>
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
