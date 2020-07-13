export interface ChargeData {
  case_number: string;
  ambiguous_charge_id: string;
  statute: string;
  expungement_result: any;
  expungement_rules: any;
  name: string;
  type_name: string;
  date: string;
  disposition: {
    status: string;
    ruling: string;
    date: string;
  };
  probation_revoked: string;
  edit_status: string;
}

export interface CaseData {
  balance_due: number;
  birth_year: number;
  case_detail_link: string;
  case_number: string;
  charges: ChargeData[];
  citation_number: string;
  current_status: string;
  edit_status: string;
  date: string;
  location: string;
  name: string;
  violation_type: string;
}

export interface RecordData {
  total_balance_due?: number;
  cases?: any[];
  errors?: string[];
  summary?: RecordSummaryData;
  questions?: QuestionsData;
}

export interface RecordSummaryData {
  total_charges: number;
  eligible_charges_by_date: { [label: string]: any[] };
  county_balances: CountyBalanceData[];
  total_balance_due: number;
  total_cases: number;
}

export interface CountyBalanceData {
  county_name: string;
  balance: number;
}

export interface ExpungementResultData {
  type_eligibility: TypeEligibilityData;
  time_eligibility?: TimeEligibilityData;
  charge_eligibility: ChargeEligibilityData;
}

export interface TypeEligibilityData {
  status: string;
  reason: string;
}

export interface TimeEligibilityData {
  status: string;
  reason: string;
  date_will_be_eligible: string;
}

export interface ChargeEligibilityData {
  status: string;
  label: string;
}

export interface ExpungementRulesData {
  reason: any;
  open: boolean;
}

export interface QuestionsData {
  [ambiguous_charge_id: string]: QuestionSummaryData;
}

export interface QuestionSummaryData {
  case_number: string;
  ambiguous_charge_id: string;
  root: QuestionData;
}

export interface QuestionData {
  question_id: string;
  text: string;
  options: { [option: string]: AnswerData };
  selection: string;
  convicted_date_string: string;
  probation_revoked_date_string: string;
}

export interface AnswerData {
  question?: QuestionData;
  edit?: { [key: string]: string };
}

export const CHARGE_TYPES = [
  "Civil Offense",
  "Criminal Forfeiture",
  "Dismissed Criminal Charge",
  "DUII",
  "Diverted DUII",
  "FareViolation",
  "Felony Class A",
  "Felony Class B",
  "Felony Class C",
  "Juvenile",
  "Marijuana Eligible",
  "Marijuana Eligible (Below age 21)",
  "Marijuana Violation",
  "Marijuana Ineligible",
  "Misdemeanor",
  "Parking Ticket",
  "Person Felony Class B",
  "Reduced to Violation",
  "Severe Charge",
  "Sex Crime",
  "137.225(6)(f) related sex crime",
  "137.225(6)(f) related sex crime",
  "Subsection 6",
  "Traffic Offense",
  "Traffic Violation",
  "Unclassified",
  "Violation",
];

export const CHARGE_TYPES_CONVICTED_ONLY = [
  "Felony Class A",
  "Felony Class B",
  "Felony Class C",
  "DUII",
  "Marijuana Eligible",
  "Marijuana Eligible (Below age 21)",
  "Marijuana Ineligible",
  "Misdemeanor",
  "Person Felony Class B",
  "Severe Charge",
  "Sex Crime",
  "137.225(6)(f) related sex crime",
  "137.225(6)(f) related sex crime",
  "Subsection 6",
  "Traffic Offense",
];

export const CHARGE_TYPES_DISMISSED_ONLY = [
  "Dismissed Criminal Charge",
  "Diverted DUII",
];
