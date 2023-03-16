import { SearchResponse } from "../../redux/search/types";

const commonResponse: SearchResponse = {
  record: {
    cases: [
      {
        balance_due: 0.0,
        birth_year: 1985,
        case_detail_link: "?404",
        case_number: "200000",
        charges: [
          {
            ambiguous_charge_id: "200000-1",
            case_number: "200000",
            date: "Sep 9, 2019",
            disposition: {
              amended: false,
              date: "Sep 9, 2019",
              ruling: "Dismissed",
              status: "Dismissed",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: undefined,
                label: "Eligible Now",
                status: "Eligible Now",
              },
              time_eligibility: {
                date_will_be_eligible: "Sep 9, 2019",
                reason: "Eligible now",
                status: "Eligible",
                unique_date: true,
              },
              type_eligibility: {
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
                status: "Eligible",
              },
            },
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            id: "200000-1-0",
            level: "Misdemeanor Class A",
            name: "Obstruction of search warrant",
            probation_revoked: undefined,
            statute: "162247",
            type_name: "Dismissed Criminal Charge",
          },
        ],
        citation_number: "something",
        current_status: "Closed",
        date: "Sep 9, 2019",
        district_attorney_number: "01234567",
        edit_status: "UNCHANGED",
        location: "Benton",
        name: "COMMON NAME",
        sid: "OR12345678",
        violation_type: "Offense Misdemeanor",
      },
      {
        balance_due: 0.0,
        birth_year: 1985,
        case_detail_link: "?404",
        case_number: "210000",
        charges: [
          {
            ambiguous_charge_id: "210000-1",
            case_number: "210000",
            date: "Nov 16, 2018",
            disposition: {
              amended: false,
              date: "Jan 21, 2019",
              ruling: "Convicted",
              status: "Convicted",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: undefined,
                label: "Needs More Analysis",
                status: "Needs More Analysis",
              },
              time_eligibility: {
                date_will_be_eligible: "Jan 21, 2024",
                reason:
                  "Five years from date of conviction (137.225(1)(b)) OR Seven years from date of conviction (137.225(1)(b)) OR Never. Type ineligible charges are always time ineligible.",
                status: "Ineligible",
                unique_date: false,
              },
              type_eligibility: {
                reason:
                  "Marijuana Manufacture Delivery \u2013 Eligible under 137.226 OR Felony Class A \u2013 Ineligible by omission from statute OR Felony Class B \u2013 Convictions that fulfill the conditions of 137.225(1)(b) are eligible OR Felony Class C \u2013 Eligible under 137.225(1)(b)",
                status: "Needs More Analysis",
              },
            },
            expungement_rules:
              'ORS 137.226 makes eligible additional marijuana-related charges - in particular, those crimes which are now considered minor felonies or below.\n    One way to identify a marijuana crime is if it has the statute section 475860.\n    Also if "marijuana", "marij", or "mj" are in the charge name, we conclude it\'s a marijuana eligible charge (after filtering out MarijuanaIneligible charges by statute).\n    \n    We broadly reclassify marijuana eligible charges that were originally Felony Class A, Felony Class B, and Felony Unclassified charges as Felony Class C.\n    We broadly reclassify all other marijuana eligible charges as Misdemeanor Class A.\n    ',
            id: "210000-1-0",
            level: "Felony Unclassified",
            name: "Poss Controlled Sub",
            probation_revoked: undefined,
            statute: "4759924A",
            type_name:
              "Marijuana Manufacture Delivery OR Felony Class A OR Felony Class B OR Felony Class C",
          },
        ],
        citation_number: "something",
        current_status: "Closed",
        date: "Nov 16, 2018",
        district_attorney_number: "01234567",
        edit_status: "UNCHANGED",
        location: "Baker",
        name: "COMMON B. NAME",
        sid: "OR12345678",
        violation_type: "Offense Misdemeanor",
      },
      {
        balance_due: 0.0,
        birth_year: 1970,
        case_detail_link: "?404",
        case_number: "100000",
        charges: [
          {
            ambiguous_charge_id: "100000-1",
            case_number: "100000",
            date: "Sep 9, 2016",
            disposition: {
              amended: false,
              date: "Oct 9, 2016",
              ruling: "Convicted",
              status: "Convicted",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: "Jan 21, 2026",
                label: "Eligible Jan 21, 2026",
                status: "Will Be Eligible",
              },
              time_eligibility: {
                date_will_be_eligible: "Jan 21, 2026",
                reason:
                  "137.225(7)(b) \u2013 Seven years from most recent other conviction from case [210000].",
                status: "Ineligible",
                unique_date: true,
              },
              type_eligibility: {
                reason:
                  "Felony Class B \u2013 Convictions that fulfill the conditions of 137.225(1)(b) are eligible",
                status: "Eligible",
              },
            },
            expungement_rules:
              "Class B felony convictions are generally eligible under ORS 137.225(1)(b). Class B felony dismissals are always eligible under 137.225(1)(d).",
            id: "100000-1-0",
            level: "Felony Class B",
            name: "Aggravated Theft in the First Degree",
            probation_revoked: undefined,
            statute: "164057",
            type_name: "Felony Class B",
          },
        ],
        citation_number: "something",
        current_status: "Closed",
        date: "Sep 9, 2016",
        district_attorney_number: "01234567",
        edit_status: "UNCHANGED",
        location: "Clackamas",
        name: "COMMON A. NAME",
        sid: "OR12345678",
        violation_type: "Offense Misdemeanor",
      },
      {
        balance_due: 0.0,
        birth_year: 1970,
        case_detail_link: "?404",
        case_number: "110000",
        charges: [
          {
            ambiguous_charge_id: "110000-1",
            case_number: "110000",
            date: "May 26, 2015",
            disposition: {
              amended: false,
              date: "Jun 25, 2015",
              ruling: "Convicted",
              status: "Convicted",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: undefined,
                label: "Eligible Now",
                status: "Eligible Now",
              },
              time_eligibility: {
                date_will_be_eligible: "Jan 21, 2022",
                reason: "Eligible now",
                status: "Eligible",
                unique_date: true,
              },
              type_eligibility: {
                reason:
                  "Misdemeanor Class A \u2013 Eligible under 137.225(1)(b)",
                status: "Eligible",
              },
            },
            expungement_rules:
              "Convictions for misdemeanors are generally eligible under ORS 137.225(1)(b).\nExceptions include convictions related to sex, child and elder abuse, and driving, including DUII.\nDismissals for misdemeanors are generally eligible under ORS 137.225(1)(d). Exceptions include cases dismissed due to successful completion of DUII diversion.",
            id: "110000-1-0",
            level: "Misdemeanor Class A",
            name: "Theft in the Second Degree",
            probation_revoked: undefined,
            statute: "164057",
            type_name: "Misdemeanor Class A",
          },
        ],
        citation_number: "something",
        current_status: "Closed",
        date: "May 26, 2015",
        district_attorney_number: "01234567",
        edit_status: "UNCHANGED",
        location: "Baker",
        name: "COMMON NAME",
        sid: "OR12345678",
        violation_type: "Offense Misdemeanor",
      },
      {
        balance_due: 0.0,
        birth_year: 1970,
        case_detail_link: "?404",
        case_number: "120000",
        charges: [
          {
            ambiguous_charge_id: "120000-1",
            case_number: "120000",
            date: "May 26, 2014",
            disposition: {
              amended: false,
              date: "Jun 25, 2014",
              ruling: "Convicted",
              status: "Convicted",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: undefined,
                label: "Eligible Now",
                status: "Eligible Now",
              },
              time_eligibility: {
                date_will_be_eligible: "Jun 25, 2014",
                reason: "Eligible now",
                status: "Eligible",
                unique_date: true,
              },
              type_eligibility: {
                reason: "Marijuana Violation \u2013 Eligible under 475B.401",
                status: "Eligible",
              },
            },
            expungement_rules:
              "Under 475B.401, convictions for possession of less than an ounce of marijuana are always eligible, regardless of any time eligibility restrictions that would normally apply.\n    This charge type is identifiable as any marijuana charge whose level is Violation.",
            id: "120000-1-0",
            level: "violation",
            name: "Poss under oz Marijuana",
            probation_revoked: undefined,
            statute: "475000",
            type_name: "Marijuana Violation",
          },
        ],
        citation_number: "something",
        current_status: "Closed",
        date: "May 26, 2015",
        district_attorney_number: "01234567",
        edit_status: "UNCHANGED",
        location: "Baker",
        name: "COMMON A NAME",
        sid: "OR12345678",
        violation_type: "Offense Misdemeanor",
      },
    ],
    errors: [],
    questions: {
      "210000-1": {
        ambiguous_charge_id: "210000-1",
        case_number: "210000",
        root: {
          convicted_date_string: "",
          options: {
            No: {
              edit: {},
              question: {
                convicted_date_string: "",
                options: {
                  "A Felony": {
                    edit: { charge_type: "FelonyClassA" },
                    question: undefined,
                  },
                  "B Felony": {
                    edit: { charge_type: "FelonyClassB" },
                    question: undefined,
                  },
                  "C Felony": {
                    edit: { charge_type: "FelonyClassC" },
                    question: undefined,
                  },
                },
                probation_revoked_date_string: "",
                question_id:
                  "210000-1-Was the underlying substance marijuana?-No-Was the charge for an A Felony, B Felony, or C Felony?",
                selection: "",
                text: "Was the charge for an A Felony, B Felony, or C Felony?",
              },
            },
            Yes: {
              edit: { charge_type: "MarijuanaManufactureDelivery" },
              question: undefined,
            },
          },
          probation_revoked_date_string: "",
          question_id: "210000-1-Was the underlying substance marijuana?",
          selection: "",
          text: "Was the underlying substance marijuana?",
        },
      },
    },
    summary: {
      charges_grouped_by_eligibility_and_case: [
        [
          "Eligible Jan 21, 2026",
          [
            [
              "",
              [
                [
                  "100000-1",
                  "Aggravated Theft in the First Degree (CONVICTED) Charged Sep 9, 2016",
                ],
              ],
            ],
          ],
        ],
        [
          "Eligible Now",
          [
            [
              "",
              [
                [
                  "200000-1",
                  "Obstruction of search warrant (DISMISSED) Charged Sep 9, 2019",
                ],
              ],
            ],
            [
              "",
              [
                [
                  "110000-1",
                  "Theft in the Second Degree (CONVICTED) Charged May 26, 2015",
                ],
              ],
            ],
            [
              "",
              [
                [
                  "120000-1",
                  "Poss under oz Marijuana (CONVICTED) Charged May 26, 2014",
                ],
              ],
            ],
          ],
        ],

        [
          "Needs More Analysis",
          [
            [
              "",
              [
                [
                  "210000-1",
                  "Poss Controlled Sub (CONVICTED) Charged Nov 16, 2018",
                ],
              ],
            ],
          ],
        ],
      ],
      county_fines: [
        { case_fines: [], county_name: "Baker", total_fines_due: 0 },
        { case_fines: [], county_name: "Benton", total_fines_due: 0 },
        { case_fines: [], county_name: "Clackamas", total_fines_due: 0 },
      ],
      total_cases: 5,
      total_charges: 5,
      total_fines_due: 0,
    },
    total_balance_due: 0.0,
  },
};

export default commonResponse;
