import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../redux/store';

interface Props {
  isAuthenticated: boolean;
}

export class Footer extends React.Component<Props> {
  public render() {
    return this.props.isAuthenticated ? (
      <footer className="mt6 pt4 pb5 ph4 bg-white">
        <a className="link underline hover-blue" href="/">
          Terms of use
        </a>
      </footer>
    ) : null;
  }
}

const mapStateToProps = (state: AppState) => ({
  isAuthenticated: state.system.loggedIn
});

export default connect(mapStateToProps)(Footer);
