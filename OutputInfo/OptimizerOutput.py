import urllib.parse
import requests
import json
def getMaximumId(vslcode,scenarioid):
    Maxid = 1
    try:
        apixx = apiurl +"optimizerapi/optresult/"
        xx = urllib.parse.quote(scenarioid)
        url = apixx + xx + "/maxid/" + vslcode
        response = requests.get(url)
        data = response.text
        dic = json.loads(data)
        Maxid=dic.get("id",1)
    except Exception as e:
        print("The Exception in getMaximumId Method: ", e)
    return Maxid

def saveOutputDetails(apiurl,WeightItemData,outputMaster,gzvalues,airDraftOutput,otherDetails,stabilityOuput,stressValues):
    outputMasterData={}
    weightitemData={}
    gzvaluesData={}
    airDraftOutputData={}
    otherDetailsData={}
    stabilityOuputData={}
    stressValuesData={}
    try:
        outputMasterData = setOuputMaster(outputMaster)
        weightitemData = setOutputWeightItems(WeightItemData)
        stabilityOuputData = setStabilityData(stabilityOuput)
        stressValuesData = setStressValue(stressValues)
        airDraftOutputData = setAirDraftOutput(airDraftOutput)
        gzvaluesData = setGZvalue(gzvalues)
        otherDetailsData = setOtherDetail(otherDetails)
        inputparms={}

        inputparms = {
            "MasterResult": outputMasterData,
            "WeightItems": weightitemData,
            "StabilityValues": stabilityOuputData,
            "StressValues": stressValuesData,
            "AirDraftValues":airDraftOutputData,
            "GZvalues":gzvaluesData,
            "OtherDetails":otherDetailsData}
        input = json.dumps(inputparms)
        print("input=saveOutputDetails=", input)

        apixx = apiurl + "optimizerapi/output/saveoutput"
        headers = {"Content-Type": "application/json"}

        r = requests.post(apixx, headers=headers, data=input)
        print(r.text)
    except Exception as e:
        print("The Exception in saveOutputDetails Method:", e)


def setOutputWeightItems(WeightItemData):
    WeightItems = []
    try:
        for i in range(len(WeightItemData)):
            tempData={}
            tempData["bcapRefNumber"]= WeightItemData[i]["bcapRefNumber"]
            tempData["pol"] =WeightItemData[i]["pol"]
            tempData["pod"]=WeightItemData[i]["pod"]
            tempData["type"]=WeightItemData[i]["type"]
            tempData["itemname"]=WeightItemData[i]["itemname"]
            tempData["category"]=WeightItemData[i]["category"]
            tempData["volumePer"]=WeightItemData[i]["volumePer"]
            tempData["weight"]=WeightItemData[i]["weight"]
            tempData["lcg"]=WeightItemData[i]["lcg"]
            tempData["vcg"]=WeightItemData[i]["vcg"]
            tempData["cond_result"]=WeightItemData[i]["cond_result"]
            WeightItems.append(tempData)
    except Exception as e:
        print("The Exception in setOutputWeightItems Method:", e)
    return WeightItems

# def setStabilityData(StabilityData):
#     StabilityDetails = []
#     try:
#         for i in range(len(StabilityData)):
#             tempData={}
#             tempData["bcapRefNumber"]= StabilityData[i]["bcapRefNumber"]
#             tempData["pol"] =StabilityData[i]["pol"]
#             tempData["pod"]=StabilityData[i]["pod"]
#             tempData["displacement"]=StabilityData[i]["displacement"]
#             tempData["meanDraft"]=StabilityData[i]["meanDraft"]
#             tempData["aftDraft"]=StabilityData[i]["aftDraft"]
#             tempData["trim"]=StabilityData[i]["trim"]
#             tempData["tpc"]=StabilityData[i]["tpc"]
#             tempData["lcg"]=StabilityData[i]["lcg"]
#             tempData["lcb"]=StabilityData[i]["lcb"]
#             tempData["mtc"]=StabilityData[i]["mtc"]
#             tempData["lcf"]=StabilityData[i]["lcf"]
#             tempData["tkm"]=StabilityData[i]["mcf"]
#             tempData["vcg"]=StabilityData[i]["vcg"]
#             StabilityDetails.append(tempData)













