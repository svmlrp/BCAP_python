import pandas as pd

def readWBTankList(localpath):
    df_WBTankList=pd.read_csv(localpath)
    return df_WBTankList
# WBlist=readWBTankList("C:/Users/deenadayalan.pu/Downloads/files/files/WBTankList.csv")
# tank=readWBTankList("C:/Users/deenadayalan.pu/Downloads/files/files/Tank.csv")

def getunpumpableWt(tankname, Tankdetail, WBlist, POLIndex):
    unpumpableWt = 0
    try:
        for index, row in WBlist.iterrows():
            for row1 in Tankdetail.itertuples(index=False):
                if (row["Tank Name"] == row1[0] and row1[0] == tankname and row["POL Idx"] == POLIndex):
                    unpumpableWt = row["unpumpable WT"]
    except Exception as e:
        print("The Exception in getunpumpableWt Method:", e)
    return unpumpableWt

# Example usage
# df2 = getunpumpableWt("NO.1 W.B.T.(P)",tank,  WBlist, 1)
# print(df2)
def get_tankname_max_weight(tankname, tankvalue, WBlist, POLIndex):
    tankWeight = 0.0
    try:
        for _, wb in WBlist.iterrows():
            for _, app in tankvalue.iterrows():
                if (
                        wb['Tank Name'] == app['Tank Name'] and
                        app['Tank Name'] == tankname and
                        wb['POL Idx'] == POLIndex
                ):
                    tankWeight = app['Capacity'] * app['Density'] * (wb['Max Percentage'] / 100)
                    # Uncomment the following line to print the values for debugging
                    # print(f"app.capacity={app['capacity']}, app.density={app['density']}, wb.maxPercentageAllowed={wb['maxPercentageAllowed']}")
                    break
            if tankWeight > 0:
                break
    except Exception as e:
        print("The exception in get_tankname_max_weight ===>", e)

    return tankWeight
# df2 = get_tankname_max_weight("NO.1 W.B.T.(P)",tank,  WBlist, 1)
# print(df2)
def getBallastTankTotalWt(WBlist,POLIndex,Tankdetail):
    tankwt=0
    try:
        for index, row in WBlist.iterrows():
            if row["POL Idx"]==POLIndex:
                for index, row1 in Tankdetail.iterrows():
                    if row1["Tank Name"]==row["Tank Name"]:
                        tankwt +=row1["Capacity"] * row1["Density"]
    except Exception as e:
        print("The Exception in getBallastTankTotalWt Method:", e)
    return tankwt
# df2 = getBallastTankTotalWt(  WBlist,1, tank)
# print(df2)
def getlistofTank(WBlist,POLIndex):
    data=[]
    try:
        for index, row in WBlist.iterrows():
            if row["POL Idx"]==POLIndex and row["holdTank"].upper() != "Y":
                data.append(row["Tank Name"])
    except Exception as e:
        print("The Exception in getlistofTank Method:", e)
    return data
# df2 = getlistofTank(  WBlist,1)
# print(df2)
def getHoldTank(WBlist,TankName,polindex):
    data = []
    try:
        for index, row in WBlist.iterrows():
            if row["Tank Name"] == TankName and row["holdTank"].upper() != "Y" and polindex == row["POL Idx"]:
                return True
    except Exception as e:
        print("The Exception in getHoldTank Method:", e)
    return False
# df2 = getHoldTank(  WBlist,'NO.1 W.B.T.(S)',1)
# print(df2)
def get_tank_max_weight(tankvalue, WBlist):
    tankWeight = 0.0
    try:
        for _, app in tankvalue.iterrows():
            if (WBlist['Tank Name'] == app['Tank Name']).any():
                tankWeight = app['Capacity'] * app['Density'] * (WBlist['Max Percentage'] / 100)
                break  # If you want to stop after finding the first match
    except Exception as e:
        print("The exception in get_tank_max_weight ===>", e)

    return tankWeight.iloc[0]
# df2 = get_tank_max_weight(tank,WBlist)
# print(df2)
def getHoldBallastTank(WBlist,polindex):
    WBTankIndex=[]
    try:
        for row in WBlist:
            if row["holdtank"].upper() =="Y" and row["portindex"] == polindex:
                WBTankIndex.append(row["tankname"])
    except Exception as e:
        print("The Exception in getHoldBallastTank Method:", e)
    return WBTankIndex
# df2 = getHoldBallastTank(WBlist,1)
# print(df2)
def getWBPOLTankList(WBlist):
    WBPOLTankList = {}
    try:
        for index, row in WBlist.iterrows():
            # Check if 'holdTank' and 'POL Idx' columns exist
            if 'holdTank' not in row or 'POL Idx' not in row:
                raise KeyError(f"Expected columns 'holdTank' or 'POL Idx' not found. Columns present: {WBlist.columns}")

            if row["holdTank"].upper() != "Y":
                if row['POL Idx'] in WBPOLTankList:
                    tempTanklist = WBPOLTankList[row['POL Idx']]
                else:
                    tempTanklist = []

                tempTanklist.append(row)
                WBPOLTankList[row['POL Idx']] = tempTanklist
    except Exception as e:
        print("The Exception in getWBPOLTankList Method:", e)
    return WBPOLTankList
# df2 = getWBPOLTankList(WBlist)
# print(df2)
def getWUIWBPOLTankList(WBlist):
    WBPOLTankList={}
    tempTanklist=[]
    TankSequence=[]
    TN=["AFT PEAK T.(C)","NO.1 W.B.T.(P)","NO.1 W.B.T.(S)","NO.2 W.B.T.(P)","NO.2 W.B.T.(S)","NO.3 W.B.T.(P)","NO.3 W.B.T.(S)","NO.4 W.B.T.(P)","NO.4 W.B.T.(S)","NO.5 W.B.T.(S)","NO.5 W.B.T.(S)"]
    TankSequence.append(TN)
    try:
        len=0
        TankName=""
        for index, row in WBlist.iterrows():
            len=0
            if row["Tank Name"].upper() != TankName:
                if row['POL Idx'] in WBPOLTankList:
                    tempTanklist = WBPOLTankList.get(row['POL Idx'], 0)
                else:
                    tempTanklist = []
                    tempTanklist.append(row)
                    WBPOLTankList[row['POL Idx']] = tempTanklist
    except Exception as e:
        print("The Exception in getWBPOLTankList Method:", e)
    return WBPOLTankList


# df2 = getWUIWBPOLTankList(WBlist)
# print(df2)


