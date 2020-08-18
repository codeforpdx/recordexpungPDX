import React from "react";
import { HashLink as Link } from "react-router-hash-link";

export default class About extends React.Component {
  componentDidMount() {
    document.title = "About - RecordSponge";
  }

  render() {
    return (
      <main>
        <div className="bg-navy pv6">
          <div className="mw7 center white pa4">
            <h1 className="f3 f2-ns fw9 lh-tight mt0 mb4">
              RecordSponge is a web application used to facilitate the
              expungement process in Oregon.
            </h1>
            <p className="f4 lh-copy">
              RecordSponge is a collaboration between Code for PDX and Qiu-Qiu
              Law. This project is an entirely volunteer effort and is part of
              the open tech group Code for PDX, a brigade of Code for America.
            </p>
          </div>
        </div>
        <div className="bg-lightest-blue1 navy pv6">
          <div className="mw7 center pa4">
            <h2 className="f3 f2-ns fw9 mb4">Our Mission</h2>
            <p className="f4 lh-copy mb3">
              RecordSponge is motivated by the fact that market-rate record
              expungement lawyers are not accessible to the very people who need
              those services. Many people with criminal records, who are
              disproportionately people of color, are limited to “low-skill” or
              low-wage jobs and also have difficulties applying for housing.
            </p>
            <p className="f4 lh-copy mb3">
              Not only does having a criminal record pose immediate financial
              and physical insecurities, but it also creates psychological and
              mental burdens that can create a negative feedback loop of
              disenfranchisement. To mitigate these burdens, legal affirmation
              of having a “clean slate” can be a huge signal to them that they
              are re-welcomed into society.
            </p>
            <p className="f4 lh-copy mb3">
              Oregon has an expungement law that makes certain records eligible
              for expungement, however analyzing which records are eligible for
              expungement is a complicated and time-consuming process even for
              lawyers. The RecordSponge software reduces this barrier by making
              the analysis process more efficient and accurate. We are working
              to make expungement analysis more accessible to potential
              beneficiaries by empowering a growing network of partner
              organizations across Oregon.
            </p>
            <p className="f4 lh-copy mb3">
              As an all-volunteer effort, RecordSponge remains an open
              opportunity for any who want to contribute to our mission.
            </p>
          </div>
        </div>
        <div className="navy pv6">
          <div className="mw7 center pa4">
            <h2 className="f3 f2-ns fw9 mb5">Our Team</h2>
            <dl className="flex flex-wrap justify-between">
              <div className="mw5 mb5 mr3">
                <img className="img w5 mb3" src="/img/mz-2x.jpg" />
                <dt className="fw8 mb2">Michael Zhang</dt>
                <dt className="fw6 mb3">Attorney</dt>
                <dd className="lh-copy">
                  Michael holds a degree in mathematics from Duke University and
                  a JD from Harvard Law School. His law practice seeks to
                  radically reduce the cost of essential legal services by
                  collaborating and learning from organizers, engineers, and
                  other trades. Before opening his practice, he worked at
                  Portland’s main public defender office. He teaches a clinical
                  course on expungement at Portland Community College.
                </dd>
              </div>

              <div className="mw5 mb5 mr3">
                <img className="img w5 mb3" src="/img/jw-2x.jpg" />
                <dt className="fw8 mb2">Jordan Witte</dt>
                <dt className="fw6 mb3">Project manager & developer</dt>
                <dd className="lh-copy">
                  Jordan studied computer science and machine learning at
                  Portland State University, completing his masters in 2019.
                  Seeking ways to contribute locally to progressive causes, he
                  joined Code for PDX in March of 2019 to work on its Record
                  Expungement software project. He currently volunteers
                  full-time at Code for PDX.
                </dd>
              </div>

              <div className="mw5 mb5 mr3">
                <img className="img w5 mb3" src="/img/ks-2x.jpg" />
                <dt className="fw8 mb2">Kent Shikama</dt>
                <dt className="fw6 mb3">Developer</dt>
                <dd className="lh-copy">
                  Kent graduated Pomona College in 2017 with a degree in
                  computer science. He has spent the last five years working on
                  various open source coding projects. Most recently, he joined
                  Code for PDX in October of 2019 to work on RecordSponge. He
                  currently volunteers full-time at Code&nbsp;for&nbsp;PDX.
                </dd>
              </div>

              <div className="mw5 mb5 mr3">
                <img className="img w5 mb3" src="/img/ns-2x.jpg" />
                <dt className="fw8 mb2">Nick Schimek</dt>
                <dt className="fw6 mb3">Former project manager & developer</dt>
                <dd className="lh-copy">
                  Nick graduated from Regis University with a degree in Computer
                  Science. He met Michael in 2018 at a Code for PDX event where
                  Michael proposed creating software for automating record
                  expungements to help those who are underrepresented by
                  democratizing the system. He was instantly drawn to the cause
                  and committed himself to seeing the project to completion.
                </dd>
              </div>

              <div className="mw5 mb5 mr3">
                <img className="img w5 mb3" src="/img/hm-2x.jpg" />
                <dt className="fw8 mb2">Hunter Marcks</dt>
                <dt className="fw6 mb3">Designer</dt>
                <dd className="lh-copy">
                  Hunter studied graphic design at the University of Minnesota.
                  He joined Code for PDX in 2018 to contribute to civic
                  technology and has primarily worked on RecordSponge. He has
                  been working on digital products for over ten years and
                  currently designs software at Renew&nbsp;Financial.
                </dd>
              </div>
            </dl>

            <hr className="bb b--navy mv5" />

            <h3 className="f3 f2-ns fw9 mb5">Contributor short list</h3>

            <dl className="flex flex-wrap f6 f5-ns mb4">
              <div className="mr4 mr6-l">
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Logan Ballard</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Greg Barker</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Cate Barnwell</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Robert Rex Beatie</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Chris Breaux</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Adam Emrich</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Michelle Fong</dt>
                  <dd className="dib v-top">Designer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Arun Ilango</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Jonah James</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Erik Jasso</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
              </div>
              <div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Evan Johnston</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Ryan Keppel</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Yoonjung Lee</dt>
                  <dd className="dib v-top">Strategy</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Forrest Longanecker</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Matt Rosanio</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Kenichi Nakamura</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Olli Nieminen</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Max Wallace</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Reggie Williams</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
                <div className="mb3">
                  <dt className="w4 dib-l fw7 mr3">Victor Zaragoza</dt>
                  <dd className="dib v-top">Developer</dd>
                </div>
              </div>
            </dl>
            <a
              className="fw7 link blue hover-dark-blue"
              href="https://www.codeforpdx.org"
            >
              Volunteer with us
            </a>
          </div>
        </div>
        <div className="bg-navy pv6">
          <div className="flex-l justify-between mw8 center white pa4">
            <div className="w-50-l bt bw2 b--blue pt4 mr5-l mb5">
              <h4 className="f3 f2-ns fw9 lh-title mt0 mb4">
                Clear your record
              </h4>
              <Link
                className="f4 f3-ns fw7 link light-blue hover-white"
                to="/"
                onClick={() => window.scrollTo(0, 0)}
              >
                Find a partner
                <span
                  className="fas fa-arrow-right f5 lh-solid pt1 pl2"
                  aria-hidden="true"
                ></span>
              </Link>
            </div>

            <div className="w-50-l bt bw2 b--blue pt4 ml5-l mb5">
              <h4 className="f3 f2-ns fw9 lh-title mt0 mb4">
                Use our software
              </h4>

              <Link
                className="f4 f3-ns fw7 link light-blue hover-white"
                to="/partner-interest"
                onClick={() => window.scrollTo(0, 0)}
              >
                Getting started
                <span
                  className="fas fa-arrow-right f5 lh-solid pt1 pl2"
                  aria-hidden="true"
                ></span>
              </Link>
            </div>
          </div>
        </div>
      </main>
    );
  }
}
