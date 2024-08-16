import pandas as pd

def readCargoDetatil(localpath):
    try:
        df=pd.read_csv(localpath)
        return df
    except Exception as e:
        print("The Exception in readCargoDetatil Method:", e)


def readSpecificgravity(df):
    SFCargoGrade={}
    try:
        for index, row in df.iterrows():
            SFCargoGrade[str(row["Name"].upper() ,row["grade"].upper())]=row["stowagefactor"]
        return SFCargoGrade
    except Exception as e:
        print("The Exception in readSpecificgravity Method:", e)
        return -1

def getMaxDischarge(df):
    maxDisch = False
    try:
        for row in df:
            if row["maxdischarge"].upper() == "Y":
                maxDisch=True
        return maxDisch
    except Exception as e:
        print("The Exception in getMaxDischarge Method:", e)
        return -1

def getMaxDischargePolIndex(df):
    portindex = 0
    try:
        for index, row in df.iterrows():
            if row["MaxDisch"].upper() == "Y":
                portindex=row["podIdx"]
        return portindex
    except Exception as e:
        print("The Exception in getMaxDischargePolIndex Method:", e)
        return -1

def getpreviousPODPOL(df,p):
    pol=[]
    pod=[]
    try:
        for index , row in df.iterrows():
            if p >= row["polIdx"]:
                pol.append(row["polIdx"])
                pod.append(row["polIdx"])

            pol=sorted(list(set(pol)))
            pod = sorted(list(set(pod)))
        return pol,pod
    except Exception as e:
        print("The Exception in getpreviousPODPOL Method:", e)
        return -1

def getCargoGradeMaxBounds(df,polIdx,cargotype,grade):
    try:
        weight = 0
        for i ,row in df.iterrows():
            if (polIdx + cargotype.upper() + grade.upper() == row['podIdx'] + row['name'].upper() + row['grade'].upper()):
                weight +=row["weight"]

        return weight
    except Exception as e:
        print("The Exception in getCargoGradeMaxBounds Method:", e)
        return -1

def getPODPort(df):
    data=[]
    try:
        for row in df:
            data.append(row["podIdx"])
        if len(data)>0:
            data=sorted(list(set(data)))
        return data
    except Exception as e:
        print("The Exception in getPODPort Method:", e)
        return -1
# getCargoType,getPOLCargoType,getPOLCargoGrade,getCargoGrade
def getcargo_value(df,col):
    data=[]
    try:
        for index, row in df.iterrows():
            data.append(row[col])
        if len(data)>0:
            data=list(set(data))
        return data
    except Exception as e:
        print("The Exception in getPODPort Method:", e)
        return -1

def getTotalWeightOf_POL_POD_Cargo2(df,polIdx,cargotype,grade):
    try:

        sumweight = 0
        for row in df:
            # print("krypto",row,polIdx,cargotype,grade)
            # print(  str(row['podIdx']) + row['name'].upper() + row['grade'].upper())
            if (str(polIdx) + cargotype.upper() + grade.upper() == str(row['polIdx']) + row['name'].upper() + row['grade'].upper()):
                # print("insdide")
                sumweight +=float(row["weight"])
        return sumweight
    except Exception as e:
        print("The Exception in getTotalWeightOf_POL_POD_Cargo2 Method:", e)
        return -1

def getTotalWeightOf_POL(df,polIdx):
    sumWeight = 0.0
    try:
        for index,row in df.iterrows():
            if polIdx >= row["polIdx"] and polIdx < row["podIdx"]:
                sumWeight +=row["WEIGHT"]
        return sumWeight
    except Exception as e:
        print("The Exception in getTotalWeightOf_POL Method:", e)
        return -1