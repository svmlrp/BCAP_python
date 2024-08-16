import pandas as pd

def readTank(localpath):
    # print("localpath_tank",localpath)
    # print("nnnnnnn====",f"{localpath}\Tank.csv")
    df_Tank=pd.read_csv(f"{localpath}\Tank.csv")
    return df_Tank


# df=readTank("C:/Users/deenadayalan.pu/Downloads/files/files/Tank.csv")
# print(df)


def getTankWtItemName(tankvalue, tank_name):
    try:
        tank = tankvalue[tankvalue['Tank Name'] == tank_name]
        # print(tankvalue['Tank Name'],tank_name)
        if len(tank) > 0:
            return tank.iloc[0]['WeightItemName']
        else:
            return tank.iloc[0]['Tank Name']
    except Exception as e:
        print("The exception in get_tank_wt_item_name ===>", e)


# df_nn=get_tank_wt_item_name(df,"NO.1 W.B.T.(P)")
# print(df_nn)

def getTankWeight(df,tank_name):
    tankWeight=0
    try:
        tank = df[df['Tank Name'] == tank_name]
        tankWeight+=tank["Capacity"]*tank["Density"]
    except Exception as e:
        print("The exception in getTankWeight ===>", e)
    return tankWeight.iloc[0]
# df_nn=getTankWeight(df,"NO.1 W.B.T.(P)")
# print(df_nn)
# optimized code for getTankCategory,getTankAptDist,getTankFwdDist,getTankLCG
def gettankcol(df,col1,col2):
    tankCategory = {}
    try:
        for index, row in df.iterrows():
            tankCategory[row[col1]] = row[col2]
    except Exception as e:
        print("The Exception in getTankCategory Method", e)
    return tankCategory

# gettankcol(df_Tank,"Tank Name","Tank Category") #getTankCategory
#
# gettankcol(df_Tank,"Tank Name","Aft Dist from AP (m)") #getTankAptDist
#
# gettankcol(df_Tank,"Tank Name","Fwd Dist from AP (m)") #getTankFwdDist
#
# tanklcg=gettankcol(df,"Tank Name","LCGLPP") #getTankLCG

def getTankLCGValue(tank_lcg, tank_name):
    tankLCG = 0.0
    try:
        tankLCG = tank_lcg.get(tank_name, 0.0)
    except Exception as e:
        print("The Exception in getTankLCGValue Method", e)
    return tankLCG
# df_nn=getTankLCGValue(tanklcg,"NO.1 W.B.T.(P)")
# print(df_nn)

def readTankDetails(localpath):
    df = pd.read_csv(localpath + "Tank.csv")
    TankDistance = {}
    TankApt = {}
    TankFwd = {}

    for index, row in df.iterrows():
        TankApt[row.iloc[3]] = row.iloc[11]
        TankFwd[row.iloc[3]] = row.iloc[12]

    TankDistance["TankApt"] = TankApt
    TankDistance["TankFwd"] = TankFwd

    return TankDistance
# df_nn=readTankDetails("C:/Users/deenadayalan.pu/Downloads/files/files/")
# print(df_nn)
def getTankDensity(tank_list, tank_name):
    try:
        # Find the index of the tank name in the tank_list
        index = tank_list.index(tank_name)
        # Use the index to get the density from the DataFrame
        return df.loc[index, 'Density']
    except Exception as e:
        print("The exception in getTankDensity ===>", e)
        return 1

# tank_list = df["Tank Name"].tolist()
# df_nn = getTankDensity(tank_list, "NO.1 W.B.T.(P)")
# print(df_nn)