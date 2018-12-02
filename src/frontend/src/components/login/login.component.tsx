import * as React from 'react'
import {IconComponent} from "../common/icon.component";

export class LoginComponent extends React.Component {
    public render() {
        return(
            <form
                className="login-form"
                id="LoginForm"
                aria-label="Record Expunge Login Form">
                <label aria-hidden="true">Record Expunge</label>
                <div className="title">
                    <IconComponent iconName="logo"/>
                    <div className="h2">
                        Record Expunge
                    </div>
                </div>
                <div className="form-group">
                    <label htmlFor="name"
                           className="f6 b db mb2">
                        Email
                    </label>
                    <input id="name"
                           className="w-100 mb4 pa3 br2 b--black-10"
                           type="text"
                           aria-describedby="name-desc"/>
                </div>
                <div className="form-group">
                    <label htmlFor="password"
                           className="f6 b db mb2">
                        Password
                    </label>
                    <input className="w-100 mb4 pa3 br2 b--black-10"
                           type="password"
                           id="password"
                           aria-describedby="password-desc"/>
                </div>
                <div className="form-group buttons">
                    <button
                        type="submit"
                        className="f4 link dim br2 ph3 pv2 mb2 dib white bg-dark-blue">
                        Log In
                    </button>
                    <a className="f4 fw6 db black link hover-hot-pink" href="#">
                        Forgot Password?
                    </a>
                </div>
            </form>
        )
    }
}
