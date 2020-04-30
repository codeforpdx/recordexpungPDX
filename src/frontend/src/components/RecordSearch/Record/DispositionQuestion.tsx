import React from 'react';
import {answerDisposition} from '../../../redux/search/actions';
import {connect} from 'react-redux';

interface Props {
  answerDisposition: Function;
}

class DispositionQuestion extends React.Component<Props> {

  // TODO: Make display of labels interactive based on radio answer
  //handleRadioChange = (e: React.BaseSyntheticEvent) => {
  //};

  // TODO: Pass through disposition answer
  handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    this.props.answerDisposition();
  };

  render() {
    return (
      <form className="w-100 bt bw3 b--light-purple pa3 pb1" onSubmit={this.handleSubmit}>
        <fieldset className="relative mb4">
            <legend className="fw7 mb2">What is the disposition?</legend>
            <div className="radio">
                <div className="dib">
                    <input id="dis" name="disposition" type="radio" value="dis" />
                    <label htmlFor="dis">Dismissed</label>
                </div>
                <div className="dib">
                    <input id="con" name="disposition" type="radio" value="con" />
                    <label htmlFor="con">Convicted</label>
                </div>
                <div className="dib">
                    <input checked id="rev" name="disposition" type="radio" value="rev" />
                    <label htmlFor="rev">Probation Revoked</label>
                </div>
                <div className="dib">
                    <input id="open" name="disposition" type="radio" value="open" />
                    <label htmlFor="open">Open</label>
                </div>
            </div>
            <label className="db fw6 mt3 mb1" htmlFor="n">Date Convicted <span className="f6 fw4">mm/dd/yyyy</span></label>
            <input className="w5 br2 b--black-20 pa3" id="n" type="text" />
            <label className="db fw6 mt3 mb1" htmlFor="n">Date Probation Revoked <span className="f6 fw4">mm/dd/yyyy</span></label>
            <input className="w5 br2 b--black-20 pa3" id="n" type="text" />
            <button className="db bg-blue white bg-animate hover-bg-dark-blue fw6 br2 pv3 ph4 mt3">Submit</button>
            <div role="alert"></div>
        </fieldset>
      </form>
    )
  }
}

export default connect(
  null,
  {
    answerDisposition: answerDisposition
  }
)(DispositionQuestion);

