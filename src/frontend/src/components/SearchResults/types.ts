export interface ChargeType {
  statute: string;
  expungement_result: any;
  name: string;
  type_name: string;
  date: string;
  disposition?: {
    ruling: string;
    date: string;
  };
}

export interface CaseType {
  balance_due: number;
  birth_year: number;
  case_detail_link: string;
  case_number: string;
  charges: ChargeType[];
  citation_number: string;
  current_status: string;
  date: string;
  location: string;
  name: string;
  violation_type: string;
}

export interface Record {
  total_balance_Due?: number;
  cases?: any[];
  errors?: string[];
  summary?: RecordSummaryType;
}

export interface RecordSummaryType {
  total_charges: number;
  cases_sorted: any;
  eligible_charges: any[];
  county_balances: CountyBalanceType[];
  total_balance_due: number;
  total_cases: number;
}

export interface CountyBalanceType {
  county_name: string;
  balance: number;
}

export interface ExpungementResultType {
  type_eligibility: TypeEligibility;
  time_eligibility?: TimeEligibility;
  charge_eligibility: ChargeEligibility;
}

export interface TypeEligibility {
  status: string;
  reason: string;
}

export interface TimeEligibility {
  status: string;
  reason: string;
  date_will_be_eligible: string;
}

export interface ChargeEligibility {
  status: string;
  label: string;
}