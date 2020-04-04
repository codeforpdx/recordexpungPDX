import React from 'react';
import { AliasData, AliasFieldNames } from './types';
import Field from './Field';


interface Props {
  ind: number;
  aliasData: AliasData;
  onChange: Function; // requires 2 arguments: the fieldName and fieldValue
  onRemoveClick: Function;
  hideRemoveButton: boolean;
}

interface State {
  firstNameHasInput: boolean;
  lastNameHasInput: boolean;
}

export default class Alias extends React.Component<Props, State> {
  state: State = {
    firstNameHasInput: false, // Initially set to false to ensure aria-invalid attribute is rendered.
    lastNameHasInput: false
  }

  handleFieldChange = (fieldName: AliasFieldNames, value: string) => {
    this.props.onChange(fieldName, value);
  };

  render() {
    return (
      <div className="flex flex-wrap items-end">
        <Field
          name="firstName"
          label="First Name"
          content={this.props.aliasData.first_name}
          inputMarkup="br-0-ns br--left-ns"
          onChange = {(fieldValue: string) => {this.handleFieldChange("first_name", fieldValue)}}
          required={true}
          errorMessage="name_msg"
          />
        <Field
          name="middleName"
          label="Middle Name"
          content={this.props.aliasData.middle_name}
          inputMarkup="br0-ns"
          coda="(Optional)"
          onChange = {(fieldValue: string) => {this.handleFieldChange("middle_name", fieldValue)}}
          required={false}
          errorMessage="name_msg"
          />
        <Field
          name="lastName"
          label="Last Name"
          content={this.props.aliasData.last_name}
          inputMarkup="bl-0-ns br--right-ns"
          onChange = {(fieldValue: string) => {this.handleFieldChange("last_name", fieldValue)}}
          required={true}
          errorMessage="name_msg"
          />
        <Field
          divMarkup="pl2-l"
          name="birthDate"
          label="Date of Birth"
          content={this.props.aliasData.birth_date}
          coda="mm/dd/yyyy"
          onChange = {(fieldValue: string) => {this.handleFieldChange("birth_date", fieldValue)}}
          required={false}
          errorMessage="dob_msg"
          />
        <div className={(this.props.hideRemoveButton ? "visually-hidden " : "" ) +
        "flex items-center pb1 mb3 ml3-ns ml0-l"}>
        { // TODO: The #-Results label is "visually-hidden" until we update the endpoint
          // to support this feature.
        }
          <span className=" visually-hidden fw5 bl bw2 b--blue bg-gray-blue-2 pa2 pr3 mr2 mb2">1 Result</span>
          <button
            className="br2 bg-gray-blue-2 link hover-dark-blue mid-gray fw5 pa2 mb2"
            onClick={() => {this.props.onRemoveClick()}}
            type="button"
          >

            <i className="fas fa-times-circle pr1"></i>Remove
            {// aria-hidden={"true"} this as a prop on the <i>?
            }
          </button>
        </div>
      </div>
      )
  }
}