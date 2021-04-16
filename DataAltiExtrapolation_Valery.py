import math as math

def DataAltiExtrapolation_Valery(DatesR, Precip, PrecipScale=True, TempMean=None, TempMin=None, TempMax=None,
                                 ZInputs=None, HypsoData=None, NLayers=None, verbose=True):
    """
    Function which extrapolates the precipitation and air temperature series for different elevation layers
    Parameters
    ----------

    DatesR [POSIXt] vector of dates
    Precip [numeric] time series of daily total precipitation (catchment average) [mm/time step]
    PrecipScale (optional) [boolean] indicating if the mean of the precipitation interpolated on the
    elevation layers must be kept or not, required to create CemaNeige module inputs, default = TRUE
    (the mean of the precipitation is kept to the original value)
    TempMean [numeric] time series of daily mean air temperature [°C]
    TempMin (optional) [numeric] time series of daily min air temperature [°C]
    TempMax (optional) [numeric] time series of daily max air temperature [°C]
    ZInputs [numeric] real giving the mean elevation of the Precip and Temp series (before extrapolation) [m]
    HypsoData [numeric] vector of 101 reals: min, q01 to q99 and max of catchment elevation distribution [m]
    NLayers [numeric] integer giving the number of elevation layers requested [-]
    verbose (optional) [boolean] boolean indicating if the function is run in verbose mode or not, default = TRUE

    Returns
    -------
    dictionary containing the extrapolated series of precip. and air temp. on each elevation layer
    LayerPrecip	[list] list of time series of daily precipitation (layer average) [mm/time step]
    LayerTempMean	[list] list of time series of daily mean air temperature (layer average) [°C]
    LayerTempMin	[list] list of time series of daily min air temperature (layer average) [°C]
    LayerTempMax	[list] list of time series of daily max air temperature (layer average) [°C]
    LayerFracSolidPrecip	[list] list of time series of daily solid precip. fract. (layer average) [-]
    ZLayers	[numeric] vector of median elevation for each layer

    """
    ##Altitudinal_gradient_functions_______________________________________________________________
    ##unique_gradient_for_precipitation
    GradP_Valery2010 = 0.00041  ### value from Valery PhD thesis page 126 TODO : remettre valeur pertinente Rheraya
    GradT_Valery2010 = 0.434

    ##ElevationLayers_Creation_____________________________________________________________________
    ZLayers = [0.] * NLayers

    if HypsoData != [None]*101:
        nmoy = 100 // NLayers
        nreste = 100 % NLayers
        ncont = 0

        for iLayer in range (NLayers):
            if (nreste > 0):
                nn = nmoy + 1
                nreste = nreste - 1
            else:
                nn = nmoy

            if nn == 1:
                ZLayers[iLayer] = HypsoData[ncont + 1]

            elif nn == 2:
                ZLayers[iLayer] = 0.5 * (HypsoData[ncont + 1] + HypsoData[ncont + 2])
                ZLayers[iLayer] = 0.5 * (HypsoData[ncont + 1] + HypsoData[ncont + 2])

            elif nn > 2:
                ZLayers[iLayer] = HypsoData[int(ncont + nn / 2)]
            ncont = ncont + nn

    ##Precipitation_extrapolation__________________________________________________________________
    ##Initialisation
    if ZInputs == HypsoData[51] and NLayers == 1:
        LayerPrecip = Precip

    else:
        ##Elevation_gradients_for_daily_mean_precipitation
        GradP = GradP_Valery2010  ### single value
        TabGradP = [GradP] * len(Precip)

        ##Extrapolation
        ##Thresold_of_inputs_median_elevation
        Zthreshold = 4000
        LayerPrecip_mat=[]
        for iLayer in range(NLayers):
            ##If_layer_elevation_smaller_than_Zthreshold
            if ZLayers[iLayer] <= Zthreshold:
                prcp = [float(Precip[i] * math.exp(TabGradP[i] * (ZLayers[iLayer] - ZInputs))) for i in range(len(Precip))]
            ##If_layer_elevation_greater_than_Zthreshold
            else:
                ##If_inputs_median_elevation_smaller_than_Zthreshold
                if (ZInputs <= Zthreshold):
                    prcp = float(Precip * math.exp(TabGradP * (Zthreshold - ZInputs)))
                ##If_inputs_median_elevation_greater_then_Zthreshold
                else:
                    prcp = float(Precip)
            LayerPrecip_mat.append(prcp)
        if PrecipScale :
            rowMeans= [sum(LayerPrecip_mat[i])/len(LayerPrecip_mat[i]) for i in range(len(LayerPrecip_mat))]
            for iLayer in range(NLayers):
                for j in range(len(LayerPrecip_mat[iLayer])):
                    LayerPrecip_mat[iLayer][j] = LayerPrecip_mat[iLayer][j] / rowMeans[iLayer] * Precip[j]
        LayerPrecip = LayerPrecip_mat



        ##Temperature_extrapolation____________________________________________________________________
        ##Initialisation
        LayerTempMean = []
        LayerTempMin = []
        LayerTempMax = []

        if ZInputs == HypsoData[51] and NLayers == 1:
            LayerTempMean[0] = [TempMean]

        if (TempMin!=None and TempMax!=None):
            LayerTempMin[0] = [TempMin]
            LayerTempMax[0] = [TempMax]

        else:

        #Elevation_gradients_for_daily_mean_min_and_max_temperature TODO : reprendre
            GradT = GradT_Valery2010
            TabGradT = [GradT]
            ##Extrapolation
            ##On_each_elevation_layer...

            for iLayer in range(NLayers):
                LayerTempMean.append([TempMean[i] + (ZInputs - ZLayers[iLayer]) *GradT/100 for i in range(len(TempMean))])
            if (TempMin is not None and TempMax is not None ):
                LayerTempMin[iLayer] = TempMin + (ZInputs - ZLayers[iLayer]) * abs(GradT) / 100
                LayerTempMax[iLayer] = TempMax + (ZInputs - ZLayers[iLayer]) * abs(GradT) / 100





        ##Solid_Fraction_for_each_elevation_layer______________________________________________________
        LayerFracSolidPrecip = []

        ##Thresold_of_inputs_median_elevation
        Zthreshold = 1500

        ##Option
        Option = "USACE"
        if (ZInputs is not None):
            if (ZInputs < Zthreshold and TempMin!=None and TempMax!=None):
                Option = "Hydrotel"

        ##On_each_elevation_layer...
        for iLayer in range(NLayers):

            ##Turcotte_formula_from_Hydrotel

            if (Option == "Hydrotel"):
                TempMin = LayerTempMin[iLayer]
                TempMax = LayerTempMax[iLayer]
                SolidFraction = 1 - TempMax / (TempMax - TempMin)
                SolidFraction[TempMin >= 0] = 0
                SolidFraction[TempMax <= 0] = 1

            ##USACE_formula
            if (Option == "USACE"):
                USACE_Tmin = -1.0
                USACE_Tmax = 3.0
                TempMean = LayerTempMean[iLayer]
                SolidFraction =[1 - (TempMean[i] - USACE_Tmin) / (USACE_Tmax - USACE_Tmin) for i in range(len(TempMean))]
                # for i in range(len(TempMean)): #TODO : reprendre
                # SolidFraction[TempMean > USACE_Tmax] = 0
                # SolidFraction[TempMean < USACE_Tmin] = 1

            LayerFracSolidPrecip.append(SolidFraction)

        ##END__________________________________________________________________________________________

        return {'LayerPrecip':LayerPrecip, 'LayerTempMean':LayerTempMean, 'LayerTempMin':LayerTempMin,
            'LayerTempMax': LayerTempMax, 'LayerFracSolidPrecip': LayerFracSolidPrecip, 'ZLayers': ZLayers}





