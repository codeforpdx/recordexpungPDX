import React from "react";
import store from "../../redux/store";
import history from "../../service/history";

interface Props {
  stopDemo: Function;
}

export default class DemoInfo extends React.Component<Props> {
  render() {
    const historicalExamples = [
      {
        name: "Rosa Parks",
        source: (
          <a
            className="link underline hover-blue"
            href="https://www.papillonfoundation.org/information/notable-criminal-records"
          >
            source
          </a>
        ),
      },
      {
        name: "George Bush",
        source: (
          <a
            className="link underline hover-blue"
            href="https://www.washingtonpost.com/wp-srv/aponline/20001103/aponline112738_000.htm"
          >
            {" "}
            {"source"}{" "}
          </a>
        ),
      },
      {
        name: "John Lennon",
        source: (
          <a
            className="link underline hover-blue"
            href="https://www.beatlesbible.com/1968/10/18/john-lennon-and-yoko-ono-are-arrested-for-drugs-possession/"
          >
            source
          </a>
        ),
      },
    ];

    const customExamples = [
      {
        name: "Example 1",
        description:
          "Charges on a single record can have several different eligibility dates.",
      },
      {
        name: "Example 2",
        description:
          "Various charge types require follow-up information from the user.",
      },
      {
        name: "Example 3",
        description:
          "A disposition may be missing if the case is open, or if there is a data error in OECI.",
      },
    ];

    return (
      <div className="bg-white mt4 mb3 pa3 br3">
        <h2 className="fw6 mb3">App Demo</h2>
        <p className="mb3">
          Instead of searching the OECI database, you can use this version of
          the app to search and display various example records.
        </p>
        <p className="mb3">
          You can also click "Enable Editing" to build other examples, or
          determine eligibility on a true record if you have that person's
          record information.
        </p>
        <p className="mb3">
          Here are some example records. Note that these charges weren't
          litigated under Oregon law and are thus ahistorical. Try searching the
          following:
        </p>

        <ol className="lh-copy pl4 mw6 mb3">
          {historicalExamples.map((info: any) => (
            <li className="mb2">
              <p>{info.name}</p>
              <p>{info.source}</p>
            </li>
          ))}
        </ol>
        <p className="mb3">
          The following are fabricated records that demonstrate particular
          features of RecordSponge.
        </p>
        <p className="mb3">
          Search using: <span className="fw6"> first name: </span> "Example",{" "}
          <span className="fw6"> last name:</span> "[number]"
        </p>
        <ol className="lh-copy pl4 mw6 mb3">
          {customExamples.map((info: any) => (
            <li className="mb2">
              <p>{info.name}</p>
              <p>{info.description}</p>
            </li>
          ))}
        </ol>
        <div className="mt3">
          Or{" "}
          <button
            className="link hover-blue underline"
            onClick={() => {
              store.dispatch(this.props.stopDemo());
              history.push("/record-search");
            }}
          >
            log in to OECI
          </button>
        </div>
      </div>
    );
  }
}
