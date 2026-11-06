/**
 * Analyses shaped like the "sb 819" demo record, built criterion by criterion so a test can
 * say which rules a conviction meets. Statuses and sections are computed by the resolver,
 * which the shared fixture table pins.
 */

import { CaseData, RecordData } from "../Record/types";
import resolveAnalysis from "./resolveAnalysis";
import {
  SB819AnalysisData,
  SB819ChargeAnalysisData,
  SB819CriterionResultData,
  SB819Determination,
  SB819Outcome,
  SB819Pathway,
  SB819PathwayResultData,
  SB819Scope,
  SB819Status,
} from "./types";

const P: SB819Status = "Possibly SB-819 Eligible";
const I: SB819Status = "SB-819 Ineligible";

interface Options {
  scope?: SB819Scope;
  pathway?: SB819Pathway | null;
  determination?: SB819Determination;
  outcome?: SB819Outcome;
  gate?: boolean;
  question?: {
    text: string;
    if_yes: SB819Status;
    if_no: SB819Status;
    note?: string;
  };
}

export function criterion(
  key: string,
  name: string,
  o: Options = {}
): SB819CriterionResultData {
  const determination = o.determination ?? "OECI";
  return {
    key,
    scope: o.scope ?? "charge",
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
const FELONY_FAILED = { ...FELONY, outcome: "Failed" as SB819Outcome };
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
const AGG_MURDER = { ...NOT_AGG_MURDER, outcome: "Failed" as SB819Outcome };

// Collateral Consequences
const CC: SB819Pathway = "Collateral Consequences";
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
const registerable = (outcome: SB819Outcome) =>
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
  registerable?: SB819Outcome;
  felonyUncertain?: boolean;
  mainFails?: "felony" | "murder";
}

export function chargeAnalysis(shape: ChargeShape): SB819ChargeAnalysisData {
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
  const pathways: SB819PathwayResultData[] = shape.mainFails
    ? []
    : [
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
  };
}

export interface DemoOptions {
  /** A second conviction on case 100. */
  theft?: boolean;
  /** A DUII on case 300, which the record rules out as not a felony. */
  duii?: boolean;
  /** Rape II on case 500, a registerable sex offense. */
  rape?: boolean;
  /** Assault II on case 800 with an amended disposition, so the felony level is a question. */
  assault?: boolean;
  /** Burglary I on case 900, a second conviction with nothing settled from the record. */
  burglary?: boolean;
  /** No charge in scope at all. */
  empty?: boolean;
  /** Only the DUII, so nothing survives the main criteria. */
  ruledOutOnly?: boolean;
}

/** The demo-shaped analysis: Robbery II on case 100 always, and the rest by option. */
export function buildAnalysis(o: DemoOptions = {}): SB819AnalysisData {
  const shapes: ChargeShape[] = o.empty
    ? []
    : o.ruledOutOnly
    ? [
        {
          id: "300-1",
          caseNumber: "300",
          name: "Driving Under the Influence of Intoxicants",
          mainFails: "felony" as const,
        },
      ]
    : [
        {
          id: "100-1",
          caseNumber: "100",
          name: "Robbery in the Second Degree",
        },
        ...(o.theft
          ? [
              {
                id: "100-2",
                caseNumber: "100",
                name: "Theft in the First Degree",
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
                registerable: "Failed" as SB819Outcome,
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
              },
            ]
          : []),
        ...(o.burglary
          ? [
              {
                id: "900-1",
                caseNumber: "900",
                name: "Burglary in the First Degree",
              },
            ]
          : []),
      ];
  const charges: SB819AnalysisData["charges"] = {};
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
    set_aside_motion: null,
  };
}

/** Every demo case, whichever of its charges the analysis covers. */
export function buildRecord(analysis: SB819AnalysisData): RecordData {
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
          "Burglary in the First Degree",
          "900",
          "Felony Class A",
          "164.225"
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
