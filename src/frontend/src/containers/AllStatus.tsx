import React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../redux/store';

type Props = {
  loading: boolean;
};

class AllStatus extends React.Component<Props> {
  render() {
    const Spinner = () => (
      <p className="bg-white mv4 pa4 br3 fw6">
        <span className="spinner mr2"></span>Loading your search results...
      </p>
    );
    const NoSearchResults = () => (
      <p className="bg-light-gray mv4 pa4 br3 fw6">No search results found.</p>
    );
    return (
      <div role="status">
        {this.props.loading ? <Spinner /> : <NoSearchResults />}
      </div>
    );
  }
}

const mapStateToProps = (state: AppState) => {
  return {
    loading: state.records.loading
  };
};

export default connect(mapStateToProps)(AllStatus);
