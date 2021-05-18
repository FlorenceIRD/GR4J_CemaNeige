import matplotlib.pyplot as plt
import csv
import pandas as pd
import GR4J
import numpy as np
import scipy.optimize
import ErreurCrit
import math as math
import DataAltiExtrapolation_Valery
import CemaNeige
import datetime as dt


##region Importation des données

# data = data[data.Qmm.apply(lambda x: x.isnumeric())]
HypsoData = pd.read_csv('HypsoDataBV_1.csv', header=0)
HypsoData = HypsoData['alti'].values.astype(float).tolist()
decoupe_BV = pd.read_csv('suface_zones_bv1.csv', header=0)
zones = decoupe_BV['fichier'].tolist()
surfaces=  decoupe_BV['area'].tolist()



# data = data.loc[:, ['DatesR', 'P', 'T', 'E', 'Qls', 'Qmm']]
data = pd.DataFrame({'P' : [0.] * 13572 ,
                     'T' : [0.] * 13572,
                     'E' :[0.] * 13572,
                     'day' :[0.] * 13572})

index = 0
if index ==0 :
# for index in range(len(zones)):
    z = zones[index]
    j,  i= int(z.split(sep="_")[0]), int(z.split(sep="_")[1])
    surface_zone = surfaces[index]
    # pluie = pd.read_csv('zone_' + str(i) + '_' + str(j) + '.csv', sep = ';')['P'][1:].values.astype(float)
    data['P'] = data['P'] + pd.read_csv('zone_' + str(i) + '_' + str(j) + '.csv', sep = ';')['P'][1:].values.astype(float)
    data['T'] = pd.read_csv('zone_' + str(i) + '_' + str(j) + '.csv', sep = ';')['T'][1:].values.astype(float)
    data['E'] = pd.read_csv('zone_' + str(i) + '_' + str(j) + '.csv', sep = ';')['E'][1:].values.astype(float)
    data['day'] = pd.read_csv('zone_' + str(i) + '_' + str(j) + '.csv', sep=';')['day'][1:].values.astype(float)

    data_dates_debits = pd.read_csv('Debits_BV1.csv', header=0, sep='\t')

# Precip = data['P'].values.astype(float)
# PotEvap = data['E'].values.astype(float)
# TempMean = data['T'].values.astype(float)
# QObs = data_dates_debits['Debit'].values.astype(float)
#
# Days_ERA5 = data['day']

Dates_ERA5 = pd.Series(dt.timedelta(date) + dt.date(1900, 1, 1) for date in data['day'])
# indices = 0

DatesR = data_dates_debits['Date']
DatesR = DatesR.tolist()
debut = DatesR.index("01/01/1990")
fin = DatesR.index("31/12/1992")
debutCemaneige = debut-365
Ind_Run = range(debut, fin)
# IndPeriodCemaneige = range(debutCemaneige, debut)
IndPeriodCemaneige = Ind_Run
LInputSeries = len(IndPeriodCemaneige)

data_num = pd.DataFrame({
    'DatesR' : Dates_ERA5,
    'P' : data['P'],
    'E' : data['E'],
    'T' : data['T'],
    'Qmm' : data_dates_debits['Debit'].values.astype(float) })
data_num = data_num.dropna()

DatesR= data_num['DatesR'].tolist()
Precip = data_num['P'].tolist()
PotEvap = data_num['E'].tolist()
TempMean = data_num['T'].tolist()
QObs = data_num['Qmm'].tolist()

plt.plot(DatesR, TempMean)



##endregion

##region Choix du critère
FUN_CRIT = "NSE_RAC_DEBITS"
# FUN_CRIT = "NSE"

##endregion
##region Initialisation_parametres
InputsPrecip = [Precip[i] for i in Ind_Run]
InputsPE = [PotEvap[i] for i in Ind_Run]
VarObs = [QObs[i] for i in Ind_Run]
Param = [257.237556, 1.012237, 88.234673,   2.207958,  0.962,  2.249]

DatesR_CemaNeige = [DatesR[i] for i in IndPeriodCemaneige]
InputsPrecip_CemaNeige= [Precip[i] for i in IndPeriodCemaneige]
TempMean_CemaNeige = [TempMean[i] for i in IndPeriodCemaneige]


RESULTS_ALTI = DataAltiExtrapolation_Valery.DataAltiExtrapolation_Valery(DatesR=DatesR_CemaNeige,
                                                                         Precip=InputsPrecip_CemaNeige,
                                                                         TempMean=TempMean_CemaNeige,
                                                                         TempMin=None,
                                                                         TempMax=None,
                                                                         ZInputs=HypsoData[50],
                                                                         HypsoData=HypsoData,
                                                                         NLayers=5,
                                                                         verbose=False)


NLayers = len(RESULTS_ALTI['LayerPrecip'])

##endregion


##endregion


##region Simulation


GCemaNeigeLayers = 100
eTGCemaNeigeLayers = 100
StateStart = [0.] * 67
StateStartGR4J = GR4J.gr4j(len(InputsPrecip), InputsPrecip, InputsPE, Param, StateStart)[2]
StateStartCemaNeige = [GCemaNeigeLayers, eTGCemaNeigeLayers]

def Simulation_GR4J_CemaNeige(X):
    Dates_choisies = [DatesR[i] for i in Ind_Run]
    InputsPrecip = [Precip[i] for i in Ind_Run]
    InputsPE = [PotEvap[i] for i in Ind_Run]
    VarObs = [QObs[i] for i in Ind_Run]
    Param = list(X)

    ParamGR = Param[:4]
    ParamCemaNeige = Param[4:]

    ##region CemaNeige

    LayerFracSolidPrecip = RESULTS_ALTI['LayerFracSolidPrecip']
    LayerPrecip = [Precip[i] for i in IndPeriodCemaneige]
    SolidPrecip = [[LayerFracSolidPrecip[iLayer][i] * LayerPrecip[i] / NLayers for i in range(len(LayerPrecip))] for
                   iLayer in range(NLayers)]
    Factor = 365.25
    MoySolid = 0
    for layer in SolidPrecip:
        for x in layer:
            MoySolid += x
    MeanAnSolidPrecip = [MoySolid * Factor] * NLayers
    CemaNeigeLayers = []
    CatchMeltAndPliqLayer = []
    for iLayer in range(NLayers):
        RESULTS = CemaNeige.cemaneige(LInputs=LInputSeries, InputsPrecip=LayerPrecip,
                                      InputsFracSolidPrecip=LayerFracSolidPrecip[iLayer],
                                      InputsTemp=RESULTS_ALTI['LayerTempMean'][iLayer],
                                      MeanAnSolidPrecip=MeanAnSolidPrecip[iLayer],
                                      Param=ParamCemaNeige,
                                      StateStart=StateStartCemaNeige,
                                      isHyst=False)
        RESULTS_Outputs = RESULTS[0]
        RESULTS_StateEnd = RESULTS[1]

        ## Data storage
        CemaNeigeLayers.append(RESULTS_Outputs)
        CatchMeltAndPliqLayer.append([RESULTS_Outputs[i][7] for i in range(len(RESULTS_Outputs))])

    CatchMeltAndPliq = [sum([CatchMeltAndPliqLayer[iLayer][i] for iLayer in range(NLayers)]) for i in
                        range(len(CatchMeltAndPliqLayer[0]))]

    Outputs = GR4J.gr4j(LInputs=len(InputsPrecip),
                             InputsPrecip=CatchMeltAndPliq,
                             InputsPE=InputsPE,
                             Param=ParamGR,
                             StateStart=StateStartGR4J)
    Output_Q = Outputs[0]
    plt.plot(Dates_choisies, Output_Q, Dates_choisies, VarObs)
    plt.show()
##endregion

##region Calibration
def Minimisation_GR4J_CemaNeige(X):
    InputsPrecip = [Precip[i] for i in Ind_Run]
    InputsPE = [PotEvap[i] for i in Ind_Run]
    VarObs = [QObs[i] for i in Ind_Run]
    Param = list(X)

    ParamGR = Param[:4]
    ParamCemaNeige = Param[4:]

    ##region CemaNeige

    LayerFracSolidPrecip = RESULTS_ALTI['LayerFracSolidPrecip']
    LayerPrecip = [Precip[i] for i in IndPeriodCemaneige]
    SolidPrecip = [[LayerFracSolidPrecip[iLayer][i] * LayerPrecip[i] / NLayers for i in range(len(LayerPrecip))] for
                   iLayer in range(NLayers)]
    Factor = 365.25
    MoySolid = 0
    for layer in SolidPrecip:
        for x in layer:
            MoySolid += x
    MeanAnSolidPrecip = [MoySolid * Factor] * NLayers
    CemaNeigeLayers = []
    CatchMeltAndPliqLayer = []
    for iLayer in range(NLayers):
        RESULTS = CemaNeige.cemaneige(LInputs=LInputSeries, InputsPrecip=LayerPrecip,
                                      InputsFracSolidPrecip=LayerFracSolidPrecip[iLayer],
                                      InputsTemp=RESULTS_ALTI['LayerTempMean'][iLayer],
                                      MeanAnSolidPrecip=MeanAnSolidPrecip[iLayer],
                                      Param=ParamCemaNeige,
                                      StateStart=StateStartCemaNeige,
                                      isHyst=False)
        RESULTS_Outputs = RESULTS[0]
        RESULTS_StateEnd = RESULTS[1]

        ## Data storage
        CemaNeigeLayers.append(RESULTS_Outputs)
        CatchMeltAndPliqLayer.append([RESULTS_Outputs[i][7] for i in range(len(RESULTS_Outputs))])

    CatchMeltAndPliq = [sum([CatchMeltAndPliqLayer[iLayer][i] for iLayer in range(NLayers)]) for i in
                        range(len(CatchMeltAndPliqLayer[0]))]

    Outputs = GR4J.gr4j(LInputs=len(InputsPrecip),
                        InputsPrecip=CatchMeltAndPliq,
                        InputsPE=InputsPE,
                        Param=ParamGR,
                        StateStart=StateStartGR4J)
    Output_Q = Outputs[0]
    # print(Output_model)
    Crit = ErreurCrit.ErrorCrit(FUN_CRIT, Output_Q, VarObs).OutputsCrit[0]
    return -Crit

# print(Minimisation_GR4J_CemaNeige([257.237556, 1.012237, 88.234673,   2.207958, 0.962,  2.249]))

## contraintes

bounds = scipy.optimize.Bounds([0, -100, 0, 0, 0, 0], [1000, 1000,1000,1000,1000,1000])


x0=np.array([680.28, -2, 110,   2,  0.5,  2]) #valeur de départ

x_calc = scipy.optimize.minimize(Minimisation_GR4J_CemaNeige,
                                 x0,
                                 options={'maxiter' : 150, 'disp' : True},
                                 bounds = bounds )
print(x_calc)
Simulation_GR4J_CemaNeige(x_calc.x)

##endregion

