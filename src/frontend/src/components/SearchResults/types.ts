export interface ChargeType {
  statute: string;
  expungement_result: any;
  name: string;
  disposition: {
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
}

export interface ExpungementResultType {
  type_eligibility: boolean | string;
  time_eligibility: boolean;
  date_of_eligibility: string;
  time_eligibility_reason: string;
  type_eligibility_reason: string;
}
