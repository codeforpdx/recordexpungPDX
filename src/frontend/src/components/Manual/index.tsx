import React from "react";
import { HashLink as Link } from "react-router-hash-link";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@reach/disclosure";
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
                <a href="#assumption1" className="link hover-blue">
                  Assumption 1
                </a>
              </li>
              <li className="mb3 ml3">
                <a href="#search" className="link hover-blue">
                  Search
                </a>
              </li>
              <li className="mb3 ml3">
                <a href="#assumption2" className="link hover-blue">
                  Assumption 2
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
                <a
                  className="bb hover-blue"
                  href="https://brigade.codeforamerica.org/brigades/Code-for-PDX"
                >
                  Code for PDX
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
                Every State has different expungement rules. Oregon’s adult
                expungement law is ORS{" "}
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
                . These statutes are 2,000+ words long and are often misleading
                and contradictory. As a result of this complexity, the market
                rate for lawyers to perform expungement services is over $1,400{" "}
                <em>per case</em>.
              </p>
              <p className="mb3">
                And so we created RecordSponge to greatly increase access to
                expungement by automating the legal analysis.
              </p>
              <p className="mb4">
                We still need partners to administer RecordSponge. Please
                contact michael@qiu-qiulaw.com if you would like to set up
                RecordSponge at your organization.
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
                Use RecordSponge
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
                  <a className="bb-dotted-2 hover-blue" href="#assumption1">
                    Assumption 1
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
                  Ensure that{" "}
                  <a className="bb-dotted-2 hover-blue" href="#assumption2">
                    Assumption 2
                  </a>{" "}
                  is met for eligible records (if any)
                </li>
                <li className="mb3">
                  Confirm positive search results with Michael:
                  michael@qiu-qiulaw.com
                </li>
                <li className="mb3">
                  Use the{" "}
                  <Link
                    className="bb hover-blue"
                    to="/appendix"
                    onClick={() => window.scrollTo(0, 0)}
                  >
                    Appendix
                  </Link>{" "}
                  or search online for expungement forms
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
              </ol>
            </section>
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="assumption1">
                Assumption 1
              </h2>
              <p className="fw7 mb3">
                Before delivering expungement analysis, ensure that this
                assumption is met.
              </p>
              <p></p>
              <p className="mb3">
                RecordSponge only has access to online records of Oregon’s
                Circuit courts. However, having an open case or a conviction{" "}
                <strong>anywhere</strong> within the last 10 years makes a
                person ineligible (until the conviction is 10 years old). The
                accuracy of the expungement analysis depends on the assumptions:
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
                  The client does not, within the last 10 years, have cases
                  which are:
                  <ol className="fw4 mt1 mb3 ml4">
                    <li className="mb2">previously expunged</li>
                    <li className="mb2">Federal</li>
                    <li className="mb2">from States besides Oregon</li>
                    <li className="mb2">from Municipal Courts</li>
                  </ol>
                  <ul className="list fw4 mb3">
                    <li className="mb3">
                      Cases closed more than 10 years ago, in any court, do not
                      affect RecordSponge’s analysis.
                    </li>
                    <li className="mb3">
                      Cases for traffic infractions do not count. However,
                      convictions for misdemeanor or felony traffic cases, such
                      as Driving While Suspended, count.
                    </li>
                    <li className="mb3">
                      Oregon expungement law considers previously expunged
                      cases. Accordingly, RecoredSponge’s analysis may not be
                      accurate if a person has a case previously expunged, and
                      that case is from the last ten years. Note that this rule
                      does not prevent a person from filing for expungement
                      multiple times within the same ten year period.
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
                <li className="fw7 mb3" id="paybalances">
                  The client does not owe money to the State, including
                  probation fees, child support, traffic tickets.
                  <ul className="list fw4 mt1">
                    <li className="mb2">
                      A personal is not eligible for expungement if they owe
                      money in the case they are trying to expunge. If a person
                      owes money on any matter - including traffic violations,
                      child support, and probation supervision - district
                      attorneys will object in at least the following counties:
                      Multnomah, Douglas. The Balance shows money the person
                      owes to the Circuit courts, but does not show balances in
                      Municipal courts, or for child support, or probation
                      supervision fees. It does not matter if a debt is “in
                      collections.”
                    </li>
                    <li className="mb3">
                      Court debt can be paid directly to the clerk’s window in
                      the Circuit Court in which the debt is owed.
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
                    besides Oregon from the last ten years?
                  </li>
                  <li className="mb2">
                    Does the client owe child support, probation supervision
                    fees, or fines and fees to municipal courts?
                  </li>
                </ol>
              </div>
              <p>
                If Assumption 1 is not met, but you would still like to conduct
                an analysis, or if you have any questions about this section,
                please contact michael@qiu-qiulaw.com.
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
                  <a className="bb-dotted-2 hover-blue" href="#assumption1">
                    Assumption 1
                  </a>{" "}
                  and{" "}
                  <a className="bb-dotted-2 hover-blue" href="#assumption2">
                    Assumption 2
                  </a>{" "}
                  are true.
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
                  <a className="bb-dotted-2 hover-blue" href="#assumption1">
                    Assumption 1
                  </a>{" "}
                  being true. Having other cases could push out the eligibility
                  date further.
                </p>
                <div className="dark-blue bg-washed-blue fw6 pv2 ph3 mb3 dib br3">
                  Eligibility date dependent on open charge: Eligible Jun 12,
                  2022 or 10 years from conviction of open charge
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
              <div className="bg-white shadow pa3 mb4">
                <h4 className="fw7 mb3">Ineligible</h4>
                <div className="red bg-washed-red fw6 pv2 ph3 mb3 dib br3">
                  Ineligible
                </div>
                <p className="mb3">
                  The specific charge is not eligible under the current law
                  because it is not “type-eligible.” The reason why the charge
                  is not type-eligible is different for each charge. This is not
                  conditional on the assumptions.
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
              <h2 className="f2 fw9 mb3" id="assumption2">
                Assumption 2
              </h2>
              <p className="mb3">
                If a charge is marked as eligible, it is eligible for
                expungement if the following are true:
              </p>
              <ol className="ml4 mb4">
                <li className="mb3">
                  <p className="fw7 mb1">
                    The person does not owe money on the case.
                  </p>
                  <p>
                    This assumption is redundant with an assumption needed for
                    correct Analysis, but bears repeating here. A charge is not
                    eligible for expungement if they owe money on the case,
                    including for associated probation fees. RecordSponge can
                    find court-imposed fines and fees, but does not have access
                    to probation fines and fees.
                  </p>
                </li>
                <li className="mb3">
                  <p className="fw7 mb1">
                    The charge is not associated with a separate case which led
                    to a conviction which is not eligible for expungement.
                  </p>
                  <p>
                    If a case is dismissed, but then re-charged as a different
                    case (including in Federal court), you must file for
                    expungement on both cases at the same time. If the
                    re-charged case is not eligible, then neither is the case
                    that is associated with it. A common situation is for a
                    State-level drug-manufacturing case to be dismissed so that
                    it can be re-charged at the Federal level. In this case, the
                    State-level dismissal is not eligible because Federal crimes
                    generally are not eligible for expungement.
                  </p>
                </li>
                <li className="mb3">
                  <p className="fw7 mb1">
                    The charge did not result in a probation revocation. If the
                    case did result in a revocation, that revocation was at
                    least ten years ago.
                  </p>
                  <p>
                    RecordSponge can generally tell if a probation revocation
                    occurred. However, the online courts are inconsistent in
                    displaying this information. Ensure that a probation
                    revocation did not occur within the last ten years by asking
                    the client.
                  </p>
                </li>
              </ol>
            </section>
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="file">
                File for Expungement
              </h2>

              <h3 className="f4 fw7 lh-title mb2">
                The next step is to fill out expungement paperwork, which
                RecordSponge can do for you.
              </h3>
              <p className="mb3">
                If a client has eligible charges, the Summary panel will display
                a button to Generate Paperwork. Click on the button and you will
                be directed to input identifying information. Inputting
                identifying information is optional but can help save you time.
              </p>
              <p className="mb4">
                After you input the information, RecordSponge will generate a
                .zip file with PDFs of the expungement paperwork for all of the
                charges, with one PDF file for each case that has eligible
                charges.
              </p>

              <Disclosure>
                <div className="bg-gray-blue-2 shadow br3 pa3 mb4">
                  <h3 className="f4 fw7 mb2">
                    Manually fill out the paperwork if preferred
                  </h3>
                  <DisclosureButton>
                    <span className="link hover-dark-blue fw6 mid-gray">
                      Show Instructions
                      <span
                        aria-hidden="true"
                        className="fas fa-angle-down pl1"
                      ></span>
                    </span>
                  </DisclosureButton>
                  <DisclosurePanel>
                    <h4 className="fw7 mt2 mb2">Selecting the correct form</h4>
                    <p className="mb3">
                      Not all counties will have their own form, but at least
                      the following do: Multnomah, Washington, Clackamas, Lane,
                      Jackson, Josephine, Tillamook, Marion, Baker, Coos, Curry,
                      Lincoln, Linn, Umatilla, Yamhill.{" "}
                      <Link
                        className="bb hover-blue"
                        to="/appendix"
                        onClick={() => window.scrollTo(0, 0)}
                      >
                        Find these forms in the Appendix.
                      </Link>
                    </p>
                    <p className="mb3">
                      If your county is not listed here, search online using
                      terms: “[county name] expungement form.”
                    </p>
                    <p className="mb3">
                      If a county does not have its own paperwork, use the{" "}
                      <Link className="bb hover-blue" to="/appendix#stockforms">
                        Stock Forms
                      </Link>
                      . At least the following counties do not have their own
                      paperwork: Deschutes, Clatsop, Hood River.
                    </p>
                    <h4 className="fw7 mb2">Conviction versus Arrest</h4>
                    <p className="mb3">
                      If there are no convicted charges in the case, use an
                      Arrest Form.
                    </p>
                    <p className="mb3">
                      If at least one charge has a Disposition of “Convicted,”
                      use a Conviction Form.
                    </p>
                    <h4 className="fw7 mb2">Fill out the form</h4>
                    <p className="mb3">For each case that is eligible now:</p>
                    <ul className="ml4">
                      <li className="mb2">
                        <span className="fw7">Case Number:</span> In the top
                        center, preceded by “CASE No.” Often starts with a two
                        numbers indicating year the case was filed.
                      </li>
                      <li className="mb2">
                        <span className="fw7">Case Name:</span> the name of the
                        person exactly as it appears in the name of the case as
                        it appears in the RecordSponge results / OECI, in the
                        top left corner.
                      </li>
                      <li className="mb2">
                        <span className="fw7">DA Number:</span> May not be
                        present. If not provided, do not write anything. Usually
                        located in the upper right corner if it exists.
                      </li>
                      <li className="mb2">
                        <span className="fw7">Arrest Date:</span> Dates listed
                        in the Charge Information. For a case with multiple
                        arrest dates, list them separated by semicolons.
                      </li>
                      <li className="mb2">
                        <span className="fw7">Conviction Date:</span> Dates
                        listed in the Charge.
                      </li>
                      <li className="mb2">
                        <span className="fw7">Arresting Agency:</span>
                        <ul className="ml4 mb3">
                          <li className="mb2">
                            If not readily attainable, do not fill it out. In
                            counties which require it (so far, just Jackson
                            County) fill in MPD or JCSO by default.
                          </li>
                          <li className="mb2">
                            Sometimes an OECI case will contain links to
                            relevant documents filed through a hyperlink
                            attached to the case number. If it does not contain
                            these links, do not fill out the arresting agency.
                          </li>
                          <li className="mb2">
                            If the hyperlink is live, click it to see if there
                            is a link titled “Information” or “Indictment.”
                            Click such link if it exists.
                          </li>
                          <li className="mb2">
                            The Arresting Agency will have its own number
                            attached to the case. Find a three- or four-letter
                            abbreviation for the Arresting Agency. Common
                            examples are PPB (Portland Police Bureau), MCSO
                            (Multnomah County Sheriff’s Office), etc.
                          </li>
                        </ul>
                      </li>
                    </ul>
                  </DisclosurePanel>
                </div>
              </Disclosure>

              <h3 className="f4 fw7 mb2" id="fingerprints">
                Obtain Fingerprints
              </h3>
              <p className="mb3">
                Obtain fingerprints printed out or inked directly onto
                cardstock. Digital fingerprints are not accepted as part of this
                process. Fingerprints printed onto cardstock can be obtained at
                sheriff's offices or fingerprinting services.
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
              <h3 className="f4 fw7 mb2" id="filepaperwork">
                File Paperwork
              </h3>
              <ul className="ml4 mb3">
                <li className="mb2">
                  You will need to file the paperwork with the courthouse in
                  each county in which you have cases you wish to expunge.
                </li>
                <li className="mb2">
                  In each county in which you have at least one conviction, you
                  will also need to bring an $80 Money Order made out to “Oregon
                  State Police.”
                </li>
                <li className="mb2">
                  Each conviction requires a $281 fee.{" "}
                  <strong className="fw7">
                    This fee is subject to waiver for income-qualified
                    individuals who complete the waiver form.
                  </strong>{" "}
                  You get this from the Clerk of Court.
                </li>
                <li className="mb2">
                  After filing with the Clerk of Court, you will receive two
                  copies. Take the following to the District Attorney’s office:
                  <ul className="ml4 mb3">
                    <li className="mb2">One copy of your paperwork</li>
                    <li className="mb2">One fingerprint card</li>
                    <li className="mb2">
                      One $80 Money Order made out to “Oregon State Police”
                    </li>
                  </ul>
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
                  It takes between two and five months for the District
                  Attorney’s office to process your paperwork. If you receive
                  communication during this time from the District Attorney that
                  you would like to review with us, please email us at
                  roe@qiu-qiulaw.com.
                </li>
                <li className="mb2">
                  Once your expungement is processed, you will receive paper
                  confirmation from the court informing you that your record was
                  expunged. You should keep copies of this confirmation and make
                  electronic copies – obtaining copies of expunged documents is
                  extremely costly.
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
