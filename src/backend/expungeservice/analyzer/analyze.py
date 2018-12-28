#!/usr/bin/env python3

#note:  Sex crimes are defined as https://www.oregon.gov/osp/sor/pages/or_reg_sex_crimes.aspx


import collections
import enum

from expungeservice.analyzer.ineligible_crimes_list import IneligibleCrimesList


# todo: write unit tests for this


def is_crime_on_ineligible_list(statute):
    """
    Searches through list of discreet values and ranges
    to determine if a given statute is on the list of ineligible crimes

    Args:
        statute  <---- a given statute number code

    Returns:
        True Or False

    """

    statute = float(statute)

    for item in IneligibleCrimesList:
        if type(item) == list:
            if statute >= float(item[0]) and statute <= float(item[1]):
                return True
        else:
            if item == statute:
                return True

    return False




