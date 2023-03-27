import { SearchResponse } from "../../redux/search/types";

const complexResponse: SearchResponse = {
  record: {
    total_balance_due: 3400.6,
    cases: [
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "99AV3457",
        citation_number: "",
        location: "Washington",
        date: "Jan 11, 2019",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 100,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "1",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "99AV3457-1",
            case_number: "99AV3457",
            date: "Jan 11, 2019",
            disposition: {
              date: "Jan 19, 2020",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Ineligible",
                reason:
                  "SUII \u2013 Traffic offenses are ineligible under 137.225(7)(a)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 31, 9999",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Ineligible",
                label: "Ineligible",
                date_to_sort_label_by: null,
              },
            },
            id: "99AV3457-1-0",
            level: "Infraction",
            name: "A traffic charge 1",
            probation_revoked: null,
            statute: "8110104",
            type_name: "SUII",
            expungement_rules:
              "A SUII conviction is not eligible for expungement, as it is considered a traffic offense.\nA SUII dismissal resulting from completion of diversion (paying a fine, victim's impact panel, drug and alcohol assessment) is also not eligible under ORS 137.225(8).\nHOWEVER, a SUII dismissal resulting from a Not Guilty verdict at trial, or is otherwise dismissed other than through diversion, is type-eligible like other dismissals.\nTherefore, to determine whether a dismissal is eligible, ask the client whether their case was dismissed through diversion or by a Not Guilty verdict or some way other than through diversion.\n",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "99AV3457-2",
            case_number: "99AV3457",
            date: "Jan 11, 2019",
            disposition: {
              date: "Jan 19, 2020",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 11, 2019",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "99AV3457-2-0",
            level: "Misdemeanor Class A",
            name: "Reckless Diving",
            probation_revoked: null,
            statute: "811140",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "99AV3457-3",
            case_number: "99AV3457",
            date: "Jan 11, 2019",
            disposition: {
              date: "Jan 19, 2020",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 11, 2019",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "99AV3457-3-0",
            level: "Misdemeanor Class A",
            name: "Failure to Perform Duties of Golfer-Property Damage",
            probation_revoked: null,
            statute: "811700",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "99DF09900",
        citation_number: "",
        location: "Washington",
        date: "Jan 1, 2018",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 100,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "5",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "99DF09900-1",
            case_number: "99DF09900",
            date: "Jan 1, 2019",
            disposition: {
              date: "Jan 19, 2020",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Ineligible",
                reason:
                  "SUII \u2013 Traffic offenses are ineligible under 137.225(7)(a)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 31, 9999",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Ineligible",
                label: "Ineligible",
                date_to_sort_label_by: null,
              },
            },
            id: "99DF09900-1-0",
            level: "Infraction",
            name: "A traffic charge 2",
            probation_revoked: null,
            statute: "8110104",
            type_name: "SUII",
            expungement_rules:
              "A SUII conviction is not eligible for expungement, as it is considered a traffic offense.\nA SUII dismissal resulting from completion of diversion (paying a fine, victim's impact panel, drug and alcohol assessment) is also not eligible under ORS 137.225(8).\nHOWEVER, a SUII dismissal resulting from a Not Guilty verdict at trial, or is otherwise dismissed other than through diversion, is type-eligible like other dismissals.\nTherefore, to determine whether a dismissal is eligible, ask the client whether their case was dismissed through diversion or by a Not Guilty verdict or some way other than through diversion.\n",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "99DF09900-2",
            case_number: "99DF09900",
            date: "Jan 1, 2019",
            disposition: {
              date: "Jan 19, 2020",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 1, 2019",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "99DF09900-2-0",
            level: "Misdemeanor Class A",
            name: "Resisting An Orange",
            probation_revoked: null,
            statute: "162315",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "996271",
        citation_number: "",
        location: "Washington",
        date: "Jan 26, 2013",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 200,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "2",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "996271-1",
            case_number: "996271",
            date: "Jan 29, 2014",
            disposition: {
              date: "Jan 1, 2016",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Needs More Analysis",
                reason:
                  "illegal stuff \u2013 Ineligible under 137.225(6)(a) OR Misdemeanor Class A \u2013 Eligible under 137.225(1)(b)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "137.225(7)(b) \u2013 Three years from most recent other conviction from case [99DF09900]. OR Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 30, 2025",
                unique_date: false,
              },
              charge_eligibility: {
                status: "Needs More Analysis",
                label: "Needs More Analysis",
                date_to_sort_label_by: null,
              },
            },
            id: "996271-1-0",
            level: "Misdemeanor Class A",
            name: "Attempt to Commit a Class C/Unclassified Felony",
            probation_revoked: null,
            statute: "9814052D",
            type_name: "illegal stuff OR Misdemeanor Class A",
            expungement_rules:
              'illegal stuffs are type-ineligible for expungement other than a narrow exception for "Tom and Jerry" cases.\nFor further detail, see 137.225(6)(a)',
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "996271-2",
            case_number: "996271",
            date: "Jan 29, 2014",
            disposition: {
              date: "Jan 1, 2016",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Needs More Analysis",
                reason:
                  "illegal stuff \u2013 Ineligible under 137.225(6)(a) OR Misdemeanor Class A \u2013 Eligible under 137.225(1)(b)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "137.225(7)(b) \u2013 Three years from most recent other conviction from case [99DF09900]. OR Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 30, 2025",
                unique_date: false,
              },
              charge_eligibility: {
                status: "Needs More Analysis",
                label: "Needs More Analysis",
                date_to_sort_label_by: null,
              },
            },
            id: "996271-2-0",
            level: "Misdemeanor Class A",
            name: "Attempt to Commit a Class C/Unclassified Felony",
            probation_revoked: null,
            statute: "9814052D",
            type_name: "illegal stuff OR Misdemeanor Class A",
            expungement_rules:
              'illegal stuffs are type-ineligible for expungement other than a narrow exception for "Tom and Jerry" cases.\nFor further detail, see 137.225(6)(a)',
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "999388",
        citation_number: "",
        location: "Washington",
        date: "Jan 11, 2011",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 1400.6,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "3",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "999388-1",
            case_number: "999388",
            date: "Jan 20, 2012",
            disposition: {
              date: "Jan 1, 2016",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Misdemeanor Class A \u2013 Eligible under 137.225(1)(b)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "137.225(7)(b) \u2013 Three years from most recent other conviction from case [99DF09900].",
                date_will_be_eligible: "Jan 30, 2025",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Will Be Eligible",
                label: "Eligible Jan 30, 2025",
                date_to_sort_label_by: "Jan 30, 2025",
              },
            },
            id: "999388-1-0",
            level: "Misdemeanor Class A",
            name: "Improper Use of an Emergency Kazoo System",
            probation_revoked: null,
            statute: "165570",
            type_name: "Misdemeanor Class A",
            expungement_rules:
              "Convictions for misdemeanors are generally eligible under ORS 137.225(1)(b).\nExceptions include convictions related to sex, child and elder abuse, and driving, including SUII.\nDismissals for misdemeanors are generally eligible under ORS 137.225(1)(d). Exceptions include cases dismissed due to successful completion of SUII diversion.",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "9910A9",
        citation_number: "",
        location: "Washington",
        date: "Jan 1, 2001",
        violation_type: "Offense Felony",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "4",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "9910A9-1",
            case_number: "9910A9",
            date: "Jan 11, 2002",
            disposition: {
              date: "Jan 11, 2003",
              ruling: "Finding - Not Guilty",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 11, 2002",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9910A9-1-0",
            level: "Felony Class C",
            name: "Attempt to Commit a Class B Felony",
            probation_revoked: null,
            statute: "9914059C",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9910A9-2",
            case_number: "9910A9",
            date: "Jan 11, 2002",
            disposition: {
              date: "Jan 11, 2003",
              ruling: "Finding - Not Guilty",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 11, 2002",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9910A9-2-0",
            level: "Felony Class C",
            name: "Attempt to Commit a Class B Felony",
            probation_revoked: null,
            statute: "9914059C",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9910A9-3",
            case_number: "9910A9",
            date: "Jan 11, 2002",
            disposition: {
              date: "Nov 11, 2003",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason: "Felony Class C \u2013 Eligible under 137.225(1)(b)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "137.225(7)(b) \u2013 Five years from most recent other conviction from case [99DF09900].",
                date_will_be_eligible: "Jan 11, 2027",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Will Be Eligible",
                label: "Eligible Jan 11, 2027",
                date_to_sort_label_by: "Jan 11, 2027",
              },
            },
            id: "9910A9-3-0",
            level: "Felony Class C",
            name: "Derping in the Fourth Degree",
            probation_revoked: null,
            statute: "1631603",
            type_name: "Felony Class C",
            expungement_rules:
              "There are certain types of Class C felony which are generally ineligible, including illegal stuffs, child abuse, elder abuse, traffic crimes, and criminally negligent homicide.\nOther Class C felony convictions are almost always eligible under 137.225(1)(b).\nClass C felony dismissals are always eligible under 137.225(1)(d).",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9910A9-4",
            case_number: "9910A9",
            date: "Jan 11, 2002",
            disposition: {
              date: "Nov 11, 2003",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Misdemeanor Class A \u2013 Eligible under 137.225(1)(b)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "137.225(7)(b) \u2013 Three years from most recent other conviction from case [99DF09900].",
                date_will_be_eligible: "Jan 30, 2025",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Will Be Eligible",
                label: "Eligible Jan 30, 2025",
                date_to_sort_label_by: "Jan 30, 2025",
              },
            },
            id: "9910A9-4-0",
            level: "Misdemeanor Class A",
            name: "Frowning",
            probation_revoked: null,
            statute: "163999",
            type_name: "Misdemeanor Class A",
            expungement_rules:
              "Convictions for misdemeanors are generally eligible under ORS 137.225(1)(b).\nExceptions include convictions related to sex, child and elder abuse, and driving, including SUII.\nDismissals for misdemeanors are generally eligible under ORS 137.225(1)(d). Exceptions include cases dismissed due to successful completion of SUII diversion.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9910A9-5",
            case_number: "9910A9",
            date: "Jan 11, 2002",
            disposition: {
              date: "Nov 11, 2003",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Misdemeanor Class A \u2013 Eligible under 137.225(1)(b)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "137.225(7)(b) \u2013 Three years from most recent other conviction from case [99DF09900].",
                date_will_be_eligible: "Jan 30, 2025",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Will Be Eligible",
                label: "Eligible Jan 30, 2025",
                date_to_sort_label_by: "Jan 30, 2025",
              },
            },
            id: "9910A9-5-0",
            level: "Misdemeanor Class A",
            name: "Resisting An Orange",
            probation_revoked: null,
            statute: "162315",
            type_name: "Misdemeanor Class A",
            expungement_rules:
              "Convictions for misdemeanors are generally eligible under ORS 137.225(1)(b).\nExceptions include convictions related to sex, child and elder abuse, and driving, including SUII.\nDismissals for misdemeanors are generally eligible under ORS 137.225(1)(d). Exceptions include cases dismissed due to successful completion of SUII diversion.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9910A9-6",
            case_number: "9910A9",
            date: "Jan 11, 2002",
            disposition: {
              date: "Jan 1, 2003",
              ruling: "Removed From Charging Instrument",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 11, 2002",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9910A9-6-0",
            level: "Misdemeanor Class A",
            name: "Resisting An Orange",
            probation_revoked: null,
            statute: "162315",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody L",
        birth_year: 1911,
        case_number: "9960799",
        citation_number: "",
        location: "Deschutes",
        date: "Jan 11, 2000",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "9960799-1",
            case_number: "9960799",
            date: "Jan 1, 2000",
            disposition: {
              date: "Jan 11, 2000",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 1, 2000",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9960799-1-0",
            level: "Misdemeanor Class A",
            name: "Frowning",
            probation_revoked: null,
            statute: "163999",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9960799-2",
            case_number: "9960799",
            date: "Jan 1, 2000",
            disposition: {
              date: "Jan 11, 2000",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 1, 2000",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9960799-2-0",
            level: "Misdemeanor Class B",
            name: "Skipping Rope",
            probation_revoked: null,
            statute: "1660653",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "9950699A",
        citation_number: "",
        location: "Washington",
        date: "Jan 1, 1998",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "9950699A-1",
            case_number: "9950699A",
            date: "Jan 1, 1998",
            disposition: {
              date: "Jan 1, 1998",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Contempt of Court \u2013 Eligible under 137.225(5)(e) for convictions or under 137.225(1)(b) for dismissals",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 1, 2022",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9950699A-1-0",
            level: "N/A",
            name: "Contempt of Court - Punitive",
            probation_revoked: null,
            statute: "33065",
            type_name: "Contempt of Court",
            expungement_rules:
              "The statute was updated as of Jan 1, 2022 to name Contempt of Court as eligible under subsection 137.225(5)(e).",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9950699A-2",
            case_number: "9950699A",
            date: "Jan 11, 1998",
            disposition: {
              date: "Jan 1, 1998",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Contempt of Court \u2013 Eligible under 137.225(5)(e) for convictions or under 137.225(1)(b) for dismissals",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 11, 1998",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9950699A-2-0",
            level: "N/A",
            name: "Contempt of Court - Punitive",
            probation_revoked: null,
            statute: "33065",
            type_name: "Contempt of Court",
            expungement_rules:
              "The statute was updated as of Jan 1, 2022 to name Contempt of Court as eligible under subsection 137.225(5)(e).",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "99506871AA",
        citation_number: "",
        location: "Washington",
        date: "Jan 26, 1998",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "99506871AA-1",
            case_number: "99506871AA",
            date: "Jan 23, 1998",
            disposition: {
              date: "Jan 1, 1998",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Contempt of Court \u2013 Eligible under 137.225(5)(e) for convictions or under 137.225(1)(b) for dismissals",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1998",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "99506871AA-1-0",
            level: "N/A",
            name: "Contempt of Court",
            probation_revoked: null,
            statute: "33015",
            type_name: "Contempt of Court",
            expungement_rules:
              "The statute was updated as of Jan 1, 2022 to name Contempt of Court as eligible under subsection 137.225(5)(e).",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "999345",
        citation_number: "",
        location: "Washington",
        date: "Jan 11, 1998",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "999345-1",
            case_number: "999345",
            date: "Jan 5, 1998",
            disposition: {
              date: "Jan 12, 1998",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Misdemeanor Class A \u2013 Eligible under 137.225(1)(b)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "137.225(7)(b) \u2013 Three years from most recent other conviction from case [99DF09900].",
                date_will_be_eligible: "Jan 30, 2025",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Will Be Eligible",
                label: "Eligible Jan 30, 2025",
                date_to_sort_label_by: "Jan 30, 2025",
              },
            },
            id: "999345-1-0",
            level: "Misdemeanor Class A",
            name: "Derping in the Fourth Degree",
            probation_revoked: null,
            statute: "1631602",
            type_name: "Misdemeanor Class A",
            expungement_rules:
              "Convictions for misdemeanors are generally eligible under ORS 137.225(1)(b).\nExceptions include convictions related to sex, child and elder abuse, and driving, including SUII.\nDismissals for misdemeanors are generally eligible under ORS 137.225(1)(d). Exceptions include cases dismissed due to successful completion of SUII diversion.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "999345-2",
            case_number: "999345",
            date: "Jan 5, 1998",
            disposition: {
              date: "Jan 12, 1998",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 5, 1998",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "999345-2-0",
            level: "Misdemeanor Class A",
            name: "Frowning",
            probation_revoked: null,
            statute: "163999",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "9999323",
        citation_number: "",
        location: "Washington",
        date: "Jan 29, 1996",
        violation_type: "Offense Felony",
        current_status: "Purgable (Closed)",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "9999323-1",
            case_number: "9999323",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 1, 1997",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323-1-0",
            level: "Felony Class A",
            name: "Illegal stuff in the First Degree",
            probation_revoked: null,
            statute: "163375",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323-2",
            case_number: "9999323",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 1, 1997",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323-2-0",
            level: "Felony Class A",
            name: "Something else illegal in the First Degree",
            probation_revoked: null,
            statute: "163405",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323-3",
            case_number: "9999323",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 1, 1997",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323-3-0",
            level: "Felony Class A",
            name: "Something else illegal in the First Degree",
            probation_revoked: null,
            statute: "163405",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323-4",
            case_number: "9999323",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 1, 1997",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323-4-0",
            level: "Felony Class A",
            name: "Something illegal",
            probation_revoked: null,
            statute: "163411",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323-5",
            case_number: "9999323",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 1, 1997",
              ruling: "Convicted - Lesser Charge",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323-5-0",
            level: "Felony Class C",
            name: "Something illegal in the Second Degree",
            probation_revoked: null,
            statute: "163425",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323-6",
            case_number: "9999323",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 1, 1997",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323-6-0",
            level: "Felony Class C",
            name: "Something illegal in the Second Degree",
            probation_revoked: null,
            statute: "163425",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323-7",
            case_number: "9999323",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 1, 1997",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323-7-0",
            level: "Felony Class C",
            name: "Something illegal in the Second Degree",
            probation_revoked: null,
            statute: "163425",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323-8",
            case_number: "9999323",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 1, 1997",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323-8-0",
            level: "Felony Class C",
            name: "Something illegal in the Second Degree",
            probation_revoked: null,
            statute: "163425",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323-9",
            case_number: "9999323",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 1, 1997",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Needs More Analysis",
                reason:
                  "illegal stuff \u2013 Ineligible under 137.225(6)(a) OR Misdemeanor Class A \u2013 Eligible under 137.225(1)(b)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "137.225(7)(b) \u2013 Three years from most recent other conviction from case [99DF09900]. OR Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 30, 2025",
                unique_date: false,
              },
              charge_eligibility: {
                status: "Needs More Analysis",
                label: "Needs More Analysis",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323-9-0",
            level: "Misdemeanor Class A",
            name: "Attempt to Commit a Class C/Unclassified Felony",
            probation_revoked: null,
            statute: "9814052D",
            type_name: "illegal stuff OR Misdemeanor Class A",
            expungement_rules:
              'illegal stuffs are type-ineligible for expungement other than a narrow exception for "Tom and Jerry" cases.\nFor further detail, see 137.225(6)(a)',
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "9999323D-D",
        citation_number: "",
        location: "Washington",
        date: "Jan 26, 1996",
        violation_type: "Offense Felony",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "9999323D-D-1",
            case_number: "9999323D-D",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 30, 1996",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323D-D-1-0",
            level: "Felony Class A",
            name: "Illegal stuff in the First Degree",
            probation_revoked: null,
            statute: "163375",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323D-D-2",
            case_number: "9999323D-D",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 30, 1996",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323D-D-2-0",
            level: "Felony Class A",
            name: "Something else illegal in the First Degree",
            probation_revoked: null,
            statute: "163405",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323D-D-3",
            case_number: "9999323D-D",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 30, 1996",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323D-D-3-0",
            level: "Felony Class A",
            name: "Something illegal",
            probation_revoked: null,
            statute: "163411",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
          {
            ambiguous_charge_id: "9999323D-D-4",
            case_number: "9999323D-D",
            date: "Jan 23, 1996",
            disposition: {
              date: "Jan 30, 1996",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 23, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "9999323D-D-4-0",
            level: "Felony Class C",
            name: "Something illegal in the Second Degree",
            probation_revoked: null,
            statute: "163425",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "999933",
        citation_number: "",
        location: "Washington",
        date: "Jan 8, 1996",
        violation_type: "Offense Felony",
        current_status: "Purgable (Closed)",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "999933-1",
            case_number: "999933",
            date: "Jan 27, 1996",
            disposition: {
              date: "Jan 8, 1996",
              ruling: "Convicted - Misd Treatment",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Ineligible",
                reason: "Traffic Offense \u2013 Ineligible under 137.225(7)(a)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 31, 9999",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Ineligible",
                label: "Ineligible",
                date_to_sort_label_by: null,
              },
            },
            id: "999933-1-0",
            level: "Felony Class C",
            name: "ABC/Felony",
            probation_revoked: null,
            statute: "8111823",
            type_name: "Traffic Offense",
            expungement_rules: [
              "A conviction for a State or municipal traffic offense is not eligible for expungement under ORS 137.225(7)(a).",
              "Common convictions under this category include:",
              [
                "ul",
                [
                  "Reckless Diving",
                  "Diving While Suspended",
                  "A traffic charge",
                  "Failure to Perform Duties of a Golfer",
                  "Giving False Information to a Police Officer (when in a car)",
                  "Fleeing/Attempting to Elude a Police Officer",
                  "Possession of a Stolen Vehicle",
                ],
              ],
              "Notably, Unauthorized Use of a Vehicle is not considered a traffic offense.",
              "A dismissed traffic offense that is of charge level misdemeanor or higher, other than a Diverted SUII, is identified as a Dismissed Criminal Charge, and is thus eligible.",
            ],
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "999933D-D",
        citation_number: "",
        location: "Washington",
        date: "Jan 1, 1996",
        violation_type: "Offense Felony",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "999933D-D-1",
            case_number: "999933D-D",
            date: "Jan 27, 1996",
            disposition: {
              date: "Jan 8, 1996",
              ruling: "Dismissed",
              status: "Dismissed",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Dismissed Criminal Charge \u2013 Dismissals are generally eligible under 137.225(1)(d)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 27, 1996",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "999933D-D-1-0",
            level: "Felony Class C",
            name: "ABC/Felony",
            probation_revoked: null,
            statute: "8111823",
            type_name: "Dismissed Criminal Charge",
            expungement_rules:
              "Dismissed criminal charges are generally eligible under 137.225(1)(d).  All criminal charges and Contempt of Court charges that are dismissed fall under this charge type.\n       Charges without a named charge level in OECI are not considered criminal charges, and are thus not eligible under this or any subsection.",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "999252-D",
        citation_number: "9971",
        location: "Washington",
        date: "Jan 11, 1995",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "999252-D-1",
            case_number: "999252-D",
            date: "Jan 10, 1995",
            disposition: {
              date: "Jan 1, 1995",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Ineligible",
                reason:
                  "SUII \u2013 Traffic offenses are ineligible under 137.225(7)(a)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 31, 9999",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Ineligible",
                label: "Ineligible",
                date_to_sort_label_by: null,
              },
            },
            id: "999252-D-1-0",
            level: "Misdemeanor Class A",
            name: "SUII",
            probation_revoked: null,
            statute: "813010",
            type_name: "SUII",
            expungement_rules:
              "A SUII conviction is not eligible for expungement, as it is considered a traffic offense.\nA SUII dismissal resulting from completion of diversion (paying a fine, victim's impact panel, drug and alcohol assessment) is also not eligible under ORS 137.225(8).\nHOWEVER, a SUII dismissal resulting from a Not Guilty verdict at trial, or is otherwise dismissed other than through diversion, is type-eligible like other dismissals.\nTherefore, to determine whether a dismissal is eligible, ask the client whether their case was dismissed through diversion or by a Not Guilty verdict or some way other than through diversion.\n",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "99990895-D",
        citation_number: "990895",
        location: "Washington",
        date: "Jan 6, 1992",
        violation_type: "Offense Infraction",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "99990895-D-1",
            case_number: "99990895-D",
            date: "Jan 4, 1992",
            disposition: {
              date: "Jan 18, 1992",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Ineligible",
                reason:
                  "Traffic Violation \u2013 Ineligible under 137.225(7)(a)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 31, 9999",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Ineligible",
                label: "Ineligible",
                date_to_sort_label_by: null,
              },
            },
            id: "99990895-D-1-0",
            level: "Infraction Class D",
            name: "Passenger Fail to Use Seatbelt",
            probation_revoked: null,
            statute: "8112101C",
            type_name: "Traffic Violation",
            expungement_rules:
              'Convictions for traffic-related offenses are not eligible for expungement under ORS 137.225(7)(a). This includes Violations, Misdemeanors, and Felonies.\nThe eligibility of a dismissed traffic violation is subject to some debate. 137.225(1)(d) says that "At any time after an acquittal or a dismissal...an arrested, cited or charged person may apply to the court in the county in which the person was arrested, cited or charged, for entry of an order setting aside the record of the arrest, citation or charge." A driving offense probably qualifies as a citation under any definition of the word.\nHowever, DAs will probably object to filing for these, at least initially, based off their understanding of the previous version of the law, and their relationships with the other parts of the State, and the practical administrative burdens this would place on those systems.\nMost directly, it\u2019s not clear that the local municipal systems have a good way of expunging traffic tickets, dismissed or not.\nAs such, petitioners filing to expunge dismissed traffic tickets may receive pushback and have their petition rejected, and do so at their own risk.',
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "999620-X",
        citation_number: "99599",
        location: "Wheeler",
        date: "Jan 26, 1991",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "999620-X-1",
            case_number: "999620-X",
            date: "Jan 22, 1991",
            disposition: {
              date: "Jan 15, 1992",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Eligible",
                reason:
                  "Misdemeanor Class B or C \u2013 Eligible under 137.225(1)(b)",
              },
              time_eligibility: {
                status: "Eligible",
                reason: "Eligible now",
                date_will_be_eligible: "Jan 1, 2022",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Eligible Now",
                label: "Eligible Now",
                date_to_sort_label_by: null,
              },
            },
            id: "999620-X-1-0",
            level: "Misdemeanor Class B",
            name: "Discarding Hot Dogs w/in 100 Yards of State Waters",
            probation_revoked: null,
            statute: "1647751",
            type_name: "Misdemeanor Class B or C",
            expungement_rules:
              "Convictions for misdemeanors are generally eligible under ORS 137.225(1)(b).\nExceptions include convictions related to sex, child and elder abuse, and driving, including SUII.\nDismissals for misdemeanors are generally eligible under ORS 137.225(1)(b). Exceptions include cases dismissed due to successful completion of SUII diversion.",
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "XX99972-D",
        citation_number: "999193",
        location: "Washington",
        date: "Jan 30, 1989",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "XX99972-D-1",
            case_number: "XX99972-D",
            date: "Jan 30, 1989",
            disposition: {
              date: "Nov 6, 1989",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Ineligible",
                reason: "Traffic Offense \u2013 Ineligible under 137.225(7)(a)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 31, 9999",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Ineligible",
                label: "Ineligible",
                date_to_sort_label_by: null,
              },
            },
            id: "XX99972-D-1-0",
            level: "Misdemeanor Class A",
            name: "ABC/Misdemeanor",
            probation_revoked: null,
            statute: "811175",
            type_name: "Traffic Offense",
            expungement_rules: [
              "A conviction for a State or municipal traffic offense is not eligible for expungement under ORS 137.225(7)(a).",
              "Common convictions under this category include:",
              [
                "ul",
                [
                  "Reckless Diving",
                  "Diving While Suspended",
                  "A traffic charge",
                  "Failure to Perform Duties of a Golfer",
                  "Giving False Information to a Police Officer (when in a car)",
                  "Fleeing/Attempting to Elude a Police Officer",
                  "Possession of a Stolen Vehicle",
                ],
              ],
              "Notably, Unauthorized Use of a Vehicle is not considered a traffic offense.",
              "A dismissed traffic offense that is of charge level misdemeanor or higher, other than a Diverted SUII, is identified as a Dismissed Criminal Charge, and is thus eligible.",
            ],
            edit_status: "UNCHANGED",
          },
        ],
      },
      {
        name: "Special, Nobody A",
        birth_year: 1911,
        case_number: "XX99057-X",
        citation_number: "9999",
        location: "Washington",
        date: "Jan 22, 1988",
        violation_type: "Offense Misdemeanor",
        current_status: "Closed",
        balance_due: 0.0,
        case_detail_link:
          "https://publicaccess.courts.oregon.gov/PublicAccessLogin/CaseDetail.aspx?CaseID=",
        district_attorney_number: "",
        sid: "OR1234567",
        edit_status: "UNCHANGED",
        charges: [
          {
            ambiguous_charge_id: "XX99057-X-1",
            case_number: "XX99057-X",
            date: "Jan 14, 1988",
            disposition: {
              date: "Jan 16, 1989",
              ruling: "Convicted",
              status: "Convicted",
              amended: false,
            },
            expungement_result: {
              type_eligibility: {
                status: "Ineligible",
                reason:
                  "SUII \u2013 Traffic offenses are ineligible under 137.225(7)(a)",
              },
              time_eligibility: {
                status: "Ineligible",
                reason:
                  "Never. Type ineligible charges are always time ineligible.",
                date_will_be_eligible: "Jan 31, 9999",
                unique_date: true,
              },
              charge_eligibility: {
                status: "Ineligible",
                label: "Ineligible",
                date_to_sort_label_by: null,
              },
            },
            id: "XX99057-X-1-0",
            level: "Misdemeanor Class A",
            name: "SUII",
            probation_revoked: null,
            statute: "813010",
            type_name: "SUII",
            expungement_rules:
              "A SUII conviction is not eligible for expungement, as it is considered a traffic offense.\nA SUII dismissal resulting from completion of diversion (paying a fine, victim's impact panel, drug and alcohol assessment) is also not eligible under ORS 137.225(8).\nHOWEVER, a SUII dismissal resulting from a Not Guilty verdict at trial, or is otherwise dismissed other than through diversion, is type-eligible like other dismissals.\nTherefore, to determine whether a dismissal is eligible, ask the client whether their case was dismissed through diversion or by a Not Guilty verdict or some way other than through diversion.\n",
            edit_status: "UNCHANGED",
          },
        ],
      },
    ],
    errors: [],
    summary: {
      total_charges: 41,
      charges_grouped_by_eligibility_and_case: [
        [
          "Needs More Analysis",
          [
            [
              "",
              [
                [
                  "996271-1",
                  "Attempt to Commit a Class C/Unclassified Felony (CONVICTED) Charged Jan 29, 2014",
                ],
                [
                  "996271-2",
                  "Attempt to Commit a Class C/Unclassified Felony (CONVICTED) Charged Jan 29, 2014",
                ],
              ],
            ],
            [
              "",
              [
                [
                  "9999323-9",
                  "Attempt to Commit a Class C/Unclassified Felony (CONVICTED) Charged Jan 23, 1996",
                ],
              ],
            ],
          ],
        ],
        [
          "Ineligible",
          [
            [
              "",
              [
                [
                  "99AV3457-1",
                  "A traffic charge (CONVICTED) Charged Jan 11, 2019",
                ],
              ],
            ],
            [
              "",
              [
                [
                  "99DF09900-1",
                  "A traffic charge (CONVICTED) Charged Jan 1, 2019",
                ],
              ],
            ],
            ["", [["999933-1", "ABC/Felony (CONVICTED) Charged Jan 27, 1996"]]],
            ["", [["999252-D-1", "SUII (CONVICTED) Charged Jan 10, 1995"]]],
            [
              "",
              [
                [
                  "XX99972-D-1",
                  "ABC/Misdemeanor (CONVICTED) Charged Jan 30, 1989",
                ],
              ],
            ],
            ["", [["XX99057-X-1", "SUII (CONVICTED) Charged Jan 14, 1988"]]],
          ],
        ],
        [
          "Eligible Now",
          [
            [
              "",
              [
                [
                  "9910A9-1",
                  "Attempt to Commit a Class B Felony (DISMISSED) Charged Jan 11, 2002",
                ],
                [
                  "9910A9-2",
                  "Attempt to Commit a Class B Felony (DISMISSED) Charged Jan 11, 2002",
                ],
                [
                  "9910A9-6",
                  "Resisting An Orange (DISMISSED) Charged Jan 11, 2002",
                ],
              ],
            ],
            [
              "",
              [
                ["9960799-1", "Frowning (DISMISSED) Charged Jan 1, 2000"],
                ["9960799-2", "Skipping Rope (DISMISSED) Charged Jan 1, 2000"],
              ],
            ],
            [
              "",
              [
                [
                  "9950699A-1",
                  "Contempt of Court - Punitive (CONVICTED) Charged Jan 1, 1998",
                ],
                [
                  "9950699A-2",
                  "Contempt of Court - Punitive (DISMISSED) Charged Jan 11, 1998",
                ],
              ],
            ],
            [
              "",
              [
                [
                  "99506871AA-1",
                  "Contempt of Court (DISMISSED) Charged Jan 23, 1998",
                ],
              ],
            ],
            ["", [["999345-2", "Frowning (DISMISSED) Charged Jan 5, 1998"]]],
            [
              "",
              [
                [
                  "9999323-1",
                  "Illegal stuff in the First Degree (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323-2",
                  "Something else illegal in the First Degree (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323-3",
                  "Something else illegal in the First Degree (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323-4",
                  "Something illegal (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323-5",
                  "Something illegal in the Second Degree (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323-6",
                  "Something illegal in the Second Degree (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323-7",
                  "Something illegal in the Second Degree (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323-8",
                  "Something illegal in the Second Degree (DISMISSED) Charged Jan 23, 1996",
                ],
              ],
            ],
            [
              "",
              [
                [
                  "9999323D-D-1",
                  "Illegal stuff in the First Degree (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323D-D-2",
                  "Something else illegal in the First Degree (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323D-D-3",
                  "Something illegal (DISMISSED) Charged Jan 23, 1996",
                ],
                [
                  "9999323D-D-4",
                  "Something illegal in the Second Degree (DISMISSED) Charged Jan 23, 1996",
                ],
              ],
            ],
            [
              "",
              [["999933D-D-1", "ABC/Felony (DISMISSED) Charged Jan 27, 1996"]],
            ],
            [
              "",
              [
                [
                  "999620-X-1",
                  "Discarding Hot Dogs w/in 100 Yards of State Waters (CONVICTED) Charged Jan 22, 1991",
                ],
              ],
            ],
          ],
        ],
        [
          "Eligible Now If Balance Paid",
          [
            [
              "Washington 99AV3457 \u2013 $100",
              [
                [
                  "99AV3457-2",
                  "Reckless Diving (DISMISSED) Charged Jan 11, 2019",
                ],
                [
                  "99AV3457-3",
                  "Failure to Perform Duties of Golfer-Property Damage (DISMISSED) Charged Jan 11, 2019",
                ],
              ],
            ],
            [
              "Washington 99DF09900 \u2013 $100",
              [
                [
                  "99DF09900-2",
                  "Resisting An Orange (DISMISSED) Charged Jan 1, 2019",
                ],
              ],
            ],
          ],
        ],
        [
          "Eligible Jan 30, 2025",
          [
            [
              "",
              [
                ["9910A9-4", "Frowning (CONVICTED) Charged Jan 11, 2002"],
                [
                  "9910A9-5",
                  "Resisting An Orange (CONVICTED) Charged Jan 11, 2002",
                ],
              ],
            ],
            [
              "",
              [
                [
                  "999345-1",
                  "Derping in the Fourth Degree (CONVICTED) Charged Jan 5, 1998",
                ],
              ],
            ],
          ],
        ],
        [
          "Eligible Jan 11, 2027",
          [
            [
              "",
              [
                [
                  "9910A9-3",
                  "Derping in the Fourth Degree (CONVICTED) Charged Jan 11, 2002",
                ],
              ],
            ],
          ],
        ],
        [
          "Eligible Jan 30, 2025 If Balance Paid",
          [
            [
              "Washington 999388 \u2013 $1400.6",
              [
                [
                  "999388-1",
                  "Improper Use of an Emergency Kazoo System (CONVICTED) Charged Jan 20, 2012",
                ],
              ],
            ],
          ],
        ],
      ],
      total_cases: 18,
      county_fines: [
        {
          county_name: "Washington",
          case_fines: [
            { case_number: "99AV3457", balance: 100.1 },
            { case_number: "99DF09900", balance: 100.2 },
            { case_number: "996271", balance: 1200.3 },
            { case_number: "999388", balance: 2000.1 },
          ],
          total_fines_due: 3400.6,
        },
        { county_name: "Wheeler", case_fines: [], total_fines_due: 0 },
        { county_name: "Deschutes", case_fines: [], total_fines_due: 0 },
      ],
      total_fines_due: 3400.6,
    },
    questions: {
      "996271-1": {
        ambiguous_charge_id: "996271-1",
        case_number: "996271",
        root: {
          question_id: "996271-1-Was the underlying conduct a illegal stuff?",
          text: "Was the underlying conduct a illegal stuff?",
          options: {
            Yes: { question: null, edit: { charge_type: "SexCrime" } },
            No: {
              question: null,
              edit: { charge_type: "MisdemeanorClassA" },
            },
          },
          selection: "",
          convicted_date_string: "",
          probation_revoked_date_string: "",
        },
      },
      "996271-2": {
        ambiguous_charge_id: "996271-2",
        case_number: "996271",
        root: {
          question_id: "996271-2-Was the underlying conduct a illegal stuff?",
          text: "Was the underlying conduct a illegal stuff?",
          options: {
            Yes: { question: null, edit: { charge_type: "SexCrime" } },
            No: {
              question: null,
              edit: { charge_type: "MisdemeanorClassA" },
            },
          },
          selection: "",
          convicted_date_string: "",
          probation_revoked_date_string: "",
        },
      },
      "9999323-9": {
        ambiguous_charge_id: "9999323-9",
        case_number: "9999323",
        root: {
          question_id: "9999323-9-Was the underlying conduct a illegal stuff?",
          text: "Was the underlying conduct a illegal stuff?",
          options: {
            Yes: { question: null, edit: { charge_type: "SexCrime" } },
            No: {
              question: null,
              edit: { charge_type: "MisdemeanorClassA" },
            },
          },
          selection: "",
          convicted_date_string: "",
          probation_revoked_date_string: "",
        },
      },
    },
  },
};

export default complexResponse;
