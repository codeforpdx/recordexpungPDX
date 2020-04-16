import React from 'react';
import Logo from '../Logo';
import history from '../../service/history';

class Landing extends React.Component {
  render() {
    return (
      <>
        <div>
          <meta name="viewport" content="width=device-width, initial-scale=1" />

          <title>RecordSponge Oregon</title>
        </div>

        <div className="f5 f4-ns navy bg-white">
          <div className="overflow-x-hidden relative">

            <nav className="mw8 center flex justify-between ph3 pb3 mt4 mb5">
              <div className="logo--landing-page">
                <Logo />
              </div>
              <button
                onClick={() => history.push('/manual')}
                className="link mid-gray hover-blue f6 f5-ns dib pa3"
                >
                Manual
              </button>
              <div>
                <a href="/login"
                  className="bg-blue white bg-animate hover-bg-dark-blue f5 fw6 br2 pv2 ph3"
                >
                  Log In
                </a>
              </div>
            </nav>

            <div className="mw8 center ph4 pb6">
              <h1 className="f3 f2-ns fw7 mw7 mb4">
                Technology to make record expungement accessible for everyone
              </h1>
              <p className="lh-copy mw6">
                This tool helps expungement professionals quickly analyze an
                individual’s criminal history to determine if they qualify to
                have their records sealed (expunged).
              </p>
            </div>

            <div className="bg-lightest-blue1 b--white bw2 bb">
              <div className="flex-l justify-between mw8 center ph4">
                <div className="w-50-l b--white br-l bw2-l pv6-l pv5 pr5-l">
                  <h2 className="f3 fw7 mb3">
                    Are you an expungement provider interested in this tool?
                  </h2>
                  <p className="lh-copy mb3">
                    Request early access by providing your name and your
                    experience with expungement to{' '}
                    <a
                      className="fw6 link hover-dark-blue no-wrap"
                      href="mailto:michael@qiu-qiulaw.com"
                    >
                      michael@qiu-qiulaw.com
                    </a>
                    .
                  </p>
                  <p className="mb4">
                    <a href="/login" className="link underline hover-dark-blue">
                      Log in if you have an account
                    </a>
                  </p>
                </div>
                <div className="w-50-l b--white bt bw2 bn-l pv6-l pv5 pl5-l">
                  <h2 className="f3 fw7 mb3">
                    Are you looking to clear your record?
                  </h2>
                  <p className="lh-copy">
                    Check at{' '}
                    <a
                      className="link underline hover-dark-blue"
                      href="https://www.qiu-qiulaw.com"
                      target="blank"
                    >
                      Qiu-qiu Law
                    </a>{' '}
                    to see if you are eligible and if there is an upcoming
                    expungement clinic in your&nbsp;area. If there are none in
                    your area reach out to them and they may be able to organize
                    one near you.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-lightest-blue2 pv6">
              <div className="mw7 center ph4">
                <h3 className="f3 f2-ns fw7 mb3">Expungement in Oregon</h3>
                <p className="lh-copy mb5">
                  For many folks who have had run-ins with the criminal justice
                  system, punishment doesn't end with the end of their sentence.
                  A criminal conviction or arrest can follow a person around for
                  the rest of their life, well past the period of incarceration,
                  probation, and financial penalty. This prevents them from
                  accessing education, employment, housing, and services which
                  might otherwise help them integrate back into society.
                </p>
                <div className="mw7 tc mb5">

                <img
                  className="wipe-illustrations"
                  alt=""
                  src="/img/wipe-illustrations.jpg"
                />

                </div>
                <p className="mw7 lh-copy">
                  The State of Oregon provides a way for people to seal certain
                  items from their records (effectively removing them), but the
                  rules for determining which items are eligible are complex and
                  prone to error when applying them by hand. As a result,
                  expungement analysis is expensive in Portland - ranging from
                  $1,000 to $3,000 when performed by private attorneys.
                </p>
              </div>
            </div>

            <div className="mw8 flex-l center ph4 pv6">
              <div className="w-50-l mb4">
                <h3 className="f3 f2-ns fw7 mb3">The Technology</h3>
                <p className="lh-copy mb4">
                  <a
                    className="link underline hover-dark-blue"
                    href="http://www.codeforpdx.org"
                    target="blank"
                  >
                    Code for PDX
                  </a>{' '}
                  and{' '}
                  <a
                    className="link underline hover-dark-blue"
                    href="https://www.qiu-qiulaw.com"
                    target="blank"
                  >
                    Qiu-qiu Law
                  </a>{' '}
                  are actively developing analytical software to help
                  expungement providers quickly determine which items on an
                  applicant's record are eligible for expungement.
                </p>
                <p className="lh-copy mb4">
                  The goal of this project is to make expungement available to
                  all Oregonians, regardless of their ability to pay. It further
                  seeks to provide these services in the communities that need
                  them the most.
                </p>
                <p className="lh-copy">
                  The project continues to need contributors. Visit the{' '}
                  <a
                    className="link underline hover-dark-blue"
                    href="https://github.com/codeforpdx/recordexpungPDX/wiki"
                    target="blank"
                  >
                    GitHub project wiki
                  </a>{' '}
                  if you are interested. Here are more details on our{' '}
                  <a
                    className="link underline hover-dark-blue"
                    href="https://www.meetup.com/Code-for-PDX"
                    target="blank"
                  >
                    next meetup
                  </a>
                  . All are welcome!
                </p>
              </div>

              <div className="w-50-l tc pa5-l pa3">
                <img
                  className="ui-sample"
                  alt=""
                  src="/img/ui-sample2.png"
                />
              </div>
            </div>

            <footer className="bg-lightest-blue1 pt6 pb7">
              <div className="mw7 center ph4">
                <p className="lh-copy mb4">
                  RecordSponge Oregon is a nonprofit service delivered by
                  <svg
                    className="code-for-pdx--logo-icon"
                    viewBox="0 0 73 46"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <g fill="none" fillRule="evenodd">
                      <path
                        d="M43.25 1.438c2.01 1.939 2.833 4.268 5.793 5.905l.758.41 1.127.598c1.912 1.03 3.29 1.938 3.379 3.744l.002.332c-.092 2.617 1.02 7.876 1.35 10.645.33 2.77-.108 6.06-2.751 7.249-2.643 1.188-1.248 2.173-1.299 3.607-.05 1.434-2.656 3.284-2.695 4.387-.04 1.102-.742 3.56-2.585 5.256-1.842 1.696-5.525 2.517-8.293 2.421-2.768-.095-6.14-2.92-8.236-4.752-1.965-1.718-4.3-1.852-7.12-2.395l-2.361-.484c-2.311-.506-4.3-1.236-5.775-4.176-1.743-3.47-1.73-6.794-1.278-9.648l.084-.498c.529-2.961.665-8.774 2.765-9.609 1.75-.695 2.002-1.386 2.07-2.518l.042-1.073c.058-1.46.191-2.813 1.431-3.963 1.336-1.238 7.377-1.467 8.468-1.845 1.091-.377 4.022-2.617 6.763-3.986 2.742-1.368 6.352-1.546 8.361.393zM18.648 15.414c-1.105-.032-1.75.39-2.287 1.406-.703 1.33-.204 3.746-.19 4.797.026 1.834-.267 1.023-.416 3.327-.18 2.789.075 5.5 1.7 7.802.71 1.728 2.976 2.904 6.795 3.53l.584.09c6.26.898 8.17 4.058 11.03 5.72 2.861 1.664 6.878 1.515 8.133.73l.496-.317c1.119-.736 2.46-1.808 2.696-3.408l.034-.378c.073-2.07 1.317-2.996 2.505-4.34 1.188-1.343-.575-2.41-1.035-3.016a1.735 1.735 0 01-.218-.372c-.373.537-.796 1.06-1.269 1.562-4.578 4.87-13.935 4.234-17.784 2.867l-1.384-.5c-3.093-1.14-5.234-2.13-6.655-3.65l-.401-.443-.388-.462c-1.265-1.584-2.232-3.637-2.097-7.456.103-2.925.44-5.382 1.129-7.339-.28-.027-.606-.139-.978-.15zm18.686-13.14c-2.164.696-2.553 1.292-4.314 2.33-1.77 1.041-3.57 2.04-5.425 2.923-2.342 1.114-5.615.04-7.516 1.954-1.271 1.28-.187 3.169.27 4.453.241-.44.51-.843.81-1.21 1.765-2.158 2.544-2.528 3.075-1.707.531.822-1.078 1.766-1.682 2.991-.566 1.15-1.1 3.854-1.243 6.375l-.07 1.427-.078 1.352c-.118 2.597.016 5.702 2.405 6.814 3.163 1.472 9.824 3.672 13.59 3.802 3.765.13 7.479-1.172 8.93-3.022 1.45-1.85 3.615-6.815 3.688-8.886.073-2.07-.514-3.315.156-4.426.67-1.111 1.567-.086 1.678 1.693l.018.365.013.763c-.006 2.13-.354 6.079-2.49 9.69.129-.024.28-.04.453-.044l.283.002c1.8.062 2.993-.759 3.641-2.367.608-1.508.263-4.8-.233-6.912l-.1-.405c-.546-2.07-.948-5.247-1.357-7.067-.409-1.82-3.296-3.235-5.747-5.194-1.634-1.306-2.908-2.443-3.821-3.41-.389-.413-.76-.836-1.165-1.241-1.423-1.426-2.578-1.426-3.77-1.043zm20.305 14.348c.634 0 2.723.69 6.02 2.564l2.216 1.302c2.303 1.376 3.313 2.05 3.955 2.363.784.383 2.011.355 2.722 1.274.71.918.695 2.5-.925 3.227l-2.836 1.293c-1.706.77-3.61 1.59-4.653 1.858-1.74.448-3.795.8-4.769.8-.596 0-.112-.398.453-.78l.92-.604c.398-.296 2.444-1.203 3.228-1.688l.168-.112c.532-.393 1.642-.978 2.463-1.234l.292-.08c.826-.187 1.825-1.224.569-2.033-.628-.405-2.22-1.258-3.731-2.052l-3.254-1.696c-.619-.335-2.196-.981-2.543-1.753l-.139-.335c-.34-.877-.736-2.314-.156-2.314zm-47.525.973c.184.651.264 2.137-.7 2.85L7.56 21.802l-.192.146c-.5.386-1.892.779-2.398 1.176-.505.398-1.09 1.333-.451 2.053.638.72 1.832 1.646 3.036 1.98 1.204.334 2.024.893 2.56 1.474.536.58.035 1.44-1.356 1.44s-3.228-.03-4.24-.735c-.886-.617-1.613-1.289-2.343-1.603l-.314-.111C1.021 27.389.01 26.565.01 25.575L0 24.634c.015-.714.147-1.418.848-1.937l.984-.71c.49-.345 1.047-.731 1.674-1.157l.704-.49c.989-.677 1.674-1.105 2.054-1.283.698-.327 2.045-1.643 2.494-1.885.449-.242 1.173-.227 1.356.423zm15.45-4.096c1.657-.71 1.948 1.261.91 1.775-.726.36-.785 1.72-.687 3.46l.024.378.149 2.02c.198 2.789 1.544 4.602 3.401 5.377 1.858.775 2.792-.614 4.502-.85l1.663-.231c1.495-.226 3.123-.555 3.825-1.155.985-.84 1.826-3.385 2.538-3.03.711.354.997.855-.11 3.114-1.108 2.26-4.019 3.036-5.864 3.09-1.846.054-2.893 1.443-3.88 1.822-.989.38-6.472-.33-7.833-2.346-1.28-1.898-.933-5.472-.541-7.435l.134-.65c.335-1.872.2-4.666 1.77-5.339zm8.58-5.598c2.894.58 4.91 1.56 5.796 2.117.886.557 3.632 1.689 4.88 2.622l.548.415c.949.741 1.586 1.417 1.769 2.798l.06.52.067.725c.195 2.41.292 6.77-.971 8.349-1.538 1.921-1.686 2.805-2.772 2.767-1.086-.038-.427-1.13.082-2.334.509-1.203 2.32-3.38 1.996-6.607-.323-3.228-4.82-6.39-6.168-7.228-1.348-.839-5.097-2.68-6.041-2.713-.944-.033-1.964.033-2.797.628-.833.595-1.177.489-1.822 1.358-.645.869-2.11-.285-.771-1.448l.468-.393c1.308-1.053 3.103-2.091 5.676-1.576zM29.15 15.46c.545-.763 2.299-.354 1.89.653-.409 1.007-.898 1.646-.71 2.538.188.892 1.143 1.876 1.479 2.978.335 1.1-1.046 1.72-2.048 1.18s-1.314-2.089-1.476-3.666c-.163-1.576.32-2.92.865-3.683zm2.502-3.511c1.697.058 3.972.72 4.51 2.007l.081.249c.332 1.45 2.832 1.19 4.106 1.407 1.275.217 2.325 1.899 1.5 2.878-.825.98-3.233 1.574-4.047 2.995-.814 1.42-2.495.373-2.45-.883.044-1.257 1.22-1.728 1.53-2.584.309-.857-1.17-1.875-1.714-2.373-.544-.497-1.392-.647-2.99-1.581-1.597-.934-2.33-2.178-.526-2.115z"
                        fill="#052A59"
                      />
                    </g>
                  </svg>
                  <a
                    className="link underline hover-dark-blue"
                    href="http://www.codeforpdx.org"
                    target="blank"
                  >
                    Code for PDX
                  </a>{' '}
                  in collaboration with{' '}
                  <a
                    className="link underline hover-dark-blue"
                    href="https://www.qiu-qiulaw.com"
                    target="blank"
                  >
                    Qiu-qiu Law
                  </a>
                  .
                </p>
                <p className="lh-copy">
                  The service is intended to be accompanied by legal advice. The
                  service is not standalone legal advice.
                </p>
              </div>
            </footer>
          </div>
        </div>
      </>
    );
  }
}

export default Landing;
