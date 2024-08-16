from InputInfo.Schedule import getPort_index
from InputInfo.CargoDetail import getMaxDischarge,getPODPort
from Tankinfo.Tank import readTank
from Tankinfo.WNTankList import getHoldBallastTank
from Vesselinfo.VesselParticulars import readVesselParticulars
from exp_building.Expression_BM_SF import bmsfcalc
from exp_building.Expression_Ballast import  readexp_Ballast
from NonlinearInfo.commonfunction import get_ballast_tank_details,get_holds_ballast_tank_weight,get_holds_ballast_tank_name,set_chartedparty_constraints,getVolumeConstraints,getWeightConstraints,getadjacentMixedBinarylink,AutoAllocation5hold,AutoAllocation7hold,AutoAllocation9hold,AutoAllocation11hold
from NonlinearInfo.Nonlinear_modelling_printing_SF_BM import getBallastTankWtConstraints
from InputInfo.TargetTrim import getBallastPOL,readParameter
from PreprocessInfo.preprocess import getPOLPort
import gurobipy as gp
from gurobipy import GRB
import time
import pandas as pd

# from V.Json_reader_2 import list_of_cargo_and_grade,list_of_pol_and_pod


# def list_of_cargo_and_grade(ChartedPartyAssumption):
#     cargo_set = set()
#     grade_set = set()
#     for party in ChartedPartyAssumption:
#
#         cargo_set.add(party.techname)
#         grade_set.add(party.grade)
#
#     return list(cargo_set), list(grade_set)
# def list_of_pol_and_pod(schedule):
#     pol_set = set()
#     pod_set = set()
#     for party in schedule:
#         pol_set.add(party.pol)
#         pod_set.add(party.pod)
#
#     return list(pol_set), list(pod_set)

def PMMOptimizer(vesseldata,apiurl,localpath,first_pass):
    # print(vesseldata)
    # print(apiurl)

    # print(localpath)


    chartedpartyRefNo=vesseldata.get("chartedpartyRefNo",0)
    CargoDetails=vesseldata.get("CargoDetails",0)
    # print("CargoDetails====",CargoDetails)
    # print("chartedpartyRefNo",chartedpartyRefNo)
    # print("CargoDetails",CargoDetails)
    inputs_flags = vesseldata.get("Input_Flags", 0)
    print("inputs_flags",inputs_flags)
    chartedPartyFlag=inputs_flags.get("chartedPartyFlag",0)
    # print("chartedPartyFlag",chartedPartyFlag)

    Schedule=vesseldata.get("Schedule",0)
    # print("Schedule", Schedule)
    pschedule = getPort_index(Schedule,"Portindex")
    # print("pschedule",pschedule)
    parameter = vesseldata.get("Parameter", [])
    ChartedParty = vesseldata.get("ChartedPartyAssumption", [])
    tankdata = vesseldata.get("Tank", [])
    WBlist=vesseldata.get("WBTankList", [])
    Arrivaltank = vesseldata.get("ArrivalTank", [])
    vesselcode=vesseldata.get("Vesselcode", [])
    WaterBallast=vesseldata.get("WaterBallast", [])
    noOfHolds=len(vesseldata)
    # print(vesselcode)
    #
    tank=readTank(localpath)
    # print(tank)
    ChartedPartyAssumption=vesseldata.get("ChartedPartyAssumption", [])
    # print("ChartedPartyAssumption",ChartedPartyAssumption)
    cargo = list({item['techname'] for item in ChartedPartyAssumption})
    grade = list({item['grade'] for item in ChartedPartyAssumption})
    # print(cargo,grade)
    polIdxs = list({item['polIdx'] for item in CargoDetails})
    podIdxs = list({item['podIdx'] for item in CargoDetails})
    listofCargo = list({item['name'] for item in CargoDetails})
    listofgrade = list({item['grade'] for item in CargoDetails})
    SFCargoGrade= {(item['name'], item['grade']): item['stowagefactor'] for item in CargoDetails}
    # print(polIdxs,podIdxs)
    ports = list({item['Portindex'] for item in Schedule})

    # getUserAllocation()
    # print("ports",ports)
    # Assuming you have imported the VesselParticulars class from the module
    # from your_module import VesselParticulars

    VesselParticulars = readVesselParticulars(localpath)
    trim=readParameter(localpath)
    print("trim",trim)

    listofPOL=[]
    listofPOL2=[]
    listofPOD=[]
    if len(CargoDetails) == 0:
        listofPOL.append(1)
        listofPOL2 = getBallastPOL(parameter)
        listofPOD.append(2)
    else:
        listofPOL = getPOLPort(CargoDetails)
        listofPOL2 = getBallastPOL(parameter)
        listofPOD = getPODPort(CargoDetails)



    # print("VesselParticulars=====",VesselParticulars)
    HoldNos = sorted(list({item['Hold No.'] for item in VesselParticulars}))
    # Create a dictionary mapping Hold No. to Max. Weight (MT)
    weight_by_hold = {int(item['Hold No.']): float(item['Max. Weight (MT)']) for item in VesselParticulars}
    # print("weight_by_hold",weight_by_hold)
    maxbounds_by_hold = {int(item['Hold No.']): float(item['Volume without Hatch']) for item in VesselParticulars}


    # Function to get Max. Weight (MT) based on Hold No.
    # def get_max_weight(hold_no):
    #     return weight_by_hold.get(hold_no, 0)

    # HoldNos = (list({item['Hold No.'] for item in VesselParticulars}))
    # print("CargoDetails",len(CargoDetails))

    mod1=gp.Model()

    if first_pass == True and len(CargoDetails) > 0 :
        # mod1.addVar(lb=0,ub=1,name="B")

        B=mod1.addVars(range(1,len(HoldNos)+1), range(1,len(ports)+1), range(1,len(cargo)+1), range(1,len(grade)+1), vtype=GRB.BINARY, name="B")
        adjcargo2=mod1.addVars(range(1,len(HoldNos)), range(1,len(ports)+1), range(1,len(cargo)+1),range(1,len(grade)+1), vtype=GRB.BINARY, name="adjcargo2")
        mod1.update()

    if len(CargoDetails) > 0:

        # mod1.display()
        X=mod1.addVars(range(1, len(HoldNos) + 1), range(1, len(ports) + 1), range(1, len(cargo) + 1),range(1, len(grade) + 1), vtype=GRB.CONTINUOUS, name="X")
        mod1.update()

        ##addee for testing
        # X = mod1.addVars(range(len(HoldNos) ), range(len(ports)), range(len(cargo)),
        #                  range(len(grade)), vtype=GRB.CONTINUOUS, name="X")
        # mod1.update()

        # print("cargo===", cargo,grade)

        for h in range(1, len(HoldNos) + 1):
            hold_capacity_mt = weight_by_hold.get(h, 0)
            # print("hold_capacity_mt",weight_by_hold)

            for i in range(1, len(ports) + 1):
                for j in range(1, len(cargo) + 1):
                    for k in range(1, len(grade) + 1):
                        # print()
                        mod1.addConstr(X[h, i, j, k] >= 0.0, name=f"lowerboundHold_{h}")
                        mod1.update()
                        mod1.addConstr(X[h, i, j, k] <= hold_capacity_mt, name=f"MaxCapacityHold_{h}")
                        mod1.update()

    # print("ports====",ports)
    cargo = list({item['techname'] for item in ChartedPartyAssumption})
    bmsf_objects = bmsfcalc.from_csv(localpath)
    listofTank = bmsfcalc.get_Ballast_tank_list(bmsf_objects)
    ballast_tank_list=bmsfcalc.get_Ballast_tank_list(bmsf_objects)
    ballast_tanks=bmsfcalc.get_countBallastTank(bmsf_objects)
    tnk_ballast=mod1.addVars(range(1,ballast_tanks+1), range(1, len(ports)), vtype=GRB.CONTINUOUS, name="tnk_ballast")
    mod1.update()
    for i in range(1, ballast_tanks+1):
        # print("ballast_tank_list[i]",ballast_tank_list[i-1])
        # print("i",i)
        unpumpable,capacity=get_ballast_tank_details(WaterBallast, i, ballast_tank_list[i-1])
        for j in range(1, len(ports) ):

            mod1.addConstr(tnk_ballast[i, j] >= unpumpable, name=f"lowerboundBallast_{i}")
            mod1.update()
            mod1.addConstr(tnk_ballast[i, j] <= capacity, name=f"upperboundBallast_{i}")
            mod1.update()

    # get_holds_ballast_tank_weight(WaterBallast, 1, tankname)
    holdasballast=get_holds_ballast_tank_name(WaterBallast, 1)
    b_holdasballast = mod1.addVars(range(1, len(ports)),range(1, len(holdasballast )+ 1), vtype=GRB.BINARY,
                               name="b_holdasballast")
    # mod1.update()
    Btnk = mod1.addVars(range(1, len(ports)), range(1, len(holdasballast) + 1), vtype=GRB.BINARY,
                           name="Btnk")

    cb_hold = mod1.addVars(range(1, len(ports)), range(1, len(holdasballast) + 1), vtype=GRB.BINARY,
                                   name="cb_hold")
    autoallocationFlag=inputs_flags.get("autoallocationFlag",0)

    if first_pass == True:
        print("autoallocationFlag",autoallocationFlag==True)
        if autoallocationFlag == True and (len(CargoDetails) >= 1) and (
                len(grade) >= 2 or len(cargo) >= 2) and len(polIdxs) >= 2:
            print("please",noOfHolds)
            if noOfHolds == 5:
                print("noOfHolds====5")
                AutoAllocation5hold(mod1,X,B, HoldNos, cargo, grade, polIdxs, CargoDetails, ChartedParty, VesselParticulars,
                                listofCargo, listofgrade)
            elif noOfHolds==7:
                print("noOfHolds====7")
                AutoAllocation7hold(mod1, X, B, HoldNos, cargo, grade, polIdxs, CargoDetails, ChartedParty,
                                    VesselParticulars,
                                    listofCargo, listofgrade)
            elif noOfHolds == 9:
                print("noOfHolds====9")
                AutoAllocation9hold(mod1, X, B, HoldNos, cargo, grade, polIdxs, CargoDetails, ChartedParty,
                                    VesselParticulars,
                                    listofCargo, listofgrade)
            elif noOfHolds == 11:
                print("noOfHolds===11")
                AutoAllocation11hold(mod1, X, B, HoldNos, cargo, grade, polIdxs, CargoDetails, ChartedParty,
                                        VesselParticulars,
                                        listofCargo, listofgrade)


    # print("afkbvkjabkjf")
    VolumeFlag=inputs_flags.get("VolumeFlag",0)
    weightFlag=inputs_flags.get("weightFlag",0)
    PreferedFlag=inputs_flags.get("PreferedFlag",0)
    mixedCargoFlag=inputs_flags.get("mixedCargoFlag",0)
    # print("mixedCargoFlag",mixedCargoFlag)
    AdjacentCargoFlag=inputs_flags.get("AdjacentCargoFlag",0)
    ArrivalDeapartureflag=inputs_flags.get("ArrivalDeaparture",0)
    # print("VesselParticulars",VesselParticulars)
    set_chartedparty_constraints(mod1,X, chartedPartyFlag,polIdxs,podIdxs,cargo,grade,HoldNos,CargoDetails,ChartedParty,VesselParticulars,pschedule,listofCargo,listofgrade)
    getVolumeConstraints(mod1, X, VesselParticulars, VolumeFlag, HoldNos, cargo, grade, polIdxs, podIdxs, listofCargo,
                         listofgrade, CargoDetails)
    getWeightConstraints(mod1,X, weightFlag, HoldNos, cargo, grade, polIdxs, VesselParticulars)

    getadjacentMixedBinarylink(mod1, X, B, adjcargo2, mixedCargoFlag, AdjacentCargoFlag, HoldNos, cargo, grade, polIdxs,
                               CargoDetails, VesselParticulars)
    BallestTankWTFlag=inputs_flags.get("BallestTankWTFlag",0)
    mod1.update()
    if not getMaxDischarge(CargoDetails):
        # print("Please")
        getBallastTankWtConstraints(mod1,Btnk,tnk_ballast,BallestTankWTFlag,polIdxs,listofPOL2,trim,WBlist,tank,CargoDetails,listofTank,pschedule)
    # Avaraible for hatch cover air draft at first and last port
    Airdrafth1 = 0.0
    Airdrafth5 = 0.0
    # number of ballast tank
    # numbertank = count(exp_Ballast -> exp_Ballast.ExpType == "Cargo", exp_Ballast)
    # exp_Ballast_list=Ballast.ballast_objects
    exp_Ballast_list = readexp_Ballast(localpath)
    # print("exp_Ballast_list",exp_Ballast_list["Expreesion type(Cargo/Ballast)"])
    numbertank = sum(1 for i,exp_Ballast in exp_Ballast_list.iterrows() if exp_Ballast["Expreesion type(Cargo/Ballast)"] == "Cargo")
    # print("Number of  ",numbertank)
    portcounter = 0
    for p in range(len(pschedule)):
        ttarr = 1
        if ArrivalDeapartureflag==True:
            ttarr = 2
        else:
            ttarr = 1
        if p==1:
            ttarr = 1
        elif p == len(pschedule):
            ttarr = 1

        # print("ttarr",ttarr)
        for tt in range(1,ttarr+1):
            portcounter += 1
            # Avaraible for hatch cover air draft at first and last port
            Airdrafth1 = 0.0
            Airdrafth5 = 0.0
            zz = 1 / 1.025  # m3/tonnes
            print("WBlist",WBlist)
            # number of hold as ballast tank at port p
            holdtank = getHoldBallastTank(WBlist, pschedule[p])
            print("Hold",holdtank)
            # hold moments variables
            WB3BHMOM = 0
            WB3BH = 0
            zz3 = 0
            zhold = len(holdtank)
            ######################################################################################################################
            ####################################################################################################################

            ######   Hold AS Ballast Tank constraint formulation start only departing port
            ##################################################################################################################
            ####################################################################################################################
            Hold_tanks_list = bmsfcalc.get_Hold_tanks_list(bmsf_objects)
            for t in range(1,zhold):
                hh = Hold_tanks_list[t]
                holdweight = getHoldWeightMaxBounds(vessel, (hh))



    ####################################################################################################################
    ##################################################################################################
    ### Displacement calc start
    ###################################################################################################
    ####################################################################################################################

    # if firstPass==True:
    #     if p == 1:

    # mod1.display()
    # mod1.computeIIS()
    # mod2.write("mod2_TIR_CHECK.ilp")
    # mod1.write("D:/BCAP_python/Bcap_12.ilp")
    # print("polIdxs=====",polIdxs)
    mod1.setObjective(gp.quicksum(X[h,i,j,k] for h in range(1, len(HoldNos) + 1) for i in polIdxs for j in range(1, len(cargo) + 1) for k in range(1, len(grade) + 1)),GRB.MAXIMIZE)
    mod1.optimize()

    # for var in mod1.getVars():
    #     print(var)
    # set_chartedparty_constraints(mod1, inputs_flags,polIdxs,podIdxs,cargo,grade,HoldNos,CargoDetails,ChartedParty,VesselParticulars,pschedule )

    # mod1.display()



