import React from "react";
import { HashLink as Link } from "react-router-hash-link";
import EditingGuide from "./EditingGuide";

class Manual extends React.Component {
  componentDidMount() {
    document.title = "Manual - RecordSponge";
  }

  render() {
    return (
      <>
        <main className="flex-l mw8 center ph4 mt5">
          <div className="mw8 center ph4 visually-hidden">
            <h1 className="f3 fw6 mv4">Manual</h1>
          </div>
          <nav
            className="shrink-none order-2 self-start sticky-l w5 bg-white shadow pa4 mt4 ml5-l"
            aria-label="Manual"
          >
            <ul className="list">
              <li className="mb3">
                <a href="#intro" className="link hover-blue">
                  Introduction
                </a>
              </li>
              <li className="mb3 pb1">
                <a href="#generalinfo" className="link hover-blue">
                  General Info
                </a>
              </li>
              <li className="bt b--light-gray pt3 mb3 ">
                <a href="#overview" className="link hover-blue">
                  Use RecordSponge
                </a>
              </li>
              <li className="mb3 ml3">
                <a href="#assumption" className="link hover-blue">
                  Assumption
                </a>
              </li>
              <li className="mb3 ml3">
                <a href="#search" className="link hover-blue">
                  Search
                </a>
              </li>
              <li className="ml3">
                <a href="#file" className="link hover-blue">
                  File for Expungement
                </a>
              </li>
            </ul>
          </nav>
          <article className="order-1 lh-copy">
            <section className="mb5">
              <h2 className="f2 fw9 mb3 mt4" id="intro">
                Introduction
              </h2>
              <p className="mb3">
                RecordSponge is a volunteer-built web application used to
                facilitate the expungement process in Oregon. It is a
                collaboration between{" "}
                <a className="bb hover-blue" href="https://www.codepdx.org">
                  Code PDX
                </a>{" "}
                and{" "}
                <a className="bb hover-blue" href="https://www.qiu-qiulaw.com">
                  Qiu-Qiu Law
                </a>
                . The codebase is published under an open source{" "}
                <a
                  className="bb hover-blue"
                  href="https://opensource.org/licenses/MIT"
                >
                  MIT license
                </a>
                .
              </p>
              <p className="mb3">
                This Manual explains how RecordSponge is used and the process of
                expunging records. It is also published under an open source MIT
                license.
              </p>
              <p className="mb3">
                As of this writing, it is likely that fewer than{" "}
                <a
                  className="bb hover-blue"
                  href="https://www.aclu.org/press-releases/trenton-marijuana-hearing-advocates-call-automatic-expungement-legalization"
                >
                  2%
                </a>{" "}
                of Oregonians who are eligible to expunge their records have
                done so. Let’s get to work.
              </p>
            </section>
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="generalinfo">
                General Info
              </h2>
              <p className="mb3">
                Every State has different expungement rules.{" "}
                <a
                  className="bb hover-blue"
                  href="https://olis.oregonlegislature.gov/liz/2021R1/Measures/Overview/SB397"
                >
                  Recent changes
                </a>{" "}
                to Oregon's expungement law make more types of criminal records
                eligible than ever before, and on a much faster timeline.
                Nevertheless, the complexity of the expungement statutes, ORS{" "}
                <a
                  className="bb hover-blue"
                  href="https://www.oregonlaws.org/ors/137.225"
                >
                  137.225
                </a>{" "}
                and{" "}
                <a
                  className="bb hover-blue"
                  href="https://www.oregonlaws.org/ors/137.226"
                >
                  137.226
                </a>
                . pose a significant barrier for people seeking expungements on
                their own. Few organizations outside of the metropolitan area
                are equipped to perform expungement services, and the market
                rate to hire an attorney is over $1,400 <em>per case</em>.
              </p>
              <p className="mb3">
                RecordSponge is and always will be free to use.
              </p>
              <p className="mb4">
                If you would like to use RecordSponge, please contact
                michael@qiu-qiulaw.com.
              </p>
              <div className="bg-gray-blue-2 shadow br3 pa3 mb4">
                <h3 className="fw7 mb2" id="juvenile">
                  Note on Juvenile Records
                </h3>
                <p className="mb3">
                  RecordSponge only deals with adult criminal records. Juvenile
                  records are eligible on a different basis,{" "}
                  <a
                    className="bb hover-blue"
                    href="https://www.osbar.org/public/legalinfo/1081_ClearingRecord.htm"
                  >
                    more info here
                  </a>
                  .
                </p>
                <p className="mb2">
                  There are generally two ways to expunge a juvenile record:
                </p>
                <ol className="ml4">
                  <li className="mb2">
                    The juvenile record is 5+ years old and the client hasn’t
                    had subsequent criminal cases.
                  </li>
                  <li className="mb2">
                    The client requests a hearing and demonstrates that it would
                    be in the “best interests of justice” to expunge the record.
                  </li>
                </ol>
              </div>
            </section>
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="overview">
                Using RecordSponge
              </h2>
              <h3 className="fw7 mb2">Overview</h3>
              <p className="mb3">
                We ask anyone using the software to be in touch so that we can
                better maintain, scale, and improve our work and community.{" "}
                <Link className="bb hover-blue" to="/partner-interest">
                  Please complete this contact form
                </Link>
                .
              </p>
              <ol className="ml4">
                <li className="mb3">
                  <p className="mb2">Log in and search records</p>
                  <ul className="fw4 ml4">
                    <li className="mb2">
                      You will need an Oregon eCourt Case Information (OECI)
                      account to search for criminal records.{" "}
                      <a
                        className="bb hover-blue"
                        href="https://www.courts.oregon.gov/services/online/Pages/ojcin-signup.aspx"
                      >
                        You can purchase a subscription here
                      </a>
                      .
                    </li>
                    <li className="mb2">
                      No OECI account yet? The demo version has all the same
                      features besides the ability to search the OECI database.
                      There are examples provided or you can even enter records
                      manually.{" "}
                      <Link className="bb hover-blue" to="/demo-record-search">
                        Check out the demo
                      </Link>
                      .
                    </li>
                  </ul>
                </li>
                <li className="mb3">
                  Ensure that{" "}
                  <a className="bb-dotted-2 hover-blue" href="#assumption">
                    Assumption
                  </a>{" "}
                  is met
                </li>
                <li className="mb3">
                  <a className="bb-dotted-2 hover-blue" href="#search">
                    Search records
                  </a>{" "}
                  by name and date of birth
                </li>
                <li className="mb3">
                  Confirm positive search results with Michael:
                  michael@qiu-qiulaw.com
                </li>
                <li className="mb3">
                  <a className="bb-dotted-2 hover-blue" href="#file">
                    Complete forms
                  </a>
                  ,{" "}
                  <a className="bb-dotted-2 hover-blue" href="#fingerprints">
                    obtain fingerprints
                  </a>
                </li>
                <li className="mb3">
                  Instruct clients to{" "}
                  <a className="bb-dotted-2 hover-blue" href="#filepaperwork">
                    file paperwork
                  </a>{" "}
                  in appropriate courts
                </li>
                <li className="mb3">
                  Mail in fingerprints to Oregon State Police
                </li>
              </ol>
            </section>
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="assumption">
                Assumption
              </h2>
              <p className="fw7 mb3">
                Before delivering expungement analysis, ensure that this
                assumption is met.
              </p>
              <p></p>
              <p className="mb3">
                RecordSponge only has access to online records of Oregon’s
                Circuit courts. However, having an open case or a conviction{" "}
                <strong>anywhere</strong> within the last 7 years could affect
                eligibility. The accuracy of the expungement analysis depends on
                these assumptions:
              </p>
              <ol className="ml4 mb4">
                <li className="fw7 mb3">
                  The client does not have any open cases in any court in the
                  United States.
                  <ul className="fw4 list">
                    <li className="mt1 mb2">
                      A person with an open case is not eligible. For example, a
                      person with a warrant is ineligible.
                    </li>
                  </ul>
                </li>
                <li className="fw7 mb3">
                  The client does not, within the last 7 years, have cases which
                  are:
                  <ol className="fw4 mt1 mb3 ml4">
                    <li className="mb2">previously expunged</li>
                    <li className="mb2">Federal</li>
                    <li className="mb2">from States besides Oregon</li>
                    <li className="mb2">from Municipal Courts</li>
                  </ol>
                  <ul className="list fw4 mb3">
                    <li className="mb3">
                      Cases closed more than 7 years ago, in any court, do not
                      affect eligibility.
                    </li>
                    <li className="mb3">
                      Traffic ticket sdo not count. However, convictions for
                      misdemeanor or felony traffic cases, such as Driving While
                      Suspended, count.
                    </li>
                    <li className="mb3">
                      Previously expunged cases affect expungement eligibility.
                      Accordingly, RecoredSponge’s analysis may not be accurate
                      if a person has a case previously expunged, and that case
                      is from the last 7 years. Note that this rule does not
                      prevent a person from filing for expungement multiple
                      times within the same 7 year period.
                    </li>
                    <li className="mb3">
                      Again, beware of convictions for misdemeanor/felony
                      traffic violations, e.g. Beaverton Municipal Court (not
                      Washington Circuit Court), Troutdale Municipal Court,
                      Medford Municipal Court, These courts generally handle
                      low-level crimes and especially traffic crimes. We only
                      need to worry about misdemeanor and felonies, including
                      for Driving While Suspended.
                    </li>
                  </ul>
                </li>
              </ol>
              <div className="bg-gray-blue-2 shadow br3 pa3 mb4">
                <p className="fw7 mb2">Questions to always ask</p>
                <ol className="ml4">
                  <li className="mb2">
                    Does the client have any open charges in other States or in
                    municipal court?
                  </li>
                  <li className="mb2">
                    Does the client have any criminal convictions in States
                    besides Oregon from the last seven years?
                  </li>
                </ol>
              </div>
              <p>
                If the Assumption is not met, but you would still like to
                conduct an analysis, or if you have any questions about this
                section, please contact michael@qiu-qiulaw.com.
              </p>
            </section>
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="search">
                Search
              </h2>
              <p className="mb3">
                Check out a quick video demonstrating how to search:
              </p>
              <div className="aspect-ratio aspect-ratio--16x9 mb4 ba bw2 b--black-10">
                <iframe
                  className="aspect-ratio--object"
                  title="Search records on RecordSponge"
                  width={560}
                  height={315}
                  src="https://www.youtube-nocookie.com/embed/l8MBVgQWhJI?cc_load_policy=1&rel=0"
                  frameBorder={0}
                  allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              </div>
              <p className="mb3">
                Enter the person’s first and last name and date of birth into
                the search bar.
              </p>
              <p className="mb3">
                If the person has a previous name, alias, maiden name, etc.,
                select the option to “Add Alias” and fill out another search.
              </p>
              <p className="mb3">
                For example, for a search Jane Smith nee Miller, DOB 1/1/1990,
                search Jane Smith, 1/1/1990; then, Add Alias of Jane Miller,
                1/1/1990.
              </p>
              <div className="bg-gray-blue-2 shadow br3 pa3 mb5">
                <h3 className="fw7 mb2">Search Tips</h3>
                <p className="mb3">
                  Courts often input incorrect information, and certain cases
                  will not show all results. If an anticipated case does not
                  show, also perform a search of the person’s first initial
                  followed by a *, the person’s first three letters of their
                  last name followed by a *, and their date of birth. For
                  example, a search for Michael Zhang with birthdate 5/9/1993
                  would be M*, Zhang*, 5/9/1993.
                </p>
                <p className="mb2">
                  Regarding names with two letter starters, e.g. Mc, De, Di, the
                  online court system will inconsistently input the two-letter
                  starter as following with a space or no space. For example,
                  McDonald could be input as Mc Donald (with a space) or
                  McDonald (without a space). You would therefore need to search
                  under both forms of the name to see which the court system has
                  used.
                </p>
              </div>
              <h3 className="f4 fw7 mb2" id="searchresults">
                Search Results
              </h3>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb3">Eligible Now</h4>
                <div className="green bg-washed-green fw6 pv2 ph3 mb3 dib br3">
                  Eligible
                </div>
                <p className="mb3">
                  The specific charge is eligible for expungement if{" "}
                  <a className="bb-dotted-2 hover-blue" href="#assumption">
                    Assumption
                  </a>{" "}
                  is true.
                </p>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb3">Eligible on a future date</h4>
                <div className="dark-blue bg-washed-blue fw6 pv2 ph3 mb3 dib br3">
                  Eligible Aug 26, 2024
                </div>
                <p className="mb3">
                  The specific charge is eligible for expungement on the date
                  specified. This is also conditional on{" "}
                  <a className="bb-dotted-2 hover-blue" href="#assumption">
                    Assumption
                  </a>{" "}
                  being true. Having other cases could push out the eligibility
                  date further.
                </p>
                <div className="dark-blue bg-washed-blue fw6 pv2 ph3 mb3 dib br3">
                  Eligibility date dependent on open charge: Eligible Jun 12,
                  2022 or 7 years from conviction of open charge
                </div>
                <p className="mb3">
                  If there is an open charge, the affected charges will show
                  multiple possible eligibity timeframes. Once the open charge
                  is closed then the analysis will update. You can edit the open
                  charges to see how the eligibility will be affected.
                </p>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb3">Further Analysis Needed</h4>
                <div className="purple bg-washed-purple fw6 pv2 ph3 mb3 dib br3">
                  Needs More Analysis
                </div>
                <p className="mb3">
                  Sometimes, there is not enough information on the OECI website
                  to determine whether or not a case is eligible. RecordSponge
                  will then prompt the user to answer questions, and the
                  analysis will update based on those answers.
                </p>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb3">Restitution Owed</h4>
                <div className="dark-blue bg-washed-blue fw6 pv2 ph3 mb3 dib br3">
                  Ineligible If Restitution Owed
                </div>
                <p className="mb3">
                  There is not enough information on the OECI website to
                  determine if Restitution is owed on this Case. Cases under
                  this heading will not print unless updated to reflect that
                  Restitution is not owed.
                </p>
                <p className="mb3">
                  RecordSponge can detect if Restitution is discussed in a
                  Case's history of events, but OECI does not always show
                  whether Restitution is still owed.
                </p>
                <p className="mb3">
                  Ask the client directly if they currently owe Restitution on
                  the Case. If Restitution has been paid, Edit the Case to
                  remove this status:
                </p>
                <ol>
                  <li className="ml3">
                    Select “Enable Editing” (see the{" "}
                    <Link className="bb hover-blue" to="#editing">
                      editing guide
                    </Link>{" "}
                    below)
                  </li>
                  <li className="ml3">
                    Click the editing pencil associated with the Case (not the
                    Charge)
                  </li>
                  <li className="ml3">
                    Select “False” under “Restitution Owed"
                  </li>
                </ol>
              </div>
              <div className="bg-white shadow pa3 mb4">
                <h4 className="fw7 mb3">Ineligible</h4>
                <div className="red bg-washed-red fw6 pv2 ph3 mb3 dib br3">
                  Ineligible
                </div>
                <p className="mb3">
                  The specific charge is not eligible under the current law
                  because it is not “type-eligible.” The reason why the charge
                  is not type-eligible is different for each charge. This is not
                  conditional on the Assumption.
                </p>
              </div>
              <section className="mb4" id="editing">
                <EditingGuide />
              </section>
              <p className="mb3">
                After producing a complete record analysis and verifying all the
                information in it is correct, proceed to next steps:
              </p>
            </section>
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="file">
                File for Expungement
              </h2>

              <h3 className="f4 fw7 lh-title mb2">
                Complete expungement paperwork using RecordSponge
              </h3>
              <p className="mb3">
                If a client has eligible charges, the Summary panel will display
                a button to Generate Paperwork. Click the button and you will be
                directed to input identifying information. Complete all fields.
              </p>
              <p className="mb4">
                After you input the information, RecordSponge will generate a
                .zip file with PDFs of the expungement paperwork for all of the
                charges, with one PDF file for each case that has eligible
                charges.
              </p>
              <p className="mb4">
                RecordSponge will also generate a Request form to Oregon State
                Police. You will need to complete this form manually and mail a
                completed copy to Oregon State Police at:
                <span className="db pt2">
                  Oregon State Police, CJIS – Unit 11
                  <br />
                  ATTN: SET ASIDE
                  <br />
                  P.O. Box 4395
                  <br />
                  Portland, OR 97208-4395
                  <br />
                </span>
              </p>
              <h3 className="f4 fw7 mb2" id="fingerprints">
                Obtain Fingerprints
              </h3>
              <p className="mb3">
                Obtain fingerprints printed or inked directly onto cardstock.
                Digital fingerprints are not accepted as part of this process.
                Fingerprints printed onto cardstock can be obtained at sheriff's
                offices or fingerprinting services.
              </p>
              <p className="mb3">
                Another option is to do it yourself with the following
                materials:
              </p>
              <ul className="ml4 mb3">
                <li className="mb2">
                  Lee Inkless Fingerprint Pad (available on Amazon), $17 for 3
                  pack which can serve several hundred people
                </li>
                <li className="mb2">
                  Fingerprint Cards, Applicant FD-258 (available on Amazon), $21
                  for a 50 pack
                </li>
              </ul>
              <h3 className="f4 fw7 mb2" id="OSPform">
                Mail Fingerprints to OSP
              </h3>
              <p className="mb3">
                Included in your expungement packet should be a form titled:
                "Oregon State Police REQUEST FOR SET ASIDE CRIMINAL RECORD
                CHECK."
              </p>
              <p className="mb3">
                Fill out the sections:
                <br />
                1. "Other Names You are Known By"
                <br />
                2. "Circuit or Municipal Court"
                <br />
                3. Check the box corresponding to whether you are seeking an
                expungement for a conviction or only arresets.
              </p>
              <p className="mb3">
                If you are seeking expungement of at least one conviction, you
                will need to include a check or money order made out to "Oregon
                State Police" for $33.
              </p>
              <h3 className="f4 fw7 mb2" id="filepaperwork">
                File Paperwork
              </h3>
              <ul className="ml4 mb3">
                <li className="mb2">
                  You will need to file the paperwork with the courthouse in
                  each county in which you have cases you wish to expunge. File
                  with the Clerk of court. There should be no filing fee.
                </li>
                <li className="mb2">Request two copies from the Clerk.</li>
                <li className="mb2">
                  Serve the District Attorney’s office with one of these copies.
                </li>
              </ul>
              <h3 className="f4 fw7 mb2">Next Steps</h3>
              <ul className="ml4 mb3">
                <li className="mb2">
                  In the vast majority of cases, your expungement will process
                  without objection from the State. <em>If</em> you receive an
                  objection from the District Attorney, please email us at
                  michael@qiu-qiulaw.com immediately so that we can assist you.
                  Even if we do not represent you in court, we will still be
                  able to assist you.
                </li>
                <li className="mb2">
                  By law, the District Attorney is required to respond within
                  four months after you file. If you receive communication
                  during this time from the District Attorney that you would
                  like to review with us, please email us at roe@qiu-qiulaw.com
                </li>
                <li className="mb2">
                  Once your expungement is processed, you will receive paper
                  confirmation from the court informing you that your record was
                  expunged. You should keep copies of this confirmation and make
                  electronic copies – obtaining copies of expunged documents is
                  extremely costly.
                </li>
                <li className="mb2">
                  After your expungement has been processed, ensure that
                  background check companies receive notice. Expungement
                  Clearinghouse is a free service that notifies major background
                  checking companies of your expungement. This is available at{" "}
                  <a
                    href="https://www.continuingjustice.org/our-projects/criminal-database-update/"
                    className="bb hover-blue"
                  >
                    https://www.continuingjustice.org/our-projects/criminal-database-update/
                  </a>
                </li>
              </ul>
            </section>
          </article>
        </main>
      </>
    );
  }
}

export default Manual;
