import * as React from 'react'

export class LoginComponent extends React.Component {
    public render() {
        return(
            <section className="cf mt4 mb3 pa4 pa5-ns pt4-ns bg-white shadow br3">
                <form
                    className="login-form"
                    id="LoginForm"
                    aria-label="Record Expunge Login Form">
                    <IconComponent iconName="logo"/>
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
                            type="submit"
                            className="br2 bg-blue white db w-100 fw6 tc mb4 pv3">
                            Log In
                        </button>
                        <a className="db tc link underline hover-blue" href="#">
                            Forgot your password?
                        </a>
                    </div>
                </form>
            </section>
        )
    }
}
