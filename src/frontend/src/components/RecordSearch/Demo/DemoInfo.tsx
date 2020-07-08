import React from "react";
import store from "../../../redux/store";
import history from "../../../service/history";

interface Props {
  stopDemo: Function;
}

export default class DemoInfo extends React.Component<Props> {
  render() {
    const examples = [
      {
        name: "Single Conviction",
        subheader: "(First Name: Single, Last Name: Conviction) ",
        info: (
          <>
            <p className="pb2">
              As a simple example, if a person's record has only a single
              convicted charge, it is eligible after three years.
            </p>
            <p>
              However, dismissed charges on the same record are subject to more
              complex rules, depending on whether those dismissals are on the
              same or a different case as the conviction.
            </p>
          </>
        ),
      },
      {
        name: "John Common",
        subheader: "(First Name: John, Last Name: Common) ",
        info: (
          <div>
            <p className="pb2">
              Searching for a common name will often bring up records that
              belong to different individuals, leading to an incorrect analysis
              for the set of resulting cases. Another source of confusion is
              that each case may or may not incude a birth year, as well as
              middle name or middle initial.
            </p>
            <p>
              It is thus always recommended to provide a birth date in the
              search. You can also use the Enable Editing feature to remove
              cases or charges from the resulting record, and these charges will
              be excluded in the eligibility analysis.
            </p>
          </div>
        ),
      },
      {
        name: "John Common (birth date: 1/1/1970)",
        subheader:
          "(First Name: John, Last Name: Common, Date of Birth: 1/1/1970)",
        info: (
          <p>
            Most charges that are eligible are also subject to the same set of
            time restrictions. There are some exceptions to this, notably Class
            B Felonies and Possession for under an ounce of marijuana.
          </p>
        ),
      },
      {
        name: "John Common (birth date: 2/2/1985)",
        subheader:
          "(First Name: John, Last Name: Common, Date of Birth: 2/2/1985)",
        info: (
          <p>
            Some charges cannot be evaluated for eligibility until the user
            provides some follow-up information about the charge. RecordSponge
            deals with this ambiguity by showing all possible cases for
            eligibility, and by asking the user for the required extra
            information in order to determine an exact analysis.
          </p>
        ),
      },
      {
        name: "Portland Protester",
        subheader: "(First Name: Portland, Last Name: Protester)",
        info: (
          <div>
            <p className="pb2">
              Our software is useful for evaluating a record with recent open
              cases, because you can assign rulings manually to consider
              hypothetical outcomes. This is particularly relevant in light of
              the recent protests against police brutality in Portland and
              nationwide.
            </p>
            <p>
              The team at RecordSponge stands in strong support of this
              movement. These protests are are seeing forceful retaliation from
              police, with peaceful protesters as well as journalists getting
              attacked, arrested, and charged with multiple and often
              felony-level charges.
            </p>
          </div>
        ),
      },
    ];
    return (
      <article className=" lh-copy">
        <div className="bg-white mt2 mb3 pa5 br3">
          <h1 className="fw6 mb3">App Demo</h1>
          <p className="mb3">
            This demo provides some example records that demonstrate the complex
            rules of expungement and the analysis features of RecordSponge. The
            demo version does not search the OECI database, and thus doesn't
            require an OECI account to use.
          </p>
          <p className="mb3">
            You can also click "Enable Editing" to build and evaluate different
            examples. If you are looking to evaluate your own record for
            expungement eligibility, we urge you to contact{" "}
            <a href="/" className="link bb hover-blue">
              {" "}
              one of our partners{" "}
            </a>
            for assistance. This software is not standalone legal advice.
          </p>

          <p className="mb3">
            Try searching any of the following examples by entering them into
            the "First Name" and "Last Name" fields in the Search Panel:
          </p>
          <div className="pw6">
            {examples.map((examples: any) => (
              <div>
                <p className="fw7 f4 ">{examples.name}</p>
                <p className="pt1 pb2">
                  {" "}
                  <span className="">{examples.subheader}</span>
                </p>
                <p className="ml3 mr5 mb3">{examples.info}</p>
              </div>
            ))}
          </div>
        </div>
      </article>
    );
  }
}
