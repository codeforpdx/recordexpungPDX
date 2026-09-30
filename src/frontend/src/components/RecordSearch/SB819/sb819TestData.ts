import { CaseData, RecordData } from "../Record/types";
import {
  SB819AnalysisData,
  SB819ChargeAnalysisData,
  SB819CriterionResultData,
  SB819Determination,
  SB819Outcome,
  SB819PathwayResultData,
  SB819Scope,
  SB819Status,
} from "./types";

const INELIGIBLE_RESULT = {
  type_eligibility: {
    status: "Ineligible",
    reason: "Ineligible under 137.225(5)(a)",
  },
  charge_eligibility: {
    status: "Ineligible",
    label: "Ineligible",
    date_to_sort_label_by: null,
  },
};

function charge(id: string, name: string, caseNumber: string) {
  return {
    case_number: caseNumber,
    ambiguous_charge_id: id,
    statute: "164.405",
    expungement_result: INELIGIBLE_RESULT,
    expungement_rules: "",
    name,
    type_name: "Person Felony Class B",
    level: "Felony Class B",
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

interface CriterionOptions {
  determination?: SB819Determination;
  scope?: SB819Scope;
  outcome?: SB819Outcome;
  group?: string;
  gate?: boolean;
  pathway?: SB819PathwayResultData["pathway"] | null;
  question?: {
    if_yes: SB819Status;
    if_no: SB819Status;
    note?: string;
    text?: string;
  } | null;
}

export function criterion(
  key: string,
  name: string,
  options: CriterionOptions = {}
): SB819CriterionResultData {
  const determination = options.determination ?? "OECI";
  return {
    key,
    scope: options.scope ?? "charge",
    disjunction_group: options.group ?? "",
    is_gate: options.gate ?? false,
    is_screenable: determination === "OECI" || determination === "Question",
    name,
    description: "Detail as published in the DA information sheet.",
    citation: "Page 3",
    determination,
    pathway: options.pathway ?? null,
    outcome: options.outcome ?? "Passed",
    explanation: `${name}: explanation`,
    question: options.question
      ? {
          // Real questions are interrogative; a requirement with a question mark on the end
          // reads as the opposite of what is being asked.
          text: options.question.text ?? `${name}?`,
          if_yes: options.question.if_yes,
          if_no: options.question.if_no,
          note: options.question.note ?? "",
        }
      : null,
  };
}

const PASSING_MAIN = [
  criterion("in-multnomah", "Conviction is from Multnomah County"),
  criterion(
    "not-expungeable",
    "Conviction is not expungeable under ORS 137.225"
  ),
  criterion("sentenced-as-felony", "Conviction was sentenced as a felony"),
  criterion("not-aggravated-murder", "Conviction is not aggravated murder"),
];

const CLEARS_ON_YES = {
  if_yes: "Possibly SB-819 Eligible" as SB819Status,
  if_no: "SB-819 Ineligible" as SB819Status,
};
const CLEARS_ON_NO = {
  if_yes: "SB-819 Ineligible" as SB819Status,
  if_no: "Possibly SB-819 Eligible" as SB819Status,
};

/** Applicant-scope question, asked once and applied to every charge. It gates the pathway. */
const CURRENTLY_INCARCERATED = criterion(
  "currently-incarcerated",
  "Applicant is currently incarcerated",
  {
    determination: "Question",
    scope: "record",
    outcome: "Unknown",
    gate: true,
    pathway: "Excessive Sentencing",
    question: {
      ...CLEARS_ON_YES,
      text: "Is the applicant currently incarcerated?",
    },
  }
);

/** Charge-scope conjunct on the same pathway, for separating a real bar from an alternative. */
const FIVE_YEARS_SERVED = criterion(
  "five-years-served",
  "Applicant has served at least five years",
  {
    determination: "Question",
    outcome: "Unknown",
    pathway: "Excessive Sentencing",
    question: {
      ...CLEARS_ON_YES,
      text: "Has the applicant served at least five years on this sentence?",
    },
  }
);

/** Two alternatives, so failing one of them is not a bar. */
const OVER_60_OR_ILL = criterion(
  "over-60-or-ill",
  "Applicant is over 60, ill, or on hospice care",
  {
    determination: "Question",
    scope: "record",
    outcome: "Unknown",
    group: "excessive-sentencing-alternatives",
    pathway: "Excessive Sentencing",
    question: {
      ...CLEARS_ON_YES,
      text: "Is the applicant over 60, ill, or on hospice care?",
    },
  }
);

const JUVENILE_TRANSFER = criterion(
  "juvenile-transfer",
  "Applicant faces transfer to adult prison",
  {
    determination: "Question",
    scope: "record",
    outcome: "Unknown",
    group: "excessive-sentencing-alternatives",
    pathway: "Excessive Sentencing",
    question: {
      ...CLEARS_ON_YES,
      text: "Is the applicant facing transfer to adult prison?",
    },
  }
);

/** Case-scope question, answered once per prosecution. It gates the pathway. */
const SENTENCE_COMPLETED = criterion(
  "sentence-completed",
  "Applicant has fully completed the sentence",
  {
    determination: "Question",
    scope: "case",
    outcome: "Unknown",
    gate: true,
    pathway: "Collateral Consequences",
    question: {
      ...CLEARS_ON_YES,
      text: "Has the applicant fully completed the sentence on this case?",
    },
  }
);

const DOMESTIC_VIOLENCE = criterion(
  "no-domestic-violence",
  "Conviction did not involve domestic violence",
  {
    determination: "Question",
    outcome: "Unknown",
    pathway: "Collateral Consequences",
    question: {
      ...CLEARS_ON_NO,
      text: "Did this conviction involve domestic violence?",
      note: "A domestic violence conviction is not disqualifying if it was committed while the applicant was a juvenile and did not involve an intimate partner.",
    },
  }
);

const REHABILITATION = criterion(
  "substantial-rehabilitation",
  "Applicant demonstrates substantial rehabilitation and low risk",
  {
    determination: "Part 2",
    outcome: "Unknown",
    pathway: "Collateral Consequences",
  }
);

/** The one Actual Innocence criterion that can be screened: the claim itself. */
const INNOCENCE_CLAIM = criterion(
  "innocence-claim",
  "Applicant asserts actual innocence of the conviction",
  {
    determination: "Question",
    outcome: "Unknown",
    pathway: "Actual Innocence",
    question: {
      ...CLEARS_ON_YES,
      text: "Is the applicant asserting that they are actually innocent of this conviction?",
    },
  }
);

const INVESTIGATION_AVENUE = criterion(
  "investigation-avenue",
  "The JIU can identify an avenue of investigation",
  {
    determination: "Discretion",
    outcome: "Unknown",
    pathway: "Actual Innocence",
  }
);

function pathway(
  name: SB819PathwayResultData["pathway"],
  status: SB819Status,
  criteria: SB819CriterionResultData[]
): SB819PathwayResultData {
  return { pathway: name, status, criteria };
}

/** The one main criterion that can be a question: the disposition was amended. */
const FELONY_UNCERTAIN = criterion(
  "sentenced-as-felony",
  "Conviction was sentenced as a felony",
  {
    determination: "OECI",
    outcome: "Unknown",
    question: {
      ...CLEARS_ON_YES,
      text: "Was this conviction sentenced as a felony?",
    },
  }
);

function chargeAnalysis(
  id: string,
  caseNumber: string,
  name: string,
  options: {
    registerableFails?: boolean;
    mainFails?: boolean;
    felonyUncertain?: boolean;
    withActualInnocence?: boolean;
  } = {}
): SB819ChargeAnalysisData {
  if (options.mainFails) {
    return {
      ambiguous_charge_id: id,
      case_number: caseNumber,
      charge_name: name,
      status: "SB-819 Ineligible",
      main_criteria: [
        ...PASSING_MAIN.slice(0, 3),
        criterion(
          "not-aggravated-murder",
          "Conviction is not aggravated murder",
          {
            outcome: "Failed",
          }
        ),
      ],
      pathways: [],
      available_pathways: [],
      blocked_pathways: [],
    };
  }

  const collateral = [
    SENTENCE_COMPLETED,
    criterion(
      "not-registerable-sex-offense",
      "Conviction is not a registerable sex offense",
      {
        outcome: options.registerableFails ? "Failed" : "Passed",
        pathway: "Collateral Consequences",
      }
    ),
    DOMESTIC_VIOLENCE,
    REHABILITATION,
  ];

  const main = options.felonyUncertain
    ? [PASSING_MAIN[0], PASSING_MAIN[1], FELONY_UNCERTAIN, PASSING_MAIN[3]]
    : PASSING_MAIN;

  return {
    ambiguous_charge_id: id,
    case_number: caseNumber,
    charge_name: name,
    status: "Needs More Analysis",
    main_criteria: main,
    pathways: [
      ...(options.withActualInnocence
        ? [
            pathway("Actual Innocence", "Needs More Analysis", [
              INNOCENCE_CLAIM,
              INVESTIGATION_AVENUE,
            ]),
          ]
        : []),
      pathway("Excessive Sentencing", "Needs More Analysis", [
        CURRENTLY_INCARCERATED,
        OVER_60_OR_ILL,
        JUVENILE_TRANSFER,
        FIVE_YEARS_SERVED,
      ]),
      pathway(
        "Collateral Consequences",
        options.registerableFails ? "SB-819 Ineligible" : "Needs More Analysis",
        collateral
      ),
    ],
    available_pathways: [
      ...(options.withActualInnocence
        ? (["Actual Innocence"] as SB819PathwayResultData["pathway"][])
        : []),
      "Excessive Sentencing",
      ...(options.registerableFails
        ? []
        : (["Collateral Consequences"] as SB819PathwayResultData["pathway"][])),
    ],
    blocked_pathways: options.registerableFails
      ? ["Collateral Consequences"]
      : [],
  };
}

interface Options {
  /** Whether any analyzed charge survived the criteria. */
  possible?: boolean;
  /** Collateral Consequences barred while the other pathways stay open. */
  blockCollateralConsequences?: boolean;
  /** No charge in scope at all, so no badge should render. */
  empty?: boolean;
  /** A second conviction on case 100, for exercising case-scope answers. */
  twoChargesOnFirstCase?: boolean;
  /** The first charge's sentencing level is a question, which holds everything behind it. */
  felonyUncertain?: boolean;
  /** The first charge also carries the Actual Innocence pathway. */
  withActualInnocence?: boolean;
}

export function buildAnalysis({
  possible = true,
  blockCollateralConsequences = false,
  empty = false,
  twoChargesOnFirstCase = false,
  felonyUncertain = false,
  withActualInnocence = false,
}: Options = {}): SB819AnalysisData {
  const charges: { [id: string]: SB819ChargeAnalysisData } = {};

  if (!empty) {
    charges["100-1"] = chargeAnalysis(
      "100-1",
      "100",
      "Robbery in the Second Degree",
      {
        registerableFails: blockCollateralConsequences,
        mainFails: !possible,
        felonyUncertain,
        withActualInnocence,
      }
    );
    if (twoChargesOnFirstCase) {
      charges["100-2"] = chargeAnalysis(
        "100-2",
        "100",
        "Theft in the First Degree"
      );
      charges["300-1"] = chargeAnalysis(
        "300-1",
        "300",
        "Arson in the First Degree"
      );
    }
  }

  const all = Object.values(charges);
  const order: SB819Status[] = [
    "Possibly SB-819 Eligible",
    "Needs More Analysis",
    "SB-819 Ineligible",
  ];

  return {
    counties_analyzed: empty ? [] : ["Multnomah"],
    has_analyzed_charges: all.length > 0,
    has_possibly_eligible: all.some((c) => c.status !== "SB-819 Ineligible"),
    sections: order.map((status) => ({
      status,
      charge_ids: all
        .filter((c) => c.status === status)
        .map((c) => c.ambiguous_charge_id),
    })),
    charges,
  };
}

export function buildRecord(analysis: SB819AnalysisData): RecordData {
  const cases = [
    aCase("100", "Multnomah", [
      charge("100-1", "Robbery in the Second Degree", "100"),
      charge("100-2", "Theft in the First Degree", "100"),
    ]),
    aCase("300", "Multnomah", [
      charge("300-1", "Arson in the First Degree", "300"),
    ]),
    aCase("200", "Clackamas", [
      charge("200-1", "Assault in the First Degree", "200"),
    ]),
  ];

  return {
    total_balance_due: 0,
    errors: [],
    questions: {},
    cases,
    summary: {
      sb819_analysis: analysis,
      total_charges: 4,
      total_cases: 3,
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
