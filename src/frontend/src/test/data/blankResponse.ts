import { SearchResponse } from "../../redux/search/types";

const blankResponse: SearchResponse = {
  record: {
    cases: [],
    errors: [],
    questions: {},
    summary: {
      total_charges: 0,
      charges_grouped_by_eligibility_and_case: [["Eligible Now", []]],
      county_fines: [],
      total_fines_due: 0,
      total_cases: 0,
    },
    total_balance_due: 0,
  },
};

export default blankResponse;
