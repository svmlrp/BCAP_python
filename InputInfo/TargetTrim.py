import pandas as pd

def readParameter(localpath):
    try:
        df=pd.read_csv(f"{localpath}TargetTrim.csv")
        return df
    except Exception as e:
        print("The Exception in readParameter Method:", e)

def getPostiveSFLimit(frameno,polIdx,trim,SFPosLim,SFPortPosLim):
    try:
        if getSeaOrPort(polIdx, trim) ==0:
            # to get "SEA" SF postive limit based upon sfvalue from parameter section of input json
            return SFPosLim.get(frameno, 0) * getSFPercentage(polIdx, trim,"")
        else:
            return SFPortPosLim.get(frameno, 0) * getSFPercentage(polIdx, trim)
    except Exception as e:
        print("The Exception in getPostiveSFLimit Method:", e)
        return -1


def getPostiveBMLimit(frameno,polIdx,trim,BMPosLim,BMPortPosLim):
    try:
        if getSeaOrPort(polIdx, trim) == 0:
            return BMPosLim.get(frameno, 0) * getBMPercentage(polIdx, trim)
        else:
            return BMPortPosLim.get(frameno, 0) * getBMPercentage(polIdx, trim)
    except Exception as e:
        print("The Exception in getPostiveBMLimit Method:", e)
        return -1


def getNegativeSFLimit(frameno,polIdx,trim,SFNegLim,SFPortNegLim):
    try:
        if getSeaOrPort(polIdx, trim) == 0 :
            return SFNegLim.get(frameno, 0) * getPercentage(polIdx, trim,col)
        else:
            return SFPortNegLim.get(frameno, 0) * getPercentage(polIdx, trim,col)

    except Exception as e:
        print("The Exception in getNegativeSFLimit Method:", e)
        return -1

def getNegativeBMLimit(frameno,polIdx,trim,BMNegLim,BMPortNegLim):
    try:
        if getSeaOrPort(polIdx, trim) == 0 :
            return BMNegLim.get(frameno, 0) * getPercentage(polIdx, trim,col)
        else:
            return BMPortNegLim.get(frameno, 0) * getPercentage(polIdx, trim,col)

    except Exception as e:
        print("The Exception in getNegativeBMLimit Method:", e)
        return -1
#getTargetTrim,getBallest,getDeBallest,getLoadline,getBallestTankWt,
# getDraftlimit,getHogorSagValue,getMeanDraft,getArrivalDraft,getStressONOff,getLoadLineDraft,getAirDraft
def getTargetTrim_value(polIdx, trim, col):
    targetTrim = 0
    try:
        # Filter the dictionary
        tmp = [item for item in trim if item['polidx'] == polIdx]
        if tmp:
            # Access the first matching item and get the value for the specified column
            targetTrim = tmp[0][col]
        return targetTrim
    except Exception as e:
        print(f"The Exception in getTargetTrim_value {col} Method:", e)
        return -1



def getNoHatchcoverandDraft(polIdx,trim):
    NoOfHatchcovers = 0
    HatchcoverAirdraft = 0
    try:
        tmp = trim[trim['polidx'] == polIdx]
        if len(tmp) > 0:
            NoOfHatchcovers = (tmp.iloc[0]["NumberofHatchCovers"])
            HatchcoverAirdraft = (tmp.iloc[0]["airdraftHatchcover"])
        return NoOfHatchcovers,HatchcoverAirdraft
    except Exception as e:
        print("The Exception in getNoHatchcoverandDraft Method:", e)
        return -1

#getSFPercentage,getBMPercentage

def getPercentage(polIdx,trim,col):
    value=0
    try:
        tmp = trim[trim['polidx'] == polIdx]
        if len(tmp) > 0:
            value = tmp.iloc[0][col] / 100
        return value
    except Exception as e:
        print(f"The Exception in getPercentage{col} Method:", e)
        return -1

#getSeaWaterDensity,getArrivalSWDensity
def getTdensity_value(polIdx,trim,col):
    targetTrim = 1.025
    try:
        tmp = trim[trim['polidx'] == polIdx]
        if len(tmp) >0:
            targetTrim = tmp.iloc[0][col]
        return targetTrim
    except Exception as e:
        print(f"The Exception in getTargetTrim_value{col} Method:", e)
        return -1


def getHogorSag(polIdx,trim,col):
    hogorsag = ""
    try:
        tmp = trim[trim['polidx'] == polIdx]
        if len(tmp) > 0:
            hogorsag = tmp.iloc[0]['hogorsag']
        return hogorsag
    except Exception as e:
        print(f"The Exception in getHogorSag Method:", e)
        return -1


def getSeaOrPort(polIdx,trim):
    seaPorton = 0
    try:
        tmp = trim[trim['polidx'] == polIdx]
        if len(tmp) > 0:
            # Checking if the seaport value in the first row is 0 or 1
            if tmp.iloc[0]['seaport'] == 0 or tmp.iloc[0]['seaport'] == 1:
                seaPorton=tmp.iloc[0]['seaport']
        return seaPorton
    except Exception as e:
        print(f"The Exception in getSeaOrPort Method:", e)
        return -1

def getBallastPOL(trim):
    data=[]
    try:
        for  row in trim:
            data.append(row["polidx"])
        if len(data) >0 :
            data=list(set(data))
        return data.sort()
    except Exception as e:
        print(f"The Exception in getBallastPOL Method:", e)
        return -1



def getBallastPOD(trim):
    data = []
    try:
        for i, row in trim.iterrows():
            data.append(row["polidx"])
        if len(data) > 0:
            data = sorted(list(set(data)))
        return data
    except Exception as e:
        print(f"The Exception in getBallastPOD Method:", e)
        return -1



