export interface ChargeData {
  case_number: string;
  ambiguous_charge_id: string;
  statute: string;
  expungement_result: any;
  name: string;
  type_name: string;
  date: string;
  disposition: {
    ruling: string;
    date: string;
  };
}

export interface CaseData {
  balance_due: number;
  birth_year: number;
  case_detail_link: string;
  case_number: string;
  charges: ChargeData[];
  citation_number: string;
  current_status: string;
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
  cases_sorted: any;
  eligible_charges_by_date: any[];
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

export interface QuestionsData {
  [ambiguous_charge_id: string]: QuestionData
}

export interface QuestionData {
  case_number: string;
  ambiguous_charge_id: string;
  question: string;
  options: { [option: string]: string; };
  answer: string;
}
