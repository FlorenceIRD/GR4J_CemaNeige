from ErreurEntree import *
import math as math

def TransfoParam(ParamIn, Direction, FUN_TRANSFO):
    if "GR4J" in FUN_TRANSFO:
        return TransfoParam_GR4J(ParamIn, Direction)
    else :
        return None #TODO remettre les autres

def TransfoParam_GR4J(ParamIn, Direction : str):

    ## number of model parameters
    NParam = 4

    ## check arguments
    isVecParamIn = (ParamIn.type == list)

    if (Direction not in ["RT", "TR"]):
        raise ErreurEntree("'Direction' must be a character vector of length 1 equal to 'RT' or 'TR'")

    if (len(ParamIn) != NParam):
        raise ErreurEntree("the GR4J model requires %i parameters"+ str(NParam))


    ParamOut = []*NParam
    ## transformation
    if (Direction == "TR"):
        ParamOut[0] = math.exp(ParamIn[0])  ### GR4J X1 (production store capacity)
        ParamOut[1] = math.sinh(ParamIn[1])  ### GR4J X2 (groundwater exchange coefficient)
        ParamOut[2] = math.exp(ParamIn[2])  ### GR4J X3 (routing store capacity)
        ParamOut[3] = 20 + 19.5 * (ParamIn[4] - 9.99) / 19.98  ### GR4J X4 (unit hydrograph time constant)

    if (Direction == "RT"):

        ParamOut[0] = math.log(ParamIn[0])  ### GR4J X1 (production store capacity)
        ParamOut[1] = math.asinh(ParamIn[1])  ### GR4J X2 (groundwater exchange coefficient)
        ParamOut[2] = math.log(ParamIn[2])  ### GR4J X3 (routing store capacity)
        ParamOut[3] = 9.99 + 19.98 * (ParamIn[3] - 20) / 19.5  ### GR4J X4 (unit hydrograph time constant)

    ## check output


    return ParamOut



