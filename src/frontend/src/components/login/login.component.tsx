import * as React from 'react'
import './login.style.scss'

export class LoginComponent extends React.Component {
    public render() {
        return(
            <form
                className="login-form bg-washed-green"
                id="LoginForm"
                aria-label="Record Expunge Login Form">
                <label className="title h2">
                    Record Expunge
                </label>
                <div className="form-group">
                    <label
                        htmlFor="LoginInputEmail">
                        Email
                    </label>
                    <input
                        type="email"
                        className="form-control"
                        id="LoginInputEmail"
                        aria-describedby="emailHelp"
                        />
                </div>
                <div className="form-group">
                    <label
                        htmlFor="LoginInputPassword1">
                        Password
                    </label>
                    <input
                        type="password"
                        className="form-control"
                        id="LoginInputPassword1"
                        />
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
        )
    }
}