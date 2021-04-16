import matplotlib.pyplot as plt
import csv
import pandas as pd
import GR4J
import numpy as np
import scipy.optimize
import ErreurCrit

##region Importation des données
data = pd.read_csv ('BasinL0123001.csv', header=0)
# data = data[data.Qmm.apply(lambda x: x.isnumeric())]

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
Ind_Run = range(debut, fin)


##endregion

##region Choix du critère
FUN_CRIT = "NSE_RAC_DEBITS"
FUN_CRIT = "NSE"

InputsPrecip = [Precip[i] for i in Ind_Run]
InputsPE = [PotEvap[i] for i in Ind_Run]
VarObs = [QObs[i] for i in Ind_Run]
Param = [257.237556, 1.012237, 88.234673,   2.207958]
StateStart = [0.] * 67
StateStart = GR4J.gr4j(len(InputsPrecip), InputsPrecip, InputsPE, Param, StateStart)[2]

def Simulation_GR4J_CemaNeige(X):
    Dates_choisies = [DatesR[i] for i in Ind_Run]
    InputsPrecip = [Precip[i] for i in Ind_Run]
    InputsPE = [PotEvap[i] for i in Ind_Run]
    VarObs = [QObs[i] for i in Ind_Run]
    Param = list(X)
    Output_model = GR4J.gr4j(len(InputsPrecip), InputsPrecip, InputsPE, Param, StateStart)[0]
    plt.plot(Dates_choisies, Output_model, Dates_choisies, VarObs)
    plt.show()

def Minimisation_GR4J_CemaNeige(X):
    InputsPrecip = [Precip[i] for i in Ind_Run]
    InputsPE = [PotEvap[i] for i in Ind_Run]
    VarObs = [QObs[i] for i in Ind_Run]
    Param = list(X)
    Output_model = GR4J.gr4j(len(InputsPrecip), InputsPrecip, InputsPE, Param, StateStart)[0]
    # print(Output_model)
    Crit = ErreurCrit.ErrorCrit(FUN_CRIT, Output_model, VarObs).OutputsCrit[0]
    return -Crit

# print(Minimisation_GR4J_CemaNeige([257.237556, 1.012237, 88.234673,   2.207958]))

def pos_X(X): #permet d'avoir que des paramètres positifs
    for x in X :
        if x < 0 :
            return -1
    return 1
constr = {'type' : 'ineq', 'fun' : pos_X}


##endregion


x0=np.array([200, 1, 110, 2]) #valeur de départ

x_calc = scipy.optimize.minimize(Minimisation_GR4J_CemaNeige, x0, constraints = constr)
print(x_calc)
Simulation_GR4J_CemaNeige(x_calc.x)



