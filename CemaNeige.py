"""
------------------------------------------------------------------------------
    Subroutines relative to the annual GR4J model
------------------------------------------------------------------------------
------------------------------------------------------------------------------
 AUTHORS
 Original fortran code: A. Valéry, P. Riboust
 Cleaning and formatting for airGR: Coron, L.
 Further cleaning: Thirel, G.
 Translation in Python: Gaborit, F.
------------------------------------------------------------------------------
 Creation date: 2011
 Last modified: 09/02/2021
------------------------------------------------------------------------------
 REFERENCES
 Riboust, P., Thirel, G., Le Moine, N. and Ribstein, P. (2019). Revisiting a
 simple degree-day model for integrating satellite data: Implementation of
 SWE-SCA hystereses. Journal of Hydrology and Hydromechanics, 67(1), 70–81,
 doi: 10.2478/johh-2018-0004.

 Valéry, A., Andréassian, V. and Perrin, C. (2014). "As simple as possible but
 not simpler": What is useful in a temperature-based snow-accounting routine?
 Part 1 - Comparison of six snow accounting routines on 380 catchments.
 Journal of Hydrology, 517(0), 1166-1175, doi: 10.1016/j.jhydrol.2014.04.059.

 Valéry, A., Andréassian, V. and Perrin, C. (2014). "As simple as possible but
 not simpler": What is useful in a temperature-based snow-accounting routine?
 Part 2 - Sensitivity analysis of the Cemaneige snow accounting routine on
 380 catchments. Journal of Hydrology, 517(0), 1176-1187,
 doi: 10.1016/j.jhydrol.2014.04.058.
"""

# ------------------------------------------------------------------------------
# Quick description of public procedures:
# ------------------------------------------------------------------------------

"""Subroutine that runs the CemaNeige model at each time step, and stores the final states"""

"""retour data alti valery :
{'LayerPrecip': LayerPrecip, 'LayerTempMean': LayerTempMean, 'LayerTempMin': LayerTempMin,
        'LayerTempMax': LayerTempMax, 'LayerFracSolidPrecip': LayerFracSolidPrecip, 'ZLayers': ZLayers}


ParamCemaNeige = Param[(len(Param) - 1 - 2 * int(IsHyst)):len(Param)]
NParamMod = int(len(Param) - (2 + 2 * int(IsHyst)))
ParamMod = Param[1:NParamMod]
NLayers = len(inputsModel.LayerPrecip)
NStatesMod = int(len(runOptions.IniStates) - NStates * NLayers)
ExportDatesR = "DatesR" in runOptions.Outputs_Sim
ExportStateEnd = "StateEnd" in runOptions.Outputs_Sim
for iLayer in range(NLayers):
    StateStartCemaNeige = [runOptions.IniStates[iLayer + 7 + 20 + 40],
                           runOptions.IniStates[iLayer + NLayers + 7 + 20 + 40],
                           runOptions.IniStates[iLayer + 2 * NLayers + 7 + 20 + 40],
                           runOptions.IniStates[iLayer + 3 * NLayers + 7 + 20 + 40]]

    RESULTS = CemaNeige.cemaneige(LInputs=LInputSeries, InputsPrecip=inputsModel.LayerPrecip[[iLayer]][IndPeriod1],
                                  InputsFracSolidPrecip=inputsModel.LayerFracSolidPrecip[[iLayer]][IndPeriod1],
                                  InputsTemp=inputsModel.LayerTemp[[iLayer]][IndPeriod1],
                                  MeanAnSolidPrecip=runOptions.MeanAnSolidPrecip[iLayer],
                                  Param=ParamCemaNeige,
                                  StateStart=StateStartCemaNeige,
                                  isHyst=False)
    RESULTS_Outputs = RESULTS[0]
    RESULTS_StateEnd = RESULTS[1]

    ## Data storage
    CemaNeigeLayers[iLayer] = [RESULTS_Outputs[IndPeriod2, i] for i in range(
        len(RESULTS_Outputs))]  # lapply(seq_len(RESULTS.NOutputs), function(i) RESULTS.Outputs[IndPeriod2, i])
    CemaNeigeLayers[iLayer].insert(0, fortranOutputs_CN[
        IndOutputsCemaNeige])  # todo : supprimer ? on ajoute le nom en tete de liste"""


def cemaneige(LInputs: int, InputsPrecip: list, InputsFracSolidPrecip: list, InputsTemp: list,
              MeanAnSolidPrecip: float, Param: list, StateStart: list, isHyst: bool = False):

    """
    Parameters
    ----------
    LInputs      : Integer, length of input and output series
    InputsPrecip : Vector of real, input series of total precipitation [mm/time step]
    InputsFracSolidPrecip : Vector of real, input series of fraction of solid precipitation [0-1]
    InputsTemp   : Vector of real, input series of air mean temperature [degC]
    MeanAnSolidPrecip     : Real, value of annual mean solid precip [mm/y]
    Param        : Vector of real, Parameter set
    StateStart   : Vector of real, state variables used when the model run starts (store levels [mm] and [-] and thresholds [mm])
    isHyst       : boolean, whether we should use the linear hysteresis [True] or not [False]
    nOutputs     : Integer, number of output series, deleted for Python Version

    Returns
    -------
    outputs      : Vector of real, output series
    stateEnd     : Vector of real, state variables at the end of the model run (store levels [mm] and [-] and thresholds [mm])


    """

    # --------------------------------------------------------------
    # Initializations
    # --------------------------------------------------------------
    # initialization of constants
    Tmelt = 0.
    MinSpeed = 0.1

    # initialization of model states using StateStart
    G: float = StateStart[0]
    eTG: float = StateStart[1]
    Gratio = 0.
    PliqAndMelt: float = 0.

    # setting Parameter values
    CTG: float = Param[0]
    Kf: float = Param[1]
    if isHyst:
        Gthreshold: float = StateStart[2]
        Glocalmax: float = StateStart[3]
        Gacc: float = Param[2]
        prct: float = Param[3]

        if Gthreshold == 0.:
            Gthreshold = prct * MeanAnSolidPrecip
        if Glocalmax == 0.:
            Glocalmax = Gthreshold

    else:
        Gthreshold = 0.9 * MeanAnSolidPrecip
        Glocalmax = -999.999
        Gacc = -999.999
        prct = -999.999

    Outputs = []  # creating an empty list for outputs
    # --------------------------------------------------------------
    # Time loop
    # --------------------------------------------------------------
    for k in range(LInputs):

        # SolidPrecip and LiquidPrecip
        Pliq: float= (1 - InputsFracSolidPrecip[k]) * InputsPrecip[k]
        Psol: float = InputsFracSolidPrecip[k] * InputsPrecip[k]

        # Accumulation

        # Snow pack volume before melt
        Ginit: float = G
        G = G + Psol

        # Snow pack thermal state before melt
        eTG = CTG * eTG + (1 - CTG) * InputsTemp[k]
        if eTG > 0:
            eTG = 0

        # Calcul de la fonte potentielle
        # Potential melt
        if eTG == 0 and InputsTemp[k] > Tmelt:
            PotMelt = Kf * (InputsTemp[k] - Tmelt)
            if PotMelt > G:
                PotMelt = G
        else:
            PotMelt = 0

        if isHyst:
            if PotMelt > 0:
                if (G < Glocalmax) and (Gratio == 1):
                    Glocalmax = G  # Update in case of potential melt and G lower than Gseuil
                Gratio = min(G / Glocalmax, 1)
        else:
            if G < Gthreshold:
                Gratio = G / Gthreshold
            else:
                Gratio = 1
        # Actual melt
        Melt: float = ((1. - MinSpeed) * Gratio + MinSpeed) * PotMelt

        # Update of snow pack volume
        G = G - Melt
        if isHyst:
            dG = G - Ginit  # Melt in case of negative dG, accumulation otherwise
            if dG > 0.:
                Gratio = min(Gratio + (Psol - Melt) / Gacc, 1)  # Psol - Melt = dG
                if Gratio == 1.:
                    Glocalmax = Gthreshold
            else:
                Gratio = min(G / Glocalmax, 1)
        else:
            if G < Gthreshold:
                Gratio = G / Gthreshold
            else:
                Gratio = 1.

        # Water volume to pass to the hydrological model
        PliqAndMelt = Pliq + Melt

        # Storage of outputs
        Outputs.append(
            [Pliq, Psol, G, eTG, Gratio, PotMelt, Melt, PliqAndMelt, InputsTemp[k], Gthreshold, Glocalmax])
        # Pliq         # observed liquid precipitation [mm/time step]
        # Psol         # observed solid precipitation [mm/time step]
        # SnowPack     # snow pack [mm]
        # ThermalState # thermal state [°C]
        # Gratio       # Gratio [-]
        # PotMelt      # potential snow melt [mm/time step]
        # Melt         # melt [mm/time step]
        # PliqAndMelt  # liquid precipitation + melt [mm/time step]
        # Temp         # air temperature [°C]
        # Gthreshold   # melt threshold [mm]
        # Glocalmax    # local melt threshold for hysteresis [mm]

    StateEnd = [G, eTG, Gthreshold, Glocalmax]

    return [Outputs, StateEnd]
