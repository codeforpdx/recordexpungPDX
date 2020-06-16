import React from "react";
import Header from "../Header";
import { Link } from "react-router-dom";

class Landing extends React.Component {
  render() {
    return (
      <>
        <Header />
        <div className="mw8 center ph4">
          <h1 className="f3 fw6 mv4">Manual</h1>
        </div>
        <main className="flex-l mw8 center ph4">
          <nav className="shrink-none order-2 self-start sticky-l w5 bg-white shadow pa4 pb4 mb4 ml5-l">
            <ul className="list">
              <li className="mb3">
                <a href="#intro" className="link hover-blue">
                  Introduction
                </a>
              </li>
              <li className="mb3">
                <a href="#generalinfo" className="link hover-blue">
                  General Info
                </a>
              </li>
              <li className="bt bw1 b--light-gray pt2 mb3">
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
              <li className="mb3 ml3">
                <a href="#file" className="link hover-blue">
                  File for Expungement
                </a>
              </li>
              <li className="bt bw1 b--light-gray pt2 mb3">
                <a href="#FAQ" className="link hover-blue">
                  FAQ
                </a>
              </li>
              <li className="mb3">
                <a href="#appendix" className="link hover-blue">
                  Appendix
                </a>
              </li>
              <li className="mb3">
                <a href="#privacypolicy" className="link hover-blue">
                  Privacy Policy
                </a>
              </li>
              <li className="mb3">
                <a href="#license" className="link hover-blue">
                  License
                </a>
              </li>
            </ul>
          </nav>
          <article className="order-1 lh-copy">
            <section className="mb4">
              <h2 className="f2 fw9 mb3" id="intro">
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
            <section className="bt bw1 b--light-gray pt2 mb5">
              <h2 className="f2 fw9 mb3" id="overview">
                Use RecordSponge
              </h2>
              <h3 className="fw7 mb2">Overview</h3>
              <p className="mb3">
                We ask anyone using the software to be in touch so that we can better maintain, scale, and improve our work and community. <a href="http://eepurl.com/g6N3Bn" className="bb hover-blue">Please complete this contact form</a>.
              </p>
              <ol className="ml4">
                <li className="mb3">
                  <p className="mb2">Log in and search records</p>
                  <ul className="fw4 ml4">
                    <li className="mb2">
                      You will need an Oregon eCourt Case Information (OECI) account to use RecordSponge. <a className="bb hover-blue" href="https://www.courts.oregon.gov/services/online/Pages/ojcin-signup.aspx">You can purchase a subscription here</a>.
                    </li>
                    <li className="mb2">
                      Go to <Link className="bb hover-blue" to="/record-search">recordsponge.com/record-search</Link> and log in with your OECI account.
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
                  <a className="bb-dotted-2 hover-blue" href="#appendix">
                    Appendix
                  </a>{" "}
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
                <li className="fw7 mb3">
                  The client does not owe money to the State, including
                  probation fees, child support, traffic tickets.
                  <ul className="list fw4 mt1">
                    <li className="mb2">
                      A person is not eligible for expungement if they owe money
                      in the case they are trying to expunge. If a person owes
                      money on any matter - including traffic violations, child
                      support, and probation supervision - district attorneys
                      will object in at least the following counties: Multnomah,
                      Douglas. The Balance shows money the person owes to
                      Circuit courts, but does not show balances in Municipal
                      courts, or for child support, or probation supervision
                      fees.
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
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb3">Further Analysis Needed</h4>
                <div className="purple bg-washed-purple fw6 pv2 ph3 mb3 dib br3">
                  Possibly Eligible Now (review)
                </div>
                <br />
                <div className="purple bg-washed-purple fw6 pv2 ph3 mb3 dib br3">
                  Possibly Eligible Mar 11, 2026 (review)
                </div>
                <br />
                <div className="purple bg-washed-purple fw6 pv2 ph3 mb3 dib br3">
                  Possibly eligible but time analysis is missing
                </div>
                <p className="mb3">
                  Sometimes, there is not enough information on the OECI website
                  to determine whether or not a case is eligible. RecordSponge
                  will then prompt the user to answer questions, and the
                  analysis will update based on those answers.
                </p>
              </div>
              <div className="bg-white shadow pa3">
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
                    revocation did not occurred within the last ten years simply
                    by asking the client.
                  </p>
                </li>
              </ol>
            </section>
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="file">
                File for Expungement
              </h2>
              <h3 className="f4 fw7 mb2">Selecting the correct form</h3>
              <p className="mb3">
                Not all counties will have their own form, but at least the
                following do: Multnomah, Washington, Clackamas, Lane, Jackson,
                Josephine, Tillamook, Marion, Baker, Coos, Curry, Lincoln, Linn,
                Umatilla, Yamhill.{" "}
                <a className="bb-dotted-2 hover-blue" href="#appendix">
                  Find these forms in the Appendix.
                </a>
              </p>
              <p className="mb3">
                If your county is not listed here, search online using terms:
                “[county name] expungement form.”
              </p>
              <p className="mb3">
                If a county does not have its own paperwork, use the{" "}
                <a className="bb-dotted-2 hover-blue" href="#stockforms">
                  Stock Forms
                </a>
                . At least the following counties do not have their own
                paperwork: Deschutes, Clatsop, Hood River.
              </p>
              <h3 className="f4 fw7 mb2">Conviction versus Arrest</h3>
              <p className="mb3">
                If the Disposition of a case is “Dismissed,” use an Arrest Form.
              </p>
              <p className="mb3">
                If the Disposition of a case is “Convicted,” use a Conviction
                Form.
              </p>
              <h3 className="f4 fw7 mb2">Fill out the form</h3>
              <p className="mb3">For each case that is eligible now:</p>
              <ul className="ml4">
                <li className="mb2">
                  <span className="fw7">Case Number:</span> In the top center,
                  preceded by “CASE No.” Often starts with a two numbers
                  indicating year the case was filed.
                </li>
                <li className="mb2">
                  <span className="fw7">Case Name:</span> the name of the person
                  exactly as it appears in the name of the case as it appears in
                  the RecordSponge results / OECI, in the top left corner.
                </li>
                <li className="mb2">
                  <span className="fw7">DA Number:</span> May not be present. If
                  not provided, do not write anything. Usually located in the
                  upper right corner if it exists.
                </li>
                <li className="mb2">
                  <span className="fw7">Arrest Date:</span> Dates listed in the
                  Charge Information. For a case with multiple arrest dates,
                  list them separated by semicolons.
                </li>
                <li className="mb2">
                  <span className="fw7">Conviction Date:</span> Dates listed in
                  the Charge.
                </li>
                <li className="mb2">
                  <span className="fw7">Arresting Agency:</span>
                  <ul className="ml4 mb3">
                    <li className="mb2">
                      If not readily attainable, do not fill it out. In counties
                      which require it (so far, just Jackson County) fill in MPD
                      or JCSO by default.
                    </li>
                    <li className="mb2">
                      Sometimes an OECI case will contain links to relevant
                      documents filed through a hyperlink attached to the case
                      number. If it does not contain these links, do not fill
                      out the arresting agency.
                    </li>
                    <li className="mb2">
                      If the hyperlink is live, click it to see if there is a
                      link titled “Information” or “Indictment.” Click such link
                      if it exists.
                    </li>
                    <li className="mb2">
                      The Arresting Agency will have its own number attached to
                      the case. Find a three- or four-letter abbreviation for
                      the Arresting Agency. Common examples are PPB (Portland
                      Police Bureau), MCSO (Multnomah County Sheriff’s Office),
                      etc.
                    </li>
                  </ul>
                </li>
              </ul>
              <h3 className="f4 fw7 mb2" id="fingerprints">
                Obtain Fingerprints
              </h3>
              <p className="mb3">
                Obtain fingerprints printed out or inked directly onto cardstock. 
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
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="FAQ">
                FAQ
              </h2>
              <p className="mb3">
                Due to the complexity of the Oregon expungement laws, incorrect
                information proliferates from State actors at all levels of the
                justice system.
              </p>
              <p className="mb3">
                Below are some common myths overheard in courtrooms all over
                Oregon.
              </p>
              <ol className="ml4 mb4">
                <li className="mb2">
                  <p className="fw7 mb3">
                    Myth: “After you complete this diversion program, there will
                    be no record of your case.”
                  </p>
                  <p className="fw7 mb3">
                    Fact 1: Without affirmatively expunging your case, it will
                    still appear on your record.
                  </p>
                  <p className="mb3">
                    Oregon courts
                    <strong> never </strong>
                    expunge adult criminal records on their own.
                  </p>
                  <p className="mb3">
                    When you successfully complete a diversion program,
                    oftentimes your case is dismissed - but that doesn’t mean it
                    “goes away.” Your entire case file – including records of
                    arrest, police reports, pleadings – are still publicly
                    available. Records of arrest are potentially just as
                    damaging on a housing or job application as records of
                    conviction.
                  </p>
                  <p className="mb3">
                    Moreover, a dismissed case is not even eligible if you have
                    a conviction within the last ten years, or an un-expunged
                    dismissed case from the last three years.
                  </p>
                  <p className="fw7 mb3">
                    Fact 2: DUII diversion dismissals are specifically
                    ineligible for expungement.
                  </p>
                  <p className="mb3">
                    Judges, DAs, and defense attorneys administering the DUII
                    diversion program sometimes say outright that successful
                    completion means that the case will disappear from your
                    record. This is not true under current law, which
                    specifically makes completion of DUII diversion ineligible
                    for expungement.
                  </p>
                </li>
                <li className="mb2">
                  <p className="fw7 mb3">
                    Myth: “Your record will be eligible after seven years.”
                  </p>
                  <p className="fw7 mb3">
                    Fact: Time-eligibility is complicated but in general has
                    nothing to do with “seven years.”
                  </p>
                  <p className="mb3">
                    The “seven-year” rule is thrown around a lot and has no
                    basis in law or practice.
                  </p>
                  <p className="mb2">
                    There are many concurrent rules governing time-eligibility.
                    Here are a few:
                  </p>
                  <ul className="ml4 mb3">
                    <li className="mb2">
                      A case is not eligible unless you have no other
                      convictions from the last ten (10) years
                    </li>
                    <li className="mb2">
                      A conviction is not eligible unless the case is, itself,
                      at least three (3) years old
                    </li>
                    <li className="mb2">
                      A dismissal is not eligible unless you have no other
                      arrests from the last three (3) years
                    </li>
                    <li className="mb2">
                      A B felony is not eligible until twenty (20) years from
                      the date of conviction
                    </li>
                  </ul>
                </li>
                <li className="mb2">
                  <p className="fw7 mb3">
                    Myth: “No one is ever eligible for expungement.”
                  </p>
                  <p className="fw7 mb3">
                    Fact: About 25% of people with criminal records are
                    currently eligible to expunge their entire records, and many
                    more are eligible at a future date.
                  </p>
                  <p className="mb3">
                    From my (Michael Zhang) experience, about one quarter of
                    people who inquire into their eligibility are already
                    eligible, and in fact have been for a long time. From my
                    conversations with people, it seems that so few people take
                    the initiative to inquire into their eligibility because
                    they either assume that expungement is unavailable or
                    because fees for expungement lawyers are so high.
                  </p>
                  <p className="mb3">
                    In fact, Oregon has one of the most permissive expungement
                    statutes in the country. Yet the complexity of the law and
                    the filing procedures effectively bar most people from
                    accessing its benefits.
                  </p>
                </li>
              </ol>
            </section>
            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="appendix">
                Appendix
              </h2>
              <h3 className="fw7 tl mb2">Forms to file for expungement</h3>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Baker</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/courts/baker/help/Pages/forms.aspx"
                    >
                      Conviction
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/courts/baker/help/Pages/forms.aspx"
                    >
                      Arrest
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Benton</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Exp%20Section%20C%20Forms%20and%20Instructions.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Exp%20Section%20A%20Forms%20and%20Instructions.pdf"
                    >
                      Arrest but no charge ever filed in Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Exp%20Section%20B%20Forms%20and%20Instructions.pdf"
                    >
                      Arrested and charged in Court but later dismissed or
                      acquitted of charge(s) <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Clackamas</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Clackamas-Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Clackamas-Arrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Coos</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/COO-ExpungementAffidavitMotionOrderSetAsideConvictionCoos.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/COO-ExpungementAffidavitMotionOrderSetAsideArrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Curry</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/CUR-ExpungementAffidavitMotionOrderSetAsideConviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/CUR-ExpungementAffidavitMotionOrdeSetAsideArrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Jackson</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/JAC-PktC-CrimSetAside-Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/JAC-PktA-CrimSetAside-Arrest.pdf"
                    >
                      Arrest but no charges or cases were filed with the Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/JAC-PktB-CrimSetAside-DismissalAcquittal.pdf"
                    >
                      Arrested and a case filed with the Court but later
                      charge(s) were dismissed or acquitted{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Josephine</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="http://www.co.josephine.or.us/Files/Setting%20Aside%20Conviction%20Form.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="http://www.co.josephine.or.us/Files/Setting%20Aside%20Arrest%20Form.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Lane</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Motion%20and%20Affidavit%20to%20Set%20Aside%20Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Motion%20and%20Affidavit%20to%20Set%20Aside%20Charges.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Lincoln</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Lincoln%20Set%20Aside%20Conviction%20-%20PACKET.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/Lincoln%20Set%20Aside%20Arrest%20-%20PACKET.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Linn</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/LIN-Criminal-SetAsideRecordsOfConviction-C.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/LIN-Criminal-SetAsideRecordsOfCharge-B.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Marion</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/MAR-SetAside-PacketC.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/MAR-SetAsidePacketA.pdf"
                    >
                      Arrest but no charges or cases were filed with the Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/MAR-SetAsidePacketB.pdf"
                    >
                      Arrested and a case filed with the Court, but later
                      charge(s) were dismissed or acquitted{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Morrow</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Umatilla-Morrow-Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Umatilla-Morrow-Arrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Multnomah</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.mcda.us/index.php/documents/conviction-motion-and-affidavit-form.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.mcda.us/index.php/documents/arrest-motion-and-affidavit-form.pdf"
                    >
                      Arrest
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Polk</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/PLK-ExpungementPACKETC.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/PLK-ExpungementPACKETA.pdf"
                    >
                      Arrest but no charges or cases were filed with the Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/PLK-ExpungementPACKETB.pdf"
                    >
                      Arrested and a case filed with the court, but later
                      charge(s) were dismissed or acquitted{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Tillamook</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/TIL-ExpungementConviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/TIL-ExpungementArrest.pdf"
                    >
                      Arrest but no charge ever filed in Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/TIL-ExpungementCharge.pdf"
                    >
                      Arrested and charged in Court but later dismissed or
                      acquitted of charge(s) <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Umatilla</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Umatilla-Morrow-Conviction.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Umatilla-Morrow-Arrest.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Washington</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/courts/washington/programs-services/Documents/WSH-ConvictionRecordExpungementPacket.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/courts/washington/programs-services/Documents/WSH-ArrestRecordExpungementPacket.pdf"
                    >
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3">
                <h4 className="fw7 mb2">Yamhill</h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/YAM-SetAsidePacketC.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/YAM-SetAsidePacketA.pdf"
                    >
                      Arrest only no charge ever filed in Court{" "}
                      <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/forms/Documents/YAM-SetAsidePacketB.pdf"
                    >
                      Arrested and charged in Court but later dismissed or
                      acquitted of charge(s) <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
              <div className="bg-white shadow pa3" id="stockforms">
                <h4 className="fw7 mb2">
                  Stock Form (if county is not listed above)
                </h4>
                <ul className="list ml2">
                  <li className="mb3">
                    <a
                      className="bb hover-blue"
                      href="/docs/Stock-Conviction-HM.pdf"
                    >
                      Conviction <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                  <li className="mb3">
                    <a className="bb hover-blue" href="/docs/Stock-Arrest.pdf">
                      Arrest <span className="f7 fw7">PDF</span>
                    </a>
                  </li>
                </ul>
              </div>
            </section>

            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="privacypolicy">
                Privacy Policy
              </h2>
              <p className="mb3">
                Our privacy policy is simple and meant to be read by all of our
                users. Please email michael@qiu-qiulaw.com if anything is
                unclear.
              </p>
              <h3 className="f4 fw7 mb2">What we collect and why</h3>
              <p className="mb3">
                Our guiding principle is to collect only what we need, and we
                will not sell your data. Here’s what that means in practice:
              </p>
              <h4 className="fw7 mb2">Search “pings” to track usage</h4>
              <p className="mb3">
                The only information we collect are user search “pings,” which
                tells us when (and only when) a user has made a search. We
                collect this information to track usage rates. That’s it.
              </p>
              <h4 className="fw7 mb2">Cookies</h4>
              <p className="mb3">
                We use persistent first-party cookies to support necessary
                functions of the application. A cookie is a piece of text stored
                by your browser to help it remember your login information, site
                preferences, and more. You can adjust cookie retention settings
                in your own browser. To learn more about cookies, including how
                to see which cookies have been set and how to manage and delete
                them, please visit:{" "}
                <a
                  href="https://www.allaboutcookies.org"
                  className="bb hover-blue"
                >
                  allaboutcookies.org
                </a>
                .
              </p>
              <h4 className="fw7 mb2">Voluntary correspondence</h4>
              <p className="mb3">
                When you write RecordSponge with a question or to ask for help,
                we keep that correspondence, including the email address, so
                that we have a history of past correspondences to reference if
                you reach out in the future.
              </p>
              <h3 className="f4 fw7 mb2">What we don't collect</h3>
              <p className="mb3">
                We care about the privacy of your clients’ criminal records.
                Indeed, this project’s purpose is to make these records more
                private. Therefore, RecordSponge does not record or collect
                search information. If you are using this software for clients,
                we have no way of identifying who they are.
              </p>
              <p className="mb3">
                We do not save your Oregon eCourt Case Information (OECI) login
                credentials. That’s why we must separately log in to OECI every
                time you use RecordSponge.
              </p>
              <h3 className="f4 fw7 mb2">How we secure your data</h3>
              <p className="mb3">
                All data is encrypted via SSL/TLS when transmitted from our
                servers to your browser.
              </p>
              <h3>
                Adapted from the{" "}
                <a
                  href="https://github.com/basecamp/policies"
                  className="bb hover-blue"
                >
                  Basecamp open-source policies
                </a>{" "}
                /{" "}
                <a
                  href="https://creativecommons.org/licenses/by/4.0"
                  className="bb hover-blue"
                >
                  CC BY 4.0
                </a>
              </h3>
            </section>

            <section className="mb5">
              <h2 className="f2 fw9 mb3" id="license">
                License
              </h2>
              <p className="mb3">Copyright 2020 Michael Zhang, Qiu-Qiu Law</p>
              <p className="mb3">
                Permission is hereby granted, free of charge, to any person
                obtaining a copy of this manual and associated documentation
                files (the "Manual"), to deal in the Manual without restriction,
                including without limitation the rights to use, copy, modify,
                merge, publish, distribute, sublicense, and/or sell copies of
                the Manual, and to permit persons to whom the Software is
                furnished to do so, subject to the following conditions:
              </p>
              <p className="mb3">
                The above copyright notice and this permission notice shall be
                included in all copies or substantial portions of the Manual.
              </p>
              <p className="mb4">
                THE MANUAL IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
                EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
                OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
                NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
                HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
                WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
                FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
                OTHER DEALINGS IN THE MANUAL.
              </p>
              <p className="fw7 mb2">Short list of Credits</p>
              <ul className="list mb3">
                <li className="mb2">Adam Emrich, software developer</li>
                <li className="mb2">Dana Danger, contributor to Manual</li>
                <li className="mb2">Forrest Longanecker, software developer</li>
                <li className="mb2">Hunter Marcks, designer</li>
                <li className="mb2">Kent Shikama, software developer</li>
                <li className="mb2">
                  Jordan Witte, current project manager, software developer
                </li>
                <li className="mb2">
                  Nick Schimek, former project manager, software developer
                </li>
                <li className="mb2">
                  Michael Zhang, product manager and creator of RecordSponge,
                  contributor to Manual
                </li>
              </ul>
            </section>
          </article>
        </main>
      </>
    );
  }
}

export default Landing;
