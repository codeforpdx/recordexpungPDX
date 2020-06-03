import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../../../redux/store';
import LoadingSpinner from '../../LoadingSpinner';
import NoSearchResults from './NoSearchResults';

type Props = {
  loading: string;
};

class Status extends React.Component<Props> {
  render() {
    return (
      <section>
        {this.props.loading === "loading" ? (
          <LoadingSpinner inputString={'your search results'} />
        ) : (
          <NoSearchResults />
        )}
      </section>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    loading: state.search.loading
  };
};

export default connect(mapStateToProps)(Status);
