# from ErreurEntree import *
# from TransfoParam import *
#
# class CalibOptions():
#
#     def __init__(self, FUN_MOD : str, FUN_CALIB : str, FUN_TRANSFO=None, IsHyst=False, IsSD=False,
#                  FixedParam=None, SearchRanges=None, StartParamList=None, StartParamDistrib=None):
#
#         """
#         Parameters
#         ----------
#         FUN_MOD	[function name] hydrological model function (e.g. RunModel_GR4J, RunModel_CemaNeigeGR4J)
#         FUN_CALIB (optional) [function name] calibration algorithm function (e.g. Calibration_Michel)
#         FUN_TRANSFO	(optional) [function name] model parameters transformation function, if the FUN_MOD used is native in the package, FUN_TRANSFO is automatically defined
#         IsHyst [boolean] boolean indicating if the hysteresis version of CemaNeige is used. See details
#         IsSD [boolean] boolean indicating if the semi-distributed lag model is used. See details
#         FixedParam (optional) [numeric] vector giving the values set for the non-optimised parameter values (NParam columns, 1 line)
#         SearchRanges (optional) [numeric] matrix giving the ranges of real parameters (NParam columns, 2 lines)
#         StartParamList	 (optional) [numeric] matrix of parameter sets used for grid-screening calibration procedure (values in columns, sets in line)
#         StartParamDistrib (optional) [numeric] matrix of parameter values used for grid-screening calibration procedure (values in columns, percentiles in line)
#
#
#         """
#
#
#
#         if (type(IsHyst) != bool) :
#             raise ErreurEntree("'IsHyst' must be a boolean")
#
#         if (type(IsSD)!= bool) :
#             raise ErreurEntree("'IsSD' must be a boolean")
#
#         ##region check FUN_MOD
#
#
#         #TODO : voir format et gérer les cas où fun_mod n'est pas dans la liste
#         ObjectClass = [FUN_MOD.partition('_')[2]]
#
#         if (IsHyst) :
#             ObjectClass.append("hysteresis")
#         if (IsSD) :
#             ObjectClass.append("SD")
#         ##endregion
#         ##region check FUN_CALIB
#         BOOL = False
#
#         if FUN_CALIB == "Calibration":
#             ObjectClass.append("HBAN")
#             BOOL = True
#         if BOOL == False :
#             raise ErreurEntree("incorrect 'FUN_CALIB' for use in 'CreateCalibOptions'")
#         ##endregion
#         ##region check FUN_TRANSFO
#         if FUN_TRANSFO == None :
#             ## set FUN1
#             FUN_GR = 'TransfoParam_' + FUN_MOD[-3 :] #vérifier que c'est dans le bon format au préalable
#             if FUN_MOD == 'RunModel_CemaNeige':
#                 if (IsHyst) :
#                     FUN_GR = 'TransfoParam_CemaNeigeHyst'
#                 else :
#                     FUN_GR = 'TransfoParam_CemaNeige'
#             if FUN_GR == None:
#                 raise ErreurEntree("'FUN_GR' was not found")
#
#             ## set FUN2
#             if (IsHyst) :
#                 self.FUN_SNOW = 'TransfoParam_CemaNeigeHyst'
#             else :
#                 self.FUN_SNOW = 'TransfoParam_CemaNeige'
#
#         ## set FUN_LAG
#         if (IsSD) :
#             self.FUN_LAG = 'TransfoParam_Lag'
#         ##endregion
#
#         ##region set FUN_TRANSFO
#
#
#         if not [x for x in ObjectClass if x in ["GR4H", "GR5H", "GR4J", "GR5J", "GR6J", "GR2M", "GR1A", "CemaNeige"]]:
#             if not IsSD :
#                 FUN_TRANSFO = FUN_GR
#             else :
#                 # def transfo1(ParamIn, Direction): todo reprendre avec pandas
#                 #     Bool = (is.matrix(ParamIn)
#                 #
#                 #     if not Bool:
#                 #     # ParamIn = rbind(ParamIn)
#                 #
#                 #     ParamOut = ['NA'] * ParamIn
#                 #     NParam = len(ParamIn)
#                 #     ParamOut[2:NParam] = FUN_GR(ParamIn[2:NParam], Direction)
#                 #     ParamOut[1] = FUN_LAG(as.matrix(ParamIn[, 1]), Direction)
#                 #     if not Bool:
#                 #         ParamOut = ParamOut[1,]
#                 #
#                 #     return ParamOut
#                 FUN_TRANSFO = "transfo1"
#
#
#
#         else :
#             if (IsHyst and not IsSD):
#                 FUN_TRANSFO = "transfo2"
#             # def transfo2(ParamIn, Direction):
#             #     Bool = is.matrix(ParamIn)
#             #     if (!Bool) :
#             #         ParamIn = rbind(ParamIn)
#             #
#             #     ParamOut = NA * ParamIn
#             #     NParam = ncol(ParamIn)
#             #     ParamOut[, 1:(NParam - 4)] = FUN_GR(ParamIn[, 1:(NParam - 4)], Direction)
#             #     ParamOut[, (NParam - 3):NParam] = FUN_SNOW(ParamIn[, (NParam - 3):NParam], Direction)
#             #     if (!Bool) :
#             #         ParamOut = ParamOut[1, ]
#             #
#             #     return (ParamOut)
#
#
#             if not IsHyst and not IsSD :
#                 FUN_TRANSFO = "transfo3"
#                 # def transfo3(ParamIn, Direction) :
#                 #     Bool = is.matrix(ParamIn)
#                 #     if (!Bool) :
#                 #         ParamIn = rbind(ParamIn)
#                 #
#                 #     ParamOut = NA * ParamIn
#                 #     NParam = ncol(ParamIn)
#                 #     if (NParam <= 3) :
#                 #         ParamOut[, 1:(NParam - 2)] = FUN_GR(cbind(ParamIn[, 1:(NParam - 2)]), Direction)
#                 #     else :
#                 #     ParamOut[, 1:(NParam - 2)] = FUN_GR(ParamIn[, 1:(NParam - 2)], Direction)
#                 #
#                 #     ParamOut[, (NParam - 1):NParam] = FUN_SNOW(ParamIn[, (NParam - 1):NParam], Direction)
#                 #     if (!Bool) :
#                 #         ParamOut = ParamOut[1, ]
#                 #
#                 #     return (ParamOut)
#
#
#             if (IsHyst and IsSD) :
#                 FUN_TRANSFO = "transfo4"
#                 # def transfo4(ParamIn, Direction) :
#                 #     Bool = is.matrix(ParamIn)
#                 #     if (!Bool) :
#                 #         ParamIn = rbind(ParamIn)
#                 #
#                 #     ParamOut = NA * ParamIn
#                 #     NParam = ncol(ParamIn)
#                 #     ParamOut[, 2:(NParam - 4)] = FUN_GR(ParamIn[, 2:(NParam - 4)], Direction)
#                 #     ParamOut[, (NParam - 3):NParam] = FUN_SNOW(ParamIn[, (NParam - 3):NParam], Direction)
#                 #     ParamOut[, 1] = FUN_LAG(as.matrix(ParamIn[, 1]), Direction)
#                 #     if (!Bool) :
#                 #         ParamOut = ParamOut[1, ]
#                 #
#                 #     return (ParamOut)
#
#
#             if (not IsHyst and IsSD) :
#                 FUN_TRANSFO = "transfo4"
#                 # def transfo4(ParamIn, Direction) :
#                 #     Bool = is.matrix(ParamIn)
#                 #     if (!Bool) :
#                 #         ParamIn = rbind(ParamIn)
#                 #
#                 #     ParamOut = NA * ParamIn
#                 #     NParam = ncol(ParamIn)
#                 #     if (NParam <= 3) :
#                 #         ParamOut[, 2:(NParam - 2)] = FUN_GR(cbind(ParamIn[, 2:(NParam - 2)]), Direction)
#                 #     else :
#                 #     ParamOut[, 2:(NParam - 2)] = FUN_GR(ParamIn[, 2:(NParam - 2)], Direction)
#                 #
#                 #     ParamOut[, (NParam - 1):NParam] = FUN_SNOW(ParamIn[, (NParam - 1):NParam], Direction)
#                 #     ParamOut[, 1] = FUN_LAG(as.matrix(ParamIn[, 1]), Direction)
#                 #     if (!Bool) :
#                 #         ParamOut = ParamOut[1, ]
#                 #
#                 #     return (ParamOut)
#
#
#
#
#             if FUN_TRANSFO == None:
#                 raise ErreurEntree("'FUN_TRANSFO' was not found")
#             # return (None)
#
#         ##endregion
#         ##region  NParam
#         if ("GR4H" in ObjectClass) :
#             NParam = 4
#
#         if ("GR5H" in  ObjectClass) :
#             NParam = 5
#
#         if ("GR4J" in ObjectClass) :
#             NParam = 4
#
#         if ("GR5J" in ObjectClass) :
#             NParam = 5
#
#         if ("GR6J" in ObjectClass) :
#             NParam = 6
#
#         if ("GR2M" in ObjectClass) :
#             NParam = 2
#
#         if ("GR1A" in ObjectClass) :
#             NParam = 1
#
#         if ("CemaNeige" in ObjectClass) :
#             NParam = 2
#
#         if ("CemaNeigeGR4H" in ObjectClass) :
#             NParam = 6
#
#         if ("CemaNeigeGR5H" in ObjectClass) :
#             NParam = 7
#
#         if ("CemaNeigeGR4J" in ObjectClass) :
#             NParam = 6
#
#         if ("CemaNeigeGR5J" in ObjectClass) :
#             NParam = 7
#
#         if ("CemaNeigeGR6J" in ObjectClass) :
#             NParam = 8
#
#         if (IsHyst) :
#             NParam = NParam + 2
#
#         if (IsSD) :
#             NParam = NParam + 1
#
#         ##endregion
#         ##region check FixedParam
#         if FixedParam is None :
#             FixedParam = [] * NParam
#         else :
#             if FixedParam.type != list :
#                 raise ErreurEntree("FixedParam must be a vector")
#
#             if (len(FixedParam) != NParam) :
#                 raise ErreurEntree("Incompatibility between 'FixedParam' len and 'FUN_MOD'")
#
#             if None not in FixedParam :
#                 raise ErreurEntree("At least one parameter must be not set (NA)")
#
#             if FixedParam.isEmpty()  :
#                 print("You have not set any parameter in 'FixedParam'")
#
#         ##endregion
#         ##region check SearchRanges
#         if SearchRanges is None :
#             ParamT = [[-9.99]*NParam, [-9.99]*NParam] #TODO : vérifier les dimensions
#             SearchRanges = TransfoParam(ParamIn=ParamT, Direction="TR", FUN_TRANSFO=FUN_TRANSFO)
#
#         else :
#             if SearchRanges.type != list:
#             #if (! is.matrix(SearchRanges)):
#                 raise ErreurEntree("'SearchRanges' must be a matrix")
#
#             # if (! is.numeric(SearchRanges)) :
#             #     raise ErreurEntree("'SearchRanges' must be a matrix of numeric values")
#             #
#             # if (sum( is.na(SearchRanges)) != 0) :
#             #     raise ErreurEntree("'SearchRanges' must not include NA values")
#             #
#             if (len(SearchRanges) != 2) :
#                 raise ErreurEntree("'SearchRanges' must have 2 rows")
#             for i in range(2):
#                 if (len(SearchRanges[i]) != NParam) :
#                     raise ErreurEntree("Incompatibility between 'SearchRanges' ncol and 'FUN_MOD'")
#         ##endregion
#         ##region check StartParamList and StartParamDistrib default values
#         if "HBAN" in ObjectClass and StartParamList is None and StartParamDistrib is None:
#             if ("GR4H" in ObjectClass) :
#                 ParamT = [[+5.12, -1.18, +4.34, -9.69],
#                           [+5.58, -0.85, +4.74, -9.47],
#                           [+6.01, -0.50, +5.14, -8.87]]
#
#         if (("GR5H" in ObjectClass) and ("interception" in ObjectClass)) :
#             ParamT = [[+3.46, -1.25, +4.04, -9.53, -9.34],
#                       [+3.74, -0.41, +4.78, -8.94, -3.33],
#                       [+4.29, +0.16, +5.39, -7.39, +3.33]]
#
#         if (("GR5H" in ObjectClass) and ("interception" not in ObjectClass)) :
#             ParamT = [[+3.28, -0.39, +4.14, -9.54, -7.49],
#                       [+3.62, -0.19, +4.80, -9.00, -6.31],
#                       [+4.01, -0.04, +5.43, -7.53, -5.33]]
#
#
#         if ("GR4J" in ObjectClass) :
#             ParamT = [[+5.13, -1.60, +3.03, -9.05],
#                       [+5.51, -0.61, +3.74, -8.51],
#                       [+6.07, -0.02, +4.42, -8.06]]
#
#         if ("GR5J" in ObjectClass) :
#             ParamT = [[+5.17, -1.13, +3.08, -9.37, -7.45],
#                       [+5.55, -0.46, +3.75, -9.09, -4.69],
#                       [+6.10, -0.11, +4.43, -8.60, -0.66]]
#
#
#         if ("GR6J" in ObjectClass) :
#             ParamT = [[+3.60, -1.00, +3.30, -9.10, -0.90, +3.00],
#                      [+3.90, -0.50, +4.10, -8.70, +0.10, +4.00],
#                      [+4.50, +0.50, +5.00, -8.10, +1.10, +5.00]]
#
#         if ("GR2M" in ObjectClass) :
#             ParamT = [[+5.03, -7.15],
#                       [+5.22, -6.74],
#                       [+5.85, -6.37]]
#
#         if ("GR1A" in ObjectClass) :
#             ParamT = [[-1.69],
#                       [-0.38],
#                       [+1.39]]
#
#
#         if ("CemaNeige" in ObjectClass) :
#             ParamT = [[-9.96, +6.63],
#                       [-9.14, +6.90],
#                       [+4.10, +7.21]]
#
#         if ("CemaNeigeGR4H" in ObjectClass) :
#             ParamT = [[+5.12, -1.18, +4.34, -9.69, -9.96, +6.63],
#                       [+5.58, -0.85, +4.74, -9.47, -9.14, +6.90],
#                       [+6.01, -0.50, +5.14, -8.87, +4.10, +7.21]]
#
#         if (("CemaNeigeGR5H" in ObjectClass) and ("interception" in ObjectClass)) :
#             ParamT = [[+3.46, -1.25, +4.04, -9.53, -9.34, -9.96, +6.63],
#                       [+3.74, -0.41, +4.78, -8.94, -3.33, -9.14, +6.90],
#                       [+4.29, +0.16, +5.39, -7.39, +3.33, +4.10, +7.21]]
#
#         if (("CemaNeigeGR5H" in ObjectClass) and ("interception" not in ObjectClass)) :
#             ParamT = [[+3.28, -0.39, +4.14, -9.54, -7.49, -9.96, +6.63],
#                       [+3.62, -0.19, +4.80, -9.00, -6.31, -9.14, +6.90],
#                       [+4.01, -0.04, +5.43, -7.53, -5.33, +4.10, +7.21]]
#
#         if ("CemaNeigeGR4J" in ObjectClass) :
#             ParamT =[[+5.13, -1.60, +3.03, -9.05, -9.96, +6.63],
#                      [+5.51, -0.61, +3.74, -8.51, -9.14, +6.90],
#                      [+6.07, -0.02, +4.42, -8.06, +4.10, +7.21]]
#
#         if ("CemaNeigeGR5J" in ObjectClass) :
#             ParamT = [[+5.17, -1.13, +3.08, -9.37, -7.45, -9.96, +6.63],
#                       [+5.55, -0.46, +3.75, -9.09, -4.69, -9.14, +6.90],
#                       [+6.10, -0.11, +4.43, -8.60, -0.66, +4.10, +7.21]]
#
#         if ("CemaNeigeGR6J" in ObjectClass) :
#             ParamT = [[+3.60, -1.00, +3.30, -9.10, -0.90, +3.00, -9.96, +6.63],
#                       [+3.90, -0.50, +4.10, -8.70, +0.10, +4.00, -9.14, +6.90],
#                       [+4.50, +0.50, +5.00, -8.10, +1.10, +5.00, +4.10, +7.21]]
#
#
#         if (IsHyst) :
#             ParamTHyst = [[-7.00, -7.00],
#                           [-0.00, -0.00],
#                           [+7.00, +7.00]]
#             ParamT = [ParamT, ParamTHyst] #todo : verifier dimension
#
#         if (IsSD) :
#             ParamTSD = [[+1.25],
#                         [+2.50],
#                         [+5.00]]
#             ParamT = [ParamTSD, ParamT]  #todo : verifier dimension
#
#
#         StartParamList = None
#         StartParamDistrib = TransfoParam(ParamIn=ParamT, Direction="TR", FUN_TRANSFO=FUN_TRANSFO)
#
#         ##endregion
#         ##region  check StartParamList and StartParamDistrib format TODO reprendre en V2
#         # if ("HBAN" in ObjectClass and StartParamList is not None) :
#         #     if type(StartParamList) != list :
#         #         raise ErreurEntree("'StartParamList' must be a matrix")
#         #
#         #     if (! is.numeric(StartParamList)) :
#         #         raise ErreurEntree("'StartParamList' must be a matrix of numeric values")
#         #
#         #     if (sum( is.na(StartParamList)) != 0) :
#         #         raise ErreurEntree("'StartParamList' must not include NA values")
#         #
#         #     if (ncol(StartParamList) != NParam) :
#         #         raise ErreurEntree("Incompatibility between 'StartParamList' ncol and 'FUN_MOD'")
#
#
#         # if ("HBAN" in ObjectClass and StartParamDistrib is not None) :
#         #     if (! is.matrix(StartParamDistrib)) :
#         #         raise ErreurEntree("'StartParamDistrib' must be a matrix")
#         #
#         #     if (! is.numeric(StartParamDistrib[1, ])) :
#         #         raise ErreurEntree("'StartParamDistrib' must be a matrix of numeric values")
#         #
#         #     if (sum( is.na(StartParamDistrib[1, ])) != 0) :
#         #         raise ErreurEntree("'StartParamDistrib' must not include NA values on the first line")
#         #
#         #     if (ncol(StartParamDistrib) != NParam) :
#         #         raise ErreurEntree("Incompatibility between 'StartParamDistrib' ncol and 'FUN_MOD'")
#
#
#
#
#         ##Create_CalibOptions
#         self.FixedParam=FixedParam
#         self.SearchRanges=SearchRanges
#         self.FUN_TRANSFO=FUN_TRANSFO
#
#         if (StartParamList is not None) :
#             self.StartParamList=StartParamList
#
#         if (StartParamDistrib is not None) :
#             self.StartParamDistrib=StartParamDistrib
