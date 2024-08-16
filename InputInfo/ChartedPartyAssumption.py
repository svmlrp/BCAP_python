import pandas as pd

def readChartedPartyAssumption(localpath):
    try:

        df=pd.read_csv(localpath)
        return df
    except Exception as e:
        print("The Exception in readChartedPartyAssumption Method:", e)
        return -1

#getCharterPartyWeight ,getCharterPartyPercentage
def getCharterPartyWeight_percent(df,col):
    chartedpartyWeight={}
    try:
        for index,row in df.iterrows():
            chartedpartyWeight[str(row["polIdx"],row["podIdx"],row["cargo"].upper(),row["grade"].upper())]=row[col]
        return chartedpartyWeight
    except Exception as e:
        print("The Exception in getCharterPartyWeight_percent Method:", e)
        return -1

def getcharterpartyMinPercentageValue2(polIdx,cargo,grade,df):
    try:
        minweight=0.0
        maxweight=0.0
        custrequest=0.0
        minrequest=0.0
        podIdx=[]
        minrequest2=[]
        for row in df:
            # print("polIdx=====", polIdx, row["polIdx"])
            # print("cargo=====", cargo.upper(), row["cargo"].upper() )
            # print("grade=====", grade.upper() , row["grade"].upper() )
            if str(polIdx) == str(row["polIdx"]) and cargo.upper() == row["cargo"].upper() and grade.upper() == row["grade"].upper() :
                # print("The")
                minweight +=row["contract_qty"] - (row["contract_qty"] * (row["plusorminus"] / 100))
                maxweight+=row["contract_qty"] + (row["contract_qty"] * (row["plusorminus"] / 100))
                custrequest+=row["customer_request"]
                minrequest= minweight if minweight >= custrequest else custrequest if maxweight > custrequest else minweight
                minweight1=row["contract_qty"] - (row["contract_qty"]*(row["plusorminus"] / 100))
                maxweight1=row["contract_qty"] + (row["contract_qty"]*(row["plusorminus"] / 100))
                custrequest1=row["customer_request"]
                minrequest1=minweight1 if minweight1 >= custrequest1 else custrequest1 if maxweight1 > custrequest1 else minweight1
                minrequest2.append(minrequest1)
                podIdx.append(row["podIdx"])
                # print(" minrequest, minrequest2, podIdx", minrequest, minrequest2, podIdx)
        return  minrequest, minrequest2, podIdx
    except Exception as e:
        print("The Exception in getcharterpartyMinPercentageValue2 Method:", e)
        return -1

def getCharterPartyWeight(charterParty):
    chartedpartyWeight={}
    try:
        for app in charterParty:
            key = ''.join([
                app['polIdx'],
                app['podIdx'],
                app['cargo'].upper(),
                app['grade'].upper()
            ])
            chartedpartyWeight[key] = app['contract_qty']
        return chartedpartyWeight
    except Exception as e:
        print("The Exception in getCharterPartyWeight Method:", e)
        return -1

def getcharterpartyMinCargopol(polIdx,cargo,grade,charterParty):
    try:
        minweight=0.0
        maxweight=0.0
        custrequest=0.0
        minrequest=0.0
        minqty=0.0
        for app in charterParty:
            if polIdx == app['polIdx'] and cargo.upper() == app['cargo'].upper() and grade.upper() == app['grade'].upper():
                minweight += app['contract_qty'] - (app['contract_qty'] * (app['plusorminus'] / 100))
                maxweight+= app['contract_qty'] + (app['contract_qty'] * (app['plusorminus'] /100))
                custrequest+=app['customer_request']
                minrequest= minweight if minweight >= custrequest else custrequest if maxweight > custrequest else minweight
                minweight1=app['contract_qty'] - app['contract_qty'] * (app['plusorminus'] / 100)
                maxweight1=app['contract_qty'] + app['contract_qty'] * (app['plusorminus'] / 100)
                custrequest1=app['customer_request']
                minrequest1=minweight1 if minweight1 >= custrequest1 else custrequest1 if maxweight1 > custrequest1 else minweight1
                minqty+=minrequest1
        return minqty
    except Exception as e:
        print("The Exception in getcharterpartyMinCargopol Method:", e)
        return -1




def getcharterpartyMinCargopod(polIdx,cargo,grade,charterParty):
    try:
        minweight :float = 0
        maxweight :float = 0
        custrequest :float = 0
        minrequest :float = 0
        minqty = 0
        for i,rows in charterParty.iterrows():
            if (
              (  polIdx == rows["podIdx"]) and
                cargo.upper() == rows["cargo"].upper() and
                grade.upper() == rows["grade"].upper()
            ):
                minweight += rows['contract_qty'] - (rows['contract_qty'] * (rows['plusorminus'] / 100))
                maxweight+= rows['contract_qty'] + (rows['contract_qty'] * (rows['plusorminus'] /100))
                custrequest+=rows['customer_request']
                minrequest= minweight if minweight >= custrequest else custrequest if maxweight > custrequest else minweight
                minweight1=rows['contract_qty'] - (rows['contract_qty'] * (rows['plusorminus'] / 100))
                maxweight1=rows['contract_qty'] + (rows['contract_qty'] * (rows['plusorminus'] / 100))
                custrequest1=rows['customer_request']
                minrequest1=minweight1 if minweight1 >= custrequest1 else custrequest1 if maxweight1 > custrequest1 else minweight1
                minqty+=minrequest1
        return minqty
    except Exception as e:
        print("The Exception in getcharterpartyMinCargopod Method:", e)
        return -1


