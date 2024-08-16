def doLinearInterpolation(Difference, dValue1, dValue2, dAddReq):
    try:
        return dValue1 + (dAddReq * (dValue2 - dValue1) / Difference)
    except Exception as e:
        print("Exception while doing the Linear Interpolation", e)
    return 0.0
def setWeightItems(weightid,xaftap,xfwdap,weight,lcgap,vcgbl,tcgcl):
    try:
        items={}
        items["id"]=weightid
        items["xAftAP"] = xaftap
        items["xFwdAP"] = xfwdap
        items["weight"] = weight
        items["lcgAP"] = lcgap
        items["vcgBL"] = vcgbl
        items["tcgCL"] = tcgcl
        return items
    except Exception as e:
        print("The Exception in setWeightItems Method", e)
    return 0.0

localpath = "C://BCAP project//WUI//files//"
includepath = "C:\\Dev julia project\\"
# apiURL="http://localhost:8090/BCAP_OPT/"

apiURL = "https://bcap.solverminds.net/BCAP_OPT/"