import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../redux/store';
import Spinner from '../components/Spinner';
import NoSearchResults from '../components/NoSearchResults';

type Props = {
  loading: boolean;
};

class AllStatus extends React.Component<Props> {
  render() {
    return (
      <section>
        {this.props.loading ? <Spinner /> : <NoSearchResults />}
      </section>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    loading: state.records.loading
  };
};

export default connect(mapStateToProps)(AllStatus);
