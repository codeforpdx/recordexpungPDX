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
        citation_number: "",
        current_status: "Closed",
        date: "Apr 1, 2010",
        location: "Josephine",
        name: "Last, First Middle",
        violation_type: "Offense Felony",
      },
      {
        balance_due: 0.0,
        birth_year: 1901,
        case_detail_link: "",
        case_number: "11AA2222",
        citation_number: "",
        current_status: "Closed",
        date: "Feb 11, 2010",
        location: "Josephine",
        name: "Last, First Middle",
        violation_type: "Offense Felony",
      },
      {
        balance_due: 1763.0,
        birth_year: 1901,
        case_detail_link: "",
        case_number: "11AA3333",
        citation_number: "",
        current_status: "Closed",
        date: "Nov 5, 2009",
        location: "Josephine",
        name: "Last, First Middle",
        violation_type: "Offense Misdemeanor",
      },
    ],
  },
};
