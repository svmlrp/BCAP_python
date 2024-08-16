from Tankinfo.WNTankList import getHoldBallastTank
from InputInfo.TargetTrim import getTargetTrim_value
from Tankinfo.Tank import getTankWeight
import traceback
import re

def extract_integer(s):
    match = re.search(r"\d+", s)
    # Check if a match is found
    if match:
        return int(match.group())
    else:
        return None

def determineSeaWaterDensity(loadLine):
    if loadLine in ["Summer Water Line (S)", "Winter Water Line(W)", "Optional Freeboard (TF)",
                    "Tropical Water Line (T)"] :
        return 1.025
    elif loadLine in ["Fresh Water Line (F)", "Tropical Fresh Water Line (TF)"]:
        return 1.0
    else:
        raise ValueError("Invalid Load Line")

def catch_backtrace():
    try:
        # code that may raise an exception
        result = 1 / 0
    except Exception as e:
        return traceback.format_exc()

def stacktrace(backtrace):
    # process backtrace data
    return backtrace
def getBallastTankWtConstraints(mod1,Btnk,tnk_ballast,BallestTankWTFlag,polsize,listofPOL,trim,WBlist,tank,cargodetails,listofTank,pschedule):
    try:
        if BallestTankWTFlag:
            for p in range(1,len(pschedule)-1):
                holdtank=getHoldBallastTank(WBlist,listofPOL[p])
                if len(holdtank)>=1:
                    BTnk=Btnk
                if (getTargetTrim_value(pschedule[p], trim,"ballest") == 1 or
                        getTargetTrim_value(pschedule[p], trim,"deballest") == 1
                ) :
                    xx= mod1.addConstr(sum(tnk_ballast[p,t] for t in range(1,len(listofTank)+1)))
                    holdtank = getHoldBallastTank(WBlist, pschedule[p])
                    bholdtank = []
                    for b in range(1,len(holdtank)+1):
                        zz=getTankWeight(tank, holdtank[b])
                        xy=mod1.addConstr(BTnk[p, b] * zz)
                        bholdtank.append(xy)
                    WBHOL2 = 0
                    if len(bholdtank) >= 1:
                        WBHOL2=mod1.addConstr(sum(bholdtank[i] for i in range(1,len(bholdtank)+1)))
                    else:
                        WBHOL2 = 0

                    if len(cargodetails)==0:
                        BallestTankWt = getTargetTrim_value(listofPOL[p], trim, "tankwt")
                        if BallestTankWt != 0:
                            mod1.addConstr(xx + WBHOL2 <= BallestTankWt)
                else:
                    xx=mod1.addConstr(sum(tnk_ballast[p,t] for t in range(1,len(listofTank)+1)))
                    holdtank = getHoldBallastTank(WBlist, pschedule[p])
                    bholdtank = []

                    for b in range(1,len(holdtank)+1):
                        zz=getTankWeight(tank, holdtank[b])
                        xy=mod1.addConstr(BTnk[p, b] * zz)
                        bholdtank.append(xy)
                    WBHOL2=0
                    if len(bholdtank) >= 1:
                        WBHOL2=mod1.addConstr(sum(bholdtank[i] for i in range(1,len(bholdtank)+1)))
                    else:
                        WBHOL2 = 0
                    mod1.addConstr(xx+ WBHOL2==0)
    except Exception as e:
        print("The Exception in getBallastTankWtConstraints Method ", e)
        bt = stacktrace(catch_backtrace())

        for frame in bt:
            print("File: {}, Line: {}, Function: {}".format(frame.file, frame.line, frame.func))
    return mod1














