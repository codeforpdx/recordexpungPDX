from typing import List, Tuple
from dateutil.relativedelta import relativedelta
from dacite import from_dict

from expungeservice.models.case import CaseSummary, OeciCase
from expungeservice.models.charge import OeciCharge, EditStatus
from expungeservice.models.record import Alias
from expungeservice.models.disposition import DispositionCreator
from expungeservice.util import DateWithFuture as date_class, LRUCache


class DemoRecords:
    @staticmethod
    def build_search_results(
        username: str, password: str, aliases: Tuple[Alias, ...], search_cache: LRUCache
    ) -> Tuple[List[OeciCase], List[str]]:

        alias_match = search_cache[aliases]
        if alias_match:
            return alias_match
        else:
            errors = []
            search_results: List[OeciCase] = []
            for alias in aliases:
                alias_lower = Alias(
                    alias.first_name.lower().strip(),
                    alias.last_name.lower().strip(),
                    alias.middle_name.lower().strip(),
                    alias.birth_date,
                )
                try:
                    alias_search_result = DemoRecords.records.get(alias_lower, [])
                    search_results += alias_search_result
                except Exception as e:
                    errors.append(str(e))
                    print(e)
            if not errors:
                search_cache[aliases] = search_results, errors
            return search_results, errors

    shared_case_data = {
        "citation_number": "something",
        "case_detail_link": "?404",
        "edit_status": EditStatus.UNCHANGED,
        "current_status": "Closed",
        "balance_due_in_cents": 0,
        "birth_year": 1995,
        "location": "Multnomah",
        "violation_type": "Offense Misdemeanor",
        "date": date_class.today(),
        "district_attorney_number": "01234567",
        "sid": "OR12345678",
        "restitution": False,
        "set_aside_motion": None,
        "caption_name": "",
    }
    shared_charge_data = {
        "balance_due_in_cents": 0,
        "edit_status": EditStatus.UNCHANGED,
        "probation_revoked": None,
        "level": "Misdemeanor Class C",
        "statute": "166.015",
        "name": "Disorderly Conduct",
        "date": date_class.today(),
        "disposition": DispositionCreator.empty(),
    }

    common_name_record_1 = [
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "COMMON A. NAME",
                    "birth_year": 1970,
                    "case_number": "100000",
                    "location": "Clackamas",
                    "date": date_class.today() - relativedelta(years=6, days=12, months=4),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "100000-1",
                        "name": "Aggravated Theft in the First Degree",
                        "statute": "164.057",
                        "level": "Felony Class B",
                        "date": date_class.today() - relativedelta(years=6, days=12, months=4),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=6, days=12, months=3), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "COMMON NAME",
                    "birth_year": 1970,
                    "case_number": "110000",
                    "location": "Baker",
                    "date": date_class.today() - relativedelta(years=7, days=26, months=7),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "110000-1",
                        "name": "Theft in the Second Degree",
                        "statute": "164.057",
                        "level": "Misdemeanor Class A",
                        "date": date_class.today() - relativedelta(years=7, days=26, months=7),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=7, days=26, months=6), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "COMMON A NAME",
                    "birth_year": 1970,
                    "case_number": "120000",
                    "location": "Baker",
                    "date": date_class.today() - relativedelta(years=7, days=26, months=7),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "120000-1",
                        "name": "Poss under oz Marijuana",
                        "statute": "475.000",
                        "level": "violation",
                        "date": date_class.today() - relativedelta(years=8, days=26, months=7),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=8, days=26, months=6), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
    ]

    common_name_record_2 = [
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "COMMON NAME",
                    "birth_year": 1985,
                    "case_number": "200000",
                    "location": "Benton",
                    "date": date_class.today() - relativedelta(years=3, days=12, months=4),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "200000-1",
                        "name": "Obstruction of search warrant",
                        "statute": "162.247",
                        "level": "Misdemeanor Class A",
                        "date": date_class.today() - relativedelta(years=3, days=12, months=4),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=3, days=12, months=4), ruling="Dismissed"
                        ),
                    },
                ),
            ),
        ),
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "COMMON B. NAME",
                    "birth_year": 1985,
                    "case_number": "210000",
                    "location": "Baker",
                    "date": date_class.today() - relativedelta(years=4, days=5, months=2),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "210000-1",
                        "name": "Poss Controlled Sub",
                        "statute": "475.9924A",
                        "level": "Felony Unclassified",
                        "date": date_class.today() - relativedelta(years=4, days=5, months=2),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=4), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
    ]

    # "date": date_class.today() - relativedelta(years=3, days=9, months =5),

    """
    Exercises every Multnomah SB-819 limiting criterion. Convictions are dated far enough back
    that the ORS 137.225(7)(b) blocking windows have all closed, so the one normally-eligible
    charge stays eligible and out of the SB-819 view.
    """
    sb819_birth_year = date_class.today().year - 36

    sb819_record = [
        # Eligible under ORS 137.225, so it never enters the SB-819 analysis.
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "SB 819",
                    "birth_year": sb819_birth_year,
                    "case_number": "SB819-100",
                    "location": "Multnomah",
                    "date": date_class.today() - relativedelta(years=12),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "SB819-100-1",
                        "name": "Theft in the Second Degree",
                        "statute": "164.045",
                        "level": "Misdemeanor Class A",
                        "date": date_class.today() - relativedelta(years=12),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=12), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
        # Ineligible under 137.225, but outside Multnomah, so it is excluded from the view.
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "SB 819",
                    "birth_year": sb819_birth_year,
                    "case_number": "SB819-200",
                    "location": "Clackamas",
                    "violation_type": "Offense Felony",
                    "date": date_class.today() - relativedelta(years=14),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "SB819-200-1",
                        "name": "Assault in the First Degree",
                        "statute": "163.185",
                        "level": "Felony Class A",
                        "date": date_class.today() - relativedelta(years=14),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=14), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
        # Fails the main criterion that the conviction was sentenced as a felony.
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "SB 819",
                    "birth_year": sb819_birth_year,
                    "case_number": "SB819-300",
                    "location": "Multnomah",
                    "date": date_class.today() - relativedelta(years=13),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "SB819-300-1",
                        "name": "Driving Under the Influence of Intoxicants",
                        "statute": "813.010",
                        "level": "Misdemeanor Class A",
                        "date": date_class.today() - relativedelta(years=13),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=13), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
        # Fails the main criterion excluding aggravated murder.
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "SB 819",
                    "birth_year": sb819_birth_year,
                    "case_number": "SB819-400",
                    "location": "Multnomah",
                    "violation_type": "Offense Felony",
                    "date": date_class.today() - relativedelta(years=20),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "SB819-400-1",
                        "name": "Aggravated Murder",
                        "statute": "163.095",
                        "level": "Felony Class A",
                        "date": date_class.today() - relativedelta(years=20),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=20), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
        # Registerable sex offense: ruled out under Collateral Consequences.
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "SB 819",
                    "birth_year": sb819_birth_year,
                    "case_number": "SB819-500",
                    "location": "Multnomah",
                    "violation_type": "Offense Felony",
                    "date": date_class.today() - relativedelta(years=15),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "SB819-500-1",
                        "name": "Rape in the Second Degree",
                        "statute": "163.365",
                        "level": "Felony Class B",
                        "date": date_class.today() - relativedelta(years=15),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=15), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
        # Passes every main criterion, so every pathway question is put to the client.
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "SB 819",
                    "birth_year": sb819_birth_year,
                    "case_number": "SB819-600",
                    "location": "Multnomah",
                    "violation_type": "Offense Felony",
                    "date": date_class.today() - relativedelta(years=16),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "SB819-600-1",
                        "name": "Robbery in the Second Degree",
                        "statute": "164.405",
                        "level": "Felony Class B",
                        "date": date_class.today() - relativedelta(years=16),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=16), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
        # Amended disposition: the sentencing level may differ from the charging level.
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "SB 819",
                    "birth_year": sb819_birth_year,
                    "case_number": "SB819-800",
                    "location": "Multnomah",
                    "violation_type": "Offense Felony",
                    "date": date_class.today() - relativedelta(years=18),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "SB819-800-1",
                        "name": "Assault in the Second Degree",
                        "statute": "163.175",
                        "level": "Felony Class A",
                        "date": date_class.today() - relativedelta(years=18),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=18), ruling="Convicted", amended=True
                        ),
                    },
                ),
            ),
        ),
        # Registerable only if the victim was under 18, which OECI does not record: the
        # reporting requirement is put to the client as a question.
        OeciCase(
            summary=from_dict(
                data_class=CaseSummary,
                data={
                    **shared_case_data,
                    "name": "SB 819",
                    "birth_year": sb819_birth_year,
                    "case_number": "SB819-1000",
                    "location": "Multnomah",
                    "violation_type": "Offense Felony",
                    "date": date_class.today() - relativedelta(years=11),
                },
            ),
            charges=(
                from_dict(
                    data_class=OeciCharge,
                    data={
                        **shared_charge_data,
                        "ambiguous_charge_id": "SB819-1000-1",
                        "name": "Kidnapping in the First Degree",
                        "statute": "163.235",
                        "level": "Felony Class A",
                        "date": date_class.today() - relativedelta(years=11),
                        "disposition": DispositionCreator.create(
                            date=date_class.today() - relativedelta(years=11), ruling="Convicted"
                        ),
                    },
                ),
            ),
        ),
    ]

    records = {
        Alias("sb", "819", "", ""): sb819_record,
        Alias("john", "common", "", ""): common_name_record_1 + common_name_record_2,
        Alias("john", "common", "", "1/1/1970"): common_name_record_1,
        Alias("john", "common", "", "2/2/1985"): common_name_record_2,
        Alias("single", "conviction", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "SINGLE OFFENSE",
                        "birth_year": 1995,
                        "case_number": "100000",
                        "location": "Deschutes",
                        "date": date_class.today() - relativedelta(years=5),
                        "violation_type": "Offense Felony",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "100000-1",
                            "name": "Identity Theft",
                            "statute": "165.800",
                            "level": "Felony Class C",
                            "date": date_class.today() - relativedelta(years=5),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=4, months=9), ruling="Convicted"
                            ),
                        },
                    ),
                ),
            ),
        ],
        Alias("multiple", "charges", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "balance_due_in_cents": 100000,
                        "name": "MULTIPLE CHARGES",
                        "birth_year": 1990,
                        "case_number": "100000",
                        "location": "Baker",
                        "date": date_class.today() - relativedelta(years=4),
                        "violation_type": "Offense Misdemeanor",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "100000-1",
                            "name": "Disorderly Conduct in the First Degree",
                            "statute": "166.223",
                            "level": "Misdemeanor Class A",
                            "date": date_class.today() - relativedelta(years=4),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=3, months=9), ruling="Convicted"
                            ),
                            "balance_due_in_cents": 100000,
                        },
                    ),
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "100000-2",
                            "name": "Disorderly Conduct in the Second Degree",
                            "statute": "166.2250A",
                            "level": "Misdemeanor Class B",
                            "date": date_class.today() - relativedelta(years=4),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=3, months=9), ruling="Dismissed"
                            ),
                            "balance_due_in_cents": 100000,
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "MULTIPLE CHARGES",
                        "birth_year": 1990,
                        "case_number": "110000",
                        "location": "Multnomah",
                        "date": date_class.today() - relativedelta(years=1),
                        "violation_type": "Offense Misdemeanor",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "110000-1",
                            "name": "Theft in the Third Degree",
                            "statute": "164.043",
                            "level": "Misdemeanor Class C",
                            "date": date_class.today() - relativedelta(years=1),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(months=9), ruling="Dismissed"
                            ),
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "MULTIPLE CHARGES",
                        "birth_year": 1990,
                        "case_number": "120000",
                        "location": "Multnomah",
                        "date": date_class.today() - relativedelta(years=12),
                        "violation_type": "Offense Violation",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "120000-1",
                            "name": "Failure to Obey Traffic Control Device",
                            "statute": "811.265",
                            "level": "Violation",
                            "date": date_class.today() - relativedelta(years=12),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=11, months=9), ruling="Dismissed"
                            ),
                        },
                    ),
                ),
            ),
        ],
        Alias("more", "categories", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "John Notaperson",
                        "case_number": "123456",
                        "violation_type": "Offense Felony",
                        "balance_due_in_cents": 50000,
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "123456-1",
                            "name": "Assaulting a Public Safety Officer",
                            "statute": "163.208",
                            "level": "Felony Class C",
                            "date": date_class.today() - relativedelta(years=2),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=1, months=9), ruling="Convicted"
                            ),
                            "balance_due_in_cents": 50000,
                        },
                    ),
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "123456-2",
                            "name": "Felony Riot",
                            "statute": "111.111",
                            "level": "Felony Class C",
                            "date": date_class.today() - relativedelta(years=2),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=1, months=9), ruling="Dismissed"
                            ),
                            "balance_due_in_cents": 50000,
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "John Notaperson",
                        "case_number": "234567",
                        "violation_type": "Offense Felony",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "234567-1",
                            "name": "Assaulting a Public Safety Officer",
                            "statute": "163.208",
                            "level": "Felony Class C",
                            "date": date_class.today() - relativedelta(years=5),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=4, months=9), ruling="Convicted"
                            ),
                        },
                    ),
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "234567-2",
                            "name": "Assaulting a Public Safety Officer",
                            "statute": "163.208",
                            "level": "Felony Class C",
                            "date": date_class.today() - relativedelta(years=5),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=4, months=9), ruling="Dismissed"
                            ),
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "John Notaperson",
                        "case_number": "333333",
                        "violation_type": "Offense Violation",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "333333-1",
                            "name": "Possession of Marijuana < 1 Ounce",
                            "statute": "4758643",
                            "level": "Violation Unclassified",
                            "date": date_class.today() - relativedelta(years=5),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=4, months=9), ruling="Convicted"
                            ),
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "John Notaperson",
                        "case_number": "444444",
                        "violation_type": "Offense Violation",
                        "balance_due_in_cents": 50000,
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "444444-1",
                            "name": "Possession of Marijuana < 1 Ounce",
                            "statute": "4758643",
                            "level": "Violation Unclassified",
                            "date": date_class.today() - relativedelta(years=5),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=4, months=9), ruling="Convicted"
                            ),
                            "balance_due_in_cents": 50000,
                        },
                    ),
                ),
            ),
            # Has an eligible and an ineligible charge
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "John Notaperson",
                        "case_number": "555555",
                        "violation_type": "Offense Felony",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "555555-1",
                            "name": "Assault in the First Degree",
                            "statute": "999999",
                            "level": "Felony Class A",
                            "date": date_class.today() - relativedelta(years=5),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=4, months=9), ruling="Convicted"
                            ),
                            "balance_due_in_cents": 0,
                        },
                    ),
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "555555-2",
                            "name": "Harassment",
                            "statute": "163.208",
                            "level": "Felony Class C",
                            "date": date_class.today() - relativedelta(years=5),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=4, months=9), ruling="Dismissed"
                            ),
                        },
                    ),
                ),
            ),
        ],
        Alias("single", "violation", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "John Notaperson",
                        "case_number": "123456",
                        "violation_type": "Offense Violation",
                        "balance_due_in_cents": 0,
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "123456-1",
                            "name": "Something minor",
                            "statute": "163.208",
                            "level": "Violation",
                            "date": date_class.today() - relativedelta(years=2),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=1, months=9), ruling="Convicted"
                            ),
                            "balance_due_in_cents": 50000,
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "John Notaperson",
                        "case_number": "1234567",
                        "violation_type": "Offense Violation",
                        "balance_due_in_cents": 0,
                        "location": "Benton",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "1234567-1",
                            "name": "Something minor",
                            "statute": "163.208",
                            "level": "Violation",
                            "date": date_class.today() - relativedelta(years=2),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=1, months=9), ruling="Convicted"
                            ),
                            "balance_due_in_cents": 50000,
                        },
                    ),
                ),
            ),
        ],
        Alias("various", "attempts", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "John Notaperson",
                        "case_number": "123456",
                        "violation_type": "Offense Felony",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "123456-1",
                            "name": "Attempt to Commit a Class A Felony",
                            "statute": "161.405(2)(c)",
                            "level": "Felony Class B",
                            "date": date_class.today() - relativedelta(years=10),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=9, months=9), ruling="Convicted"
                            ),
                            "balance_due_in_cents": 0,
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "Jon Notaperson",
                        "case_number": "223456",
                        "violation_type": "Offense Felony",
                        "d" "balance_due_in_cents": 0,
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "223456-1",
                            "name": "Attempt to Commit a Class B Felony",
                            "statute": "161.405(2)(c)",
                            "level": "Felony Class C",
                            "date": date_class.today() - relativedelta(years=10),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=9, months=9), ruling="Convicted"
                            ),
                            "balance_due_in_cents": 0,
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "current_status": "Closed",
                        "name": "John Notaperson",
                        "case_number": "323456",
                        "violation_type": "Offense Misdemeanor",
                        "d" "balance_due_in_cents": 0,
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "323456-1",
                            "name": "Attempt to Commit a Class A Misdemeanor",
                            "statute": "161.405(2)(c)",
                            "level": "Misdemeanor Class B",
                            "date": date_class.today() - relativedelta(years=10),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=9, months=9), ruling="Convicted"
                            ),
                            "balance_due_in_cents": 0,
                        },
                    ),
                ),
            ),
        ],
        Alias("contempt", "one", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "CONTEMPT ONE",
                        "birth_year": 1990,
                        "case_number": "600000",
                        "location": "Multnomah",
                        "date": date_class.today() - relativedelta(years=2),
                        "violation_type": "Offense Violation",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "600000-1",
                            "name": "Contempt of Court",
                            "statute": "33.015",
                            "level": "Violation",
                            "date": date_class.today() - relativedelta(years=2),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=1, months=9), ruling="Convicted"
                            ),
                        },
                    ),
                ),
            ),
        ],
        # Washington County contempt asks whether it involves child support; Yes serves the DOJ on
        # the contempt template, No serves the DA like the theft case beside it. Both motions
        # caption the defendant as the court does, from caption_name.
        Alias("washington", "contempt", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "CONTEMPT, WASHINGTON",
                        "caption_name": "WASHINGTON CONTEMPT",
                        "birth_year": 1988,
                        "case_number": "700000",
                        "location": "Washington",
                        "date": date_class.today() - relativedelta(years=6),
                        "violation_type": "Procedural Matters - Contempt of Court Punitive",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "700000-1",
                            "name": "Contempt of Court",
                            "statute": "33.015",
                            "level": "Violation",
                            "date": date_class.today() - relativedelta(years=6),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=5, months=9), ruling="Convicted"
                            ),
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "CONTEMPT, WASHINGTON",
                        "caption_name": "WASHINGTON CONTEMPT",
                        "birth_year": 1988,
                        "case_number": "710000",
                        "location": "Washington",
                        "date": date_class.today() - relativedelta(years=7),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "710000-1",
                            "name": "Theft in the Third Degree",
                            "statute": "164.043",
                            "level": "Misdemeanor Class C",
                            "date": date_class.today() - relativedelta(years=7),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=6, months=9), ruling="Convicted"
                            ),
                        },
                    ),
                ),
            ),
        ],
    }
