import React from "react";

interface Props {
  fieldLabel: string;
  onChange: Function;
  inputId: string;
  value: string;
}

export default class DateField extends React.Component<Props> {
  handleChange = (e: React.BaseSyntheticEvent) => {
    this.props.onChange(e.target.value);
  };

  render() {
    return (
      <div>
        <label className="db fw6 mt3 mb1" htmlFor={this.props.inputId}>
          {this.props.fieldLabel} <span className="f6 fw4">mm/dd/yyyy</span>
        </label>
        <input
          value={this.props.value}
          onChange={this.handleChange}
          className="w5 br2 b--black-20 pa3"
          id={this.props.inputId}
          type="text"
          name="conviction_date"
        />
      </div>
    );
  }
}
