import React from "react";
import { Link } from "react-router-dom";

class DemoInfo extends React.Component {
  formattedInfo = (
    firstName: string,
    lastName: string,
    description: string[],
    dateOfBirth: string
  ) => {
    return (
      <div>
        <p className="flex lh-title mb3">
          <div className="mr4">
            <div className="fw6">First Name</div>
            <div>{firstName}</div>
          </div>
          <div className="mr4">
            <div className="fw6">Last Name</div>
            <div>{lastName}</div>
          </div>
          {dateOfBirth && (
            <div>
              <div className="fw6">Date of Birth</div>
              <div>{dateOfBirth}</div>
            </div>
          )}
        </p>
        {description.map((line: string, idx: number) => (
          <p key={idx} className="pb2">
            {line}
          </p>
        ))}
      </div>
    );
  };

  render() {
    const examplesData = [
      {
        name: "Single Conviction",
        firstName: "Single",
        lastName: "Conviction",
        description: [
          "As a simple example, if a person's record has only a single convicted charge, it is eligible after three years.",
        ],
      },
      {
        name: "Multiple Charges",
        firstName: "Multiple",
        lastName: "Charges",
        description: [
          "If a record has more than one case, the time restrictions quickly get more complex, as this example demonstrates. Eligibility dates depend on whether dismissals are on the same or a different case as a conviction. Searching OECI will also reveal traffic violations, which are always ineligible.",
          "This record also includes a case with an outstanding balance due for fines, which is indicated in both the record summary and on the case itself.",
        ],
      },
      {
        name: "John Common",
        firstName: "John",
        lastName: "Common",
        description: [
          "Searching for a common name will often bring up records that belong to different individuals, leading to an incorrect analysis for the set of resulting cases. Another source of confusion is that each case may or may not incude a birth year, as well as middle name or initial.",
          "It is thus always recommended to provide a birth date in the search. You can also use the Enable Editing feature to remove cases or charges from the resulting record, and these charges will be excluded in the eligibility analysis.",
        ],
      },
      {
        name: "John Common – Class B Felony and Marijuana",
        firstName: "John",
        lastName: "Common",
        description: [
          "Most charges that are eligible are also subject to the same set of time restrictions. There are some exceptions to this, notably Class B Felonies, and possession of less than an ounce of marijuana.",
        ],
        dateOfBirth: "1/1/1970",
      },
      {
        name: "John Common – Needs More Analysis",
        firstName: "John",
        lastName: "Common",
        description: [
          "Some charges cannot be evaluated for eligibility until the user provides some follow-up information about the charge. RecordSponge deals with this ambiguity by showing the different possible outcomes for eligibility, and by asking the user for the required extra information in order to determine an exact analysis.",
        ],
        dateOfBirth: "2/2/1985",
      },
    ];
    return (
      <article className="lh-copy">
        <div className="bg-white shadow bl bw3 b--blue mv4 pv4 ph4 ph5-l br3">
          <h1 className="f3 fw9 ma0 mb2">App Demo</h1>
          <p className="mw7 mb3">
            This demo provides example records that demonstrate the complex
            rules of expungement and the analysis features of RecordSponge. The
            demo version does not search the OECI database, and thus doesn't
            require an OECI account to use.
          </p>
          <p className="mw7 mb3">
            You can also "Enable Editing" below the search panel to build and
            evaluate different examples. If you are looking to evaluate your own
            record for expungement eligibility, we urge you to contact{" "}
            <Link
              to="/"
              className="link bb hover-blue"
              onClick={() => window.scrollTo(0, 0)}
            >
              {" "}
              one of our partners{" "}
            </Link>
            for assistance. This software is not standalone legal advice.
          </p>

          <p className="mb3 mw7 ">
            Try searching any of the following examples by entering them in the
            search panel below.
          </p>

          <p className="mb4">
            Or,{" "}
            <Link
              to="/oeci"
              className="link bb mid-gray hover-blue"
              onClick={() => window.scrollTo(0, 0)}
            >
              log in to OECI
            </Link>
            .
          </p>
          <div>
            {examplesData.map((e: any, idx: number) => (
              <div key={idx}>
                <h2 className="fw9 bt b--light-gray pt2 mb3">{e.name}</h2>
                <div className="mw7 mb4">
                  {this.formattedInfo(
                    e.firstName,
                    e.lastName,
                    e.description,
                    e.dateOfBirth
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </article>
    );
  }
}

export default DemoInfo;
