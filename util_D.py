"""------------------------------------------------------------------------------
Subroutines relative to the daily unit hydrographs and hyperbolic tangent calculation
------------------------------------------------------------------------------
TITLE: airGR
PROJECT: airGR
FILE: utils_D.f
------------------------------------------------------------------------------
AUTHORS
Original code: Unknown soldier
Cleaning and formatting for airGR: Coron, L.
Further cleaning: Thirel, G.
Translation in python: Gaborit, F.
------------------------------------------------------------------------------
Creation date: 2000
Last modified: 0
9 / 02 / 2021
------------------------------------------------------------------------------
REFERENCES

------------------------------------------------------------------------------
Quick description of public procedures:
1. UH1 Subroutine that computes the ordinates of the daily GR unit hydrograph UH1 using successive differences on
the S curve SS1
2. UH2 Subroutine that computes the ordinates of the daily GR unit hydrograph UH2 using successive
differences on the S curve SS2
3. SS1 Function that computes the values of the S curve(cumulative UH curve) of GR unit hydrograph UH1
4. SS2 Function that computes the values of the S curve(cumulative UH curve) of GR unit hydrograph UH2
------------------------------------------------------------------------------
"""

""" Subroutine that computes the ordinates of the daily GR unit hydrograph UH1 using successive differences on
the S curve SS1 """

def UH1(OrdUH1, c, d):
    """

    Parameters
    ----------
    OrdUH1
    c float, time constant
    d float, exponent

    Returns
    -------
    OrdUH1 : List of float, NH ordinates of the discrete hydrograph

    """
    NH = 20
    for i in range(NH):
        OrdUH1[i] = SS1(i, c, d) - SS1(i - 1, c, d)
    return OrdUH1

"""Subroutine that computes the ordinates of the daily GR unit hydrograph UH2 using successive
differences on the S curve SS2"""
def UH2(OrdUH2, c, d):
    """

    Parameters
    ----------
    OrdUH2
    c float, time constant
    d float, exponent

    Returns
    -------
    OrdUH2: List of float, 2 * NH ordinates of the discrete hydrograph
    """
    NH = 20
    for i in range(2*NH):
        OrdUH2[i] = SS2(i, c, d) - SS2(i-1, c, d)
    return OrdUH2

"""Function that computes the values of the S curve(cumulative UH curve) of GR unit hydrograph UH1"""
def SS1(i, c, d):
    """

    Parameters
    ----------
    i integer, time - step
    c float, time constant
    d float, exponent

    Returns
    -------
    SS1 : float, value of the S curve for i

    """
    if i <= 0 :
        SS1 = 0.
        return SS1
    elif i < c :
        SS1 = (i / c) ** d
        return SS1
    SS1 = 1.
    return SS1

"""Function that computes the values of the S curve(cumulative UH curve) of GR unit hydrograph UH2"""
def SS2(i, c, d):
    """

    Parameters
    ----------
    i integer, time - step
    c float, time constant
    d float, exponent

    Returns
    -------
    SS2 float, value of the S curve for I
    """
    if i <= 0 :
        SS2=0
        return SS2
    elif i<=c :
        SS2 = 0.5 * (i / c) ** d
        return SS2
    if i < (2*c):
        SS2 = 1. - 0.5 * (2. - i / c) ** d
        return SS2
    SS2 = 1.
    return SS2
