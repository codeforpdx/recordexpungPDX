import React from "react";
import InvalidInputs from "../InvalidInputs";
import { Link } from "react-router-dom";

interface State {
  email: string;
  invalidEmail: boolean;
}

export default class PartnerInterest extends React.Component<State> {
  state = {
    email: "",
    invalidEmail: false,
  };

  validateEmail = (email: string) => {
    return /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w+)+$/.test(email);
  };

  handleSubmit = (e: React.FormEvent) => {
    if (!this.validateEmail(this.state.email)) {
      e.preventDefault();
      this.setState({ invalidEmail: true });
    } else {
      this.setState({ invalidEmail: false });
    }
  };

  render() {
    return (
      <>
        <div className="f6 f5-ns f4-l bg-lightest-blue1">
          <main className="mw7 center ph4 ph5-ns pt5 pb6">
            <section className="lh-copy mb5">
              <h1 className="mw6-l f3 f2-l fw9 lh-solid pr4-l ma0 mb3">
                Provide expungement help with RecordSponge
              </h1>
              <p className="mb3">
                RecordSponge is made for organizations to become expungement
                service providers. We provide both the software and supervision
                by volunteer attorneys – organizations provide the clients and,
                to a large extent, the expungement service.
              </p>
              <p className="mb4">
                We are therefore looking to partner with organizations who have
                contact with many people with criminal records. If you would
                like to learn more about partnering please get in contact below.
              </p>
              <p className="fw9 mb2">More Details</p>
              <p className="mb3">
                You will need an Oregon eCourt Case Information (OECI) account
                to use RecordSponge, otherwise there is no additional charge.
              </p>
              <p className="mb3">
                <a
                  className="link hover-blue bb"
                  href="https://www.courts.oregon.gov/services/online/Pages/ojcin-signup.aspx"
                >
                  You can purchase a subscription here
                </a>
                .
              </p>
              <p className="mb4">
                No OECI account yet?
                <br />
                <Link
                  className="fw7 dark-blue link hover-navy nowrap"
                  to="/demo-record-search"
                  onClick={() => window.scrollTo(0, 0)}
                >
                  Check out the demo version
                  <span className="fas fa-arrow-right pl1"></span>
                </Link>
              </p>
              <p className="pl3 bl bw2 b--blue">
                We ask anyone using the software to be in touch so that we can
                better maintain, scale, and improve our work and community.
                Please complete this contact form even if you already have an
                OECI account.
              </p>
            </section>

            <section>
              <div className="" id="mc_embed_signup">
                {" "}
                {/* This section is based on Mailchimp's generated Embed html*/}
                <form
                  action="https://recordsponge.us10.list-manage.com/subscribe/post?u=8aa8348c6b5b43cde29949c59&amp;id=17b2f23a63"
                  method="post"
                  id="mc-embedded-subscribe-form"
                  name="mc-embedded-subscribe-form"
                  className=""
                  target="_blank"
                  noValidate
                >
                  <div
                    className="bg-gray-blue-2 shadow mv4 pv4 ph4 ph5-l br3"
                    id="mc_embed_signup_scroll"
                  >
                    <h2 className="fw9 mb2">Subscribe</h2>
                    <div className="mb1 dt dt--fixed mc-field-group">
                      <label className="dtc" htmlFor="mce-EMAIL">
                        Email Address (required)
                      </label>
                      <input
                        type="email"
                        name="EMAIL"
                        className="dtc required email"
                        id="mce-EMAIL"
                        onChange={(e: React.BaseSyntheticEvent) => {
                          this.setState({
                            email: e.target.value,
                            invalidEmail: false,
                          });
                        }}
                      />
                    </div>
                    <div className="mb1 dt dt--fixed mc-field-group">
                      <label className="dtc" htmlFor="mce-NAME">
                        Name{" "}
                      </label>
                      <input
                        type="text"
                        name="NAME"
                        className="dtc"
                        id="mce-NAME"
                      />
                    </div>
                    <div className="mb2 dt dt--fixed mc-field-group">
                      <label className="dtc" htmlFor="mce-ORG">
                        Organization{" "}
                      </label>
                      <input
                        type="text"
                        name="ORG"
                        className="dtc"
                        id="mce-ORG"
                      />
                    </div>
                    <div className="mb2 mc-field-group input-group">
                      <input
                        type="checkbox"
                        value="1"
                        name="group[19029][1]"
                        id="mce-group[19029]-19029-0"
                      />
                      <label
                        className="ml2 "
                        htmlFor="mce-group[19029]-19029-0"
                      >
                        I'm interested in a demonstration of the software!
                      </label>
                    </div>
                    <div id="mce-responses" className="clear">
                      <div
                        className="response"
                        id="mce-error-response"
                        visually-hidden
                      ></div>
                      <div
                        className="response"
                        id="mce-success-response"
                        visually-hidden
                      ></div>
                    </div>{" "}
                    {/*This div captures bot signups, according to Mailchimp.*/}
                    <div className="clear">
                      <input
                        type="submit"
                        value="Subscribe"
                        name="subscribe"
                        id="mc-embedded-subscribe"
                        className="button"
                        onClick={this.handleSubmit}
                      />
                    </div>
                  </div>
                </form>
                <InvalidInputs
                  conditions={[this.state.invalidEmail]}
                  contents={[<span>A valid email address is required </span>]}
                />
              </div>
            </section>
          </main>
        </div>
      </>
    );
  }
}
