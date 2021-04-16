import ErreurEntree
import math


class ErrorCrit:
    def __init__(self, FUN_CRIT, outputsModel, VarObs, warnings=True, verbose=True):
        ## ----- Single criterion
        self.VarSim = outputsModel
        self.VarObs = VarObs
        if type(FUN_CRIT) is str:
            if FUN_CRIT == "NSE":
                OutputsCrit = self.ErrorCrit_NSE(outputsModel=outputsModel, warnings=warnings, verbose=verbose)
                self.ObjectClass = ["NSE", "ErrorCrit"]
            if FUN_CRIT == "NSE_RAC_DEBITS":
                OutputsCrit = self.ErrorCrit_NSE_RAC_DEBITS(outputsModel=outputsModel, warnings=warnings, verbose=verbose)
            self.ObjectClass = ["NSE_RAC_DEBITS", "ErrorCrit"]
        self.OutputsCrit = OutputsCrit


    def ErrorCrit_NSE(self, outputsModel, warnings=True, verbose=True):

        ##region  Arguments check

        Crit = None

        ## Other variables preparation

        meanVarObs =  sum(self.VarObs) / len(self.VarObs)
        meanVarSim = sum(self.VarSim) / len(self.VarSim)

        ## ErrorCrit
        Emod = 0
        for i in range(len(self.VarSim)):
            if self.VarObs[i] < 10000000 and self.VarSim[i] < 10000000 :
                Emod += (self.VarSim[i] - self.VarObs[i])**2
            else :
                print(self.VarObs[i], self.VarSim[i])
        Eref = 0
        for i in range(len(self.VarObs)):
            if self.VarObs[i] < 10000000 :
                Eref += (self.VarObs[i] - meanVarObs)**2
            else :
                print(self.VarObs[i])

        if Eref == 0:
            if Emod == 0:
                Crit = 0
            else :
                Crit = float ('inf')
        else:
            Crit = (1 - Emod / Eref)


        ## Output
        OutputsCrit = [Crit]


        return OutputsCrit


    def ErrorCrit_NSE_RAC_DEBITS(self, outputsModel, warnings=True, verbose=True):

        ##region  Arguments check

        Crit = None

        ## Other variables preparation

        meanVarObs =  sum(self.VarObs) / len(self.VarObs)
        meanVarSim = sum(self.VarSim) / len(self.VarSim)

        ## ErrorCrit
        Emod = 0
        for i in range(len(self.VarSim)):
            if self.VarObs[i] < 10000000 and self.VarSim[i] < 10000000 :
                Emod += (math.sqrt(self.VarSim[i]) - math.sqrt(self.VarObs[i]))**2
            else :
                print(self.VarObs[i], self.VarSim[i])
        Eref = 0
        for i in range(len(self.VarObs)):
            if self.VarObs[i] < 10000000 :
                Eref += (math.sqrt(self.VarObs[i]) - math.sqrt(meanVarObs))**2
            else :
                print(self.VarObs[i])

        if Eref == 0:
            if Emod == 0:
                Crit = 0
            else :
                Crit = float ('inf')
        else:
            Crit = (1 - Emod / Eref)


        ## Output
        OutputsCrit = [Crit]


        return OutputsCrit





