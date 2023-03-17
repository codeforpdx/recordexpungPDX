import { SearchResponse } from "../../redux/search/types";

const multipleResponse: SearchResponse = {
  record: {
    cases: [
      {
        balance_due: 0.0,
        birth_year: 1990,
        case_detail_link: "?404",
        case_number: "110000",
        charges: [
          {
            ambiguous_charge_id: "110000-1",
            case_number: "110000",
            date: "Jan 21, 2022",
            disposition: {
              amended: false,
              date: "Apr 21, 2022",
              ruling: "Dismissed",
              status: "Dismissed",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: null,
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
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
                status: "Eligible",
              },
            },
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            id: "110000-1-0",
            level: "Misdemeanor Class C",
            name: "Theft in the Third Degree",
            probation_revoked: null,
            statute: "164043",
            type_name: "Dismissed Criminal Charge",
          },
          {
            ambiguous_charge_id: "110000-2",
            case_number: "110000",
            date: "Jan 21, 2022",
            disposition: {
              amended: false,
              date: "Apr 21, 2022",
              ruling: "Dismissed",
              status: "Dismissed",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: null,
                label: "Ineligible",
                status: "Ineligible",
              },
              time_eligibility: {
                date_will_be_eligible: "Jan 21, 2022",
                reason: "Eligible now",
                status: "Eligible",
                unique_date: true,
              },
              type_eligibility: {
                reason: "Infraction reason",
                status: "Ineligible",
              },
            },
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            id: "110000-2-0",
            level: "A low level infraction",
            name: "A low level infraction",
            probation_revoked: null,
            statute: "164043",
            type_name: "Dismissed Criminal Charge",
          },
        ],
        citation_number: "something",
        current_status: "Closed",
        date: "Jan 21, 2022",
        district_attorney_number: "01234567",
        edit_status: "UNCHANGED",
        location: "Multnomah",
        name: "MULTIPLE CHARGES",
        sid: "OR12345678",
        violation_type: "Offense Misdemeanor",
      },
      {
        balance_due: 1000.0,
        birth_year: 1990,
        case_detail_link: "?404",
        case_number: "100000",
        charges: [
          {
            ambiguous_charge_id: "100000-1",
            case_number: "100000",
            date: "Jan 21, 2019",
            disposition: {
              amended: false,
              date: "Apr 21, 2019",
              ruling: "Convicted",
              status: "Convicted",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: null,
                label: "Eligible Now",
                status: "Eligible Now",
              },
              time_eligibility: {
                date_will_be_eligible: "Apr 21, 2022",
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
            id: "100000-1-0",
            level: "Misdemeanor Class A",
            name: "Disorderly Conduct in the First Degree",
            probation_revoked: null,
            statute: "166223",
            type_name: "Misdemeanor Class A",
          },
          {
            ambiguous_charge_id: "100000-2",
            case_number: "100000",
            date: "Jan 21, 2019",
            disposition: {
              amended: false,
              date: "Apr 21, 2019",
              ruling: "Unrecognized",
              status: "Unrecognized",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: null,
                label: "Eligible Now",
                status: "Eligible Now",
              },
              time_eligibility: {
                date_will_be_eligible: "Jan 21, 2019",
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
            id: "100000-2-0",
            level: "Misdemeanor Class B",
            name: "Disorderly Conduct in the Second Degree",
            probation_revoked: null,
            statute: "1662250A",
            type_name: "Dismissed Criminal Charge",
          },
        ],
        citation_number: "something",
        current_status: "Closed",
        date: "Jan 21, 2019",
        district_attorney_number: "01234567",
        edit_status: "UNCHANGED",
        location: "Baker",
        name: "MULTIPLE CHARGES",
        sid: "OR12345678",
        violation_type: "Offense Misdemeanor",
      },
      {
        balance_due: 0.0,
        birth_year: 1990,
        case_detail_link: "?404",
        case_number: "120000",
        charges: [
          {
            ambiguous_charge_id: "120000-1",
            case_number: "120000",
            date: "Jan 21, 2011",
            disposition: {
              amended: false,
              date: "Apr 21, 2011",
              ruling: "Dismissed",
              status: "Dismissed",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: null,
                label: "Possibly Eligible",
                status: "Unknown",
              },
              time_eligibility: null,
              type_eligibility: {
                reason:
                  "Traffic Violation \u2013 Dismissed violations are eligible under 137.225(1)(b) but administrative reasons may make this difficult to expunge.",
                status: "Needs More Analysis",
              },
            },
            expungement_rules:
              'Convictions for traffic-related offenses are not eligible for expungement under ORS 137.225(7)(a). This includes Violations, Misdemeanors, and Felonies.\nThe eligibility of a dismissed traffic violation is subject to some debate. 137.225(1)(d) says that "At any time after an acquittal or a dismissal...an arrested, cited or charged person may apply to the court in the county in which the person was arrested, cited or charged, for entry of an order setting aside the record of the arrest, citation or charge." A driving offense probably qualifies as a citation under any definition of the word.\nHowever, DAs will probably object to filing for these, at least initially, based off their understanding of the previous version of the law, and their relationships with the other parts of the State, and the practical administrative burdens this would place on those systems.\nMost directly, it\u2019s not clear that the local municipal systems have a good way of expunging traffic tickets, dismissed or not.\nAs such, petitioners filing to expunge dismissed traffic tickets may receive pushback and have their petition rejected, and do so at their own risk.',
            id: "120000-1-0",
            level: "Violation",
            name: "Failure to Obey Traffic Control Device",
            probation_revoked: null,
            statute: "811265",
            type_name: "Traffic Violation",
          },
          {
            ambiguous_charge_id: "120001-1",
            case_number: "120001",
            date: "Jan 22, 2011",
            disposition: {
              amended: false,
              date: "Apr 22, 2011",
              ruling: "Convicted",
              status: "Convicted",
            },
            edit_status: "UNCHANGED",
            expungement_result: {
              charge_eligibility: {
                date_to_sort_label_by: null,
                label: "Ineligible",
                status: "Ineligible",
              },
              time_eligibility: null,
              type_eligibility: {
                reason: "Public derpiness is never excusable.",
                status: "Needs More Analysis",
              },
            },
            expungement_rules: "Rule that everyone knows",
            id: "120000-1-0",
            level: "Violation",
            name: "Public Derpiness",
            probation_revoked: null,
            statute: "811265",
            type_name: "Traffic Violation",
          },
        ],
        citation_number: "something",
        current_status: "Closed",
        date: "Jan 21, 2011",
        district_attorney_number: "01234567",
        edit_status: "UNCHANGED",
        location: "Washington",
        name: "MULTIPLE CHARGES",
        sid: "OR12345678",
        violation_type: "Offense Violation",
      },
    ],
    errors: [],
    questions: {},
    summary: {
      charges_grouped_by_eligibility_and_case: [
        [
          "Eligible Now",
          [
            [
              "",
              [
                [
                  "110000-1",
                  "Theft in the Third Degree (DISMISSED) Charged Jan 21, 2022",
                ],
              ],
            ],
          ],
        ],
        [
          "Eligible Now If Balance Paid",
          [
            [
              "Baker 100000 \u2013 $1000.0",
              [
                [
                  "100000-1",
                  "Disorderly Conduct in the First Degree (CONVICTED) Charged Jan 21, 2019",
                ],
                [
                  "100000-2",
                  "Disorderly Conduct in the Second Degree (DISMISSED) Charged Jan 21, 2019",
                ],
              ],
            ],
          ],
        ],
      ],
      county_fines: [
        {
          case_fines: [{ balance: 1000.0, case_number: "100000" }],
          county_name: "Baker",
          total_fines_due: 1000.0,
        },
        { case_fines: [], county_name: "Multnomah", total_fines_due: 0 },
      ],
      total_cases: 3,
      total_charges: 6,
      total_fines_due: 1000.0,
    },
    total_balance_due: 1000.0,
  },
};

export default multipleResponse;
