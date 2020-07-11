import React from "react";
import history from "../../service/history";
import { downloadExpungementPacket } from "../../redux/search/actions";
import { connect } from "react-redux";
import { AppState } from "../../redux/store";
import { AliasData } from "../RecordSearch/SearchPanel/types";

interface Props {
  aliases: AliasData[];
  downloadExpungementPacket: Function;
}

interface State {
  name: string;
  dob: string;
  mailingAddress: string;
  phoneNumber: string;
  city: string;
  state: string;
  zipCode: string;
}

class UserForm extends React.Component<Props, State> {
  private buildName = () => {
    if (this.props.aliases.length > 0) {
      const firstAlias = this.props.aliases[0];
      return `${firstAlias.first_name} ${firstAlias.middle_name} ${firstAlias.last_name}`;
    } else {
      return "";
    }
  };

  private buildDob = () => {
    if (this.props.aliases.length > 0) {
      const firstAlias = this.props.aliases[0];
      return firstAlias.birth_date;
    } else {
      return "";
    }
  };

  public state: State = {
    name: this.buildName(),
    dob: this.buildDob(),
    mailingAddress: "",
    phoneNumber: "",
    city: "",
    state: "",
    zipCode: "",
  };

  public handleChange = (e: React.BaseSyntheticEvent) => {
    // See https://github.com/DefinitelyTyped/DefinitelyTyped/issues/26635 for why we're
    // using the "any" type.
    this.setState<any>({
      [e.target.id]: e.target.value,
    });
  };

  public handleSubmit = (e: React.BaseSyntheticEvent) => {
    e.preventDefault();
    return this.props.downloadExpungementPacket(
      this.state.name,
      this.state.dob,
      this.state.mailingAddress,
      this.state.phoneNumber,
      this.state.city,
      this.state.state,
      this.state.zipCode
    );
  };

  public componentDidMount() {
    if (!(this.props.aliases.length > 0)) {
      history.push("/record-search");
    }
  }

  public render() {
    return (
      <>
        <main className="mw6 ph2 center">
          <section className="cf mt4 mb3 pa3 pa4-l bg-white shadow br3">
            <h1 className="mb4 f4 fw6">User Information</h1>
            <form onSubmit={this.handleSubmit} noValidate={true}>
              <legend className="visually-hidden">User Information</legend>
              <div className="mb4">
                <label htmlFor="name" className="db mb2 fw6">
                  Full Name
                </label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  required={true}
                  className="w-100 pa3 br2 b--black-20"
                  onChange={this.handleChange}
                  value={this.state.name}
                />
              </div>
              <div className="mb4">
                <label htmlFor="dob" className="db mb2 fw6">
                  Date of Birth
                </label>
                <input
                  id="dob"
                  name="dob"
                  type="text"
                  required={true}
                  className="w-100 pa3 br2 b--black-20"
                  onChange={this.handleChange}
                  value={this.state.dob}
                />
              </div>
              <div className="mb4">
                <label htmlFor="mailingAddress" className="db mb2 fw6">
                  Mailing Address
                </label>
                <input
                  id="mailingAddress"
                  name="mailingAddress"
                  type="text"
                  required={true}
                  className="w-100 pa3 br2 b--black-20"
                  onChange={this.handleChange}
                  value={this.state.mailingAddress}
                />
              </div>
              <div className="mb4">
                <label htmlFor="phoneNumber" className="db mb2 fw6">
                  Phone Number
                </label>
                <input
                  id="phoneNumber"
                  name="phoneNumber"
                  type="text"
                  required={true}
                  className="w-100 pa3 br2 b--black-20"
                  onChange={this.handleChange}
                  value={this.state.phoneNumber}
                />
              </div>
              <div className="mb4">
                <label htmlFor="city" className="db mb2 fw6">
                  City
                </label>
                <input
                  id="city"
                  name="city"
                  type="text"
                  required={true}
                  className="w-100 pa3 br2 b--black-20"
                  onChange={this.handleChange}
                  value={this.state.city}
                />
              </div>
              <div className="mb4">
                <label htmlFor="state" className="db mb2 fw6">
                  State
                </label>
                <input
                  id="state"
                  name="state"
                  type="text"
                  required={true}
                  className="w-100 pa3 br2 b--black-20"
                  onChange={this.handleChange}
                  value={this.state.state}
                />
              </div>
              <div className="mb4">
                <label htmlFor="zipCode" className="db mb2 fw6">
                  Zip code
                </label>
                <input
                  id="zipCode"
                  name="zipCode"
                  type="text"
                  required={true}
                  className="w-100 pa3 br2 b--black-20"
                  onChange={this.handleChange}
                  value={this.state.zipCode}
                />
              </div>
              <button className="bg-blue white bg-animate hover-bg-dark-blue fw6 db w-100 br2 pv3 ph4 mb4 tc">
                Download Expungement Packet
              </button>
            </form>
          </section>
        </main>
      </>
    );
  }
}

const mapStateToProps = (state: AppState) => ({
  aliases: state.search.aliases,
});

export default connect(mapStateToProps, { downloadExpungementPacket })(
  UserForm
);
