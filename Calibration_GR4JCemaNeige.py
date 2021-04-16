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

##region Importation des données
data = pd.read_csv ('BasinL0123001.csv', header=0)
# data = data[data.Qmm.apply(lambda x: x.isnumeric())]
HypsoData = [471.0,656.2,749.4,808.0,868.0,908.0,948.0,991.2,1022.6,1052.0,1075.0,1101.0,1120.4,1147.6,1166.8,1185.0,1210.0,1229.0,1242.0,1259.0,1277.0,1291.0,1305.4,1318.0,1328.0,1340.0,1350.2,1366.4
,1377.0,1389.0,1402.0,1413.0,1424.0,1435.0,1448.8,1460.0,1474.2,1487.4,1498.0,1511.0,1523.0,1538.0,1551.4,1564.0,1573.0,1584.0,1593.0,1603.4,1614.0,1626.0,1636.0,1648.0,1661.4,1672.0,1682.0,1693.0
,1705.0,1715.0,1724.0,1733.0,1742.0,1751.0,1759.0,1768.0,1777.0,1787.0,1795.0,1802.0,1813.0,1822.0,1832.0,1840.0,1849.0,1857.6,1867.0,1874.0,1882.2,1891.0,1899.0,1908.8,1919.0,1931.0,1941.0,1948.0
,1957.8,1965.0,1976.0,1987.0,1999.0,2013.0,2027.0,2047.0,2058.0,2078.0,2097.0,2117.0,2146.0,2177.0,2220.6,2263.6,2539.0]
#TODO refaire l'import

data = data.loc[:, ['DatesR', 'P', 'T', 'E', 'Qls', 'Qmm']]
Precip = data['P'].values.astype(float)
PotEvap = data['E'].values.astype(float)
TempMean = data['T'].values.astype(float)
QObs = data['Qmm'].values.astype(float)

data_num = pd.DataFrame({
    'DatesR' : data['DatesR'],
    'P' : Precip,
    'E' : PotEvap,
    'T' : TempMean,
    'Qmm' : QObs })
data_num = data_num.dropna()

DatesR= data_num['DatesR'].tolist()
Precip = data_num['P'].tolist()
PotEvap = data_num['E'].tolist()
TempMean = data_num['T'].tolist()
QObs = data_num['Qmm'].tolist()

debut = DatesR.index("1990-01-01")
fin = DatesR.index("1992-12-31")
debutCemaneige = debut-365

Ind_Run = range(debut, fin)
# IndPeriodCemaneige = range(debutCemaneige, debut)
IndPeriodCemaneige = Ind_Run
LInputSeries = len(IndPeriodCemaneige)

##endregion

##region Choix du critère
FUN_CRIT = "NSE_RAC_DEBITS"
FUN_CRIT = "NSE"

##endregion
##region Initialisation_parametres
InputsPrecip = [Precip[i] for i in Ind_Run]
InputsPE = [PotEvap[i] for i in Ind_Run]
VarObs = [QObs[i] for i in Ind_Run]
Param = [257.237556, 1.012237, 88.234673,   2.207958,  0.962,  2.249]

DatesR_CemaNeige = [DatesR[i] for i in IndPeriodCemaneige]
InputsPrecip_CemaNeige= [Precip[i] for i in IndPeriodCemaneige]
TempMean_CemaNeige = [TempMean[i] for i in IndPeriodCemaneige]

ParamGR=Param[:3]
ParamCemaNeige = Param [4:]

StateStart = [0.] * 67
StateStartGR4J = GR4J.gr4j(len(InputsPrecip), InputsPrecip, InputsPE, Param, StateStart)[2]

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
##region CemaNeige
GCemaNeigeLayers = 100
eTGCemaNeigeLayers =100
StateStartCemaNeige = [GCemaNeigeLayers, eTGCemaNeigeLayers]

LayerFracSolidPrecip=RESULTS_ALTI['LayerFracSolidPrecip']
LayerPrecip=[Precip[i] for i in IndPeriodCemaneige]
SolidPrecip = [[LayerFracSolidPrecip[iLayer][i] * LayerPrecip[i] / NLayers for i in range(len(LayerPrecip))] for iLayer in range(NLayers)]
Factor = 365.25
MoySolid=0
for layer in SolidPrecip:
    for x in layer :
        MoySolid += x
MeanAnSolidPrecip = [MoySolid * Factor] * NLayers
CemaNeigeLayers = []
CatchMeltAndPliqLayer = []
CatchMeltAndPliq =[]
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

CatchMeltAndPliq = [sum([CatchMeltAndPliqLayer[iLayer][i] for iLayer in range(NLayers)]) for i in range(len(CatchMeltAndPliqLayer[0]))]
##endregion
##region Simulation


# RESULTS =

def Simulation_GR4J_CemaNeige(X):
    Dates_choisies = [DatesR[i] for i in Ind_Run]
    InputsPrecip = [Precip[i] for i in Ind_Run]
    InputsPE = [PotEvap[i] for i in Ind_Run]
    VarObs = [QObs[i] for i in Ind_Run]
    Param = list(X)
    Outputs = GR4J.gr4j(LInputs=len(InputsPrecip),
                             InputsPrecip=CatchMeltAndPliq,
                             InputsPE=InputsPE,
                             Param=Param,
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
    Outputs = GR4J.gr4j(LInputs=len(InputsPrecip),
                        InputsPrecip=CatchMeltAndPliq,
                        InputsPE=InputsPE,
                        Param=Param,
                        StateStart=StateStartGR4J)
    Output_Q = Outputs[0]
    # print(Output_model)
    Crit = ErreurCrit.ErrorCrit(FUN_CRIT, Output_Q, VarObs).OutputsCrit[0]
    return -Crit

# print(Minimisation_GR4J_CemaNeige([257.237556, 1.012237, 88.234673,   2.207958]))

## contraintes

def pos_X(X): #permet d'avoir que des paramètres positifs
    for x in X :
        if x < 0 :
            return -1
    return 1

constr = {'type' : 'ineq', 'fun' : pos_X}

x0=np.array([200, 1, 110, 2]) #valeur de départ

x_calc = scipy.optimize.minimize(Minimisation_GR4J_CemaNeige, x0, constraints = constr, options={'maxiter' : 100, 'disp' : True} )
print(x_calc)
Simulation_GR4J_CemaNeige(x_calc.x)

##endregion

