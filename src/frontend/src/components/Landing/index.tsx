import React from "react";
import PartnerTable from "../PartnerTable";
import { Link } from "react-router-dom";
import SVG from "../common/SVG";

class Landing extends React.Component {
  componentDidMount() {
    document.title = "RecordSponge - Home";
  }

  render() {
    return (
      <>
        <main className="f5 f4-ns navy bg-white mt5">
          <div className="overflow-x-hidden relative">
            <div className="flex justify-center mb5">
              <div className="flex justify-center items-center w-100 shadow bg-blue white pv3 ph4">
                <i
                  className="fas fa-award f2 light-blue"
                  aria-hidden="true"
                ></i>
                <p className="fw6 ml3">
                  <a
                    href="https://www.osbar.org/osbevents"
                    className="underline-hover white"
                  >
                    Winner of the 2020 Oregon State Bar Technology & Innovation
                    Award
                  </a>
                </p>
              </div>
            </div>

            <div className="mw8 center ph4 pb5">
              <div className="flex-l mt5">
                <h1 className="f3 f2-ns fw9 w-60-l mr2-l mt0 mb3">
                  Making Record <br />
                  Expungement Affordable
                </h1>
                <p className="f5 w-40-l lh-title mw6">
                  <span className="db w4 bb bw2 b--blue pt3 mt2 mb2"></span>
                  RecordSponge is software that helps community organizations
                  quickly analyze an individual’s criminal history to determine
                  if they qualify to have their records expunged.
                </p>
              </div>
            </div>

            <div className="flex flex-column justify-center items-center w-100 shadow white pv4 ph4 bg-washed-blue bt b--lightest-blue">
              <div className="flex w-100 mw7 relative left--1-ns">
                <SVG
                  name="oregonSilouhette"
                  className="mr3 w4 h3 mw4 mh3 flex-none" 
                  viewBox="0 0 110 80"
                />
                <p className="fw6 ml3 mt3">
                  <a
                    href="/community"
                    className="f4 blue fw5 link"
                  >
                    <span className="navy fw9 mr1">NEW</span> 
                    Visit the Community Board for insights into best practices by County
                    <span className="fas fa-arrow-right lh-solid pl3 f5 fw9"></span>
                  </a>
                </p>
              </div>
            </div>

            <div className="w-100 bg-navy h1 overflow-hidden">
                <span className="db h-25 w-100 bg-dark-blue"></span>
            </div>

            <div className="bg-navy pv6">
              <div className="mw7 center">
                <div className="mh4">
                  <h2 className="white tc f3 f2-ns fw9 mb3">
                    Are you looking to clear your record?
                  </h2>
                  <p className="white tc center mw6 mb4">
                    Select a partner below near you. They can provide your
                    analysis and help you file for expungement.
                  </p>
                </div>
                <PartnerTable />
                <span className="db w4 center bb bw2 b--blue mb3"></span>
                <p className="tc fw7 white mw7 mh4">
                  Over 27,000 analyses delivered as of January 2026
                </p>
              </div>
            </div>

            <div className="bg-lightest-blue1 pv6">
              <div className="flex flex-wrap justify-around w-90 center ph4 pb0">
                <div className="mw7 flex-auto mb5">
                  <div className="mw7 center">
                    <h3 className="f3 f2-ns fw9 mb3">Expungement in Oregon</h3>
                    <p className="lh-copy mb5">
                      For many folks who have had run-ins with the criminal justice system,
                      punishment doesn't end with the end of their sentence. A criminal
                      conviction or arrest can follow a person around for the rest of their
                      life, well past the period of incarceration, probation, and financial
                      penalty. This prevents them from accessing education, employment,
                      housing, and services which might otherwise help them integrate back
                      into society.
                    </p>
                  </div>
                  <div className="mw9 center tc mb5">
                    <img
                      className="wipe-illustrations"
                      alt=""
                      src="/img/wipe-illustrations-v3.jpg"
                    />
                  </div>
                  <div className="mw7 center">
                    <p className="lh-copy mb4">
                      The State of Oregon provides a way for people to seal certain items
                      from their records (effectively removing them), but the rules for
                      determining which items are eligible are complex and prone to error
                      when applying them by hand. As a result, expungement analysis is
                      expensive in Portland - ranging from $1,000 to $3,000 when performed
                      by private attorneys.
                    </p>
                    <p className="lh-copy mb5">
                      And so we created RecordSponge to greatly increase access to
                      expungement by automating the legal analysis. We are seeking more
                      partners to administer RecordSponge.
                    </p>
                    <div className="mb0">
                      <Link
                        className="inline-flex items-center f3-ns blue hover-dark-blue fw7"
                        to="/partner-interest"
                        onClick={() => window.scrollTo(0, 0)}
                      >
                        <span>Learn more about partnering</span>
                        <span
                          className="fas fa-arrow-right lh-solid pt1 pl2"
                          aria-hidden="true"
                        ></span>
                      </Link>
                    </div>
                  </div>
                </div>
                <div>
                  <ul className="feature-list center list">
                    <li className="flex pv3">
                      <span>
                        <span className="diamond dib rotate-45 br4 bg-white pa3">
                          <span
                            className="fas fa-search f4 rotate-315 blue"
                            aria-hidden="true"
                          ></span>
                        </span>
                      </span>
                      <span className="fw5 pt2 pt1-ns pl3">
                        Search the OECI database for records
                      </span>
                    </li>

                    <li className="flex pv3">
                      <span>
                        <span className="diamond dib rotate-45 br4 bg-white pa3">
                          <span
                            className="fas fa-pen f4 rotate-315 blue"
                            aria-hidden="true"
                          ></span>
                        </span>
                      </span>
                      <span className="fw5 pt2 pt1-ns pl3">
                        Edit or enter records manually
                      </span>
                    </li>

                    <li className="flex pv3">
                      <span>
                        <span className="diamond dib rotate-45 br4 bg-white pa3">
                          <span
                            className="fas fa-check f3 rotate-315 blue"
                            aria-hidden="true"
                          ></span>
                        </span>
                      </span>
                      <span className="fw5 pt2 pt1-ns pl3">
                        Get Instant eligibility results
                      </span>
                    </li>

                    <li className="flex pv3">
                      <span>
                        <span className="diamond dib rotate-45 br4 bg-white pa3">
                          <span
                            className="fas fa-bolt f3 rotate-315 blue pl1"
                            aria-hidden="true"
                          ></span>
                        </span>
                      </span>
                      <span className="fw5 pt2 pt1-ns pl3">
                        Automatically generate paperwork
                      </span>
                    </li>

                    <li className="flex pv3">
                      <span>
                        <span className="diamond dib rotate-45 br4 bg-white pa3">
                          <span
                            className="fas fa-compass f3 rotate-315 blue"
                            aria-hidden="true"
                          ></span>
                        </span>
                      </span>
                      <span className="fw5 pt2 pt1-ns pl3">
                        Guidance on how to file for expungement
                      </span>
                    </li>
                    <div className="hover-navy pt4">
                      <Link
                        className="f4 f3-ns fw7 link blue hover-navy"
                        to="/partner-interest"
                        onClick={() => window.scrollTo(0, 0)}
                      >
                        Getting started
                        <span
                          className="fas fa-arrow-right f5 blue pt1 pl2 hover-navy"
                          aria-hidden="true"
                        ></span>
                      </Link>
                    </div>
                  </ul>
                </div>
              </div>
            </div>

          <div className="bg-lightest-blue1 pt0 pb6">
            <div className="flex flex-column items-center justify-center w-100">
              <div className="mh4 w-100">
                <div className="flex flex-wrap justify-around items-center relative pa3 w-100">
                  <span
                    className="fas fa-arrow-left lh-solid blue pt1 pl2"
                    aria-hidden="true"
                  ></span>
                  
                  <blockquote className="w-100 w-30-ns">
                    <div className="center tc f3 mb1">
                      <span className="fas fa-quote-left blue" aria-hidden="true"></span>
                    </div>
                    <p className="mw7 lh-copy tc center mb3">
                      Having performed expungement analysis both with and without the
                      assistance of RecordSponge, I know that this program vastly
                      decreases the time to perform expungement analysis, and vastly
                      increases the number of people we can assist with expungements.
                    </p>
                    <footer className="mw7 tc center fw6 f5-ns mb5">
                      Leni Tupper, Portland Community College CLEAR Clinic
                    </footer>
                  </blockquote>

                  <blockquote className="w-100 w-30-ns">
                    <div className="center tc f3 mb1">
                      <span className="fas fa-quote-left blue" aria-hidden="true"></span>
                    </div>
                    <p className="mw7 lh-copy tc center mb3">
                      RecordSponge levels the playing field. It has been inspiring to see
                      people fully return to our community as their records are expunged –
                      Michael and his team have a heart for people, a knowledge of the
                      system, and a solution that works in RecordSponge.
                    </p>
                    <footer className="mw7 tc center fw6 f5-ns mb5">
                      Eric Guyer, Jackson County Community Justice Director
                    </footer>
                  </blockquote>

                  <blockquote className="w-100 w-30-ns">
                    <div className="center tc f3 mb1">
                      <span className="fas fa-quote-left blue" aria-hidden="true"></span>
                    </div>
                    <p className="mw6 lh-copy tc center mb3">
                      I love that I can just pull my phone out and tell someone whether
                      they can get their record expunged.
                    </p>
                    <footer className="mw7 tc center fw6 f5-ns mb5">
                      Sarah Kolb, Signs of Hope
                    </footer>
                  </blockquote>
                  
                  <span
                    className="fas fa-arrow-right lh-solid blue pt1 pl2"
                    aria-hidden="true"
                  ></span>
                </div>
              </div>
            </div>
          </div>

            <div className="mw8 flex-l center ph4 pv6">
              <div className="w-50-l mb5">
                <h2 className="f3 f2-ns fw9 mb3">Who We Are</h2>
                <p className="lh-copy mb3">
                  <a
                    className="link bb hover-dark-blue"
                    href="http://www.codepdx.org"
                  >
                    Code PDX
                  </a>{" "}
                  and{" "}
                  <a
                    className="link bb hover-dark-blue"
                    href="https://www.qiu-qiulaw.com"
                  >
                    Qiu-Qiu Law
                  </a>{" "}
                  have developed and continue to improve analytical software to
                  help expungement providers quickly determine which items on an
                  applicant's record are eligible for expungement.
                </p>
                <p className="lh-copy mb3">
                  The goal of this project is to make expungement available to
                  all Oregonians, regardless of their ability to pay. It further
                  seeks to provide these services in the communities that need
                  them the most.
                </p>
                <Link
                  className="inline-flex items-center blue hover-dark-blue fw7"
                  to="/about"
                  onClick={() => window.scrollTo(0, 0)}
                >
                  <span>More about us</span>
                  <span
                    className="fas fa-arrow-right lh-solid pt1 pl2"
                    aria-hidden="true"
                  ></span>
                </Link>
              </div>
              <div className="w-50-l tc pa5-l pa3 mb5 ml4-l">
                {/* SVG kept as is as it uses standard SVG attributes, but added class for targeting */}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  xmlnsXlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 257 243"
                  aria-hidden="true"
                  className="who-we-are-logos w-100 h-auto"
                >
                  {/* ... SVG Definitions ... */}
                  <defs>
                    <path id="a" d="M.453.556H21.55v13.803H.453z"></path>
                    <path id="c" d="M47.382.31c-.422.179-.771.43-1.047.757a2.998 2.998 0 00-.601 1.16 5.46 5.46 0 00-.187 1.462v1.058l-1.369.104v1.783h1.369v8.294h2.385V6.634h1.99V4.747h-1.99v-1.1c0-1.146.428-1.72 1.285-1.72.373 0 .747.083 1.12.249l.457-1.784a4.953 4.953 0 00-.84-.249A4.968 4.968 0 0048.926.04c-.608 0-1.123.09-1.545.27zM28.222.289v3.69l.083 1.639a5.902 5.902 0 00-1.203-.819c-.4-.2-.891-.3-1.472-.3a3.67 3.67 0 00-1.607.372c-.519.25-.978.602-1.379 1.058-.401.456-.722 1.016-.964 1.68-.242.663-.363 1.41-.363 2.24 0 1.686.376 2.996 1.13 3.929.753.933 1.773 1.4 3.059 1.4.552 0 1.078-.132 1.576-.395.497-.263.933-.58 1.306-.954h.083l.166 1.1h1.97V.288h-2.385zm-3.847 12.058c-.393-.574-.59-1.414-.59-2.519 0-1.08.228-1.908.684-2.489.456-.58 1.016-.87 1.68-.87.346 0 .687.061 1.026.186.339.124.688.346 1.047.663v4.749c-.663.76-1.376 1.14-2.135 1.14-.748 0-1.318-.287-1.712-.86zM4.006 1.596c-.754.317-1.41.78-1.97 1.388-.56.609-1.002 1.351-1.327 2.23-.325.878-.487 1.87-.487 2.975 0 1.12.159 2.116.476 2.986.319.871.751 1.604 1.297 2.199a5.347 5.347 0 001.939 1.347 6.306 6.306 0 002.405.456c.87 0 1.662-.17 2.374-.507a5.825 5.825 0 001.897-1.463l-1.286-1.514a5.05 5.05 0 01-1.285 1.006c-.47.256-1.009.383-1.617.383-1.148 0-2.057-.438-2.727-1.316-.67-.877-1.006-2.09-1.006-3.639 0-.76.093-1.445.28-2.052.187-.61.45-1.124.788-1.545.339-.423.74-.747 1.202-.975a3.409 3.409 0 011.525-.342c.525 0 .995.107 1.41.321.415.214.802.5 1.161.86l1.286-1.555c-.43-.456-.975-.856-1.638-1.202-.664-.346-1.424-.52-2.281-.52-.857 0-1.663.16-2.416.479zm96.097-.23l-1.43 3.007c-.153.319-.3.643-.446.976-.145.331-.3.697-.467 1.098h-.083c-.207-.4-.39-.767-.55-1.098a34.69 34.69 0 00-.486-.976l-1.493-3.006h-2.675L96.08 7.94l-3.857 6.987h2.55l1.618-3.193a91.628 91.628 0 00.995-2.218h.083c.207.414.397.798.57 1.15.173.353.35.709.53 1.068l1.658 3.193h2.675l-3.857-6.884 3.608-6.677h-2.551zm-18.334 0v13.562h3.754c1.008 0 1.911-.145 2.705-.435a5.362 5.362 0 002.032-1.296c.561-.574.99-1.29 1.286-2.146.298-.857.446-1.845.446-2.966 0-2.239-.58-3.919-1.742-5.039-1.161-1.119-2.778-1.68-4.852-1.68h-3.629zm2.405 1.95h1.058c1.369 0 2.427.38 3.172 1.14.747.761 1.121 1.971 1.121 3.63 0 1.672-.37 2.906-1.11 3.7-.74.796-1.8 1.193-3.183 1.193h-1.058V3.316zm-13.42-1.95v13.562h2.407V9.952h1.949c.732 0 1.414-.087 2.042-.259a4.554 4.554 0 001.638-.81 3.826 3.826 0 001.09-1.378c.262-.553.393-1.203.393-1.95 0-.787-.131-1.448-.394-1.98a3.397 3.397 0 00-1.1-1.295 4.479 4.479 0 00-1.668-.705 9.889 9.889 0 00-2.084-.208h-4.272zm2.407 1.93h1.679c1.01 0 1.773.161 2.291.487.519.324.778.916.778 1.773 0 1.645-.996 2.467-2.986 2.467H73.16V3.295zm-8.862 1.731c-.51.352-.947.86-1.306 1.524h-.083l-.166-1.804h-1.97v10.181h2.385v-6.22c.318-.775.698-1.318 1.14-1.628.443-.312.864-.466 1.265-.466a3.113 3.113 0 011.057.165l.416-2.073c-.29-.139-.678-.208-1.162-.208-.539 0-1.064.177-1.576.529zm-11.511-.166a4.678 4.678 0 00-1.546 1.047 4.967 4.967 0 00-1.067 1.68c-.263.664-.394 1.417-.394 2.26s.13 1.597.394 2.26a4.967 4.967 0 001.067 1.68c.45.456.964.801 1.546 1.036.58.236 1.188.353 1.824.353.636 0 1.248-.117 1.835-.353a4.41 4.41 0 001.545-1.036 5.187 5.187 0 001.068-1.68c.27-.663.405-1.416.405-2.26 0-.843-.136-1.596-.405-2.26a5.187 5.187 0 00-1.068-1.68 4.544 4.544 0 00-1.545-1.047 4.778 4.778 0 00-1.835-.363 4.7 4.7 0 00-1.824.363zm.072 7.444c-.421-.615-.633-1.434-.633-2.457 0-1.037.212-1.863.633-2.477.422-.616 1.005-.924 1.752-.924.746 0 1.334.308 1.763.924.428.614.643 1.44.643 2.477 0 1.023-.215 1.842-.643 2.457-.429.615-1.017.923-1.763.923-.747 0-1.33-.308-1.752-.923zM34.861 4.871a4.653 4.653 0 00-1.504 1.058c-.435.456-.784 1.016-1.047 1.68-.262.663-.393 1.41-.393 2.24 0 .843.127 1.592.383 2.25a4.771 4.771 0 001.068 1.668c.457.456.989.805 1.597 1.047a5.272 5.272 0 001.97.363 5.62 5.62 0 001.866-.311 7.316 7.316 0 001.617-.788l-.808-1.493a5.47 5.47 0 01-1.13.55 3.75 3.75 0 01-1.234.197c-.83 0-1.51-.245-2.043-.736-.532-.491-.854-1.192-.964-2.105h6.47a4.23 4.23 0 00.073-.498c.02-.207.03-.429.03-.663 0-.705-.09-1.355-.27-1.95a4.405 4.405 0 00-.797-1.534 3.56 3.56 0 00-1.317-.995c-.526-.235-1.133-.353-1.825-.353-.594 0-1.175.124-1.742.373zm.208 2.116a2.258 2.258 0 011.596-.643c.705 0 1.227.224 1.566.673.338.45.508 1.068.508 1.857h-4.521c.11-.83.394-1.459.85-1.887zM13.952 4.86a4.67 4.67 0 00-1.544 1.047 4.96 4.96 0 00-1.069 1.68c-.262.664-.394 1.417-.394 2.26s.132 1.597.394 2.26a4.96 4.96 0 001.069 1.68c.449.456.963.801 1.544 1.036.581.236 1.19.353 1.826.353.635 0 1.247-.117 1.835-.353a4.41 4.41 0 001.544-1.036 5.169 5.169 0 001.068-1.68c.27-.663.404-1.416.404-2.26 0-.843-.135-1.596-.404-2.26a5.169 5.169 0 00-1.068-1.68 4.544 4.544 0 00-1.544-1.047 4.783 4.783 0 00-1.835-.363c-.636 0-1.245.121-1.826.363zm.073 7.444c-.422-.615-.633-1.434-.633-2.457 0-1.037.21-1.863.633-2.477.421-.616 1.005-.924 1.753-.924.745 0 1.332.308 1.761.924.429.614.644 1.44.644 2.477 0 1.023-.215 1.842-.644 2.457-.429.615-1.016.923-1.761.923-.748 0-1.332-.308-1.753-.923z"
                    ></path>
                    <path id="e" d="M3.888 1.358C2.411 1.97 1.597 2.604.648 3.052c-.948.449-.777 1.877 0 2.26.778.381.485-.082 2.519 1.046 1.122.622 3.937.991 4.946 2.603 4.257 6.799 2.16 1.61 2.237.53.17-2.41-2.3-2.672-3.536-3.452-1.237-.779-2.4-.862-2.926-1.926-.525-1.063.361-.893 1.357-1.647.995-.755 2.007-.779 1.57-1.87C6.688.284 6.515.162 6.3.162c-.54 0-1.358.757-2.412 1.196z"></path>
                    <path id="g" d="M.57 3.016c-.305 2.47 2.23 2.871 3.463 3.74 1.235.868 3.176 1.053 3.66 2.174.485 1.122-1.164.863-2.233 1.585-1.068.722-1.129 1.04-.957 1.402.17.362.74.362 2.298-.19 1.556-.55 2.432-1.158 3.434-1.567 1.002-.409.903-1.888.122-2.322-.781-.435-.505.058-2.542-1.211-1.125-.701-4.01-1.233-4.964-2.945C1.305.911.629.006.377.006c-.405 0 .278 2.329.194 3.01z"></path>
                    <path id="i" d="M15.027.777c-1.852.933-3.832 2.46-4.57 2.716-.736.258-4.817.414-5.72 1.258-.902.844-.937 1.849-.975 2.931-.037 1.085 0 1.65-1.418 2.218-1.42.569-1.511 4.53-1.868 6.55-.357 2.018-.44 4.41.806 6.915 1.247 2.505 3.034 2.657 5.112 3.098 2.078.441 3.78.462 5.195 1.71 1.416 1.25 3.693 3.175 5.564 3.24 1.87.065 4.357-.495 5.602-1.65 1.245-1.156 1.72-2.832 1.746-3.583.027-.751 1.787-2.012 1.82-2.99.035-.977-.907-1.649.878-2.459 1.785-.81 2.082-3.052 1.859-4.94-.224-1.888-.974-5.472-.912-7.257.062-1.784-1.558-2.349-3.558-3.465-2-1.116-2.556-2.703-3.913-4.025-.7-.683-1.69-.98-2.737-.98-.982 0-2.016.262-2.91.713zm-9.732 9.5c.279-.671-1.423-2.582-.273-3.75 1.284-1.305 3.495-.573 5.077-1.333a46.987 46.987 0 003.665-1.992c1.19-.707 1.452-1.113 2.914-1.588.805-.26 1.585-.26 2.546.71.274.278.525.566.788.848.616.658 1.476 1.433 2.58 2.323 1.657 1.336 3.607 2.3 3.883 3.541.276 1.24.547 3.405.916 4.816.37 1.412.664 3.892.226 4.988-.438 1.096-1.243 1.656-2.46 1.613-1.216-.042-1.115.57-.805.984.31.414 1.501 1.14.7 2.057-.803.915-1.644 1.547-1.693 2.957-.049 1.411-1.332 2.262-2.18 2.797-.847.535-3.561.637-5.493-.497-1.933-1.133-3.223-3.287-7.452-3.9-2.819-.408-4.48-1.23-4.985-2.467-1.098-1.57-1.27-3.417-1.148-5.318.1-1.57.298-1.017.281-2.267-.01-.717-.347-2.363.128-3.27.363-.693.798-.98 1.545-.958.292.008.542.11.754.11.193 0 .354-.084.486-.403z"></path>
                    <path id="k" d="M2.152 1.537C.96 3.008.462 5.35.352 8.475c-.108 3.125.854 4.514 1.95 5.698 1.098 1.185 2.83 1.898 5.431 2.83 2.6.931 8.922 1.365 12.014-1.954 3.094-3.32 3.048-7.927 2.973-9.14-.074-1.214-.68-1.912-1.132-1.155-.452.757-.056 1.606-.106 3.017-.049 1.412-1.511 4.796-2.492 6.057-.98 1.26-3.488 2.148-6.033 2.06-2.543-.089-7.043-1.588-9.18-2.591-2.136-1.004-1.602-4.388-1.54-6.198.064-1.81.448-3.851.856-4.687C3.5 1.576 4.587.934 4.229.374 4.114.195 3.983.099 3.817.099c-.35 0-.854.437-1.665 1.438z"></path>
                    <path id="m" d="M.653 1.752c-.905.792.085 1.578.521.986.435-.592.667-.519 1.23-.925.563-.405 1.252-.45 1.89-.428.638.022 3.17 1.277 4.081 1.85.91.57 3.948 2.726 4.167 4.925.219 2.2-1.004 3.684-1.349 4.504-.343.82-.789 1.565-.055 1.591.734.026.834-.576 1.872-1.886 1.039-1.31.717-5.427.571-6.54-.147-1.112-.721-1.553-1.565-2.189-.844-.636-2.699-1.408-3.298-1.787C8.12 1.473 6.758.804 4.803.409a4.524 4.524 0 00-.899-.093c-1.464 0-2.493.772-3.251 1.436z"></path>
                    <path id="o" d="M1.527.266C.41.749.573 2.844.291 4.11c-.28 1.266-.603 3.93.317 5.305.918 1.375 4.623 1.858 5.29 1.6.667-.259 1.375-1.206 2.622-1.243 1.246-.037 3.213-.566 3.961-2.106.748-1.54.555-1.881.074-2.123-.48-.242-1.049 1.493-1.714 2.066-.665.573-2.553.783-3.708.945-1.154.16-1.786 1.107-3.04.579-1.255-.528-2.164-1.765-2.299-3.665-.134-1.901-.353-3.642.348-3.992.596-.298.543-1.314-.174-1.314-.126 0-.273.031-.44.104z"></path>
                    <path id="q" d="M1.316 1.73c1.078.637 1.651.739 2.019 1.078.368.34 1.366 1.033 1.157 1.617-.209.584-1.003.905-1.033 1.761-.03.856 1.105 1.57 1.656.603.55-.969 2.176-1.375 2.733-2.042.558-.667-.152-1.814-1.013-1.962-.86-.148-2.55.03-2.773-.96C3.837.839 2.178.332.96.29L.874.288c-1.108 0-.612.822.442 1.442z"></path>
                    <path id="s" d="M.71.522c-.368.52-.694 1.436-.585 2.51.11 1.075.32 2.131.997 2.5.678.368 1.61-.055 1.384-.806-.226-.75-.872-1.422-.999-2.029-.127-.608.203-1.044.48-1.73.177-.441-.25-.714-.675-.714C1.076.253.84.336.71.522z"></path>
                  </defs>
                  <g fill="none" fillRule="evenodd">
                    <path fill="#F3F8FF" fillRule="nonzero" d="M241.5 0h-226C7.216 0 .5 6.716.5 15v213c0 8.284 6.716 15 15 15h226c8.284 0 15-6.716 15-15V15c0-8.284-6.716-15-15-15zm0 9a6 6 0 016 6v213a6 6 0 01-6 6h-226a6 6 0 01-6-6V15a6 6 0 016-6h226z"></path>
                    <path fill="#002656" d="M101.3 176.633c0-7.098-3.845-10.015-7.631-10.015-3.732 0-7.435 2.833-7.435 9.846 0 6.762 3.34 9.707 7.435 9.707 4.235 0 7.63-3.057 7.63-9.538zm2.804 11.782c-.448.533-1.065.785-1.767.785-1.374 0-3.141-.981-5.105-3a10.569 10.569 0 01-3.563.616c-6.229 0-10.044-5.106-10.044-10.267 0-5.303 3.9-10.548 10.268-10.548 5.499 0 9.987 4.46 9.987 10.463 0 3.675-1.795 6.902-4.628 8.753.785.87 2.917 3.31 4.291 3.31a.924.924 0 00.533-.168l.028.056zm19.579-11.782c0-7.098-3.844-10.015-7.63-10.015-3.733 0-7.435 2.833-7.435 9.846 0 6.762 3.339 9.707 7.434 9.707 4.236 0 7.63-3.057 7.63-9.538zm2.805 11.782c-.449.533-1.066.785-1.767.785-1.375 0-3.142-.981-5.105-3a10.569 10.569 0 01-3.564.616c-6.228 0-10.043-5.106-10.043-10.267 0-5.303 3.899-10.548 10.267-10.548 5.5 0 9.988 4.46 9.988 10.463 0 3.675-1.796 6.902-4.629 8.753.786.87 2.918 3.31 4.292 3.31a.924.924 0 00.533-.168l.028.056zm20.728-5.498c-.028 2.356-.169 2.468-.169 3.702-2.61-.084-3.17-.084-5.78-.084-2.131 0-5.048.028-5.637.056v-.14c1.346-.224 1.599-.645 1.599-2.552v-15.065c0-2.245-.365-2.385-1.404-2.553v-.14a53.855 53.855 0 004.882 0v.14c-1.038.168-1.403.308-1.403 2.553v16.691c.309.113 1.066.169 2.384.169 4.378 0 4.967 0 5.387-2.777h.14zm8.862-1.319c-.589-.56-1.626-.897-2.692-.897-2.02 0-3.06 1.458-3.06 2.86 0 1.263.842 2.47 2.555 2.47 1.29 0 2.384-.618 3.197-1.544v-2.889zm3.59 3.787c-.42.674-1.037 1.432-2.019 1.432-1.01 0-1.57-.758-1.57-1.767-1.095 1.064-2.581 1.767-4.18 1.767-2.386 0-3.592-1.488-3.592-3.087 0-1.963 1.74-3.562 4.518-3.562 1.15 0 2.412.336 3.253.925v-4.741c0-1.768-.673-2.777-2.552-2.777-1.515 0-3.171 1.122-3.255 3.534h-1.43c.392-2.525 2.496-4.04 4.91-4.04 2.019 0 4.123.646 4.123 3.647v7.379c0 1.15.196 1.57.813 1.57.253 0 .533-.056.926-.42l.056.14z"></path>
                    <g transform="translate(158.85 172.626)">
                      <mask id="b" fill="#fff"><use xlinkHref="#a"></use></mask>
                      <path fill="#002656" d="M13.835 14.359L10.72 5.297 6.794 14.36h-.198L1.968 2.043C1.548.92 1.183.837.453.697V.556c.392 0 1.319.028 2.329.028 1.065 0 2.02-.028 2.412-.028v.141c-.842.112-1.262.251-1.262.756 0 .198.084.477.196.815l3.226 8.977 3.002-6.958L9.6 2.043C9.262 1.06 8.84.92 7.804.697V.556a70.4 70.4 0 003.31.084c1.122 0 1.739-.056 2.777-.084v.141c-.702.168-1.29.477-1.992 1.992l2.72 8.556 3.255-7.126c.505-1.094.814-1.88.814-2.384 0-.618-.42-.954-1.458-1.038V.556c.393 0 1.038.028 2.272.028.926 0 1.655-.028 2.048-.028v.141c-.954.223-1.487.335-3.114 3.927l-4.405 9.735h-.196z" mask="url(#b)"></path>
                    </g>
                    <path fill="#F3F8FF" fillRule="nonzero" d="M252 117v9H5v-9z"></path>
                    <g transform="translate(77 70.61)">
                      <mask id="d" fill="#fff"><use xlinkHref="#c"></use></mask>
                      <path fill="#052A59" d="M-1.218 16.617h105.561V-1.4H-1.218z" mask="url(#d)"></path>
                    </g>
                    <g transform="translate(105.44 46.85)">
                      <mask id="f" fill="#fff"><use xlinkHref="#e"></use></mask>
                      <path fill="#052A59" d="M-1.8 14.202h14.4v-15.84H-1.8z" mask="url(#f)"></path>
                    </g>
                    <g transform="translate(140.72 42.17)">
                      <mask id="h" fill="#fff"><use xlinkHref="#g"></use></mask>
                      <path fill="#052A59" d="M13.3-1.12l-14.74-.772-.812 15.483 14.74.772z" mask="url(#h)"></path>
                    </g>
                    <g transform="translate(113.72 35.33)">
                      <mask id="j" fill="#fff"><use xlinkHref="#i"></use></mask>
                      <path fill="#052A59" d="M-.82-2.395l32.38 1.13-1.22 34.94-32.38-1.13z" mask="url(#j)"></path>
                    </g>
                    <g transform="translate(117.32 42.53)">
                      <mask id="l" fill="#fff"><use xlinkHref="#k"></use></mask>
                      <path fill="#052A59" d="M-1.087-1.874l25.904.905-.728 20.867-25.904-.905z" mask="url(#l)"></path>
                    </g>
                    <g transform="translate(123.44 40.37)">
                      <mask id="n" fill="#fff"><use xlinkHref="#m"></use></mask>
                      <path fill="#052A59" d="M-1.375-1.671l17.27.603-.604 17.27-17.269-.604z" mask="url(#n)"></path>
                    </g>
                    <g transform="translate(120.92 44.33)">
                      <mask id="p" fill="#fff"><use xlinkHref="#o"></use></mask>
                      <path fill="#052A59" d="M-1.512-1.762l16.55.578-.502 14.391-16.55-.577z" mask="url(#p)"></path>
                    </g>
                    <g transform="translate(125.6 43.25)">
                      <mask id="r" fill="#fff"><use xlinkHref="#q"></use></mask>
                      <path fill="#052A59" d="M-1.477-1.598l11.513.402-.364 10.434-11.513-.402z" mask="url(#r)"></path>
                    </g>
                    <g transform="translate(124.16 45.41)">
                      <mask id="t" fill="#fff"><use xlinkHref="#s"></use></mask>
                      <path fill="#052A59" d="M-1.551-1.65l6.116.214-.314 8.995-6.117-.214z" mask="url(#t)"></path>
                    </g>
                  </g>
                </svg>
              </div>
            </div>

            <footer className="f5 pt6 pb5">
              <div className="flex-l mw8 center ph4">
                <p className="mw6 lh-copy mr3-l mb4">
                  RecordSponge Oregon is a nonprofit service delivered by{" "}
                  <a
                    className="link bb hover-dark-blue"
                    href="http://www.codepdx.org"
                  >
                    Code&nbsp;PDX
                  </a>{" "}
                  in collaboration with{" "}
                  <a
                    className="link bb hover-dark-blue"
                    href="https://www.qiu-qiulaw.com"
                  >
                    Qiu-Qiu Law
                  </a>
                  .
                </p>
                <p className="mw6 lh-copy mb4">
                  The service is intended to be accompanied by legal advice.
                  <br />
                  The service is not standalone legal advice.
                </p>
              </div>
            </footer>
          </div>
        </main>
      </>
    );
  }
}

export default Landing;