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
                    alias.first_name.lower(), alias.last_name.lower(), alias.middle_name.lower(), alias.birth_date
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
        "birth_year": 980,
        "location": "Oregon",
        "violation_type": "Offense Misdemeanor",
    }
    shared_charge_data = {
        "balance_due_in_cents": 0,
        "edit_status": EditStatus.UNCHANGED,
        "probation_revoked": None,
        "level": "Felony Class C",
        "statute": "166.015",
        "name": "Disorderly Conduct",
    }

    records = {
        # Source: https://www.papillonfoundation.org/information/notable-criminal-records
        Alias("rosa", "parks", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "Rosa Parks",
                        "birth_year": 1913,
                        "case_number": "1010101",
                        "location": "Montgomery",
                        "date": date_class(1955, 12, 1),
                        "violation_type": "Offense Misdemeanor",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "1",
                            "name": "Disorderly Conduct",
                            "statute": "166.225",
                            "level": "Misdemeanor Class B",
                            "date": date_class(1955, 12, 1),
                            "disposition": DispositionCreator.create(date=date_class(1956, 2, 1), ruling="Convicted"),
                        },
                    ),
                ),
            )
        ],
        # Source: https://www.beatlesbible.com/1968/10/18/john-lennon-and-yoko-ono-are-arrested-for-drugs-possession/
        Alias("john", "lennon", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "John Lennon",
                        "birth_year": 1913,
                        "case_number": "420-420",
                        "location": "London",
                        "date": date_class(1968, 10, 18),
                        "balance_due_in_cents": 5000,
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "1",
                            "name": "Obstruction of search warrant",
                            "statute": "162.247",
                            "level": "Misdemeanor Class A",
                            "date": date_class(1955, 12, 1),
                            "disposition": DispositionCreator.create(date=date_class(1968, 12, 1), ruling="Convicted"),
                        },
                    ),
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "2",
                            "name": "Poss Controlled Sub",
                            "statute": "475.9924A",
                            "level": "Felony Unclassified",
                            "date": date_class(1955, 12, 1),
                            "disposition": DispositionCreator.create(date=date_class(1968, 12, 1), ruling="Convicted"),
                        },
                    ),
                ),
            ),
        ],
        Alias("george", "bush", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "George Walker Bush",
                        "birth_year": 1946,
                        "case_number": "43",
                        "location": "Cumberland County (Maine)",
                        "date": date_class(1976, 9, 4),
                        "violation_type": "Offense Misdemeanor",
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "1",
                            "name": "DUII",
                            "statute": "813010",
                            "date": date_class(1976, 9, 4),
                            "disposition": DispositionCreator.create(date=date_class(1976, 9, 5), ruling="Convicted"),
                        },
                    ),
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "2",
                            "name": "DUII",
                            "statute": "813010",
                            "level": "Misdemeanor Class A",
                            "date": date_class(1976, 9, 4),
                            "disposition": DispositionCreator.create(date=date_class(1976, 9, 5), ruling="Dismissed"),
                        },
                    ),
                ),
            ),
        ],
        Alias("example", "1", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "Peter Protest",
                        "case_number": "001",
                        "date": date_class.today() - relativedelta(years=8),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "001-1",
                            "date": date_class.today() - relativedelta(years=8),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=8, months=4, days=15), ruling="Convicted"
                            ),
                            "name": "Riot",
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "Peter Protest",
                        "case_number": "002",
                        "date": date_class.today() - relativedelta(years=15),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "002-1",
                            "date": date_class.today() - relativedelta(years=15),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=14, months=4, days=15), ruling="Convicted"
                            ),
                            "name": "Unlawful Assembly",
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "Peter Protest",
                        "case_number": "003",
                        "date": date_class.today() - relativedelta(years=1),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "003-1",
                            "date": date_class.today() - relativedelta(years=1),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(months=4, days=15), ruling="Dismissed"
                            ),
                            "name": "Interfering with a peace officer",
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "Peter Protest",
                        "case_number": "004",
                        "date": date_class.today() - relativedelta(years=2),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "004-1",
                            "date": date_class.today() - relativedelta(years=2),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=1, months=4, days=15), ruling="Dismissed"
                            ),
                        },
                    ),
                ),
            ),
        ],
        Alias("example", "2", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "Firstname Lastname",
                        "case_number": "001",
                        "date": date_class.today() - relativedelta(years=16),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "001-1",
                            "statute": "813010",
                            "date": date_class.today() - relativedelta(years=15, months=3),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=15, months=3), ruling="Dismissed"
                            ),
                            "name": "Driving while Intoxicated",
                        },
                    ),
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "001-2",
                            "statute": "813010",
                            "date": date_class.today() - relativedelta(years=15, months=3),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=15, months=3), ruling="Convicted"
                            ),
                            "name": "Driving while Intoxicated",
                        },
                    ),
                ),
            ),
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "Firstname Lastname",
                        "case_number": "002",
                        "date": date_class.today() - relativedelta(years=15),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "002-1",
                            "name": "Manufacture/Delivery Controlled Substance",
                            "statute": "",
                            "level": "Felony Unclassified",
                            "date": date_class.today() - relativedelta(years=14, months=3),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=14, months=3), ruling="Convicted"
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
                        "name": "Firstname Lastname",
                        "case_number": "003",
                        "date": date_class.today() - relativedelta(years=14),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "003-1",
                            "name": "Criminal mistreatment in the second degree)",
                            "statute": "163205",
                            "date": date_class.today() - relativedelta(years=13, months=3),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=13, months=3), ruling="Convicted"
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
                        "name": "Firstname Lastname",
                        "case_number": "004",
                        "date": date_class.today() - relativedelta(years=13),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "004-1",
                            "name": "Criminal mistreatment in the first degree)",
                            "statute": "163200",
                            "date": date_class.today() - relativedelta(years=12, months=3),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=12, months=3), ruling="Convicted"
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
                        "name": "Firstname Lastname",
                        "case_number": "005",
                        "date": date_class.today() - relativedelta(years=12),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "005-1",
                            "name": "(Endangering the welfare of a minor) (1)(a)",
                            "statute": "163575",
                            "date": date_class.today() - relativedelta(years=11,),
                            "disposition": DispositionCreator.create(
                                date=date_class.today() - relativedelta(years=11, months=3), ruling="Convicted"
                            ),
                        },
                    ),
                ),
            ),
        ],
        Alias("example", "3", "", ""): [
            OeciCase(
                summary=from_dict(
                    data_class=CaseSummary,
                    data={
                        **shared_case_data,
                        "name": "Firstname Lastname",
                        "case_number": "001",
                        "date": date_class.today() - relativedelta(years=1),
                    },
                ),
                charges=(
                    from_dict(
                        data_class=OeciCharge,
                        data={
                            **shared_charge_data,
                            "ambiguous_charge_id": "001-1",
                            "statute": "813010",
                            "date": date_class.today() - relativedelta(years=1),
                            "disposition": DispositionCreator.empty(),
                            "name": "Driving while Intoxicated",
                        },
                    ),
                ),
            )
        ],
    }
