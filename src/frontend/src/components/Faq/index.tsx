import React from "react";

class Faq extends React.Component {
  render() {
    return (
      <>
        <main className="flex-l mw7 f5 f4-ns center ph4 mv5">
          <article className="order-1 lh-copy">
            <section className="mb5">
              <h1 className="f2 fw9 mb3 mt0" id="FAQ">
                FAQ
              </h1>
              <p className="mb3">
                Due to the complexity of the Oregon expungement laws, incorrect
                information proliferates from State actors at all levels of the
                justice system.
              </p>
              <p className="mb4">
                Below are some common myths overheard in courtrooms all over
                Oregon.
              </p>
              <ol className="ml4 mb4">
                <li className="mb4">
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
                <li className="mb4">
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
                <li className="mb4">
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
          </article>
        </main>
      </>
    );
  }
}

export default Faq;
