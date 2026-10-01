/**
 * Analyses shaped like the "sb 819" demo record, built criterion by criterion so a test can
 * say which rules a conviction meets. Statuses and sections are computed by the resolver,
 * which the shared fixture table pins.
 */

import { CaseData, RecordData } from "../Record/types";
import resolveAnalysis from "./resolve";
import {
  AnalysisData,
  ChargeAnalysisData,
  CriterionData,
  Determination,
  Outcome,
  Pathway,
  PathwayData,
  Scope,
  Status,
} from "./types";

const P: Status = "Possibly SB-819 Eligible";
const I: Status = "SB-819 Ineligible";
const ALTERNATIVES = "excessive-sentencing-alternatives";

interface Options {
  scope?: Scope;
  pathway?: Pathway | null;
  determination?: Determination;
  outcome?: Outcome;
  group?: string;
  gate?: boolean;
  question?: { text: string; if_yes: Status; if_no: Status; note?: string };
}

export function criterion(
  key: string,
  name: string,
  o: Options = {}
): CriterionData {
  const determination = o.determination ?? "OECI";
  return {
    key,
    scope: o.scope ?? "charge",
    disjunction_group: o.group ?? "",
    is_gate: o.gate ?? false,
    is_screenable: determination === "OECI" || determination === "Question",
    name,
    description: "",
    citation: "Page 3",
    determination,
    pathway: o.pathway ?? null,
    outcome: o.outcome ?? (o.question ? "Unknown" : "Passed"),
    explanation: `${name}: explanation`,
    question: o.question ? { note: "", ...o.question } : null,
  };
}

// Main criteria
const IN_MULTNOMAH = criterion(
  "in-multnomah",
  "Conviction is from Multnomah County"
);
const NOT_EXPUNGEABLE = criterion(
  "not-expungeable",
  "Conviction is not expungeable under ORS 137.225"
);
const FELONY = criterion(
  "sentenced-as-felony",
  "Conviction was sentenced as a felony"
);
const FELONY_FAILED = { ...FELONY, outcome: "Failed" as Outcome };
const FELONY_UNCERTAIN = criterion(
  "sentenced-as-felony",
  "Conviction was sentenced as a felony",
  {
    question: {
      text: "Was this conviction sentenced as a felony?",
      if_yes: P,
      if_no: I,
    },
  }
);
const NOT_AGG_MURDER = criterion(
  "not-aggravated-murder",
  "Conviction is not aggravated murder"
);
const AGG_MURDER = { ...NOT_AGG_MURDER, outcome: "Failed" as Outcome };

// Actual Innocence
const AI: Pathway = "Actual Innocence";
const INNOCENCE = criterion(
  "innocence-claim",
  "Applicant asserts actual innocence of the conviction",
  {
    pathway: AI,
    determination: "Question",
    question: {
      text: "Is the applicant asserting that they are actually innocent of this conviction?",
      if_yes: P,
      if_no: I,
    },
  }
);
const AVENUE = criterion(
  "investigation-avenue",
  "The JIU can identify an avenue of investigation",
  {
    pathway: AI,
    determination: "Discretion",
    outcome: "Unknown",
  }
);

// Excessive Sentencing
const ES: Pathway = "Excessive Sentencing";
const INCARCERATED = criterion(
  "currently-incarcerated",
  "Applicant is currently incarcerated",
  {
    pathway: ES,
    scope: "record",
    determination: "Question",
    gate: true,
    question: {
      text: "Is the applicant currently incarcerated?",
      if_yes: P,
      if_no: I,
    },
  }
);
const FIVE_YEARS = criterion(
  "five-years-served",
  "Applicant has served at least 5 years of the term of incarceration",
  {
    pathway: ES,
    determination: "Question",
    question: {
      text: "Has the applicant served at least five years of the term of incarceration on this sentence?",
      if_yes: P,
      if_no: I,
    },
  }
);
const GLOBAL_PLEA = criterion(
  "not-global-plea",
  "Conviction was not part of a global plea deal across counties",
  {
    pathway: ES,
    scope: "case",
    determination: "Question",
    question: {
      text: "Was this conviction part of a global plea deal involving multiple counties?",
      if_yes: I,
      if_no: P,
    },
  }
);
const REPEAT_SEX_CLEAR = criterion(
  "not-repeat-sex-offender",
  "Conviction is not subject to ORS 137.690 or ORS 137.719",
  {
    pathway: ES,
  }
);
const REPEAT_SEX_QUESTION = criterion(
  "not-repeat-sex-offender",
  "Conviction is not subject to ORS 137.690 or ORS 137.719",
  {
    pathway: ES,
    question: {
      text: "Was this conviction sentenced under ORS 137.690 or ORS 137.719?",
      if_yes: I,
      if_no: P,
    },
  }
);
const JUVENILE = criterion(
  "juvenile-transfer",
  "Sentenced as a juvenile and approaching transfer to adult prison",
  {
    pathway: ES,
    scope: "record",
    determination: "Question",
    group: ALTERNATIVES,
    question: {
      text: "Was the applicant sentenced as a juvenile, with incarceration remaining, approaching age 25 and facing transfer to adult prison?",
      if_yes: P,
      if_no: I,
    },
  }
);
const under18 = (outcome: Outcome) =>
  criterion(
    "under-18-at-offense",
    "Applicant committed the crime when under 18",
    {
      pathway: ES,
      group: ALTERNATIVES,
      outcome,
      question:
        outcome === "Unknown"
          ? {
              text: "Was the applicant under 18 when this crime was committed?",
              if_yes: P,
              if_no: I,
            }
          : undefined,
    }
  );
const OVER_60 = criterion(
  "over-60-or-ill",
  "Applicant is over 60, terminally or debilitatingly ill, or on hospice care",
  {
    pathway: ES,
    scope: "record",
    group: ALTERNATIVES,
    question: {
      text: "Is the applicant over 60, terminally or debilitatingly ill, or currently on hospice care?",
      if_yes: P,
      if_no: I,
    },
  }
);
const nonPersonOver10 = (personCrime: boolean) =>
  criterion(
    "non-person-over-10-years",
    "Non-person crime with sentences longer than 10 years in total",
    {
      pathway: ES,
      scope: "record",
      determination: "Question",
      group: ALTERNATIVES,
      outcome: personCrime ? "Failed" : "Unknown",
      question: personCrime
        ? undefined
        : {
            text: "Do the applicant's sentences for non-person crimes total more than 10 years?",
            if_yes: P,
            if_no: I,
          },
    }
  );
const personOver16 = (personCrime: boolean) =>
  criterion(
    "person-over-16-years",
    "Person crime with sentences longer than 16 years in total",
    {
      pathway: ES,
      scope: "record",
      determination: "Question",
      group: ALTERNATIVES,
      outcome: personCrime ? "Unknown" : "Failed",
      question: personCrime
        ? {
            text: "Do the applicant's sentences for person crimes total more than 16 years?",
            if_yes: P,
            if_no: I,
          }
        : undefined,
    }
  );

// Collateral Consequences
const CC: Pathway = "Collateral Consequences";
const SENTENCE_COMPLETED = criterion(
  "sentence-completed",
  "Applicant has fully completed the sentence",
  {
    pathway: CC,
    scope: "case",
    determination: "Question",
    gate: true,
    question: {
      text: "Has the applicant fully completed the sentence on this case, including all post-prison supervision and probation?",
      if_yes: P,
      if_no: I,
    },
  }
);
const registerable = (outcome: Outcome) =>
  criterion(
    "not-registerable-sex-offense",
    "Conviction is not a registerable sex offense",
    {
      pathway: CC,
      outcome,
      question:
        outcome === "Unknown"
          ? {
              text: "Does this conviction require the applicant to report as a sex offender?",
              if_yes: I,
              if_no: P,
            }
          : undefined,
    }
  );
const DOMESTIC_VIOLENCE = criterion(
  "no-domestic-violence",
  "Conviction did not involve domestic violence",
  {
    pathway: CC,
    determination: "Question",
    question: {
      text: "Did this conviction involve domestic violence?",
      if_yes: I,
      if_no: P,
    },
  }
);
const REHABILITATION = criterion(
  "substantial-rehabilitation",
  "Applicant demonstrates substantial rehabilitation and low risk",
  {
    pathway: CC,
    determination: "Part 2",
    outcome: "Unknown",
  }
);
const HARDSHIP = criterion(
  "manifest-hardship",
  "Applicant demonstrates manifest and particularized hardship",
  {
    pathway: CC,
    determination: "Part 2",
    outcome: "Unknown",
  }
);

export interface ChargeShape {
  id: string;
  caseNumber: string;
  name: string;
  /** Whether the statute is on the person-felony list, which decides the sentence alternative. */
  personCrime?: boolean;
  under18?: Outcome;
  registerable?: Outcome;
  /** The record carries a felony sex crime conviction, so ORS 137.690/137.719 is a question. */
  repeatSexQuestion?: boolean;
  felonyUncertain?: boolean;
  mainFails?: "felony" | "murder";
}

export function chargeAnalysis(shape: ChargeShape): ChargeAnalysisData {
  const main = [
    IN_MULTNOMAH,
    NOT_EXPUNGEABLE,
    shape.mainFails === "felony"
      ? FELONY_FAILED
      : shape.felonyUncertain
      ? FELONY_UNCERTAIN
      : FELONY,
    shape.mainFails === "murder" ? AGG_MURDER : NOT_AGG_MURDER,
  ];
  const person = shape.personCrime ?? true;
  const pathways: PathwayData[] = shape.mainFails
    ? []
    : [
        {
          pathway: AI,
          status: "Needs More Analysis",
          criteria: [INNOCENCE, AVENUE],
        },
        {
          pathway: ES,
          status: "Needs More Analysis",
          criteria: [
            INCARCERATED,
            FIVE_YEARS,
            GLOBAL_PLEA,
            shape.repeatSexQuestion ? REPEAT_SEX_QUESTION : REPEAT_SEX_CLEAR,
            JUVENILE,
            under18(shape.under18 ?? "Failed"),
            OVER_60,
            nonPersonOver10(person),
            personOver16(person),
          ],
        },
        {
          pathway: CC,
          status: "Needs More Analysis",
          criteria: [
            SENTENCE_COMPLETED,
            registerable(shape.registerable ?? "Passed"),
            DOMESTIC_VIOLENCE,
            REHABILITATION,
            HARDSHIP,
          ],
        },
      ];
  return {
    ambiguous_charge_id: shape.id,
    case_number: shape.caseNumber,
    charge_name: shape.name,
    status: "Needs More Analysis",
    main_criteria: main,
    pathways,
    available_pathways: [],
    blocked_pathways: [],
  };
}

export interface DemoOptions {
  /** A second, non-person conviction on case 100. */
  theft?: boolean;
  /** A DUII on case 300, which the record rules out as not a felony. */
  duii?: boolean;
  /** Rape II on case 500, a registerable sex offense; it also puts ORS 137.690/137.719 in question everywhere. */
  rape?: boolean;
  /** Assault II on case 800 with an amended disposition, so the felony level is a question. */
  assault?: boolean;
  /** Arson I on case 900, committed under 18. */
  arson?: boolean;
  /** No charge in scope at all. */
  empty?: boolean;
}

/** The demo-shaped analysis: Robbery II on case 100 always, and the rest by option. */
export function buildAnalysis(o: DemoOptions = {}): AnalysisData {
  const shapes: ChargeShape[] = o.empty
    ? []
    : [
        {
          id: "100-1",
          caseNumber: "100",
          name: "Robbery in the Second Degree",
          repeatSexQuestion: o.rape,
        },
        ...(o.theft
          ? [
              {
                id: "100-2",
                caseNumber: "100",
                name: "Theft in the First Degree",
                personCrime: false,
                repeatSexQuestion: o.rape,
              },
            ]
          : []),
        ...(o.duii
          ? [
              {
                id: "300-1",
                caseNumber: "300",
                name: "Driving Under the Influence of Intoxicants",
                mainFails: "felony" as const,
              },
            ]
          : []),
        ...(o.rape
          ? [
              {
                id: "500-1",
                caseNumber: "500",
                name: "Rape in the Second Degree",
                registerable: "Failed" as Outcome,
                repeatSexQuestion: true,
              },
            ]
          : []),
        ...(o.assault
          ? [
              {
                id: "800-1",
                caseNumber: "800",
                name: "Assault in the Second Degree",
                felonyUncertain: true,
                repeatSexQuestion: o.rape,
              },
            ]
          : []),
        ...(o.arson
          ? [
              {
                id: "900-1",
                caseNumber: "900",
                name: "Arson in the First Degree",
                under18: "Passed" as Outcome,
                repeatSexQuestion: o.rape,
              },
            ]
          : []),
      ];
  const charges: AnalysisData["charges"] = {};
  shapes.forEach((shape) => (charges[shape.id] = chargeAnalysis(shape)));
  return resolveAnalysis(
    {
      counties_analyzed: shapes.length ? ["Multnomah"] : [],
      has_analyzed_charges: shapes.length > 0,
      has_possibly_eligible: false,
      sections: [],
      charges,
    },
    {}
  );
}

function charge(
  id: string,
  name: string,
  caseNumber: string,
  level = "Felony Class B",
  statute = "164.405"
) {
  return {
    case_number: caseNumber,
    ambiguous_charge_id: id,
    statute,
    expungement_result: {
      type_eligibility: { status: "Ineligible", reason: "" },
      charge_eligibility: {
        status: "Ineligible",
        label: "Ineligible",
        date_to_sort_label_by: null,
      },
    },
    expungement_rules: "",
    name,
    type_name: "Person Felony Class B",
    level,
    date: "Jan 1, 2010",
    disposition: {
      status: "Convicted",
      ruling: "Convicted",
      date: "Jan 1, 2010",
    },
    probation_revoked: "",
    edit_status: "UNCHANGED",
  };
}

function aCase(caseNumber: string, location: string, charges: any[]): CaseData {
  return {
    balance_due: 0,
    birth_year: 1990,
    case_detail_link: "?404",
    case_number: caseNumber,
    charges,
    citation_number: "",
    current_status: "Closed",
    district_attorney_number: "",
    edit_status: "UNCHANGED",
    date: "Jan 1, 2010",
    location,
    name: "SB 819",
    violation_type: "Offense Felony",
    restitution: false,
  };
}

/** Every demo case, whichever of its charges the analysis covers. */
export function buildRecord(analysis: AnalysisData): RecordData {
  return {
    total_balance_due: 0,
    errors: [],
    questions: {},
    cases: [
      aCase("100", "Multnomah", [
        charge("100-1", "Robbery in the Second Degree", "100"),
        charge(
          "100-2",
          "Theft in the First Degree",
          "100",
          "Felony Class C",
          "164.055"
        ),
      ]),
      aCase("300", "Multnomah", [
        charge(
          "300-1",
          "Driving Under the Influence of Intoxicants",
          "300",
          "Misdemeanor Class A",
          "813.010"
        ),
      ]),
      aCase("500", "Multnomah", [
        charge(
          "500-1",
          "Rape in the Second Degree",
          "500",
          "Felony Class B",
          "163.365"
        ),
      ]),
      aCase("800", "Multnomah", [
        charge(
          "800-1",
          "Assault in the Second Degree",
          "800",
          "Felony Class B",
          "163.175"
        ),
      ]),
      aCase("900", "Multnomah", [
        charge(
          "900-1",
          "Arson in the First Degree",
          "900",
          "Felony Class A",
          "164.325"
        ),
      ]),
      aCase("200", "Clackamas", [
        charge(
          "200-1",
          "Assault in the First Degree",
          "200",
          "Felony Class A",
          "163.185"
        ),
      ]),
    ],
    summary: {
      sb819_analysis: analysis as any,
      total_charges: 7,
      total_cases: 6,
      county_fines: [],
      total_fines_due: 0,
      charges_grouped_by_eligibility_and_case: [
        [
          "Ineligible",
          [["", [["100-1", "Robbery in the Second Degree (CONVICTED)"]]]],
        ],
      ],
    },
  };
}
