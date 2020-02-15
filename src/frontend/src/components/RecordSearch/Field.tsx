import React from 'react';

interface Props {
  name: string;
  label: string;
  content: string;
  coda: string;
  divMarkup: string;
  inputMarkup: string;
  onChange: Function; // arg: value
  errorMessage: string;
  required: boolean;
}

interface State {
  hasInput: boolean;
}

export default class Field extends React.Component<Props, State> {
  state: State = {
    hasInput: false
  }
  public static defaultProps = {
    coda: "",
    divMarkup: "",
    inputMarkup: ""
    };

  handleInputChange = (e: React.BaseSyntheticEvent) => {
    let fieldContent : string = e.target.value
    this.setState(
      {
        hasInput: fieldContent.length > 0
      }
      )

    this.props.onChange(e.target.value);
  };

  render() {
    return(
      <div className={"w-100 w-third-ns w-25-l mb3 " + this.props.divMarkup}>
        <label htmlFor={this.props.name} className="db mb1 fw6">
          {this.props.label} <span className= "fw2 f6">{this.props.coda}</span>
        </label>
        <input
          value={this.props.content}
          id={this.props.name}
          type="text"
          className={"w-100 br2 b--black-20 pa3 " + this.props.inputMarkup}
          required
          aria-invalid={false} // this.state.firstNameHasInput}
          aria-describedby={
            this.props.required && this.state.hasInput ? this.props.errorMessage : undefined
          }
          onChange={this.handleInputChange}
        />
      </div>
      )
  }
}
