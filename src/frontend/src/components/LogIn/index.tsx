import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';
import { logIn } from '../../redux/system/actions';
import Logo from '../Logo';
import { SystemState } from '../../redux/system/types';
import history from '../History';
import { Link } from 'react-router-dom';
import axios from 'axios';
import apiService, { Request } from '../../service/api-service';

interface Props {
  system: SystemState;
  logIn: typeof logIn;
}
interface State {}

// interface FormTypes {
//   [key: string]: {
//     value: string
//   };
// }

class LogIn extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.logInNow = this.logInNow.bind(this);
  }

  public logInNow(event: React.BaseSyntheticEvent) {
    event.preventDefault();
    event.stopPropagation();

    // need to figure out how I can appease both inputs
    // FormTypes[]
    const formData: any = event.target;

    const request: Request = {
      url: '/api/auth_token',
      data: {
        email: formData.email.value.toLowerCase().trim(),
        password: formData.password.value.trim()
      },
      method: 'post'
    };
    apiService(request)
      .then(response => {
        console.log(response);
        // attach token to auth headers
        this.props.logIn();
        history.push('/oeci');
      })
      .catch(error => {
        console.log(error.response);
      });
  }

  public render() {
    return (
      <main className="mw6 ph2 center">
        <section className="cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
          <Logo />
          <form onSubmit={this.logInNow} noValidate>
            <legend className="visually-hidden">Log in</legend>
            <label htmlFor="email" className="db mt4 mb1 fw6">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              className="w-100 mb4 pa3 br2 b--black-20"
            />
            <label htmlFor="password" className="db mb1 fw6">
              Password
            </label>
            <input
              id="input1"
              name="password"
              type="password"
              className="w-100 mb4 pa3 br2 b--black-20"
            />
            <button className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 mb4 tc">
              Log In
            </button>
            <div role="alert" />
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
