import React from "react";

class PartnerInterest extends React.Component {
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
                RecordSponge is made for organizations to become expungement service providers. We provide both the software and supervision by volunteer attorneys – organizations provide the clients and, to a large extent, the expungement service.
              </p>
              <p className="mb4">
                We are therefore looking to partner with organizations who have contact with many people with criminal records. If you would like to learn more about partnering please get in contact below.
              </p>
              <p className="fw9 mb2">
                More Details
              </p>
              <p className="mb3">
                You will need an Oregon eCourt Case Information (OECI) account to use RecordSponge, otherwise there is no additional charge.
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
                <br/>
                <a 
                  className="fw7 dark-blue link hover-navy nowrap" 
                  href="/demo-record-search"
                >
                  Check out the demo version
                  <span className="fas fa-arrow-right pl1"></span>
                </a>
              </p>
              <p className="pl3 bl bw2 b--blue">
                We ask anyone using the software to be in touch so that we can better maintain, scale, and improve our work and community. Please complete this contact form even if you already have an OECI account.
              </p>
            </section>
            <section>
              Embedded Mailchimp form goes here, or we could just link to it.
            </section>
          </main>
        </div>
      </>
    );
  }
}

export default PartnerInterest;
