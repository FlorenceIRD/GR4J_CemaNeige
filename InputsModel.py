from ErreurEntree import *
from DataAltiExtrapolation_Valery import *


class InputsModel:
    def __init__(self, FUN_MOD : str, DatesR: list, Precip: list, PrecipScale=True, PotEvap=None, TempMean=None,
                 TempMin=None, TempMax=None, ZInputs=None, HypsoData=None, NLayers: int = 5,
                 Qupstream=None, LengthHydro=None, BasinAreas=None, verbose=True):
        """
        Parameters
        ----------
        DatesR [POSIXt] vector of dates required to create the GR model and CemaNeige module inputs
        Precip	[numeric] time series of total precipitation (catchment average) [mm/time step], required to create the GR model and CemaNeige module inputs
        PrecipScale (optional) [boolean] indicating if the mean of the precipitation interpolated on the elevation layers must be kept or not, required to create CemaNeige module inputs, default = TRUE (the mean of the precipitation is kept to the original value)
        PotEvap	[numeric] time series of potential evapotranspiration (catchment average) [mm/time step], required to create the GR model inputs
        TempMean (optional) [numeric] time series of mean air temperature [°C], required to create the CemaNeige module inputs
        TempMin	(optional) [numeric] time series of min air temperature [°C], possibly used to create the CemaNeige module inputs
        TempMax	(optional) [numeric] time series of max air temperature [°C], possibly used to create the CemaNeige module inputs
        ZInputs	(optional) [numeric] real giving the mean elevation of the Precip and Temp series (before extrapolation) [m], possibly used to create the CemaNeige module inputs
        HypsoData (optional) [numeric] vector of 101 reals: min, q01 to q99 and max of catchment elevation distribution [m], if not defined a single elevation is used for CemaNeige
        NLayers	(optional) [numeric] integer giving the number of elevation layers requested [-], required to create CemaNeige module inputs, default=5
        verbose	(optional) [boolean] boolean indicating if the function is run in verbose mode or not, default = TRUE
        Qupstream (optional) [numerical matrix] time series of upstream flows (catchment average) [mm/time step or m3/time step, see details], required to create the SD model inputs . See details
        LengthHydro (optional) [numeric] real giving the distance between the downstream outlet and each upstream inlet of the sub-catchment [m], required to create the SD model inputs . See details
        BasinAreas (optional) [numeric] real giving the area of each upstream sub-catchment [km2] and the area of the downstream sub-catchment in the last item, required to create the SD model inputs . See details
        x [InputsModel] object of class InputsModel
        i [integer] of the indices to subset a time series or [character] names of the elements to extract

        Returns
        -------
        Object of class InputsModel containing the data required to evaluate the model outputs; it can include the following:
            'DatesR'	[POSIXlt] vector of dates
            'Precip'	[numeric] time series of total precipitation (catchment average) [mm/time step]
            'PotEvap'	[numeric] time series of potential evapotranspiration (catchment average) [mm/time step],
            defined if FUN_MOD includes GR4H, GR5H, GR4J, GR5J, GR6J, GR2M or GR1A
            'LayerPrecip'	[list] list of time series of precipitation (layer average) [mm/time step],
            defined if FUN_MOD includes CemaNeige
            'LayerTempMean'	[list] list of time series of mean air temperature (layer average) [°C],
            defined if FUN_MOD includes CemaNeige
            'LayerFracSolidPrecip'	[list] list of time series of solid precipitation fraction (layer average) [-],
            defined if FUN_MOD includes CemaNeige
        """

        ##region check_FUN_MOD
        ObjectClass = []
        BOOL = False
        if FUN_MOD == "RunModel_GR4H" or FUN_MOD == "RunModel_GR5H":
            ObjectClass.append("GR")
            ObjectClass.append("hourly")
            TimeStep = 60 * 60
            BOOL = True

        if FUN_MOD == "RunModel_GR4J" or FUN_MOD == "RunModel_GR5J" or FUN_MOD == "RunModel_GR6J":
            ObjectClass.append("GR")
            ObjectClass.append("daily")
            TimeStep = 24 * 60 * 60
            BOOL = True

        if FUN_MOD == "RunModel_GR2M":
            ObjectClass.append("GR")
            ObjectClass.append("monthly")
            BOOL = True
            #todo remettre time step

        if (FUN_MOD == "RunModel_GR1A"):
            ObjectClass.append("GR")
            ObjectClass.append("yearly")
            BOOL = True
            #todo remettre time step

        if (FUN_MOD == "RunModel_CemaNeige"):
            ObjectClass.append("CemaNeige")
            ObjectClass.append("daily")
            TimeStep = 24 * 60 * 60
            BOOL = True

        if FUN_MOD == "RunModel_CemaNeigeGR4J" or FUN_MOD == "RunModel_CemaNeigeGR5J" \
                or FUN_MOD == "RunModel_CemaNeigeGR6J":
            ObjectClass.append("GR")
            ObjectClass.append("CemaNeige")
            ObjectClass.append("daily")
            TimeStep = 24 * 60 * 60
            BOOL = True

        if FUN_MOD == "RunModel_CemaNeigeGR4H" or FUN_MOD == "RunModel_CemaNeigeGR5H":
            ObjectClass.append("GR")
            ObjectClass.append("CemaNeige")
            ObjectClass.append("hourly")
            TimeStep = 60 * 60
            BOOL = True

        if not BOOL:
            raise ErreurEntree("incorrect 'FUN_MOD' for use in 'CreateRunOptions'")

        self.ObjectClass = list(set(ObjectClass))

        ##endregion

        ##region check_arguments

        if DatesR is None:
            raise ErreurEntree("'DatesR' is missing")

        # if (!"POSIXlt" in class(DatesR) & !"POSIXct" in class(DatesR)):
        #       stop("'DatesR' must be defined as 'POSIXlt' or 'POSIXct'")
        #
        #     if (!"POSIXlt" in class(DatesR)) :
        #       DatesR = as.POSIXlt(DatesR)
        #
        #     if (!difftime(tail(DatesR, 1), tail(DatesR, 2), units = "secs")[[1]] in TimeStep) :
        #       TimeStepName = grep("hourlyordailyormonthlyoryearly", ObjectClass, value = True)
        #       stop(paste0("the time step of the model inputs must be ", TimeStepName, "\n"))

        if len(DatesR) != len(list(set(DatesR))):
            raise ErreurEntree("'DatesR' must not include duplicated values")

        if Precip is None:
            raise ErreurEntree("Precip is missing")

        if PotEvap is None:
            raise ErreurEntree("'PotEvap' is missing")

        # if (!is.vector(Precip) or !is.vector(PotEvap)) :
        #   stop("'Precip' and 'PotEvap' must be vectors of numeric values")
        #
        # if (!is.numeric(Precip) or !is.numeric(PotEvap)) :
        #   stop("'Precip' and 'PotEvap' must be vectors of numeric values")


        if len(Precip) != len(DatesR) or len(PotEvap) != len(DatesR) or len(TempMean) != len(DatesR):
            raise ErreurEntree("'Precip', 'PotEvap', 'TempMean' and 'DatesR' must have the same length")

        if TempMean is None:
            raise ErreurEntree("'TempMean' is missing")

        # if (!is.vector(Precip) or !is.vector(TempMean)) :
        #   stop("'Precip' and 'TempMean' must be vectors of numeric values")
        #
        # if (!is.numeric(Precip) or !is.numeric(TempMean)) :
        #   stop("'Precip' and 'TempMean' must be vectors of numeric values")

        if (TempMax is None) != (TempMin is None):
            raise ErreurEntree("'TempMin' and 'TempMax' must be both defined if not null")

        if TempMin is not None and TempMax is not None:
            # if (!is.vector(TempMin) or !is.vector(TempMax)):
            #   raise ErreurEntree("'TempMin' and 'TempMax' must be vectors of numeric values")
            # if (!is.numeric(TempMin) or !is.numeric(TempMax)) :
            #   raise ErreurEntree("'TempMin' and 'TempMax' must be vectors of numeric values")
            if len(TempMin) != len(DatesR) or len(TempMax) != len(DatesR):
                raise ErreurEntree("'TempMin', 'TempMax' and 'DatesR' must have the same length")

        if HypsoData is not None:
            #   if (!is.vector(HypsoData)) :
            #   stop("'HypsoData' must be a vector of numeric values  if not null")
            #
            # if (!is.numeric(HypsoData)) :
            #   stop("'HypsoData' must be a vector of numeric values  if not null")
            #
            if len(HypsoData) != 101:
                raise ErreurEntree("'HypsoData' must be of length 101 if not null")

        # if (sum(is.na(HypsoData)) != 0 & sum(is.na(HypsoData)) != 101):
        #       stop("'HypsoData' must not contain any NA if not null")

        if ZInputs is not None:
            if len(ZInputs) != 1:
                raise ErreurEntree("'ZInputs' must be a single numeric value if not null")

        # if (is.na(ZInputs) or !is.numeric(ZInputs)) :
        #   stop("'ZInputs' must be a single numeric value if not null")

        # if (is.null(HypsoData)) :
        #   if (verbose) :
        #     print("'HypsoData' is missing: a single layer is used and no extrapolation is made")
        #
        #   HypsoData = as.numeric(rep(NA, 101))
        #   ZInputs   = as.numeric(NA)
        #   NLayers   = as.integer(1)
        # if (is.null(ZInputs)) :
        #   if (verbose & !identical(HypsoData, as.numeric(rep(NA, 101)))) :
        #     print("'ZInputs' is missing: HypsoData[51] is used")
        #
        #   ZInputs = HypsoData[51L]

        if NLayers <= 0:
            raise ErreurEntree("'NLayers' must be a positive integer value")

        ## check semi-distributed mode TODO : vérifier si c'est utile
        # if (!is.null(Qupstream) & !is.null(LengthHydro) & !is.null(BasinAreas)) :
        #   ObjectClass = c(ObjectClass, "SD")
        #  else if (verbose & !all(c(is.null(Qupstream), is.null(LengthHydro), is.null(BasinAreas)))) :
        #   print("Missing argument: 'Qupstream', 'LengthHydro' and 'BasinAreas' must all be set to run in a semi-distributed mode. The lumped mode will be used")
        #
        #
        #   if (!is.matrix(Qupstream) or !is.numeric(Qupstream)) :
        #     stop("'Qupstream' must be a matrice of numeric values")
        #
        #   if (!is.vector(LengthHydro) or !is.vector(BasinAreas) or !is.numeric(LengthHydro) or !is.numeric(BasinAreas)) :
        #     stop("'LengthHydro' and 'BasinAreas' must be vectors of numeric values")
        #
        #   if (ncol(Qupstream) != len(LengthHydro)) :
        #     stop("'Qupstream' number of columns and 'LengthHydro' length must be equal")
        #
        #   if (len(LengthHydro) + 1 != len(BasinAreas)) :
        #     stop("'BasinAreas' must have one more element than 'LengthHydro'")
        #
        #   if (nrow(Qupstream) != LLL) :
        #     stop("'Qupstream' must have same number of rows as 'DatesR' length")
        #
        #   if(any(is.na(Qupstream))) :
        #     stop("'Qupstream' cannot contain any NA value")
        #
        #

        ##check_NA_values
        # BOOL_NA = [False] * len(DatesR) supprimé : todo : faire un break en cas de valeur qui merdoie vraiment

        if ("GR" in ObjectClass):
            for i in Precip :
                if i is None:
                    print("Empty values detected in 'Precip' series")
                if i<0 :
                    print("Values < 0  detected in 'Precip' series")

            for i in PotEvap:
                if i is None:
                    print("Empty values detected in 'PotEvap' series")
                if i < 0:
                    print("Values < 0  detected in 'PotEvap' series")

        if ("CemaNeige" in ObjectClass):
            for i in Precip :
                if i is None:
                    print("Empty values detected in 'Precip' series")
                if i<0 :
                    print("Values < 0  detected in 'Precip' series")

            for i in TempMean :
                if i is None:
                    print("Empty values detected in 'TempMean' series")
                if i<-150 :
                    print("Values < -150 detected in 'TempMean' series")

            if (TempMin is not None and TempMax is not None):
                for i in TempMin:
                    if i is None:
                        print("Empty values detected in 'TempMin' series")
                    if i < -150:
                        print("Values < -150  detected in 'TempMin' series")

                for i in TempMax:
                    if i is None:
                        print("Empty values detected in 'TempMax' series")
                    if i < -150:
                        print("Values < -150  detected in 'TempMax' series")

        #TODO : supprimer section : si ça merdoie on ne tronque pas, on break

        # if (sum(BOOL_NA) != 0):
        #     WTxt = None
        #     WTxt = paste(WTxt, "\t Missing values are not allowed in 'InputsModel'", sep="")
        #
        #     Select = (max(which(BOOL_NA)) + 1):len(BOOL_NA)
        #
        #     if (Select[1L] > Select[2L]):
        #         stop("time series could not be trunced since missing values were detected at the last time-step")
        #
        #     if ("GR" in ObjectClass):
        #         Precip = Precip[Select]
        #         PotEvap = PotEvap[Select]
        #
        #     if ("CemaNeige" in ObjectClass):
        #         Precip = Precip[Select]
        #         TempMean = TempMean[Select]
        #         if (! is.null(TempMin) & ! is.null(TempMax)):
        #             TempMin = TempMin[Select]
        #             TempMax = TempMax[Select]
        #
        #     DatesR = DatesR[Select]
        #
        #     WTxt = paste0(WTxt, "\t -> data were trunced to keep the most recent available time-steps")
        #     WTxt = paste0(WTxt, "\t -> ", len(Select), " time-steps were kept")
        #
        #     if (! is.null(WTxt) & verbose):
        #         print(WTxt)

        ##endregion

        ##region DataAltiExtrapolation_Valery

        if ("CemaNeige" in ObjectClass):
            RESULT = DataAltiExtrapolation_Valery(DatesR=DatesR, Precip=Precip, PrecipScale=PrecipScale,
                                                  TempMean=TempMean, TempMin=TempMin, TempMax=TempMax,
                                                  ZInputs=ZInputs, HypsoData=HypsoData, NLayers=NLayers,
                                                  verbose=verbose)
            if verbose:
                if NLayers == 1:
                    print("input series were successfully created on 1 elevation layer for use by CemaNeige")
                else:
                    print("input series were successfully created on ", NLayers, " elevation layers for use by CemaNeige")
        ##endregion

        ##region Create_InputsModel
        self.DatesR = DatesR
        if "GR" in ObjectClass:
            self.Precip = Precip
            self.PotEvap = PotEvap
        if "CemaNeige" in ObjectClass:
            self.LayerPrecip = RESULT['LayerPrecip']
            self.LayerTempMean = RESULT['LayerTempMean']
            self.LayerFracSolidPrecip = RESULT['LayerFracSolidPrecip']
            self.ZLayers = RESULT['ZLayers']

        if "SD" in ObjectClass:
            self.Qupstream = Qupstream
            self.LengthHydro = LengthHydro,
            self.BasinAreas = BasinAreas
        ##endregion
