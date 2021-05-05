"""
------------------------------------------------------------------------------
    Subroutines relative to the annual GR4J model
------------------------------------------------------------------------------
 TITLE   : airGR
 PROJECT : airGR
 FILE    : GR4J.py
------------------------------------------------------------------------------
 AUTHORS
 Original code: Perrin, C.
 Cleaning and formatting for airGR: Coron, L.
 Further cleaning: Thirel, G.
  Translation in python: Gaborit, F.
------------------------------------------------------------------------------
 Creation date: 2000
 Last modified: 09/02/2021
------------------------------------------------------------------------------
 REFERENCES
 Perrin, C., Michel, C. and Andréassian, V. (2003). Improvement of a
 parsimonious model for streamflow simulation. Journal of Hydrology,
 279(1-4), 275-289, doi: 10.1016/S0022-1694(03)00225-7.
------------------------------------------------------------------------------
 Quick description of public procedures:
         1. gr4j Subroutine that initializes GR4J, get its parameters, performs the call
 to the MOD_GR4J subroutine at each time step, and stores the final states
         2. MOD_GR4J Calculation of streamflow on a single time step (day) with the GR4J model
------------------------------------------------------------------------------
"""

from util_D import UH1, UH2
import math as math

"""Subroutine that initializes GR4J, get its parameters, performs the call
to the MOD_GR4J subroutine at each time step, and stores the final states"""


def gr4j(LInputs: int, InputsPrecip: list, InputsPE: list, Param: list, StateStart: list):
    """
    Parameters
    ----------
    LInputs      : Integer, length of input and output series
    InputsPrecip : Vector of real, input series of total precipitation [mm/day]
    InputsPE     : Vector of real, input series of potential evapotranspiration (PE) [mm/day]
    Param        : Vector of real, parameter set
    StateStart   : Vector of real, state variables used when the model run starts (store levels [mm] and Unit Hydrograph (UH) storages [mm])

    Returns
    -------
    Outputs      : Vector of real, output series
    StateEnd     : Vector of real, state variables at the end of the model run (store levels [mm] and Unit Hydrograph (UH) storages [mm])
    """
    ## --------------------------------------------------------------
    ##region Initializations
    ## --------------------------------------------------------------

    NH = 20
    St = [None] * 2
    StUH1 = [None] * NH
    StUH2 = [None] * (2 * NH)

    St[0] = StateStart[0]
    St[1] = StateStart[1]
    for i in range(NH):
        StUH1[i] = StateStart[7 + i]
    for i in range(2 * NH):
        StUH2[i] = StateStart[7 + i + NH]

    # parameter values
    # Param(1) : production store capacity (X1 - PROD) [mm]
    # Param(2) : intercatchment exchange coefficient (X2 - CES) [mm/day]
    # Param(3) : routing store capacity (X3 - ROUT) [mm]
    # Param(4) : time constant of unit hydrograph (X4 - TB) [day]

    # Computation of UH ordinates
    OrdUH1 = [0.]*NH
    OrdUH2 = [0.]*(2*NH)

    d = 2.5
    OrdUH1 = UH1(OrdUH1, Param[3], d)
    OrdUH2 = UH2(OrdUH2, Param[3], d)

    # # Initialization of model outputs
    #     Q = -999.999
    #     MISC = -999.999
    #     StateEnd = -999.999 !initialization
    #     made in R
    #     Outputs = -999.999  !initialization
    #     made in R

    ##endregion --------------------------------------------------------------
    ##region Time loop
    # --------------------------------------------------------------
    Outputs = []
    QOutputs = []
    for k in range(LInputs):
        P1 = InputsPrecip[k]
        E = InputsPE[k]

        # model run on one time step
        St, StUH1, StUH2, Q, MISC = MOD_GR4J(St, StUH1, StUH2, OrdUH1, OrdUH2, Param, P1, E)
        # storage of outputs
        Outputs.append(MISC)
        QOutputs.append(Q)
    # model states at the end of the run
    StateEnd = [None] * (3 * NH + 7)
    StateEnd[0] = St[0]
    StateEnd[1] = St[1]
    for k in range(NH):
        StateEnd[7 + k] = StUH1[k]
    for k in range(2 * NH):
        StateEnd[7 + NH + k] = StUH2[k]

    return [QOutputs, Outputs, StateEnd]


##########################################################################
"""Calculation of streamflow on a single time step (day) with the GR4J model"""
def MOD_GR4J(St: list, StUH1: list, StUH2: list, OrdUH1: list, OrdUH2,
             Param: list, P1: float, E: float):
    """

    Parameters
    ----------
    St     : list of float, model states in stores at the beginning of the time step [mm]
    StUH1  : list of float, model states in Unit Hydrograph 1 at the beginning of the time step [mm]
    StUH2  : list of float, model states in Unit Hydrograph 2 at the beginning of the time step [mm]
    OrdUH1 : list of float, ordinates in UH1 [-]
    OrdUH2 : list of float, ordinates in UH2 [-]
    Param  : list of float, model parameters [various units]
    P1     : float, value of rainfall during the time step [mm/day]
    E      : float, value of potential evapotranspiration during the time step [mm/day]

    Returns
    -------
    St     : list of float, model states in stores at the end of the time step [mm]
    StUH1  : list of float, model states in Unit Hydrograph 1 at the end of the time step [mm]
    StUH2  : list of float, model states in Unit Hydrograph 2 at the end of the time step [mm]
    Q      : float, value of simulated flow at the catchment outlet for the time step [mm/day]
    MISC   : list of float, model outputs for the time step [mm/day]

    """
    # nParam=4
    # nMISC=30
    NH: int = 20
    B: float = 0.9
    stored_val: float = (9 / 4) ** 4
    A = Param[0]

    # Interception and production store
    if P1 <= E:
        EN = E - P1
        PN = 0.
        WS = EN / A
        if WS >= 13.:
            WS = 13.
        # speed-up
        expWS = math.exp(2. * WS)
        TWS = (expWS - 1.) / (expWS + 1.)
        Sr = St[0] / A
        ER = St[0] * (2. - Sr) * TWS / (1. + (1. - Sr) * TWS)
        # ER=X(2)*(2.-X(2)/A)*tanHyp(WS)/(1.+(1.-X(2)/A)*tanHyp(WS))
        #    end speed-up TODO : tout repasser en speedup après débuggage
        AE = ER + P1
        St[0] = St[0] - ER
        PS = 0.
        PR = 0.
    else:
        EN = 0.
        AE = E
        PN = P1 - E
        WS = PN / A
        if WS > 13:
            WS = 13.
        # speed-up
        expWS = math.exp(2. * WS)
        TWS = (expWS - 1.) / (expWS + 1.)
        Sr = St[0] / A
        PS = A * (1. - Sr * Sr) * TWS / (1. + Sr * TWS)
        # PS=A*(1.-(X(2)/A)**2.)*tanHyp(WS)/(1.+X(2)/A*tanHyp(WS))
        # end speed-up
        PR = PN - PS
        St[0] = St[0] + PS

    # Percolation from production store
    if St[0] <= 0:
        St[0] = 0.

    # speed-up
    Sr = (St[0] / Param[0]) ** 4
    PERC = St[0] * (1 - 1 / math.sqrt(math.sqrt(1. + Sr / stored_val)))
    # PERC=X(2)*(1.-(1.+(X(2)/(9./4.*Param(1)))**4.)**(-0.25))
    #  end speed-up
    St[0] = St[0] - PERC

    PR = PR + PERC

    # Split of effective rainfall into the two routing components
    PRHU1: float = PR * B
    PRHU2: float = PR * (1. - B)

    # Convolution of unit hydrograph UH1
    for k in range(max(1, min(NH - 1, int(Param[3] + 1.)))):
        StUH1[k] = StUH1[k + 1] + OrdUH1[k] * PRHU1
    StUH1[NH-1] = OrdUH1[NH-1] * PRHU1

    # Convolution of unit hydrograph UH2
    for k in range(max(1, min(2 * NH - 1, 2 * int(Param[3] + 1.)))):
        StUH2[k] = StUH2[k + 1] + OrdUH2[k] * PRHU2

    StUH2[2 * NH-1] = OrdUH2[2 * NH-1] * PRHU2

    # Potential intercatchment semi-exchange
    # speed-up
    Rr = St[1] / Param[2]
    EXCH = Param[1] * Rr **3.5
    # EXCH=Param(2)*(X(1)/Param(3))**3.5
    #  end speed-up

    # Routing store
    AEXCH1 = EXCH
    if (St[1] + StUH1[1] + EXCH) < 0.:
        AEXCH1 = -St[1] - StUH1[1]
    St[1] = St[1] + StUH1[1] + EXCH
    if St[1] < 0.:
        St[1] = 0.
    # speed-up
    Rr = St[1] / Param[2]
    Rr = Rr * Rr
    Rr = Rr * Rr
    QR = St[1] * (1. - 1. / math.sqrt(math.sqrt(1. + Rr)))
    # QR=X(1)*(1.-(1.+(X(1)/Param(3))**4.)**(-1./4.))
    #  end speed-up
    St[1] = St[1] - QR

    # Runoff from direct branch QD
    AEXCH2 = EXCH
    if (StUH2[1] + EXCH) < 0.:
        AEXCH2 = -StUH2[1]
    QD = max(0, StUH2[1] + EXCH)

    # Total runoff
    Q = QR + QD
    if Q <= 0.:
        Q = 0.

    # Variables storage
    MISC = [E, P1, St[0], PN, PS, AE, PERC, PR, StUH1[1], StUH2[1], St[1], EXCH, AEXCH1, AEXCH2, AEXCH1 + AEXCH2, QR,
            QD, Q]

    return St, StUH1, StUH2, Q, MISC
