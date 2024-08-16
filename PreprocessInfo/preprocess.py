from StabilityInfo.HydroStaticData import getStatbilityinfo
from typing import Dict
from Vesselinfo.VesselParticulars import getHoldWeightMaxBounds
from InputInfo.CargoDetail import getCargoGradeMaxBounds,getTotalWeightOf_POL,getPODPort
from Vesselinfo.Lightship import getLightshipweight
from InputInfo.TankData import getWeightConstantWeight
from Tankinfo.BallastWeight import readBallastWt
from Tankinfo.WNTankList import getBallastTankTotalWt
from InputInfo.TargetTrim import getTargetTrim_value,getTdensity_value,getTargetTrim_value
# getHoldVolumeMaxBounds
# from NonlinearInfo.Nonlinear_modelling_printing_SF_BM import
from StabilityInfo.HydroStaticData import getStatbilityData
# from InputInfo.Json_reader_2 import vessel_api

import traceback

def getLCFMeanDraft(Trim,LCfDraft,df,LCFvalue):
    meanDraft=0.0
    try:
        res = abs(Trim / df["lpp"][1])
        Lcflppdiff = LCFvalue - (df["lpp"][1]/2)
        ratio = res * Lcflppdiff
        meanDraft=ratio + LCfDraft if Trim >= 0 else LCfDraft - ratio
        return round(meanDraft,2)
    except Exception as e:
        print("The Exception in getLCFMeanDraft Method:", e)

def getLCFLMom(item,polIndex,Trim,MeanDraft,trim,vesselMain,df):
    try:
        DISPL = item.get("DISPL", 0)
        LCB = item.get("LCB", 0)
        MTC = item.get("MTC", 0)
        TRIM = item.get("TRIM", 0)
        LCF = item.get("LCF", 0)

        LCFNew = MeanDraft
        tmp=trim[trim["polIndex"]==polIndex]
        var={}
        if len(tmp)>0:
            trimmed_value = tmp.iloc[1]['polIndex'].strip()
            var=getStatbilityinfo(trimmed_value,LCFNew,df)
        if len(var) >0:
            DISPL = item.get("DISPL", 0)
            LCB = item.get("LCB", 0)
            MTC = item.get("MTC", 0)
            TRIM = item.get("TRIM", 0)
            LCG = abs(-(TRIM * (MTC) / DISPL) + LCB)
        return LCG * DISPL
    except Exception as e:
        print("Exception while doing the interpolation getLCFLMom ==> ", e)
        return 0

def calculateSSandSB(dMean,trim,svalue,fmStation):
    sigmaWi = 0.0  # The total of all frame loads from forward to the frame in question (Wi)
    sigmaMi = 0.0  # The toal of all frame moments from forwward to the frame in question(Mi)
    sValIndex = 0.0
    SS=0.0
    SB=0.0
    result=[]
    FmStSS: Dict[float, float] = {}
    FmStSB: Dict[float, float] = {}
    loadFactor=0.0
    weightLcg=0.0
    weightSF=0.0
    sigmaW=0.0
    sigmaM=0.0
    Fs=0.0
    Ms=0.0
    try:
        for _,sv in svalue.iterrows():
            if sv["BASE DRAFT"] <=dMean:
                sValIndex +=1
            else:
                break
        draughtBase = svalue["BASE DRAFT"][sValIndex]
        draughtDiff = round((dMean - draughtBase),2)
        fsIndex=len(fmStation)
        fsIndex = fsIndex - 1
        for fsIndex in reversed(range(1,fsIndex)):
            for _,sv in svalue.iterrows():
                if sv["FRAMES"] == fmStation["FRAMES"][fsIndex] and  svalue["BASE DRAFT"] == draughtBase:
                    SS=(sv["BASE VALUE (SF)"]+(sv["DRAFT CORRECT. (CD) SF"] * draughtDiff ) + sv["TRIM CORRECT. (CT) SF"] * trim)
                    SB=(sv["BASE VALUE (BM)"]+(sv["DRAFT CORRECT. (CD) BM"] * draughtDiff ) + sv["TRIM CORRECT. (CT) SF"] * trim)
                    FmStSS[sv["FRAMES"]]=SS
                    FmStSB[sv["FRAMES"]]=SB
                    break
    except Exception as e:
        print("The Exception in calculateSSandSB Method:", e)
    return FmStSS,FmStSB

def getAboveframeStation(frameno,df):
    fsIndex=len(df)
    frameStation=[]
    try:
        for i in reversed(range(1,fsIndex)):
            frameStation.append(df["FRAMES"][i])
            if df["FRAMES"][i]== frameno:
                break
    except Exception as e:
        print("The Exception in getAboveframeStation Method:", e)
    return frameStation

def getMaxHoldNoAtEachFrame(frameNo,fmStation,FmStItems,CargoHold,FmStWeightRatio,FmStLcgvalue):
    holdno = 1
    FmStWeight: Dict[str, float] = {}
    FmStLcg: Dict[str, float] = {}
    try:
        FmStLcgCount: Dict[str, float] = {}
        fsIndex=len(fmStation)
        weightratio = 0
        lcg = 0
        lcgCount = 0
        Items = []
        for i in reversed(range(1,fsIndex)):
            zz=fmStation["FRAMES"][i]
            Itemszz =  FmStItems.get(zz,0)
            Items = FmStItems.get(fmStation["FRAMES"][i],0)
            if not isinstance(Items, int):
                for it in range(len(Items)):
                    if Items[it] in FmStWeight:
                        weightratio=FmStItems.get(zz,0) + FmStWeightRatio.get(str(Items[it],fmStation["FRAMES"][i]),0)
                        FmStWeight[Items[it] ]=weightratio
                    else:
                        FmStWeight[Items[it]] = FmStWeightRatio.get(str(Items[it],fmStation["FRAMES"][i]),0)
                    if Items[it] in FmStLcg:
                        lcg=FmStLcg.get(Items[it],0) + FmStLcgvalue.get(str(Items[it],fmStation["FRAMES"][i]),0)
                        lcgCount=FmStLcgCount.get(Items[it],0) + 1
                        FmStLcgCount[Items[it]]=lcgCount
                        FmStLcg[Items[it]]=lcg
                    else:
                        FmStLcg[Items[it]] = FmStLcgvalue.get(str(Items[it],fmStation["FRAMES"][i]),0)
                        FmStLcgCount[Items[it]] = 1
            if frameNo==fmStation["FRAMES"][i]:
                break
            for k, v in FmStWeight.items():
                if k in CargoHold:
                    last_char_as_int = int(k[-1])
                    if holdno < last_char_as_int:
                        holdno = last_char_as_int
    except Exception as e:
        print("The Exception in getMaxHoldNoAtEachFrame Method:", e)
    return holdno, FmStWeight, FmStLcg

def getLCF(item,Trim,MeanDraft,vesselMain):
    LCFNew=0
    try:
        DISPL = item.get("DISPL", 0)
        LCB = item.get("LCB", 0)
        MTC = item.get("MTC", 0)
        TRIM = item.get("TRIM", 0)
        LCF=item.get("LCF",0)

        result=(Trim * ((vesselMain["LPP"][1]/2) - LCF)) / vesselMain["LPP"][1]
        LCFNew = MeanDraft + result
        return LCFNew
    except Exception as e:
        print("The Exception in getLCF Method:", e)


def setOnBoardData(result,cargodetails,h,polIdx,PodIdx,cargotype,grade,vessel,pl,pd,c,g,lower):
    try:
        if result in str(h,pl,pd,c,g):
            return result.get(str(h,pl,pd,c,g),0)
        else:
            if(lower==1):
                return 0
            else:
                return (
                    getCargoGradeMaxBounds(cargodetails, polIdx, cargotype, grade)
                    if getHoldWeightMaxBounds(vessel, h) > getCargoGradeMaxBounds(cargodetails, polIdx, cargotype, grade)
                    else getHoldWeightMaxBounds(vessel, h)
                )

    except Exception as e:
        print("The Exception in setOnBoardData Method:", e)

def setOnBoardPMMData(result,cargodetails,h,polIdx,PodIdx,cargotype,grade,vessel,pl,pd,c,g,lower,dischargeFlag):
    try:
        if result in str(h,pl,pd,c,g):
            print(str(h,pl,pd,c,g), "====>",lower,"=======>",result.get(str(h,pl,pd,c,g),0))
            if not dischargeFlag:
                if lower==1:
                    result.get(str(h, pl, pd, c, g), 0) - (result.get(str(h,pl,pd,c,g),0) * 0.10)
                else:
                    result.get(str(h, pl, pd, c, g), 0) + (result.get(str(h, pl, pd, c, g), 0) * 0.10)
            else:
                return result.get(str(h, pl, pd, c, g), 0)
        else:
            if lower==1:
                return 0
            else:
                hold_weight_max_bounds = getHoldWeightMaxBounds(vessel, h)
                cargo_grade_max_bounds = getCargoGradeMaxBounds(cargodetails, polIdx, cargotype, grade)

                return cargo_grade_max_bounds if hold_weight_max_bounds > cargo_grade_max_bounds else hold_weight_max_bounds
    except Exception as e:
        print("The Exception in setOnBoardPMMData Method:", e)

# def getBallastPOLWt(listofPOL,Tankdetail,WBlist,cargodetails,tankdata,trim,WtItems,Hydro_Data,vesselMain,ballastWt,Message,WBallastWt):
#     PolBallastWt={}
#     try:
#         LSWeight=getLightshipweight(WtItems)
#         draft: float = 0
#         swDensity: float = 1.025
#         voyageDisplacement: float = 0
#         voyageDisp: float = 0
#         displacement: float = 0
#         MaxBallastWT: float = 0
#         BallastWt: float = 0
#         voyageDisp = getVoyageDisplacement(listofPOL, Hydro_Data, trim, vesselMain)
#
#         for i in range(len(listofPOL)):
#             draft = 0
#             cargoWt: float = getTotalWeightOf_POL(cargodetails, listofPOL[i])
#             constWt: float = getWeightConstantWeight(tankdata, listofPOL[i])
#             WBWt: float = readBallastWt(ballastWt, cargoWt)
#
#             if cargoWt > 0:
#                 MaxBallastWT = voyageDisp - (LSWeight + cargoWt + constWt)
#                 BallastWt = getBallastTankTotalWt(listofPOL[i], Tankdetail, WBlist)
#             elif cargoWt == 0:
#                 BallastWt = getTargetTrim_value(listofPOL[i], trim,col)
#                 MaxBallastWT = BallastWt
#
#             if (Message == ""):
#                 if (BallastWt > MaxBallastWT):
#                     if (MaxBallastWT < 0):
#                         BallastWt = 0
#                         MaxBallastWT = 0
#                     else:
#                         BallastWt = MaxBallastWT
#                 if (BallastWt > WBWt):
#                     BallastWt = WBWt
#                 PolBallastWt[str(listofPOL[i], "MaxBALLASTWT")]=round(BallastWt,0)
#             elif (Message == "Infeasible" or Message == "Second"):
#                 PolBallastWt[str(listofPOL[i], "MaxBALLASTWT")] = round(WBallastWt.get((listofPOL[i], "MaxBALLASTWT"),0), 0)
#                 BallastWt=round(WBallastWt.get(listofPOL[i], "MaxBALLASTWT"),0)
#                 PolBallastWt[listofPOL[i],"BALLASTWT"]=BallastWt
#                 PolBallastWt[str(listofPOL[i], "DRAFT")]=round(WBallastWt.get((listofPOL[i],"DRAFT"),0),2)
#                 PolBallastWt[str(listofPOL[i], "LCF")]=round(WBallastWt.get(str(listofPOL[i], "LCF"),0),2)
#             elif (Message == "third"):
#                 PolBallastWt[str(listofPOL[i], "MaxBALLASTWT") ]=round(WBallastWt.get(str(listofPOL[i], "MaxBALLASTWT"),0),0)
#                 BallastWt =round(WBallastWt.get(str(listofPOL[i], "BALLASTWT"), 0), 0)
#                 PolBallastWt[str(listofPOL[i], "BALLASTWT")]=BallastWt
#                 displacement = round(WBallastWt.get("DISPL", 0),0)
#             newDisplacement: float = (LSWeight + cargoWt + constWt + BallastWt)
#             if (Message == ""):
#                 if (voyageDisp < newDisplacement):
#                     BallastWt = voyageDisp - (LSWeight + cargoWt + constWt)
#                     newDisplacement = (LSWeight + cargoWt + constWt + BallastWt)
#
#             tmp = trim[trim['polidx'] == listofPOL[i]]
#             if (len(tmp, 1) > 0):
#                 var = getStatbilityData(
#                     tmp[1].trim,
#                     round(newDisplacement, digits=0),
#                     Hydro_Data,
#                 )



def getPOLOnBoardWeight(WBallastWt,polindex,listofPOD,cargoTypesize,grade_size,noOfHolds,listofPOL):
    cargowt = 0
    try:
        for h in range(len(noOfHolds)):
            for p in range(len(polindex)):
                for pd in range(len(listofPOD)):
                    for c in range(len(cargoTypesize)):
                        for g in range(len(grade_size)):
                            if polindex >= listofPOL[p] and polindex < listofPOD[pd]:
                                if WBallastWt in f"{h},{p},{pd},{c},{g}":
                                    cargowt+=WBallastWt.get(str(h, p, pd, c, g),0)
    except Exception as e:
        print("The Exception in getPOLOnBoardWeight Method:", e)
    return cargowt

def getMaxDraft(polIdx,trim):
    maxDraft = 0
    try:
        tmp = trim[trim["polidx"]==polIdx]
        if len(tmp)>0:
            draftlimit =  tmp.iloc[0]['draftlimit']
            arrivaldraft=tmp.iloc[0]['arrivaldraft']
            loadlinedraft = tmp.iloc[0]['loadlinedraft']
            maxDraft=min(min(draftlimit, arrivaldraft), min(loadlinedraft, 100))
    except Exception as e:
        print("The Exception in getMaxDraft Method:", e)
    return maxDraft

def getMaxDraft2(polIdx,trim):
    maxDraft = 0
    try:
        tmp = trim[trim["polidx"] == polIdx]
        if len(tmp) > 0:
            draftlimit = tmp.iloc[0]['draftlimit']
            arrivaldraft = tmp.iloc[0]['arrivaldraft']
            maxDraft = min(draftlimit, arrivaldraft)
    except Exception as e:
        print("The Exception in getMaxDraft2 Method:", e)
    return maxDraft


def getPOLPort(loadlistcargo):
    data=[]
    try:
        for row in loadlistcargo:
            data.append(row["polIdx"])
        if len(data) > 0:
            data=list(set(data))
    except Exception as e:
        print("The Exception in getPOLPort Method:", e)
    return data.sort()

def getPortList(cargodetails):
    listofPOL=[]
    try:
        listofPOL = getPODPort(cargodetails)
        listofPOD = getPOLPort(cargodetails)

        for p in range(len(listofPOD)):
            if listofPOD[p] not in listofPOL:
                listofPOL.append(listofPOD[p])
    except Exception as e:
        print("The Exception in getPortList Method:", e)
    return listofPOL.sort()

def getPortDisplacement(listofPOL,Hydro_Data,trim,vesselMain,polindex,vslcode):
    voyageDisp = 1000000
    portDisp={}
    swDensity = 1.025
    voyageDisplacement = 0
    departdisdp = 0.0
    Arrivaldisdp = 0.0
    try:
        tmp = trim[trim["polidx"] == polindex]
        if len(tmp) > 0:
            loadlineDISPL = getLoadLineDisplacement(vslcode, tmp[1].draftLoadLine)
            portdraft = tmp[0]["draftlimit"]  # current port
            arrivaldraft = tmp[0]["arrivaldraft"]  # nextport
            print("Hydro_Data", Hydro_Data)
            Depvar = getStatbilityinfo(tmp[0]["trim"], tmp[0]["draftlimit"], Hydro_Data)  # draftLimit
            DepportDISPL = (Depvar.get("DISPL", 0) / 1.025) * tmp[0]["seaWaterDensity"]  # sea water norm draftLimit
            ##displacement for arrival at port p for draftlimit and trim
            arrvar = getStatbilityinfo(tmp[0]["trim"], tmp[0]["arrivaldraft"], Hydro_Data)  # arrival
            # arrival displacement based upon port draft and  arrival density
            arrivalportDISPL = (arrvar.get( "DISPL", 0) / 1.025) * tmp[0]["arrivalswdensity"]  # sea water normailize
            departdisdp = min(DepportDISPL, loadlineDISPL)
            Arrivaldisdp = min(arrivalportDISPL, loadlineDISPL)
    except Exception as e:
        print("The Exception in getPortDisplacement Method:", e)
    return departdisdp,Arrivaldisdp

def getPortDisplacement2(listofPOL,Hydro_Data,apiurl,trim,vesselMain,polindex,vslcode):
    voyageDisp = 1000000
    portDisp={}
    swDensity = 1.025
    voyageDisplacement = 0
    departdisdp = 0.0
    Arrivaldisdp = 0.0
    # api_url=apiurl(localpath,vsl)
    try:
        print("listofPOL",type(listofPOL),listofPOL)
        print("trim",trim)
        tmp = [row for row in trim if row["polidx"] == polindex]
        # api_url = "http://bcap-ecs-new-develop-1876779902.ap-southeast-1.elb.amazonaws.com/bcap/api/"
        if len(tmp) > 0:
            # print("tmp",tmp[0]["loadwaterline"])
            loadlineDISPLD = getLoadLineDisplacement(vslcode, apiurl ,tmp[0]["loadwaterline"])
            portdraft = tmp[0]["draftlimit"]  # current port
            arrivaldraft = tmp[0]["arrivaldraft"]  # nextport
            Depvar = getStatbilityinfo(tmp[0]["trim"], tmp[0]["draftlimit"], Hydro_Data)  # draftLimit
            DepportDISPL = (Depvar.get("DISPL",0)/1.025) * tmp[0]["seaWaterDensity"]
            departdisdp = min(DepportDISPL, loadlineDISPLD)
        return departdisdp
    except Exception as e:

        print("The Exception in getPortDisplacement2 Method:", e)
        tb = traceback.extract_tb(e.__traceback__)
        print(f"Error occurred on line{tb[-1].lineno}")
    return departdisdp


def getVoyageDisplacement(listofPOL,Hydro_Data,trim,vesselMain):
    voyageDisp = 1000000
    try:
        draft = 0
        swDensity = 1.025
        voyageDisplacement = 0
        for p in range(len(listofPOL)):
            tmp = trim[trim["polidx"] == listofPOL[p]]
            if len(tmp)>0:
                maxDraft = getMaxDraft(listofPOL[p], trim)
                density = getTdensity_value(listofPOL[p], trim,"seaWaterDensity")
                loadlineDraft = getTargetTrim_value(listofPOL[p], trim,"loadlinedraft")

                if (loadlineDraft > maxDraft):
                    draft = maxDraft
                    var = getStatbilityinfo(tmp[0]["trim"], draft, Hydro_Data)
                    lcf = getLCF(var, tmp[0]["trim"], draft, vesselMain)
                    var = getStatbilityinfo(tmp[0]["trim"], round(lcf, 2), Hydro_Data)
                    DISPL = var.get("DISPL", 0)
                    voyageDisplacement =(DISPL / getTdensity_value(listofPOL[p], trim,"seaWaterDensity")) * swDensity
                else:
                    draft = loadlineDraft
                    var = getStatbilityinfo(tmp[0]["trim"], draft, Hydro_Data)
                    lcf = getLCF(var, tmp[0]["trim"], draft, vesselMain)
                    var = getStatbilityinfo(tmp[0]["trim"], round(lcf, 2), Hydro_Data)
                    voyageDisplacement = var.get( "DISPL", 0)
                if (voyageDisp > voyageDisplacement):
                    voyageDisp = voyageDisplacement

    except Exception as e:
        print("The Exception in getVoyageDisplacement Method:", e)
    return voyageDisp


def getTrimpercentage(sPOL,trim,df,Trim,MeanDraft,vesselMain):
    result: float = 0.0
    try:
        tmp = trim[trim["polidx"] == sPOL]
        if len(tmp)>0:
            var = getStatbilityinfo(tmp[0]["trim"], (MeanDraft), df)
            MeanDraft = round(MeanDraft, 2)
            if (len(var) > 0):
                result = 0
    except Exception as e:
        print("The Exception in getTrimpercentage Method:", e)
    return result

def getBallastTankIndex(Tanklist,tankName):
    index = 0
    try:
        for i in range(len(Tanklist)):
            if (str(Tanklist[i]) == tankName):
                return i
    except Exception as e:
        print("The Exception in getBallastTankIndex Method:", e)
    return index


def getPOLPortIdx(wtItems):
    data=[]
    try:
        for i ,row in wtItems.iterrows():
            data.append(row["polidx"])
        if len(data) > 0:
            data =list(set(data))
    except Exception as e:
        print("The Exception in getPOLPortIdx Method:", e)
    return data

def getPODPortIdx(wtItems):
    data=[]
    try:
        for i,row in wtItems.iterrows():
            data.append(row["podidx"])
        if len(data) > 0:
            data = list(set(data))
    except Exception as e:
        print("The Exception in getPODPortIdx Method:", e)
    return data

def getlistofTankName(wtItems,polIdx):
    data = []
    try:
        for i,row in wtItems.iterrows():
            if row["polidx"]==polIdx:
                data.append(row["weightitem"])
    except Exception as e:
        print("The Exception in getlistofTankName Method:", e)
    return data


import requests
import json




import requests
import json


def getLoadLineDisplacementAD(vslCode, api_url, LoadLineDraftD, LoadLineDraftA):
    try:
        apixx = api_url + "masterapi/vesselmaster/" + vslCode
        r = requests.get(apixx)
        #         print("r",r)

        print("inside getLoadLineDisplacementAD")
        print("inside getLoadLineDisplacementAD")

        data = r.text
        #         print("data",data)
        dic = json.loads(data)
        #         print("dic",dic)

        loadlinelimit = dic[1]
        #         print("loadlinelimit",loadlinelimit)

        DloadlineDraft = [row for row in loadlinelimit if row.get("loadwaterline", 0) == LoadLineDraftD]
        AloadlineDraft = [row for row in loadlinelimit if row.get("loadwaterline", 0) == LoadLineDraftA]

        Ddisp = DloadlineDraft[0].get("displacement", 0)
        Adisp = AloadlineDraft[0].get("displacement", 0)
        print("Ddisp,Adisp", Adisp, Ddisp)

        return Ddisp, Adisp

    except Exception as e:
        print("The Exception in getLoadLineDisplacement Method:", e)

    return 0


def getLoadLineDisplacement(vslCode,apiurl, LoadLineDraft):
    try:
        apixx = apiurl + "masterapi/vesselmaster/" + vslCode
        r = requests.get(apixx)

        data = r.text
        dic = json.loads(data)
        print("dic:", dic)

        loadlinelimit = dic[1]

        loadlineDraft = [row for row in loadlinelimit if row.get("loadwaterline", 0) == LoadLineDraft]
        print("LoadLineDraft", loadlineDraft)

        return loadlineDraft[0].get("displacement", 0)

    except Exception as e:
        print("The Exception in getLoadLineDisplacement Method:", e)

    return 0
def getSeawaterDensity(polIdx,inputdata):
    seaWaterDensity = 1.025
    try:
        tmp = [row for row in inputdata if row['polidx'] == polIdx and row['types'].upper() == "S"]
        if len(tmp) >0:
            seaWaterDensity = tmp["seaWaterDensity"]
    except Exception as e:
        print("The Exception in getSeawaterDensity Method:", e)
    return seaWaterDensity

def getCurrentPortTankWeight(scenarioid,apiurl,version,polIndex):
    try:
        # apiurl = "http://10.254.16.12:8080/api/v1/scenarios/"
        apixx = apiurl + scenarioid + version
        r = requests.get(apixx)

        print("inside getCurrentPortTankWeight")
        print("inside getCurrentPortTankWeight")

        data = r.text
        dic = json.loads(data)

        PortTankDetail = dic[0].get("portTankDetail", 0)
        tankdetail=[row for row in PortTankDetail if row['portindex'] == polIndex ]
        sumTankweight = 0
        for n in range(1,len(tankdetail)):
            if (
                    tankdetail[n].get( "stankcategory", "") == "FO" or
                    tankdetail[n].get( "stankcategory", "") == "FW" or
                    tankdetail[n].get( "stankcategory", "") == "DO"
            ):
                sumTankweight+=tankdetail[n].get("dweight",0)
        Schedule=dic.get("Schedule",[])

        if len(Schedule) >0:
            # schedule=[row for row in Schedule if row['Portindex'] == polIndex ]
            schedule = list(filter(lambda row: row.get("Portindex", 0) == polIndex, Schedule))
            # consumption at port +1
            InputTankDetail = dic.get( "InputTankDetail", [])
            # perday consumption rate at port p+1
            DOCinputtank=list(filter(lambda row: row.get("inputName", 0) == "DOC at Port", InputTankDetail))
            # DOCinputtank =filter(row -> get(row, "inputName", 0) == "DOC at Port", InputTankDetail)
            FOCinputtank=list(filter(lambda row: row.get("inputName", 0) == "FOC at Port", InputTankDetail))
            FWinputtank=list(filter(lambda row: row.get("inputName", 0)=="FW Consumption at Sea",InputTankDetail))
            doctotal=schedule[1].get("terminalTime", 0)* DOCinputtank[1].get("inputValue", 0)
            foctotal=schedule[1].get("terminalTime", 0)* FOCinputtank[1].get("inputValue", 0)
            fwtotal=schedule[1].get("terminalTime", 0)* FWinputtank[1].get("inputValue", 0)
            if sumTankweight >0:
                return  sumTankweight - (doctotal + foctotal + fwtotal) if sumTankweight > (
                            doctotal + foctotal + fwtotal) else (doctotal + foctotal + fwtotal) - sumTankweight
            else:
                return (doctotal + foctotal + fwtotal)
    except Exception as e:
        print("The Exception in getSeawaterDensity Method:", e)
        return 0


def getPortDraft(listofPOL,Hydro_Data,trim,vesselMain,polindex,tankdata,scenarioid,version,vesselcode):
    voyageDisp = 1000000
    portDisp={}
    swDensity :float = 1.025
    portDraft :float = 0
    arrdraft :float= 0
    departdraft :float = 0
    loadlineDraft :float = 0
    try:
        minDraft :float = 100
        tmp=[row for row in trim if row['polidx'] == polindex]

        if len(tmp)>0:
            maxDraft :float = getMaxDraft(polindex, trim)
            density :float = getSeawaterDensity(polindex, trim)
            loadlineDraft = getTargetTrim_value(polindex, trim,"loadlinedraft")

            loadDISPL :float = getLoadLineDisplacement(vesselcode, tmp[0]["draftLoadLine"])
            portdraft=tmp[0]["draftlimit"]
            arrivaldraft :float=tmp[0]["arrivaldraft"]


            departureTank = getWeightConstantWeight(tankdata, polindex)
            arrivalTank = getWeightConstantWeight(tankdata, ((polindex + 1)))
            arrivalportloadedtankWeight =getCurrentPortTankWeight(scenarioid, version, (polindex + 1))
            arrivalTank-=arrivalportloadedtankWeight

            consumption = departureTank - arrivalTank

            Depvar = getStatbilityinfo(tmp[0]["trim"], tmp[0]["draftlimit"], Hydro_Data)
            DepportDISPL = (Depvar.get( "DISPL", 0) / 1.025) * tmp[0]["seaWaterDensity"]

            displ = (DepportDISPL / tmp[0]["seaWaterDensity"]) * 1.025

            arrvar = getStatbilityData(tmp[0]["trim"], displ, Hydro_Data)

            departdraft=arrvar.get("DRAFT", 0)

            arrvar = getStatbilityinfo(tmp[0]["trim"], tmp[0]["arrivaldraft"], Hydro_Data)
            arrivalportDISPL = (arrvar.get( "DISPL", 0) / 1.025) * tmp[0]["arrivalswdensity"]

            displ = (arrivalportDISPL / tmp[0]["arrivalswdensity"]) * 1.025

            arrvar = getStatbilityData(tmp[0]["trim"], displ, Hydro_Data)

            arrdraft = arrvar.get( "DRAFT", 0)

            if (arrivalportDISPL < DepportDISPL):
                arrivalwithoutConsume = arrivalportDISPL + consumption
                arrivalwithoutConsume =((arrivalwithoutConsume / tmp[0]["seaWaterDensity"]) * 1.025)
                arrivalportDISPL = arrivalwithoutConsume
                displ = arrivalportDISPL
                arrvar = getStatbilityData(float(tmp[0]["trim"]), float(displ), Hydro_Data)

                arrdraft = arrvar.get( "DRAFT", 0)
            portDraft = min(min(arrdraft, departdraft), min(voyageDisp, loadlineDraft))
    except Exception as e:
        print("The Exception in getPortDraft Method:", e)
    return portDraft



def getPortDraftLimit(Hydro_Data,vesselcode,trim,polindex):
    voyageDisp = 1000000
    portDisp = {}
    swDensity: float = 1.025
    portDraft: float = 0
    arrdraft: float = 0
    departdraft: float = 0
    loadlineDraft: float = 0
    try:
        minDraft = 100
        tmp=[row for row in trim if row['polidx'] == polindex]
        if len(tmp)>0:
            maxDraft :float = getMaxDraft(polindex, trim)
            density :float = getSeawaterDensity(polindex, trim)
            loadlineDraft = getTargetTrim_value(polindex, trim,"loadlinedraft")

            loadDISPL: float = getLoadLineDisplacement(vesselcode, tmp[0]["draftLoadLine"])
            portdraft = tmp[0]["draftlimit"]
            arrivaldraft: float = tmp[0]["arrivaldraft"]

            Depvar = getStatbilityinfo(tmp[0]["trim"], tmp[0]["draftlimit"], Hydro_Data)
            DepportDISPL = (Depvar.get("DISPL", 0) / 1.025) * tmp[0]["seaWaterDensity"]

            displ = (DepportDISPL / tmp[0]["arrivalswdensity"]) * 1.025

            arrvar = getStatbilityData(tmp[0]["trim"], float(displ), Hydro_Data)

            departdraft = arrvar.get( "DRAFT", 0)

            arrvar=getStatbilityinfo(tmp[0]["trim"], tmp[0]["arrivaldraft"], Hydro_Data)
            arrivalportDISPL :float = (arrvar.get("DISPL", 0) / 1.025) * tmp[0]["arrivalswdensity"]
            displ=(arrivalportDISPL / tmp[0]["arrivalswdensity"]) * 1.025

            arrvar = getStatbilityData(float(tmp[0]["trim"]), float(displ), Hydro_Data)

            arrdraft = arrvar.get("DRAFT", 0)

            portDraft = min(arrdraft, departdraft)
    except Exception as e:
        print("The Exception in getPortDraftLimit Method:", e)
    return portDraft






















































































