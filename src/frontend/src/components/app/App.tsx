import * as React from 'react';
import './App.style.scss';

class App extends React.Component {

    public render() {
        return (
            <div className="landing-container bg-gray-blue">
                <form
                    className="login-form bg-washed-green"
                    id="LoginForm"
                    aria-label="Record Expunge Login Form">
                    <div className="title h2">
                        Record Expunge
                    </div>
                    <div className="form-group">
                        <label
                            htmlFor="exampleInputEmail1">
                            Email
                        </label>
                        <input
                            type="email"
                            className="form-control"
                            id="exampleInputEmail1"
                            aria-describedby="emailHelp"
                            placeholder="Enter email" />
                    </div>
                    <div className="form-group">
                        <label
                            htmlFor="exampleInputPassword1">
                            Password
                        </label>
                        <input
                            type="password"
                            className="form-control"
                            id="exampleInputPassword1"
                            placeholder="Password"/>
                    </div>
                    <div className="form-group buttons">
                        <button
                            type="submit"
                            className="btn btn-primary btn-block">
                            Log In
                        </button>
                        <a href="#">
                            Forgot Password?
                        </a>
                    </div>
                </form>
            </div>
    );
  }
}

export default App;
