import { hasBalanceDue } from "./selectors";

describe("SEARCH SELECTORS TEST", () => {
  describe("hasBalanceDue", () => {
    it("only returns cases with balance_due > 0", () => {
      const result = mockData.record.cases.filter(hasBalanceDue);

      expect(result.length).toBe(1);
    });
  });
});

const mockData = {
  record: {
    cases: [
      {
        balance_due: 0.0,
        birth_year: 1901,
        case_detail_link: "",
        case_number: "11AA1111",
        charges: [],
        citation_number: "",
        current_status: "Closed",
        district_attorney_number: "1",
        date: "Apr 1, 2010",
        edit_status: "in process",
        location: "Josephine",
        name: "Last, First Middle",
        violation_type: "Offense Felony",
        restitution: false
      },
      {
        balance_due: 0.0,
        birth_year: 1901,
        case_detail_link: "",
        case_number: "11AA2222",
        charges: [],
        citation_number: "",
        current_status: "Closed",
        date: "Feb 11, 2010",
        district_attorney_number: "1",
        edit_status: "in process",
        location: "Josephine",
        name: "Last, First Middle",
        violation_type: "Offense Felony",
        restitution: false
      },
      {
        balance_due: 1763.0,
        birth_year: 1901,
        case_detail_link: "",
        case_number: "11AA3333",
        charges: [],
        citation_number: "",
        current_status: "Closed",
        edit_status: "in process",
        date: "Nov 5, 2009",
        district_attorney_number: "1",
        location: "Josephine",
        name: "Last, First Middle",
        violation_type: "Offense Misdemeanor",
        restitution: false
      },
    ],
  },
};
