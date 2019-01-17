#!/usr/bin/env python3

import collections
import enum

# TODO we may need to change this to Enum since only a few valid values are allowed.
class CrimeLevel(object):
    """ Crime Level.

    Describes crime level. e.g. Felony Class A.

    Attributes:
        type_: A string describing the type of crime.
        class_: A string of length 1 specifying the class.
    """
    def __init__(self, type_, class_=None):
        self.type_ = type_
        self.class_ = class_

    def __str__(self):
        if class_:
            return '{} Class {}'.format(self.type_, self.class_)
        else:
            return self.type_

DispositionType = enum.Enum('DispositionType',
                            ' '.join([
                                'CONVICTED',
                                'PROBATION_REVOKED',
                                'DISMISSED',
                                'ACQUITTED',
                                'NO_COMPLAINT'
                                ]))

class Disposition(object):
    """ Disposition for a charge.

    Attributes:
        type_: An enum of type DispositionType.
        date: A datetime.date specifying the date of the disposition.
    """
    def __init__(self, type_, date):
        self.type_ = type_
        self.date = date

class Statute(object):
    """ Statute corresponding to a law

    Statutes are represented by numbers in hierarchical manner:
    chapter.subchapter(section)(subsection) e.g. 653.412(5)(c)

    Attributes:
        chapter: An integer that specifies statute chapter.
        subchapter: An integer that specifies statute sub-chapter.
        section: An integer that specifies the section within sub-chapter.
        subsection: A string of length 1 that specifies the sub-section within
                    section.
    """
    def __init__(self, chapter, subchapter, section=None, subsection=None):
        self.chapter = chapter
        self.subchapter = subchapter
        self.section = section
        self.subsection = subsection
        # TODO we may need to add components beyond subsection

    def __eq__(self, other):
        return (self.chapter == other.chapter and
                self.subchapter == other.subchapter and
                ((not self.section and not other.section) or
                 self.section == other.section) and
                ((not self.subsection and not other.subsection) or
                 self.subsection == other.subsection))

    def __str__(self):
        # TODO do these need to have leading zeros?
        statute = '{}'.format(self.chapter)
        if self.subchapter:
            statute = '{}.{:03d}'.format(statute, self.subchapter)
        if self.section:
            statute = '{}({})'.format(statute, self.section)
        if self.subsection:
            statute = '{}({})'.format(statute, self.subsection)
        return statute

class Charge(object):
    """ Charge filed on a Client.

    Attributes:
        name: A string describing the charge.
        statute: A Statute object that applies for the charge.
        date: A datetime.date object specifying the date of the charge.
        disposition: A Disposition object for the charge.
    """
    def __init__(
            self,
            name,
            statute,
            level,
            date,
            disposition):
        self.name = name
        self.statute = statute
        self.level = level
        self.date = date
        self.disposition = disposition
        self._result = None

    @property
    def type_elig_result(self):
        return self._result

    @type_elig_result.setter
    def type_elig_result(self, result):
        self._result = result

CaseState = enum.Enum('CaseState', 'OPEN CLOSED')

class Case(object):
    """ Case associated with a Client.

    Attributes:
        charges: A list of Charge(s).
        state: A CaseState enum.
        balance_due: A float that tells how much money is owed to the court.
    """
    def __init__(self, charges, state, balance_due=0.0):
        self.charges = charges
        self.state = state
        self.balance_due = balance_due

    def num_charges(self):
        return len(self.charges)

class Client(object):
    """ Client - An individual who wants to expunge charges from their record.

    Attributes:
        name: A string that specifies client's name.
        dob: A datetime.date that specifies date of birth.
        cases: A list of Case(s).
    """
    def __init__(self, name, dob, cases):
        self.name = name
        self.dob = dob
        self.cases = cases

    def num_charges(self):
        num = 0
        for case in self.cases:
            num += case.num_charges()
        return num

class ResultCode(enum.Enum):
    INELIGIBLE = 'Ineligible'
    ELIGIBLE = 'Eligible'
    FURTHER_ANALYSIS = 'Further analysis needed'
    EXAMINE = 'Examine'
    NO_ACTION = 'Take no action'
    OPEN_CASE = 'Open Case'

"""
A class for storing individual analysis steps

Attributes:
    result: A boolean that's the result of the check
    check: A string that breifly describes the check
    check_desc: A string that elaborates the check (optional)
"""
CheckResult = collections.namedtuple('CheckResult', 'result check check_desc',
                                     defaults=[None])

class Result(object):
    """
    A class for storing analysis results

    Attributes:
        code: A ResultCode instance.
        statute: A Statute instance that's associated with arrived result.
        date: A datetime.date instance that specifies eligibility date.
        analysis: A list of CheckResult instances that describes the analysis done.
    """
    def __init__(self, code=None, analysis=None,
                 statute=None, date=None):
        self.code = code
        self.analysis = analysis
        self.statute = statute
        self.date = date

    def __str__(self):
        return ' '.join([str(self.code), str(self.analysis), str(self.statute), str(self.date)])

class ResultInElig_137_225_5(Result):
    def __init__(self, **kwargs):
        Result.__init__(self, code=ResultCode.INELIGIBLE,
                        statute=Statute(137, 225, 5), **kwargs)

class RecordAnalyzer(object):
    """
    A class for analyzing client's records

    Attributes:
        client: A Client instance
    """

    def __init__(self, client):
        self.client = client

    def _is_charge_level(charge, type_, class_):
        check = 'Is the charge a {}'.format(type_)
        if class_:
            check += ' class {}'.format(class_)

        result = (charge.level.type_ ==  type_ and
                  (not class_ or charge.level.class_ == class_))
        return CheckResult(check=check, result=result)

    def _is_charge_statute(charge, statute):
        check = 'Does the charge fall under statute: ' + str(statute)
        return CheckResult(check=check, result=charge.statute == statute)

    def _is_charge_in_statute_list(charge, statutes, desc):
        check = ('Does the charge fall under any of these statutes: ' +
                 ','.join(str(statute) for statute in statutes))
        # TODO implement this
        return CheckResult(check=check, result=False, check_desc=desc)

    def _is_charge_sex_crime(charge):
        # TODO update
        _statutes_sex_crimes = []
        return RecordAnalyzer._is_charge_in_statute_list(
            charge, _statutes_sex_crimes, 'Is the charge a sex crime')

    def _is_charge_traffic_crime(charge):
        # TODO update
        _statutes_traffic_crimes = []
        return RecordAnalyzer._is_charge_in_statute_list(
            charge, _statutes_traffic_crimes, 'Is the charge a traffic crime')

    def _have_open_case(self):
        check = 'Is there a open case for the client'
        result = any([case.state == CaseState.OPEN for case in self.client.cases])
        return CheckResult(check=check, result=result)

    """
    Run Time Eligibility analysis on the client and their records

    TODO: make it return analysis for each charge as well (which is supposed
    to be an update on eligibility date and relevan statutes)

    Returns:
        An Result instance
    """
    def time_eligibility(self):
        analysis = []

        analysis.append(self._have_open_case())
        if analysis[-1].result:
            return Result(ResultCode.OPEN_CASE, analysis)

        # TODO implement the rest

        return Result(ResultCode.NO_ACTION)

    """
    Run Type Eligibility analysis on a charge

    Args:
        charge: A Charge instance

    Returns:
        A Result instance
    """
    def type_eligibility(self, charge):
        analysis = []

        analysis.append(RecordAnalyzer._is_charge_level(charge, 'Felony', 'A'))
        if analysis[-1].result:
            return ResultInElig_137_225_5(analysis=analysis)

        analysis.append(RecordAnalyzer._is_charge_sex_crime(charge))
        if analysis[-1].result:
            return ResultInElig_137_225_5(analysis=analysis)

        analysis.append(RecordAnalyzer._is_charge_traffic_crime(charge))
        if analysis[-1].result:
            return ResultInElig_137_225_5(analysis=analysis)

        # TODO add remaining analysis

        return Result(ResultCode.FURTHER_ANALYSIS, analysis)

    """
    Analyze which records are expungeable

    The method sets the Charge instance's result attribute with type eligibility
    analysis result.

    Returns:
        A tuple consisting of:
            - A Result instance that describes the Time Eligibility analysis.
    """
    def analyze(self):
        for case in self.client.cases:
            for charge in case.charges:
                charge.type_elig_result = self.type_eligibility(charge)

        return self.time_eligibility()
