import React, { useEffect, useState } from "react";
import { HashLink as Link } from "react-router-hash-link";
import EditingGuide from "./EditingGuide";
import Accordion, { openDetailsById } from "../common/Accordion";
import Sidebar from "./Sidebar";
import IconButton from "../common/IconButton";
// import VideoEmbed from "../common/VideoEmbed";
import Figure from "../common/Figure";
import useLockBodyScroll from "../../hooks/useLockBodyScroll";

function Manual() {
  const [isOpen, setIsOpen] = useState(false);

  const handleSidebarOpen = () => {
    setIsOpen((prev) => !prev);
  };

  useLockBodyScroll(isOpen);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 960) {
        setIsOpen(false);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    document.title = "Manual - RecordSponge";
  }, []);

  /**
   * Intercepts clicks on in-page `#hash` links
   * to open the target accordion before scrolling.
   */
  const handleArticleClick = (e: React.MouseEvent<HTMLElement>) => {
    const target = e.target as HTMLElement;
    const anchor = target.closest("a[href^='#']");
    const href = anchor?.getAttribute("href");
    if (href) {
      openDetailsById(href.slice(1));
    }
  };

  return (
    <div className="scroll-mt-20" id="intro">
      <main className="flex-l items-start mw8 center ph4 mt5">
        <div className="mw8 center ph4 visually-hidden">
          <h1 className="f3 fw6 mv4">Manual</h1>
        </div>

        {/* Mobile Sidebar/Drawer */}
        <button className="mobile-nav-btn dn-l" onClick={handleSidebarOpen}>
          <div className={`sidebar-hamburger ${isOpen ? "open" : ""}`}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </button>
        <aside className={`mobile-sidebar dn-l ${isOpen ? "open" : ""}`}>
          <Sidebar handleSidebarOpen={handleSidebarOpen} />
        </aside>

        {/* Sidebar */}
        <aside className="dn db-l pa1 order-2-l sticky-l self-start">
          <div className="shadow mt4 ml5-l">
            <Sidebar />
          </div>
        </aside>

        <article
          className="order-1-l lh-copy manual-content"
          onClick={handleArticleClick}
        >
          <section className="mb4">
            <h2 className="f2 fw9 mt4">How to use RecordSponge</h2>
            <p>
              <strong>RecordSponge</strong> is built by{" "}
              <a
                className="bb hover-blue"
                href="https://www.codepdx.org"
                target="_blank"
                rel="noreferrer noopener"
              >
                Code PDX
              </a>
              , a volunteer organization. Its codebase is published under the{" "}
              <a
                className="bb hover-blue"
                href="https://opensource.org/licenses/MIT"
                target="_blank"
                rel="noreferrer noopener"
              >
                MIT license
              </a>
              . It is and always will be free to use. Only a small percentage of
              Oregonians who are eligible to expunge their records have done so.
              Let's get to work.
            </p>
            <p>
              We ask anyone using the software to reach out so we can better
              maintain and improve our work. Prior to using RecordSponge for the
              first time, please reach out to us at{" "}
              <a className="bb hover-blue" href="mailto:michael@qiu-qiulaw.com">
                michael@qiu-qiulaw.com
              </a>
              . Have questions? Check the{" "}
              <a className="bb-dotted-2 hover-blue" href="#faqs">
                FAQs
              </a>
              .
            </p>
          </section>

          <section className="mb4">
            <div className="flex flex-column gap4">
              <Accordion title="General Info" id="general-info">
                <div className="mt1">
                  <h3 className="f4 fw7 mt1 scroll-mt-20">How it works</h3>
                  <p>
                    RecordSponge connects directly to the{" "}
                    <strong>Oregon eCourt Case Information</strong> (OECI)
                    system using your credentials. When you search, it logs into
                    OECI, submits your query, and collects case data from the
                    results using a web scraper — a tool that reads and extracts
                    information from websites.
                  </p>
                  <p>
                    This scraper then applies an algorithm based on Oregon's
                    expungement statutes (ORS{" "}
                    <a
                      href="https://oregon.public.law/statutes/ors_137.225"
                      className="bb hover-blue"
                      target="_blank"
                      rel="noreferrer noopener"
                    >
                      137.225
                    </a>{" "}
                    and{" "}
                    <a
                      href="https://oregon.public.law/statutes/ors_137.226"
                      className="bb hover-blue"
                      target="_blank"
                      rel="noreferrer noopener"
                    >
                      137.226
                    </a>
                    ) to determine eligibility for every case found by OECI.
                  </p>
                  <h3 className="f4 fw7 mt1">Checklist</h3>
                  <p>
                    Using RecordSponge, the expungement process has 5 steps:
                  </p>
                  <ol className="ml4">
                    <li className="mb3">
                      <a className="bb-dotted-2 hover-blue" href="#oeci-login">
                        Log in to OECI
                      </a>
                      <ul className="fw4 ml4 mt2">
                        <li>
                          You will need an OECI account to search for criminal
                          records.{" "}
                          <a
                            className="bb hover-blue"
                            href="https://www.courts.oregon.gov/services/online/Pages/ojcin-signup.aspx"
                            target="_blank"
                            rel="noreferrer noopener"
                          >
                            You can purchase a subscription here
                          </a>
                          .
                        </li>
                        <li>
                          No OECI account yet? The demo version has all the same
                          features besides the ability to search the OECI
                          database. Examples are provided, or you can enter
                          records manually.{" "}
                          <Link
                            className="bb hover-blue"
                            to="/demo-record-search"
                          >
                            Check out the demo
                          </Link>
                          .
                        </li>
                      </ul>
                    </li>
                    <li className="mb3">
                      <a
                        className="bb-dotted-2 hover-blue"
                        href="#search-records"
                      >
                        Search records
                      </a>
                      <ul className="fw4 ml4 mt2">
                        <li>
                          Ensure that{" "}
                          <a
                            className="bb-dotted-2 hover-blue"
                            href="#assumptions"
                          >
                            Assumptions
                          </a>{" "}
                          are met
                        </li>
                        <li>
                          <a className="bb-dotted-2 hover-blue" href="#search">
                            Search
                          </a>{" "}
                          by name and date of birth
                        </li>
                        <li>
                          Review{" "}
                          <a className="bb-dotted-2 hover-blue" href="#results">
                            Results
                          </a>{" "}
                          and{" "}
                          <a
                            className="bb-dotted-2 hover-blue"
                            href="#fines-and-fees"
                          >
                            Fines and Fees
                          </a>
                        </li>
                      </ul>
                    </li>
                    <li className="mb3">
                      <a
                        className="bb-dotted-2 hover-blue"
                        href="#complete-paperwork"
                      >
                        Complete paperwork
                      </a>{" "}
                      for expungement
                      <ul className="fw4 ml4 mt2">
                        <li>
                          This includes{" "}
                          <a
                            className="bb-dotted-2 hover-blue"
                            href="#feewaiver"
                          >
                            paperwork to modify financial obligations
                          </a>{" "}
                          if applicable
                        </li>
                      </ul>
                    </li>
                    <li className="mb3">
                      <a
                        className="bb-dotted-2 hover-blue"
                        href="#obtain-fingerprints"
                      >
                        Obtain fingerprints
                      </a>
                      <ul className="fw4 ml4 mt2">
                        <li>Mail to Oregon State Police</li>
                      </ul>
                    </li>
                    <li className="mb3">
                      <a
                        className="bb-dotted-2 hover-blue"
                        href="#file-paperwork"
                      >
                        File paperwork
                      </a>{" "}
                      in appropriate courts
                    </li>
                  </ol>
                  <p>
                    <a
                      className="bb hover-blue"
                      href="/docs/expungement-checklist.pdf"
                      download="expungement-checklist.pdf"
                      target="_blank"
                      rel="noreferrer"
                    >
                      Download checklist as PDF
                    </a>
                  </p>
                  <p>
                    If new to RecordSponge, confirm results with Michael Zhang
                    at{" "}
                    <a
                      className="bb hover-blue"
                      href="mailto:michael@qiu-qiulaw.com"
                    >
                      michael@qiu-qiulaw.com
                    </a>
                    .
                  </p>
                  <div className="bg-gray-blue-2 shadow br3 pa3 mt3 mb1 scroll-mt-20 ba">
                    <h3 className="fw7">Access and Limitations</h3>
                    <ul className="ml4 mb2">
                      <li className="mb1">
                        <strong>Adult Records Only:</strong> RecordSponge only
                        deals with adult criminal records.
                      </li>
                      <li className="mb1">
                        <strong>Juvenile Records:</strong> Juvenile records are
                        eligible on a different basis. They generally require
                        the record to be 5+ years old with no subsequent cases,
                        or a showing that expungement is in the "best interests
                        of justice." (see{" "}
                        <a
                          className="pointer bb hover-blue"
                          href="https://www.osbar.org/public/legalinfo/1081_ClearingRecord.htm"
                          target="_blank"
                          rel="noreferrer noopener"
                        >
                          more info here
                        </a>
                        )
                      </li>
                    </ul>
                  </div>
                </div>
              </Accordion>

              <Accordion title="Part 1: OECI Login" id="oeci-login">
                <p className="mt1 mb2">
                  To search criminal records, you will need an{" "}
                  <strong>Oregon eCourt Case Information (OECI)</strong>{" "}
                  account.
                </p>
                <p className="mb1">For existing users:</p>
                <ul className="pl4">
                  <li>
                    Navigate to the login page by clicking "Search" in the
                    navbar
                    <div className="mt2 mb2">
                      <span
                        className="f5 fw6 pv2 ph3 blue br2 ba b--blue dib tc"
                        aria-hidden="true"
                      >
                        Search
                      </span>
                    </div>
                  </li>
                  <li>
                    Enter your OECI login credentials and click "Log in to OECI"
                    <div className="mt2 mb2">
                      <span
                        className="bg-blue white fw6 dib br2 pv2 ph2 tc"
                        aria-hidden="true"
                      >
                        Log in to OECI
                      </span>
                    </div>
                  </li>
                </ul>
                <p className="mb1">For new users:</p>
                <ul className="pl4">
                  <li>
                    <a
                      className="bb hover-blue"
                      href="https://www.courts.oregon.gov/services/online/Pages/ojcin-signup.aspx"
                      target="_blank"
                      rel="noreferrer noopener"
                    >
                      Create an OECI account
                    </a>
                  </li>
                </ul>
              </Accordion>
              <Accordion
                title="Part 2: Search Client Records"
                id="search-records"
              >
                <div className="flex flex-column gap4 mt2">
                  <Accordion title="Assumptions" id="assumptions" defaultOpen>
                    <div className="mt1">
                      <p>
                        RecordSponge only analyzes public{" "}
                        <strong>Oregon Circuit Court</strong> records. However,
                        having an open case or a conviction anywhere within the
                        last 7 years could affect eligibility. To ensure the
                        accuracy of your expungement analysis, please review the
                        following conditions when brought up:
                      </p>
                      <div className="bg-gray-blue-2 shadow ba br3 pa3 mb3">
                        <ol className="ml3">
                          <li>
                            <div>
                              <h4 className="fw6">The Scope</h4>
                              <span>
                                Eligibility may be affected if there are records
                                from the last 7 years in:
                              </span>
                              <ul className="ml4 mt2 fw5">
                                <li>Federal or Out-of-State Courts</li>
                                <li>
                                  Municipal (City) Courts (see{" "}
                                  <a
                                    href="#municipal-courts"
                                    className="bb-dotted-2 hover-blue"
                                  >
                                    Notes on Municipal Courts
                                  </a>
                                  )
                                </li>
                                <li>
                                  Previous Expungements: If you successfully
                                  expunged a case within the last 7 years, it
                                  may still affect your current eligibility
                                </li>
                              </ul>
                            </div>
                          </li>
                          <li>
                            <div>
                              <h4 className="fw6">Disqualifying Factors</h4>
                              <span>
                                The client may be ineligible for expungement if
                                they:
                              </span>
                              <ul className="ml4 mt2 fw5">
                                <li>
                                  Have any open case in any courts in the US
                                </li>
                                <li>Have an active warrant</li>
                              </ul>
                            </div>
                          </li>
                          <li>
                            <div>
                              <h4 className="fw6">Traffic Violations</h4>
                              <ul className="ml4 mt2 fw5">
                                <li>
                                  Non-Criminal: Standard traffic tickets{" "}
                                  <strong className="underline">do not</strong>{" "}
                                  affect eligibility
                                </li>
                                <li>
                                  Criminal: Misdemeanor or felony traffic
                                  convictions (such as Driving While Suspended){" "}
                                  <strong className="underline">do</strong>{" "}
                                  count and must be factored into the 7-year
                                  lookback period
                                </li>
                              </ul>
                            </div>
                          </li>
                          <li>
                            <div>
                              <h4 className="fw6">The 7-Year Rule</h4>
                              <ul className="ml4 mt2 fw5">
                                <li>
                                  The Cutoff: Generally, any case closed more
                                  than 7 years ago (in any court) will not
                                  affect your current eligibility
                                </li>
                                <li className="mb3">
                                  Multiple Filings: You are allowed to file for
                                  expungement multiple times within a 7-year
                                  period, provided each specific case meets the
                                  necessary criteria
                                </li>
                              </ul>
                            </div>
                          </li>
                        </ol>
                      </div>
                      <p>
                        All search results are based on the assumption that the
                        conditions above are met for the client's case(s).
                      </p>
                      <p className="mb3">
                        If the{" "}
                        <a
                          className="bb-dotted-2 hover-blue"
                          href="#assumptions"
                        >
                          Assumptions
                        </a>{" "}
                        are not met, but you would still like to conduct an
                        analysis, or if you have any questions about this
                        section, please contact{" "}
                        <a
                          className="bb hover-blue"
                          href="mailto:michael@qiu-qiulaw.com"
                        >
                          michael@qiu-qiulaw.com
                        </a>
                        .
                      </p>
                      <div
                        className="bg-gray-blue-2 shadow ba br3 pa3 mb3 scroll-mt-20"
                        id="municipal-courts"
                      >
                        <h4 className="fw7">Notes on Municipal Courts</h4>
                        <p>
                          Beware of misdemeanor/felony traffic convictions from
                          municipal courts such as Beaverton Municipal Court
                          (not Washington Circuit Court), Troutdale Municipal
                          Court, and Medford Municipal Court. These courts
                          handle low-level and traffic crimes — only
                          misdemeanors and felonies matter for eligibility,
                          including Driving While Suspended.
                        </p>
                      </div>
                    </div>
                  </Accordion>
                  <Accordion title="Search" id="search">
                    <div className="mt1">
                      <p>
                        After logging into OECI, find your client's records
                        using the "Search" feature.
                      </p>
                      <Figure
                        src="/img/search-form.webp"
                        alt="search form"
                        caption="Search form - Desktop View"
                      />
                      <p>
                        Court records often contain errors - a client’s name may
                        be misspelled or their date of birth may be incorrect.
                      </p>
                      <p>
                        The goal is to pull all of the client’s records without
                        pulling records of other persons. You can do this by
                        searching using a "smart" combination of the client’s
                        legal name(s) and date of birth or through a more direct
                        input approach.
                      </p>
                      <p className="flex flex-column mb2">
                        <span className="mb2">
                          Consider the following client:
                        </span>
                        <em className="f5">Date of Birth: 01/01/1900</em>
                        <em className="f5">
                          Current preferred name: Sam "Mo" Alice Roe-Thomas
                        </em>
                        <em className="f5">
                          Current legal name: Samantha Alice Roe-Thomas
                        </em>
                        <em className="f5">
                          Previous legal name: Samantha Alice Roe, Samantha
                          Alice Thomas
                        </em>
                        <em className="f5">
                          Aliases (not legal name): "Mo" Roe
                        </em>
                      </p>

                      <p>
                        Several approaches could be made to locate this client's
                        records.
                      </p>
                      <div className="mb2">
                        <Accordion title="Simple Search">
                          <p className="mt1 mb2">
                            Enter the client's name and date of birth, then
                            press the "Search" button. Typically, using the name
                            along with date of birth is enough to narrow the
                            search.
                          </p>
                          <p>
                            In rare cases, the middle name could also be used.
                          </p>
                          <p>
                            However, depending on the name's complexity, a more
                            powerful approach might be needed (see{" "}
                            <a
                              href="#smart-search"
                              className="bb-dotted-2 hover-blue"
                            >
                              "Smart Search"
                            </a>
                            ).
                          </p>
                          <Figure
                            src="/img/simple-search.webp"
                            alt="simple search"
                            caption="Simple search inputs"
                          />
                        </Accordion>
                      </div>
                      <div className="mb2">
                        <Accordion title="Wildcard Search">
                          <div className="mt1 mb2">
                            A different approach is to use the asterisk (*) to
                            shorten names. This can be especially useful for
                            long names.
                          </div>

                          <Figure
                            src="/img/wildcard-search.webp"
                            alt="wildcard search"
                            caption="Wildcard search inputs"
                          />
                        </Accordion>
                      </div>
                      <div className="mb2">
                        <Accordion title={`"Smart Search"`} id="smart-search">
                          <div className="mt1 mb2">
                            For clients who are difficult to find — often due to
                            incorrect court records — "Smart Search" combines
                            both the Simple Search and Wildcard Search
                            approaches. Using the "Alias" button would let you
                            fill in additional rows.
                          </div>

                          <Figure
                            src="/img/smart-search.webp"
                            alt="smart search"
                            caption="Smart search inputs"
                          />
                          <div
                            className="bg-gray-blue-2 shadow br3 pa3 mt3 mb3 scroll-mt-20 ba"
                            id="search-tips"
                          >
                            <h3 className="fw7">Search Tips</h3>
                            <p>
                              If an expected case is missing even after "smart
                              searching", try searching with{" "}
                              <a
                                href="#aliases"
                                className="bb-dotted-2 hover-blue"
                              >
                                aliases
                              </a>
                              .
                            </p>
                            <p>
                              Names with prefixes like Mc, De, or Di may be
                              stored by the court with or without a space. For
                              example, McDonald could be stored as Mc Donald
                              (with a space) or McDonald (without a space).
                              Search both forms to ensure complete results.
                            </p>
                          </div>
                        </Accordion>
                      </div>
                      <p>
                        To reset or clear the existing search results, simply
                        click "Clear Data".
                      </p>
                      <Accordion title="Aliases" id="aliases">
                        <p className="mt1">
                          Clients may have aliases from marriage and/or
                          nicknames in court records. Courts may have input
                          names incorrectly (see{" "}
                          <a
                            href="#search-tips"
                            className="bb-dotted-2 hover-blue"
                          >
                            Search Tips
                          </a>{" "}
                          for more details). The "Alias" feature can let you add
                          additional names for the search filter.
                        </p>
                        <div className="mb2">
                          <Figure
                            src="/img/aliases.webp"
                            alt="aliases"
                            caption="Multiple alias inputs"
                          />
                        </div>
                      </Accordion>
                    </div>
                  </Accordion>

                  <Accordion title="Results" id="results">
                    <p className="mt1 mb3">
                      RecordSponge analyzes records for eligibility on a
                      charge-by-charge basis. After the search is performed, you
                      can see results in the{" "}
                      <a
                        href="#search-summary"
                        className="bb-dotted-2 hover-blue"
                      >
                        "Search Summary"
                      </a>{" "}
                      panel by default. Every charge can be viewed in greater
                      detail in{" "}
                      <a
                        href="#full-results"
                        className="bb-dotted-2 hover-blue"
                      >
                        Full Results
                      </a>
                      , or you can view everything on one page via{" "}
                      <a
                        href="#expanded-view"
                        className="bb-dotted-2 hover-blue"
                      >
                        Expanded View
                      </a>
                      .
                    </p>
                    <Figure
                      src="/img/search-results.webp"
                      alt="search results"
                      caption="Example search result"
                      className="mt3"
                      id="example-search-results"
                      imgClassName="scroll-mt-20"
                    />
                    <div className="flex flex-column gap4">
                      <Accordion title="Search Summary" id="search-summary">
                        <p className="mt1">
                          Usually, the search results in the panel will appear as the following:
                        </p>
                        <div className="ba br3 mb3">
                          <div className="bg-white shadow pa3 br--top-l br3 bl3">
                            <h4 className="fw7 mb3">Eligible Now</h4>
                            <div className="green bg-washed-green fw6 pv2 ph3 mb3 dib br3">
                              Eligible
                            </div>
                            <p>
                              The specific charge is eligible for expungement if{" "}
                              <a
                                className="bb-dotted-2 hover-blue"
                                href="#assumptions"
                              >
                                Assumption
                              </a>{" "}
                              is true.
                            </p>
                          </div>
                          <div className="bg-white shadow pa3">
                            <h4 className="fw7 mb3">
                              Eligible on a future date
                            </h4>
                            <div className="dark-blue bg-washed-blue fw6 pv2 ph3 mb3 dib br3">
                              Eligible Aug 26, 2024
                            </div>
                            <p className="mb3">
                              The specific charge is eligible for expungement on
                              the date specified. This is also conditional on{" "}
                              <a
                                className="bb-dotted-2 hover-blue"
                                href="#assumptions"
                              >
                                Assumption
                              </a>{" "}
                              being true. Having other cases could push out the
                              eligibility date further.
                            </p>
                            <div className="dark-blue bg-washed-blue fw6 pv2 ph3 mb3 dib br3">
                              Eligibility date dependent on open charge:
                              Eligible Jun 12, 2022 or 7 years from conviction
                              of open charge
                            </div>
                            <p>
                              If there is an open charge, the affected charges
                              will show multiple possible eligibility
                              timeframes. Once the open charge is closed then
                              the analysis will update. You can edit the open
                              charges to see how the eligibility will be
                              affected.
                            </p>
                          </div>
                          <div className="bg-white shadow pa3 br--bottom-l br3 bl3">
                            <h4 className="fw7 mb3">Ineligible</h4>
                            <div className="red bg-washed-red fw6 pv2 ph3 mb3 dib br3">
                              Ineligible
                            </div>
                            <p className="mb3">
                              The specific charge is not eligible under the
                              current law because it is not "type-eligible." The
                              reason why the charge is not type-eligible is
                              different for each charge. This is not conditional
                              on the{" "}
                              <a
                                className="bb-dotted-2 hover-blue"
                                href="#assumptions"
                              >
                                Assumptions
                              </a>
                              .
                            </p>
                          </div>
                        </div>
                        <p>
                          However, there could be cases that may require
                          additional action, of which the following results
                          would be shown:
                        </p>
                        <div className="ba br3 mb3">
                          <div className="bg-white shadow pa3 br--top-l br3 bl3">
                            <h4 className="fw7 mb3">Further Analysis Needed</h4>
                            <div className="purple bg-washed-purple fw6 pv2 ph3 mb3 dib br3">
                              Needs More Analysis
                            </div>
                            <p>
                              Sometimes, there is not enough information on the
                              OECI website to determine whether or not a case is
                              eligible. RecordSponge will then prompt the user
                              to answer questions, and the analysis will update
                              based on those answers.
                            </p>
                          </div>
                          <div className="bg-white shadow pa3 br--bottom-l br3 bl3">
                            <h4 className="fw7 mb3">Restitution Owed</h4>
                            <div className="dark-blue bg-washed-blue fw6 pv2 ph3 mb3 dib br3">
                              Ineligible If Restitution Owed
                            </div>
                            <p>
                              RecordSponge can detect if Restitution is
                              discussed in a Case's history, but OECI does not
                              always show whether it is still owed. Cases under
                              this heading will not print unless updated to
                              reflect that Restitution is not owed.
                            </p>
                            <p>
                              Ask the client directly if they currently owe
                              Restitution on the Case. If Restitution has been
                              paid, edit the Case to remove this status:
                            </p>
                            <ol className="ml4">
                              <li>
                                Select "Enable Editing" on the right below
                                "Search Summary"
                              </li>
                              <li>
                                Click the editing pencil associated with the
                                Case (not the Charge)
                              </li>
                              <li>Select "False" under "Restitution Owed"</li>
                            </ol>
                            <p className="mb3">
                              <strong>Note:</strong> Edits are temporary and
                              will revert when leaving RecordSponge. See the{" "}
                              <a
                                href="#editing"
                                className="bb-dotted-2 hover-blue"
                              >
                                Editing Guide
                              </a>{" "}
                              for more details.
                            </p>
                          </div>
                        </div>
                      </Accordion>
                      <Accordion title="Full Results" id="full-results">
                        <div className="mt1">
                          <p>
                            Every charge in "Search Summary" can be seen in
                            greater detail in the subsequent panels.
                          </p>
                          <Figure
                            src="/img/full-results.webp"
                            alt="full results"
                            caption="Example of detailed result"
                            className="mt3"
                          />
                          <p>
                            Within these panels, the case number under "Case"
                            will be linked to the OECI page and an explanation
                            for eligibility. This information may help to
                            explain results that are inconsistent with user
                            expectations.
                          </p>
                          <p>
                            You can also use this to diagnose problems with
                            RecordSponge's analysis, usually related to search
                            results including:
                          </p>
                          <ul className="ml4 mt2">
                            <li>
                              Search results contain other people's records (see{" "}
                              <a
                                href="#smart-search"
                                className="bb-dotted-2 hover-blue"
                              >
                                Smart Search
                              </a>
                              )
                            </li>
                            <li>
                              OECI records incomplete or inaccurate (common with
                              records from before 2005)
                            </li>
                          </ul>
                        </div>
                      </Accordion>
                      <Accordion title="Expanded View" id="expanded-view">
                        <div className="mt1">
                          <p>
                            When viewing from the Expanded View, it will pull
                            all of RecordSponge's functionality into the
                            existing page.
                          </p>
                          <p>
                            The "Summary Results" panel will be separated into
                            "Review Summary" and "Counts". The full results for
                            each charge will be placed within the "Analyze
                            Cases" panel. The "Quick Links" panel contains links
                            that let you quickly navigate to specific cases.
                          </p>
                          <Figure
                            src="/img/expanded-view.webp"
                            alt="expanded view results"
                            caption="Example of Expanded View"
                            className="mt3"
                          />
                          <p>
                            At the end of the page past the full results, the
                            button for downloading the analysis report as a PDF
                            as well as the form to generate paperwork will be
                            available.
                          </p>
                          <Figure
                            src="/img/expanded-view-generate-paperwork.webp"
                            alt="expanded view generate paperwork"
                            caption="Example of Expanded View Generate Paperwork"
                            className="mt3"
                          />
                        </div>
                      </Accordion>
                      <EditingGuide />
                    </div>
                  </Accordion>

                  <Accordion title="Fines and Fees" id="fines-and-fees">
                    <p className="mt1 mb3">
                      Under "Generate Paperwork," any outstanding Circuit Court
                      balance owed by the client will appear (see{" "}
                      <strong>Balance due by county</strong> in{" "}
                      <a
                        href="#example-search-results"
                        className="bb-dotted-2 hover-blue"
                      >
                        example search result
                      </a>
                      ). Oregon law gives judges broad discretion to reduce or
                      waive non-restitution fines and fees.
                    </p>
                    <p>
                      To request a reduction or waiver, applicants must file a
                      Motion to Modify Financial Obligations (see{" "}
                      <a href="#feewaiver" className="bb-dotted-2 hover-blue">
                        Financial Obligations
                      </a>{" "}
                      for details) in the court where the balance is owed.
                    </p>
                    <div className="bg-gray-blue-2 shadow br3 pa3 mt3 mb3 ba">
                      <h3 className="fw7">Exclusions and Limitations</h3>
                      <p>
                        "Balance due by county" only shows fines and fees owed
                        in Circuit Court. It does not include municipal courts
                        (where many traffic violations are handled) or
                        restitution that has been sent to a collection agency.
                        Restitution is not eligible for waiver and may not
                        appear.
                      </p>
                    </div>
                  </Accordion>
                </div>
              </Accordion>
              <Accordion
                title="Part 3: Complete Paperwork"
                id="complete-paperwork"
              >
                <div className="flex flex-column gap4 mt2">
                  <Accordion
                    title="Paperwork for Expungement"
                    id="generate-paperwork"
                  >
                    <div className="mt1 mb2">
                      <p>
                        When a search is finished, the "Search Summary" panel
                        will appear with cases that may or may not be eligible
                        for expungement.
                      </p>
                      <Figure
                        src="/img/search-results.webp"
                        alt="search results"
                        caption="Example search result"
                        className="mb3"
                      />
                      <p className="mb1">
                        If a client has eligible charges, the "Search Summary"
                        will display a button to "Generate Paperwork".
                      </p>
                      <IconButton
                        styling="link"
                        buttonClassName="hover-blue"
                        iconClassName="fa-bolt pr2"
                        displayText="Generate Paperwork"
                      />
                      <p className="mb3">
                        Clicking the button will redirect you to a form for
                        entering the information needed to file the expungement.
                      </p>
                      <Figure
                        src="/img/generate-expungement-forms.webp"
                        alt="generate expungement forms"
                        caption="Generate expungement forms"
                        className="mb3"
                        imgClassName="ba b--gray scroll-mt-20"
                        id="generate-paperwork-img"
                      />
                      <p>
                        After you input the information, you can download the
                        expungement paperwork from RecordSponge via the
                        "Download Expungement Packet" button.
                      </p>
                      <span
                        className="bg-blue white fw6 dib br2 pv3 ph4 mt1 mb2 tc"
                        aria-hidden="true"
                      >
                        Download Expungement Packet (N charges)
                      </span>
                      <p>
                        The download is a .zip file containing all eligible
                        cases, with one PDF per case. Each PDF must be printed
                        and signed by the client.
                      </p>
                      <p className="mb3">
                        RecordSponge will also generate a Request form to Oregon
                        State Police. You will need to complete this form
                        manually and mail a completed copy to Oregon State
                        Police at:
                        <span className="db pt2 scroll-mt-20" id="osp-address">
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
                      <p className="mb3">
                        You will also need to{" "}
                        <a
                          href="#fingerprints"
                          className="bb-dotted-2 hover-blue"
                        >
                          obtain fingerprints
                        </a>{" "}
                        to include with this mailing (see Part 4).
                      </p>
                    </div>
                  </Accordion>
                  <Accordion
                    title="Modify Financial Obligations"
                    id="feewaiver"
                  >
                    <div className="mt1 mb2">
                      <h3 className="f4 fw7 mt1">
                        Motions to Modify Financial Obligation
                      </h3>
                      <p className="mb3">
                        RecordSponge can also help reduce fines and fees on
                        criminal cases. Oregon Circuit Courts other than
                        Multnomah County now accept a standardized Motion for
                        this purpose. A copy of this Motion is available{" "}
                        <a
                          className="bb hover-blue"
                          href="https://www.courts.oregon.gov/forms/Documents/MotionModFinancialObligations.pdf"
                          target="_blank"
                          rel="noreferrer noopener"
                        >
                          here
                        </a>
                        .
                      </p>
                      <ul className="ml4">
                        <li>
                          A Motion must be filed for each case, but the content
                          can be identical
                        </li>
                        <li>Restitution cannot be waived</li>
                        <li>No separate filing fee</li>
                        <li>
                          The Motion is granted entirely at the Court's
                          discretion
                        </li>
                        <li>
                          These Motions are filed and served the same way as
                          expungement motions (see{" "}
                          <a
                            href="#file-paperwork"
                            className="bb-dotted-2 hover-blue"
                          >
                            File Paperwork
                          </a>
                          )
                        </li>
                      </ul>
                      <p className="mb3">
                        On the{" "}
                        <a
                          href="#generate-paperwork-img"
                          className="bb-dotted-2 hover-blue"
                        >
                          Generate Paperwork
                        </a>{" "}
                        page, click the "Motions to Waive Fees" button and
                        complete the additional questions in the form.
                      </p>
                      <span
                        className="bg-blue white fw6 dib br2 pv3 ph4 mb2 tc"
                        aria-hidden="true"
                      >
                        {"Motions to Waive Fees (N cases) >>"}
                      </span>
                    </div>
                  </Accordion>
                </div>
              </Accordion>
              <Accordion
                title="Part 4: Obtain Fingerprints"
                id="obtain-fingerprints"
              >
                <p className="mt1">
                  After completing your paperwork (see{" "}
                  <a
                    href="#generate-paperwork"
                    className="bb-dotted-2 hover-blue"
                  >
                    Part 3
                  </a>
                  ), you will need to obtain fingerprints and mail them along
                  with the OSP request form. You will also need to{" "}
                  <a href="#file-paperwork" className="bb-dotted-2 hover-blue">
                    file paperwork
                  </a>{" "}
                  with the appropriate courts (see Part 5).
                </p>
                <h3 className="f4 fw7 scroll-mt-20" id="fingerprints">
                  Fingerprints
                </h3>
                <p>
                  Fingerprints must be printed or inked directly onto cardstock
                  — digital prints are not accepted. These can be obtained at
                  sheriff's offices or fingerprinting services.
                </p>
                <p>
                  Another option is to do it yourself with the following
                  materials:
                </p>
                <ul className="ml4">
                  <li className="mb1">
                    Lee Inkless Fingerprint Pad (available on Amazon), $17 for a
                    3-pack, which serves several hundred people
                  </li>
                  <li className="mb1">
                    Fingerprint Cards, Applicant FD-258 (available on Amazon),
                    $21 for a 50 pack
                  </li>
                </ul>
                <h3 className="f4 fw7 scroll-mt-20" id="osp-form">
                  Mail Fingerprints to OSP
                </h3>
                <p>
                  Included in your expungement packet should be a form titled:
                  "Oregon State Police REQUEST FOR SET ASIDE CRIMINAL RECORD
                  CHECK."
                </p>
                <p>Fill out the sections:</p>
                <ul className="ml4 mb2">
                  <li>"Other Names You are Known By"</li>
                  <li>"Circuit or Municipal Court"</li>
                  <li>
                    Check the box corresponding to whether you are seeking an
                    expungement for a conviction or only arrests.
                  </li>
                </ul>
                <p className="mb3">
                  If you are seeking expungement of at least one conviction, you
                  will need to include a check or money order made out to
                  "Oregon State Police" for $33.
                </p>
                <p className="mb3">
                  Mail the completed form and fingerprints to the{" "}
                  <a href="#osp-address" className="bb-dotted-2 hover-blue">
                    OSP mailing address
                  </a>{" "}
                  noted in Part 3.
                </p>
              </Accordion>
              <Accordion title="Part 5: File Paperwork" id="file-paperwork">
                <p className="mt1 mb2">
                  Ensure you have completed your paperwork (see{" "}
                  <a
                    href="#generate-paperwork"
                    className="bb-dotted-2 hover-blue"
                  >
                    Part 3
                  </a>
                  ) before filing. These steps apply to both expungement motions
                  and{" "}
                  <a href="#feewaiver" className="bb-dotted-2 hover-blue">
                    Motions to Modify Financial Obligation
                  </a>
                  .
                </p>
                <ul className="ml4">
                  <li>
                    You will need to file the paperwork with the courthouse in
                    each county in which you have cases you wish to expunge.
                    File with the Clerk of court. There should be no filing fee.
                  </li>
                  <li>Request two copies from the Clerk.</li>
                  <li>
                    Serve the District Attorney's office with one of these
                    copies.
                  </li>
                </ul>
                <h3 className="f4 fw7">Next Steps</h3>
                <ul className="ml4">
                  <li>
                    Most expungements process without objection from the State.{" "}
                    <em>If</em> the District Attorney objects, email{" "}
                    <a
                      className="bb hover-blue"
                      href="mailto:michael@qiu-qiulaw.com"
                    >
                      michael@qiu-qiulaw.com
                    </a>{" "}
                    immediately — we can assist even if we don't represent you
                    in court.
                  </li>
                  <li>
                    By law, the District Attorney is required to respond within
                    four months. To review any communication you receive, email{" "}
                    <a
                      className="bb hover-blue"
                      href="mailto:roe@qiu-qiulaw.com"
                    >
                      roe@qiu-qiulaw.com
                    </a>
                  </li>
                  <li>
                    Once processed, you will receive paper confirmation from the
                    court. Keep physical and electronic copies — obtaining
                    copies of expunged documents later is extremely costly.
                  </li>
                  <li>
                    Notify background check companies of your expungement.
                    Expungement Clearinghouse is a free service that notifies
                    major background checking companies, available at{" "}
                    <a
                      href="https://www.continuingjustice.org/our-projects/criminal-database-update/"
                      className="bb hover-blue"
                      target="_blank"
                      rel="noreferrer noopener"
                    >
                      https://www.continuingjustice.org/our-projects/criminal-database-update/
                    </a>
                  </li>
                </ul>
              </Accordion>
              <Accordion title="Frequently Asked Questions" id="faqs">
                <div className="mt2 mb3">
                  <Accordion
                    title="I got results for different records when I searched in OECI and when I searched in RecordSponge. What happened?"
                    type="qna"
                  >
                    <div className="mt1">
                      <strong>A:</strong> I receive this question more than any
                      other, which is why I’m addressing it first. Every single
                      time I’ve gotten the question from a user, the solution
                      has always been the same: the search inputs were
                      different. As explained in{" "}
                      <a className="bb-dotted-2 hover-blue" href="#search">
                        Search
                      </a>
                      , court records are sometimes incomplete or inaccurate, so
                      we recommend "Smart Searching" to capture all (but only
                      applicable) records. If you actually get different records
                      when using the same search, please email me at{" "}
                      <a
                        className="bb hover-blue"
                        href="mailto:michael@qiu-qiulaw.com"
                      >
                        michael@qiu-qiulaw.com
                      </a>
                      .
                    </div>
                  </Accordion>
                </div>
                <div className="mb2">
                  <Accordion
                    title="How long will it take to expunge my record?"
                    type="qna"
                  >
                    <div className="mt1">
                      <strong>A:</strong> It depends on the County. Visit the{" "}
                      <a
                        className="link hover-blue underline"
                        href="/community"
                      >
                        Community Board
                      </a>{" "}
                      for details.
                    </div>
                  </Accordion>
                </div>
              </Accordion>
            </div>
          </section>
        </article>
      </main>
    </div>
  );
}

export default Manual;
