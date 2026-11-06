import React, { useEffect, useState } from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";
import setupPage from "../../service/setupPage";
import { sb819IsEnabled } from "../../service/featureFlags";

interface CriterionBlock {
  kind: "criterion";
  number: string;
  key: string;
  name: string;
  citation: string;
  citation_url: string;
  source_text: string;
  how_determined: string;
  concerns: string;
  screened: boolean;
}

interface Section {
  number: string;
  title: string;
  rule: string;
  blocks: CriterionBlock[];
}

interface LogicSheet {
  county: string;
  source: string;
  source_title: string;
  source_url: string;
  sections: Section[];
  questions: {
    number: string;
    name: string;
    text: string;
    if_yes: string;
    if_no: string;
    note: string;
  }[];
  resolution: { number: string; text: string }[];
}

function Criterion({ block }: { block: CriterionBlock }) {
  return (
    <div className="mb4">
      <h3 className="fw7 mb1">
        {block.number && <span className="mr2">{block.number}</span>}
        {block.name}
        <a
          href={block.citation_url}
          target="_blank"
          rel="noopener noreferrer"
          className="f6 fw4 link bb gray hover-blue ml2"
        >
          {block.citation}
        </a>
        {!block.screened && (
          <span className="f6 fw6 br2 ph2 pv1 ml2 mid-gray bg-light-gray">
            Not screened
          </span>
        )}
      </h3>
      <blockquote className="bl bw2 b--light-gray pl3 ml0 mb2 i">
        {block.source_text}
      </blockquote>
      <p className="mb1">
        <span className="fw7">How determined. </span>
        {block.how_determined}
      </p>
      {block.concerns && (
        <p className="f6 gray mb0">This concerns {block.concerns}.</p>
      )}
    </div>
  );
}

export default function SB819Rules() {
  setupPage("SB-819 Rules");
  const [sheet, setSheet] = useState<LogicSheet | null>(null);
  const [error, setError] = useState("");
  // Part of the same unreleased feature as the analysis it documents.
  const released = sb819IsEnabled();

  useEffect(() => {
    if (!released) return;
    axios
      .request({ url: "/api/sb819/rules", method: "get" })
      .then((response) => setSheet(response.data))
      .catch((e) => setError(e.message));
  }, [released]);

  if (!released) return <Navigate to="/" />;

  if (error)
    return (
      <main className="mw8 center ph4 mt5">
        <p className="bg-washed-red pa3 br3 fw6">
          The rules could not be loaded: {error}
        </p>
      </main>
    );

  if (!sheet) return <></>;

  return (
    <main className="mw8 center ph4 mt5 lh-copy">
      <article className="mb5">
        <h1 className="f2 fw9 mb3 mt4">
          SB-819 Rules &mdash; {sheet.county} County
        </h1>
        <p className="mb2">
          Every rule the software applies when screening a conviction under SB
          819, in the order it applies them.
        </p>
        <p className="mb2 f6 gray">
          {sheet.source}{" "}
          <a
            href={sheet.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="link bb hover-blue"
          >
            Read the {sheet.source_title}
          </a>
          .
        </p>
        <p className="mb4 f6 gray">
          This page is generated from the criteria the software runs, so it
          cannot describe a rule that is not applied, or omit one that is.
        </p>

        {sheet.sections.map((section) => (
          <section
            key={section.number}
            className="mb5"
            id={`s${section.number}`}
          >
            <h2 className="f3 fw9 mb2 mt4 bt b--light-gray pt3">
              {section.number}. {section.title}
            </h2>
            <p className="mb3">{section.rule}</p>
            <div className="ml3">
              {section.blocks.map((block, index) => (
                <Criterion key={index} block={block} />
              ))}
            </div>
          </section>
        ))}

        <section className="mb5" id="s4">
          <h2 className="f3 fw9 mb2 mt4 bt b--light-gray pt3">
            4. Questions put to the client
          </h2>
          <p className="mb3">
            The exact wording, and what each answer settles.
          </p>
          <div className="overflow-x-auto">
            <table className="w-100 collapse f6">
              <thead>
                <tr className="bb b--light-gray">
                  <th className="tl pv2 pr3">#</th>
                  <th className="tl pv2 pr3">Question</th>
                  <th className="tl pv2 pr3">Yes</th>
                  <th className="tl pv2">No</th>
                </tr>
              </thead>
              <tbody>
                {sheet.questions.map((question) => (
                  <tr
                    key={question.number + question.text}
                    className="bb b--light-gray"
                  >
                    <td className="pv2 pr3 nowrap">{question.number}</td>
                    <td className="pv2 pr3">
                      {question.text}
                      {question.note && (
                        <div className="gray mt1">{question.note}</div>
                      )}
                    </td>
                    <td className="pv2 pr3">{question.if_yes}</td>
                    <td className="pv2">{question.if_no}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb5" id="s5">
          <h2 className="f3 fw9 mb2 mt4 bt b--light-gray pt3">
            5. How a result is reached
          </h2>
          {sheet.resolution.map((rule) => (
            <p key={rule.number} className="mb3">
              <span className="fw7 mr2">{rule.number}</span>
              {rule.text}
            </p>
          ))}
        </section>
      </article>
    </main>
  );
}
