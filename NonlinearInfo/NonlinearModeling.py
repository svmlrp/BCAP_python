from InputInfo.Schedule import getPort_index
from InputInfo.CargoDetail import getMaxDischarge,getPODPort,getpreviousPODPOL
from exp_building.Expression_hatch import find_hatch_value,readexp_Hatch
from Tankinfo.Tank import readTank,getTankWeight
from Tankinfo.WNTankList import getHoldBallastTank
from StabilityInfo.SFandBMFrameStation import getFrameStationItem,readSFandBMFrameStation,get_LCG_DISTAP_WTRATIO,getCargoHold
from Vesselinfo.VesselParticulars import readVesselParticulars,getHoldWeightMaxBounds
from exp_building.Expression_BM_SF import readexp_BMSF,find_Frame_value,Frame_hold,getcountBMusedFrame,polynomial_frame,getBallast_tank_list,
from exp_building.Expression_Ballast import  readexp_Ballast
from NonlinearInfo.commonfunction import get_ballast_tank_details,get_holds_ballast_tank_weight,get_holds_ballast_tank_name,set_chartedparty_constraints,getVolumeConstraints,getWeightConstraints,getadjacentMixedBinarylink,AutoAllocation5hold,AutoAllocation7hold,AutoAllocation9hold,AutoAllocation11hold,getpodforpol,getmaxqtypod
from NonlinearInfo.Nonlinear_modelling_printing_SF_BM import getBallastTankWtConstraints
from InputInfo.TargetTrim import getBallastPOL,readParameter,getTargetTrim_value,getTdensity_value,getPostiveSFLimit,getNegativeSFLimit
from PreprocessInfo.preprocess import getPOLPort,getPortDisplacement2,getAboveframeStation,getMaxHoldNoAtEachFrame
# from InputInfo.Json_reader_2 import vessel_api
from StabilityInfo.HydroStaticData import readHydroStatic
# from exp_building.Expression_BM_SF import getSFusedFrame
from InputInfo.ChartedPartyAssumption import getcharterpartyMinCargopod,getcharterpartyMinPercentageValue2
import gurobipy as gp
from InputInfo.TankData import getWeightConstantLMOM,getWCTankList
from Vesselinfo.Lightship import getLightShipLMOM
import numpy as np
from StabilityInfo.SoundingData import get_souding_lcg_and_vcg
from NonlinearInfo.commonfunction import getpolforpod
from Vesselinfo.Lightship import getLightshipweight,readLightShip
from exp_building.Expression_deflection import find_deflection_value,polynomial_deflection,getUDDraftMConstwfame,readexp_Deflection,getUDDraftMDegreewfame
from gurobipy import GRB
from exp_building.Expression_trim import find_trim_value,polynomial_trim
from InputInfo.TankData import getWeightConstantWeight
from exp_building.Expression_Ballast import find_value
from StabilityInfo.FrameStation import frame_col
import time
import pandas as pd
import traceback
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
    WBlist=vesseldata.get("WaterBallast", [])
    Arrivaltank = vesseldata.get("ArrivalTank", [])
    vesselcode=vesseldata.get("Vesselcode", [])
    # WaterBallast=vesseldata.get("WaterBallast", [])
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
    Hydro_value = readHydroStatic(localpath)


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
    bmsf_objects = readexp_BMSF(localpath)
    listofTank = getBallast_tank_list(bmsf_objects)
    ballast_tank_list=getBallast_tank_list(bmsf_objects)

    # ballast_tanks=find_Frame_value(bmsf_objects,Frame_number,cols)
    tnk_ballast=mod1.addVars(range(1,len(pschedule)-1), range(1,len(listofTank)+1), vtype=GRB.CONTINUOUS, name="tnk_ballast")
    # print("ballast_tanks",ballast_tanks,ports)
    # print("pschedule",pschedule,listofTank)

    # Tnk=mod1.addVars(range(1,pschedule),range(1,len(listofTank)+1))
    mod1.update()
    for i in range(1, len(pschedule)-1):
        # print("ballast_tank_list[i]",ballast_tank_list[i-1])
        # print("i",i)
        unpumpable,capacity=get_ballast_tank_details(WBlist, i, ballast_tank_list[i-1])
        for j in range(1, len(ports)+1 ):

            mod1.addConstr(tnk_ballast[i, j] >= unpumpable, name=f"lowerboundBallast_{i}")
            mod1.update()
            mod1.addConstr(tnk_ballast[i, j] <= capacity, name=f"upperboundBallast_{i}")
            mod1.update()

    # get_holds_ballast_tank_weight(WaterBallast, 1, tankname)
    holdasballast=get_holds_ballast_tank_name(WBlist, 1)
    b_holdasballast = mod1.addVars(range(1, len(ports)),range(1, len(holdasballast )+ 1), vtype=GRB.BINARY,
                               name="b_holdasballast")
    # mod1.update()
    Btnk = mod1.addVars(range(1, len(ports)), range(1, len(holdasballast) + 1), vtype=GRB.BINARY,
                           name="Btnk")
    # tnk = mod1.addVars(range(1, len(pschedule)), range(1, len(holdasballast) + 1), vtype=GRB.BINARY,
    #                     name="tnk")

    CBhold = mod1.addVars(range(1, len(ports)), range(1, len(holdasballast) + 1), vtype=GRB.BINARY,
                                   name="CBhold")
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
    TrimConstFlag=inputs_flags.get("TrimConstFlag",0)
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
    xtemp = [0.0, 0.0]
    WtItem=readLightShip(localpath)
    TrimConstFlag = inputs_flags.get("TrimConstFlag", 0)
    exp_Hatchlist=readexp_Hatch(localpath)
    maxDispalcement = find_hatch_value(exp_Hatchlist,"MaxDisplcament")
    getholdasBltTank_displ(mod1,ArrivalDeapartureflag,Btnk,X,CBhold,parameter,localpath,first_pass,cargo,grade,VesselParticulars,TrimConstFlag,xtemp,pschedule,WBlist,bmsf_objects,CargoDetails,listofCargo,listofgrade)
    # mod1.display()
    displacement_calc_start(mod1, WtItem, pschedule,Hydro_value, localpath, apiurl,tnk_ballast, Btnk, X, listofTank, maxDispalcement, inputs_flags,
                            tank, parameter, WBlist, vesseldata, vesselcode, first_pass, cargo, grade, CargoDetails,
                            listofCargo, listofgrade, noOfHolds, ChartedParty)
    #
    # print("Number of  ",numbertank)
    # getVesselCalculatorInput(mod1,
    #                          WtItems,
    #                          tankdataxx,
    #                          pl,
    #                          listofPOL,
    #                          soundingData,
    #                          listofCargo,
    #                          listofGrade,
    #                          listofPOD,
    #                          noOfHolds,
    #                          WBlist,
    #                          SFCargoGrade,
    #                          vessel,
    #                          AftDistfromAP,
    #                          FwdDistfromAP,
    #                          TankAptDist,
    #                          TankFwdDist,
    #                          tank,
    #                          TankCategory,
    #                          x,
    #                          last_port,
    #                          listofPOL2,
    #                          listofTank,
    #                          pschedule,
    #                          cargodetails,
    #                          Arrival,
    #                          Tnktemp,
    #                          BTnktemp, )




    mod1.setObjective(gp.quicksum(
        X[h, i, j, k] for h in range(1, len(HoldNos) + 1) for i in polIdxs for j in range(1, len(cargo) + 1) for k in
        range(1, len(grade) + 1)), GRB.MAXIMIZE)
    mod1.optimize()
def getholdasBltTank_displ(mod1,ArrivalDeapartureflag,Btnk,X,CBhold,parameter,localpath,first_pass,cargo,grade,VesselParticulars,TrimConstFlag,xtemp,pschedule,WBlist,bmsf_objects,CargoDetails,listofCargo,listofgrade):
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
            # print(".WBlist",WBlist)
            # number of hold as ballast tank at port p
            holdtank = getHoldBallastTank(WBlist, pschedule[p])
            # print("Hold",holdtank)
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
            Frame_number=bmsf_objects["Frame_number"]

            for t in range(1,zhold):
                Hold_tanks_list = Frame_hold(bmsf_objects, Frame_number, "Hold_tanks_list")
                hh = Hold_tanks_list
                holdweight = getHoldWeightMaxBounds(VesselParticulars, hh)
                holdweight2 = holdweight * 7
                if first_pass==True:
                    if p==1:
                        cargo_load = []
                        for c in range( len(cargo) ):
                            for g in range(len(grade) ):
                                dis = getpodforpol(CargoDetails, (p), listofCargo[c], listofgrade[g])
                                if len(dis) >=1:
                                    for pd in dis:
                                        cld=mod1.addConstr(X[hh,pd,c+1,g+1]*1.0)
                                        cargo_load.append(cld)
                                else:
                                    cargo_load.append(0)
                        xclen=len(cargo_load)
                        if xclen >=1:
                            loadp=mod1.addVar(vtype=GRB.CONTINUOUS, name="loadp")
                            mod1.addConstr(loadp==gp.quicksum(cargo_load[i] for i in range(1,xclen)))
                            mod1.addConstr(loadp>= 0 - holdweight2 * (1 - CBhold[p,t]))
                            mod1.addConstr(loadp<= 0 + holdweight2 * CBhold[p,t])
                            mod1.addConstr(Btnk[p,t]+CBhold[p,t] <=1)
                            mod1.update()
                    if p > 1 and p <len(pschedule):
                        if tt == 2:
                            Arrival=False
                            cargo_load = []
                            for c in range( len(cargo) ):
                                for g in range(len(grade) ):
                                    prepol, prepod = getpreviousPODPOL(CargoDetails, p)
                                    for pl in prepol:
                                        pod12=getpodforpol(CargoDetails,pl,listofCargo[c],listofgrade[g])
                                        for d11 in pod12:
                                            if d11 >p:
                                                cld=mod1.addConstr(X[hh,d11,c+1,g+1]*1.0)
                                                cargo_load.append(cld)
                        xclen=len(cargo_load)
                        if xclen >=1:
                            loadp=mod1.addVar(vtype=GRB.CONTINUOUS, name="loadp")
                            mod1.addConstr(loadp==gp.quicksum(cargo_load[i] for i in range(1,xclen)))
                            mod1.addConstr(loadp>= 0 - holdweight2 * (1 - CBhold[p,t]))
                            mod1.addConstr(loadp <= 0 + holdweight2 * CBhold[p,t])
                            mod1.addConstr(Btnk[p,t]+CBhold[p,t] <=1)
            if first_pass==False:
                if p==1:
                    cargo_load=0.0
                    for c in range( len(cargo) ):
                        for g in range(len(grade) ):
                            dis = getpodforpol(CargoDetails, (p), listofCargo[c], listofgrade[g])
                            if len(dis) >=1:
                                for pd in dis:
                                    cargo_load+=xtemp[hh,pd,c+1,g+1]
                    if cargo_load >=1:
                        mod1.addConstr(Btnk[p,t]==0)
                if p >1 and p<len(pschedule):
                    if tt==2:
                        Arrival=False
                        cargo_load=0.0
                        for c in range( len(cargo) ):
                            for g in range(len(grade) ):
                                prepol, prepod = getpreviousPODPOL(CargoDetails, p)
                                for pl in prepol:
                                    pod12=getpodforpol(CargoDetails,pl,listofCargo[c],listofgrade[g])
                                    for d11 in pod12:
                                        if d11 >p:
                                            cargo_load+=xtemp[hh,d11,c+1,g+1]
                        if cargo_load >=1:
                            mod1.addConstr(Btnk[p,t]==0)
            #####################################################################################################################
            ####################################################################################################################
            ######   Hold As Ballast Tank constraint formulation end
            ##################################################################################################################
            ####################################################################################################################
            # Dictionary of weight items and associated frame number
            SFBMFrames=readSFandBMFrameStation(localpath)
            FmStItems = getFrameStationItem(SFBMFrames)

            # Dictionary of weight items|| frames and distance from aft perpendicular
            FmStDistAP = get_LCG_DISTAP_WTRATIO(SFBMFrames,"Dist. From AP")
            gravity = 9.80665
            # Dictionary of weight items|| frames and weight ratio
            FmStWeightRatio = get_LCG_DISTAP_WTRATIO(SFBMFrames,"Ratio")
            # Dictionary of weight items|| frames and LCG
            FmStLcgvalue = get_LCG_DISTAP_WTRATIO(SFBMFrames,"LCG(from AP) in SFBMCalc")

            # Array of cargo holds
            CargoHold = getCargoHold(SFBMFrames)
            # get trim value for port p from parameter

            TRIM2 = getTargetTrim_value(pschedule[p], parameter, "trim")

            # for ballast condition
            if TrimConstFlag == False:

                TRIM = mod1.addVar(vtype=GRB.CONTINUOUS, name="TRIM")
                # seeting lower bounds
                mod1.addConstr(TRIM >= 0)
                # seeting upper bounds
                mod1.addConstr(TRIM <= TRIM2)
            else:
                TRIM = TRIM2


                # cargo_loadf=0
                # cargo_loadf = cargo_load
                # Ballast_load=mod1.addConstr(gp.quicksum(Btnk[p-1,t] for t in range(1,len(listofTank)+1)))
                # constant1 = getWeightConstantWeight(ArrivaltankData, (pschedule[p]))
                # portDisp1 = getPortDisplacement2(pschedule, Hydro_value, parameter, vesselMain, UInt8(pschedule[p]),
                #                                  vesselcode)


    ####################################################################################################################
    ##################################################################################################
    ### Displacement calc start
    ###################################################################################################
    ####################################################################################################################
def displacement_calc_start(mod1,WtItem,pschedule,Hydro_value,localpath,apiurl,tnk_ballast,BTnk,X,listofTank,maxDispalcement,inputs_flags,tank,parameter,WBlist,vesseldata,vesselcode,first_pass,cargo,grade,CargoDetails,listofCargo,listofgrade,noOfHolds,charterparty):
    # Lightship weight
    lwt = getLightshipweight(WtItem)
    for p in range(len(pschedule)):
        if first_pass==True:
            if p == 1:
                xMincargo = 0
                xMaxcargo = 0
                cargo_load = []
                for c in range(len(cargo)):
                    for g in range(len(grade)):
                        dis = getpodforpol(CargoDetails, (p), listofCargo[c], listofgrade[g])
                        if len(dis) >= 1:
                            for pd in dis:
                                cld = mod1.addConstr(X[h, pd, c + 1, g + 1] for h in range(1,len(noOfHolds)+1))
                                cargo_load.append(cld)
                                minqty = getcharterpartyMinCargopod((pd), listofCargo[c], listofgrade[g],
                                                                    charterparty)
                                maxqty = getmaxqtypod(CargoDetails, pd, listofCargo[c], listofgrade[g],
                                                      charterparty)

                                xMincargo = xMincargo + minqty
                                xMaxcargo = xMaxcargo + maxqty
            tankdataxx=vesseldata.get("Tank", [])
            vesselMain=vesseldata.get("vesselMain", [])
            # Hydro_value=vesseldata.get("HydroStatic",[])

            constant1 = getWeightConstantWeight(tankdataxx, (pschedule[p]))
            # api_url = vessel_api.get_api_url('XXX')
            portDisp1 = getPortDisplacement2(pschedule, Hydro_value,apiurl, parameter, vesselMain, (pschedule[p]),
                                             vesselcode)
            # print("p,t",p,listofTank)
            for t in range(1, len(listofTank) + 1):
                if tnk_ballast[p + 1, t] is None:
                    print(f"Warning: tnk_ballast[{p + 1}, {t}] is None")

            # Ensure tnk_ballast values are not None before summing
            Ballast_load = mod1.addConstr(
                gp.quicksum(
                    tnk_ballast[p + 1, t] for t in range(1, len(listofTank) + 1) if tnk_ballast[p + 1, t] is not None)
            )
            # Ballast_load=mod1.addConstr(gp.quicksum(tnk_ballast[p+1,t] for t in range(1,len(listofTank)+1)))
            cargo_loadf = 0
            xc_len = len(cargo_load)
            if xc_len >=1:
                cargo_loadf = gp.quicksum(cargo_load[i] for i in range(xc_len))
            WB3BH=[]
            holdtank = getHoldBallastTank(WBlist, pschedule[p])
            zhold = len(holdtank)
            WB={}
            for t in range(zhold):
                WB[t]=mod1.addVar(vtype=GRB.CONTINUOUS, name=f"WB_{t}")
                zz3=getTankWeight(tank, holdtank[t])
                mod1.addConstr(WB[t]==zz3 * BTnk[p, t])
                WB3BH.append(WB[t])
            WB3F=0
            if zhold>=1:
                WB3F=gp.quicksum(WB3BH[i] for i in range(zhold))

            DISPL=mod1.addVar(vtype=GRB.CONTINUOUS, name="DISPL")
            mod1.addConstr(DISPL==cargo_loadf+Ballast_load+WB3F+lwt)
            mod1.addConstr(DISPL>=constant1+lwt+xMincargo)

            LoadableFlag = inputs_flags.get("LoadableFlag", 0)

            if LoadableFlag==True:
                if maxDispalcement<=portDisp1:
                    mod1.addConstr(DISPL<=maxDispalcement)
                else:
                    mod1.addConstr(DISPL<=portDisp1)
            else:
                mod1.addConstr(DISPL<=maxDispalcement)
            if p==len(pschedule):
                cargo_load = []
                xMincargo = 0
                xMaxcargo = 0
                for c in range(len(cargo)):
                    for g in range(len(grade)):
                        pol = getpodforpol(CargoDetails, (p), listofCargo[c], listofgrade[g])
                        minqtyall, minqty, podidxall = getcharterpartyMinPercentageValue2(
                            pschedule[p],
                            listofCargo[c],
                            listofgrade[g],
                            charterparty, )

                        for pd in dis:
                            cld = mod1.addConstr(X[h, pd, c + 1, g + 1] for h in range(1,len(noOfHolds)+1))
                            cargo_load.append(cld)
                            minqty = getcharterpartyMinCargopod((pd), listofCargo[c], listofgrade[g],
                                                                charterparty)
                            maxqty = getmaxqtypod(CargoDetails, pd, listofCargo[c], listofgrade[g],
                                                  charterparty)

                            xMincargo = xMincargo + minqty
                            xMaxcargo = xMaxcargo + maxqty


                cargo_loadf=0
                xc_len=len(cargo_load)
                if xc_len>=1:
                    cargo_loadf = gp.quicksum(cargo_load[i] for i in range(xc_len))
                Ballast_load=mod1.addConstr(gp.quicksum(tnk_ballast[p-1,t] for t in range(listofTank)))
                ArrivaltankD = vesseldata.get("ArrivaltankData", [])
                constant1 = getWeightConstantWeight(ArrivaltankD, (pschedule[p]))
                # api_url = vessel_api.get_api_url('XXX')
                print("getPortDisplacement2",pschedule,Hydro_value,apiurl, parameter, vesselMain, (pschedule[p]),
                                                 vesselcode)
                portDisp1 = getPortDisplacement2(pschedule, Hydro_value,apiurl, parameter, vesselMain, (pschedule[p]),
                                                 vesselcode)
                WB3BH=[]
                for t in range(zhold):
                    zz3=getTankWeight(tank, holdtank[t])
                    mod1.addConstr(WB[t]==zz3 * BTnk[p-1, t])
                    WB3BH.append(WB[t])
                WB3F=0
                if zhold>=1:
                    WB3F=gp.quicksum(WB3BH[i] for i in range(zhold))
                DISPL=mod1.addVar(vtype=GRB.CONTINUOUS, name="DISPL")
                mod1.addConstr(DISPL==cargo_loadf+Ballast_load+WB3F+lwt)
                mod1.addConstr(DISPL>=constant1+lwt+xMincargo)
                if LoadableFlag==True:
                    if maxDispalcement<=portDisp1:
                        mod1.addConstr(DISPL<=maxDispalcement)
                    else:
                        mod1.addConstr(DISPL<=portDisp1)
                else:
                    mod1.addConstr(DISPL<=maxDispalcement)
            if p>1 and p<len(pschedule):
                if tt == 1:  # Arrival
                    xMincargo = 0
                    xMaxcargo = 0
                    Arrival = True
                    cargo_load = []
                    for c in range(len(cargo)):
                        for g in range(len(grade)):
                            prepol, prepod = getpreviousPODPOL(CargoDetails, (p - 1))
                            for pl in prepol:
                                pod12 = getpodforpol(CargoDetails, (p), listofCargo[c], listofgrade[g])

                                for d11 in pod12:
                                    if d11 >=p and Arrival==True:
                                        cld = mod1.addConstr(X[h, d11, c + 1, g + 1] for h in range(1,len(noOfHolds)+1))
                                        cargo_load.append(cld)
                                        minqty = getcharterpartyMinCargopod((pd), listofCargo[c], listofgrade[g],
                                                                            charterparty)
                                        maxqty = getmaxqtypod(CargoDetails, pd, listofCargo[c], listofgrade[g],
                                                              charterparty)

                                        xMincargo = xMincargo + minqty
                                        xMaxcargo = xMaxcargo + maxqty

                    cargo_loadf=0
                    xc_len=len(cargo_load)
                    if xc_len>=1:
                        cargo_loadf = gp.quicksum(cargo_load[i] for i in range(xc_len))
                    Ballast_load=mod1.addConstr(gp.quicksum(tnk_ballast[p-1,t] for t in range(listofTank)))
                    ArrivaltankD = vesseldata.get("ArrivaltankData", [])
                    constant1 = getWeightConstantWeight(ArrivaltankD, (pschedule[p]))
                    portDisp1 = getPortDisplacement2(pschedule, Hydro_value,apiurl, parameter, vesselMain, (pschedule[p]),
                                                 vesselcode)
                    WB3BH=[]
                    for t in range(zhold):
                        zz3=getTankWeight(tank, holdtank[t])
                        mod1.addConstr(WB==zz3 * BTnk[p-1, t])
                        WB3BH.append(WB)
                    WB3F=0
                    if zhold>=1:
                        WB3F=gp.quicksum(WB3BH[i] for i in range(zhold))
                    DISPL=mod1.addVar(vtype=GRB.CONTINUOUS, name="DISPL")
                    mod1.addConstr(DISPL==cargo_loadf+Ballast_load+WB3F+lwt)
                    mod1.addConstr(DISPL>=constant1+lwt+xMincargo)
                    if LoadableFlag==True:
                        if maxDispalcement<=portDisp1:
                            mod1.addConstr(DISPL<=maxDispalcement)
                        else:
                            mod1.addConstr(DISPL<=portDisp1)
                    else:
                        mod1.addConstr(DISPL<=maxDispalcement)
                elif tt==2:
                    Arrival=False
                    cargo_load=0
                    xMincargo=0
                    xMaxcargo=0
                    for c in range(len(cargo)):
                        for g in range(len(grade)):
                            prepol, prepod = getpreviousPODPOL(CargoDetails, p)
                            for pl in prepol:
                                pod12 = getpodforpol(CargoDetails, p, listofCargo[c], listofgrade[g])
                                for d11 in pod12:
                                    if d11 >= p :
                                        cld = mod1.addConstr(X[h, d11, c + 1, g + 1] for h in range(1,len(noOfHolds)+1))
                                        cargo_load.append(cld)
                                        minqty = getcharterpartyMinCargopod((pd), listofCargo[c], listofgrade[g],
                                                                            charterparty)
                                        maxqty = getmaxqtypod(CargoDetails, pd, listofCargo[c], listofgrade[g],
                                                              charterparty)
                                        xMincargo = xMincargo + minqty
                                        xMaxcargo = xMaxcargo + maxqty
                    cargo_loadf=0
                    xc_len=len(cargo_load)
                    if xc_len>=1:
                        cargo_loadf = gp.quicksum(cargo_load[i] for i in range(xc_len))
                    Ballast_load=mod1.addConstr(gp.quicksum(tnk_ballast[p,t] for t in range(listofTank)))
                    tankdataxx=vesseldata.get("TankData", [])
                    constant1 = getWeightConstantWeight(tankdataxx, (pschedule[p]))
                    portDisp1 = getPortDisplacement2(pschedule, Hydro_value,apiurl, parameter, vesselMain, (pschedule[p]),
                                                     vesselcode)
                    WB3BH=[]
                    for t in range(zhold):
                        zz3=getTankWeight(tank, holdtank[t])
                        mod1.addConstr(WB[t]==zz3 * BTnk[p, t])
                        WB3BH.append(WB[t])
                    WB3F=0
                    if zhold>=1:
                        WB3F=gp.quicksum(WB3BH[i] for i in range(zhold))
                    DISPL=mod1.addVar(vtype=GRB.CONTINUOUS, name="DISPL")
                    mod1.addConstr(DISPL==cargo_loadf+Ballast_load+WB3F+lwt)
                    mod1.addConstr(DISPL>=constant1+lwt+xMincargo)
                    if LoadableFlag==True:
                        if maxDispalcement<=portDisp1:
                            mod1.addConstr(DISPL<=maxDispalcement)
                        else:
                            mod1.addConstr(DISPL<=portDisp1)
                    else:
                        mod1.addConstr(DISPL<=maxDispalcement)
        if first_pass==False:
            if p==1:
                cargo_load = 0
                for c in range(len(cargo)):
                    for g in range(len(grade)):
                        dis=getpodforpol(CargoDetails, p, listofCargo[c], listofgrade[g])
                        if len(dis)>=1:
                            for pd in dis:
                                for h in range(1,len(noOfHolds)+1):
                                    cargo_load+=xtemp[h, pd, c, g]

                tankdataxx=vesseldata.get("TankData", [])
                constant1 = getWeightConstantWeight(tankdataxx, (pschedule[p]))
                portDisp1 = getPortDisplacement2(pschedule, Hydro_value,apiurl, parameter, vesselMain, (pschedule[p]),
                                                 vesselcode)
                Ballast_load=mod1.addConstr(gp.quicksum(tnk_ballast[p,t] for t in range(listofTank)))
                cargo_loadf=0
                WB3BH=[]
                for t in range(zhold):
                    zz3=getTankWeight(tank, holdtank[t])
                    mod1.addConstr(WB[t]==zz3 * BTnk[p, t])
                    WB3BH.append(WB[t])
                WB3F=0
                if zhold>=1:
                    WB3F=gp.quicksum(WB3BH[i] for i in range(zhold))
                DISPL=mod1.addVar(vtype=GRB.CONTINUOUS, name="DISPL")
                if LoadableFlag==True:
                    if maxDispalcement<=portDisp1:
                        mod1.addConstr(DISPL<=maxDispalcement)
                    else:
                        mod1.addConstr(DISPL<=portDisp1)
                else:
                    mod1.addConstr(DISPL<=maxDispalcement)
                if p==len(pschedule):
                    cargo_load=0
                    for c in range(len(cargo)):
                        for g in range(len(grade)):
                            pol=getpodforpol(CargoDetails, p, listofCargo[c], listofgrade[g])
                            for pl in pol:
                                for h in range(1,len(noOfHolds)+1):
                                    cargo_load+=xtemp[h, pd, c, g]

                    cargo_loadf=0
                    cargo_loadf=cargo_load
                    Ballast_load=mod1.addConstr(gp.quicksum(tnk_ballast[p-1,t] for t in range(listofTank)))
                    ArrivaltankD=vesseldata.get("ArrivaltankData", [])
                    constant1 = getWeightConstantWeight(ArrivaltankD, (pschedule[p]))
                    portDisp1 = getPortDisplacement2(pschedule, Hydro_value,apiurl, parameter, vesselMain, (pschedule[p]),
                                                 vesselcode)
                    WB3BH=[]
                    for t in range(zhold):
                        zz3=getTankWeight(tank, holdtank[t])
                        mod1.addConstr(WB[t]==zz3 * BTnk[p-1, t])
                        WB3BH.append(WB[t])
                    WB3F=0
                    DISPL=mod1.addVar(vtype=GRB.CONTINUOUS, name="DISPL")
                    if LoadableFlag==True:
                        if maxDispalcement<=portDisp1:
                            mod1.addConstr(DISPL<=maxDispalcement)
                        else:
                            mod1.addConstr(DISPL<=portDisp1)
                    else:
                        mod1.addConstr(DISPL<=maxDispalcement)
                if p>1 and p<len(pschedule):
                    if tt==1:
                        Arrival=True
                        cargo_load=0.0
                        for c in range(len(cargo)):
                            for g in range(len(grade)):
                                prepol, prepod = getpreviousPODPOL(CargoDetails, (p - 1))
                                for pl in prepol:
                                    pod12 = getpodforpol(CargoDetails, pl, listofCargo[c], listofgrade[g])
                                    for d11 in pod12:
                                        if d11 >= p and Arrival==True :
                                            for h in range(1,len(noOfHolds)+1):
                                                cargo_load+=xtemp[h,d11,c+1,g+1]


                        cargo_loadf=0
                        cargo_loadf=cargo_load
                        Ballast_load=mod1.addConstr(gp.quicksum(tnk_ballast[p-1,t] for t in range(listofTank)))
                        ArrivaltankD=vesseldata.get("ArrivaltankData", [])
                        constant1 = getWeightConstantWeight(ArrivaltankD, (pschedule[p]))
                        portDisp1=getPortDisplacement2(pschedule, Hydro_value,apiurl,parameter,vesselMain,pschedule[p],vesselcode)
                        WB3BH=[]
                        for t in range(zhold):
                            zz3=getTankWeight(tank, holdtank[t])
                            mod1.addConstr(WB[t]==zz3 * BTnk[p-1, t])
                            WB3BH.append(WB[t])
                        WB3F=0
                        if zhold >=1:
                            WB3F=gp.quicksum(WB3BH[i] for i in range(zhold))
                        DISPL=mod1.addConstr(cargo_loadf+Ballast_load+constant1+WB3F+lwt)
                        if LoadableFlag==True:
                            if maxDispalcement<=portDisp1:
                                mod1.addConstr(DISPL<=maxDispalcement)
                            else:
                                mod1.addConstr(DISPL<=portDisp1)
                        else:
                            mod1.addConstr(DISPL<=maxDispalcement)
                    elif tt==2:
                        Arrival=True
                        cargo_load=0.0
                        for c in range(len(cargo)):
                            for g in range(len(grade)):
                                prepol, prepod = getpreviousPODPOL(CargoDetails, (p - 1))
                                for pl in prepol:
                                    pod12 = getpodforpol(CargoDetails, pl, listofCargo[c], listofgrade[g])
                                    for d11 in pod12:
                                        if d11 >= p :
                                            for h in range(1,len(noOfHolds)+1):
                                                cargo_load+=xtemp[h,d11,c,g]

                        cargo_loadf=0
                        cargo_loadf=cargo_load
                        Ballast_load=mod1.addConstr(gp.quicksum(tnk_ballast[p-1,t] for t in range(listofTank)))
                        tankdataxx=vesseldata.get("TankData", [])
                        constant1 = getWeightConstantWeight(tankdataxx, (pschedule[p]))
                        portDisp1 = getPortDisplacement2(pschedule, Hydro_value,apiurl, parameter, vesselMain, (pschedule[p]),
                                                 vesselcode)
                        WB3BH=[]
                        for t in range(zhold):
                            zz3=getTankWeight(tank, holdtank[t])
                            mod1.addConstr(WB[t]==zz3 * BTnk[p-1, t])
                            WB3BH.append(WB[t])
                        WB3F=0
                        DISPL=mod1.addConstr(cargo_loadf+Ballast_load+constant1+WB3F+lwt)
                        if LoadableFlag==True:
                            if maxDispalcement<=portDisp1:
                                mod1.addConstr(DISPL<=maxDispalcement)
                            else:
                                mod1.addConstr(DISPL<=portDisp1)
                        else:
                            mod1.addConstr(DISPL<=maxDispalcement)

        ####################################################################################################################
        ##################################################################################################
        ### Displacement calc end
        ####################################################################################################################
        ##################################################################################################
def propeller_calc(mod1,localpath,parameter,propellerFlag,pschedule,DISPL,):
    for p in range(len(pschedule)):
        ############################################################ #####################################
        ##################################################################################################
        # Propeller immersion constraint  start only depart port
        ############################################################ #####################################
        ##################################################################################################
        swdensity = 0.0
        exp_Deflectionlist=readexp_Deflection(localpath)
        UDDraftMConst=getUDDraftMConstwfame(exp_Deflectionlist)
        UDDraftMDegree2=getUDDraftMDegreewfame(exp_Deflectionlist)
        meanDraft={}
        for i in range(len(UDDraftMConst)):
            meanDraft[i] = mod1.addVar(lb=0, ub=GRB.INFINITY,vtype=GRB.CONTINUOUS, name="meanDraft")
        if p==1:
            swdensity = getTdensity_value(p, parameter, "SeaWaterDensity")
            volume=mod1.addVar(vtype=GRB.CONTINUOUS, name="volume")

            mod1.addConstr(volume==((DISPL / swdensity) * 1.025))
            if UDDraftMDegree2 in range(1, 9):
                mod1.addGenConstrPoly( volume, meanDraft[i],UDDraftMConst)
                if propellerFlag == True:
                    # proAftMinDraft is input from json
                    mod1.addConstr(meanDraft + TRIM / 2 >= proAftMinDraft)

            else:

                mod1.addConstr(meanDraft[i] == UDDraftMConst[0])
                mod1.update()
            if p>1 and p<len(pschedule):
                if tt==2:
                    swdensity = getTdensity_value(p, parameter, "SeaWaterDensity")
                    volume=mod1.addVar(vtype=GRB.CONTINUOUS, name="volume")

                    mod1.addConstr(volume==((DISPL / swdensity) * 1.025))
                    if UDDraftMDegree2 in range(1, 9):
                        mod1.addGenConstrPoly(volume, meanDraft[i],UDDraftMConst)
                        if propellerFlag == True:
                            # proAftMinDraft is input from json
                            mod1.addConstr(meanDraft + TRIM / 2 >= proAftMinDraft)
                    else:
                        mod1.addConstr(meanDraft[i] == UDDraftMConst[0])
                        mod1.update()



def Trim_flag(TrimFlag,pschedule,X,BTnk,WtItem,xtemp,vesseldata,SFCargoGrade,listofgrade,listofCargo,mod1,tnk_Ballast,exp_Ballast,noOfHolds,parameter,cargo,grade,cargodetails,exp_Trim,DISPL,listofTank,first_pass):
    try:
        for p in range(len(pschedule)):
            if TrimFlag:
                zz=0.0
                p1L=0
                if p==1: #depart parameter
                    p1L=p
                if p==len(pschedule):
                    p1L = p
                if p>1 and p<len(pschedule) and tt==1:#Arrival port p
                    p1L=p
                if p>1 and p<len(pschedule) and tt==2:#depart port p
                    p1L=p
                swdensity = getTdensity_value(p, parameter, "SeaWaterDensity")
                if getLoadLineDraft(p1L,parameter) > getMaxDraft2(p1L, parameter):
                    zz=1/swdensity
                else:
                    Loadline = getLoadline(p1L, parameter)
                    if Loadline == "Summer Water Line (S)":
                        zz = 1.0 / 1.025
                    elif Loadline == " Winter Water Line(W)":
                        zz = 1.0 / 1.025
                    elif Loadline == "Fresh Water Line (F)":
                        zz = 1.0 / 1.0
                    elif Loadline == "Optional Freeboard (TF)" : # Please check this
                        zz = 1.0 / 1.025
                    elif Loadline == "Tropical Fresh Water Line (TF)":
                        zz = 1.0 / 1.0
                    elif Loadline == "Tropical Water Line (T)":
                        zz = 1.0 / 1.025
                hh=1

                MCTCDegree= find_trim_value(exp_Trim, hh, "mctcdegree")
                LCBDegree=find_trim_value(exp_Trim, hh, "lcbdegree")
                MCTCConst=polynomial_trim(exp_Trim,hh,"mctcconst")
                LCBConst=polynomial_trim(exp_Trim,hh,"lcbconst")
                LCB = mod1.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="LCB")

                #
                DISPL2 = mod1.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="DISPL2")
                MCTC = mod1.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="MCTC")
                mod1.addConstr(DISPL2 ==(DISPL * zz))


                if LCBDegree in range(1, 9):
                    # print(LCBConst)
                    mod1.addGenConstrPoly(DISPL2, LCB, LCBConst)
                elif LCBDegree == 0:
                    # print(LCBConst)
                    mod1.addConstr(LCB == LCBConst[0])

                if MCTCDegree in range(1, 9):
                    # print(MCTCConst)
                    mod1.addGenConstrPoly(DISPL2, MCTC, MCTCConst, "FuncNonlinear=1")
                elif MCTCDegree == 0:
                    mod1.addConstr(MCTC == MCTCConst[0])

                WBMOM=[]
                zz=1/1.025 #m3/tonnes
                x1={}
                for i in range(listofTank):
                    if len(cargodetails) >0:
                        ExpType = "Cargo"
                    else:
                        ExpType = "Cargo"
                    # ballast tank LCG polynomial degree
                    TankDegree=find_value(exp_Ballast, listofTank[t], ExpType, 'TankDegree')
                    TankConst=find_value(exp_Ballast, listofTank[t], ExpType,'TankConst')
                    # creating Tank moments NL expression fro trim constraint
                    pt = 1
                    if p==1:
                        pt = 1
                    if p== len(pschedule):
                        pt=p-1
                    if p>1 and p < len(pschedule) and tt==1:#Arrival
                        pt=p-1
                    if p > 1 and p < len(pschedule) and tt==2:
                        pt=p

                    Tnk_pt_t = mod1.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="Tnk_pt_t")
                    x1[p] = mod1.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name=f"x1{p}")
                    mod1.addConstr(Tnk_pt_t[p] == (zz*tnk_Ballast[pt,t]))

                    if TankDegree in range(1,9):
                        mod1.addGenConstrPoly(Tnk_pt_t,x1,TankConst[i])
                        WBMOM.append(x1)
                    else:
                        mod1.addConstr(x1 == TankConst[0]*tnk_Ballast[pt,t])
                        WBMOM.append(x1)
                    # creating hold moments NL expression for trim constraint
                    HLOADMOM = []
                    zgrade = np.zeros(cargo, grade)
                    if len(cargodetails)>0 and first_pass==True:
                        for h in range(1,len(noOfHolds)+1):
                            find_trim_value(exp_Trim, h, "trimdegree")
                            trimholddegree = find_trim_value(exp_Trim, h, "trimdegree")
                            volumestart = polynomial_trim(exp_Trim, h, "volume start")
                            volumeend = polynomial_trim(exp_Trim, h, "volume end")
                            lcg=polynomial_trim(exp_Trim, h, "lcg")
                            # hold lcg polynomial constant
                            trimholdconst = polynomial_trim(exp_Trim, h, "trimholdconst")
                            xht = {}
                            xt = {}
                            for c in range(len(cargo)):
                                for g in range(len(grade)):
                                    xsfgrade=1/SFCargoGrade.get(str(listofCargo[c]).upper(),str(listofgrade[g]).upper())
                                    if p == 1: #depart
                                        dis = getpodforpol(cargodetails, p, listofCargo[c], listofgrade[g])
                                        for pd in dis:
                                            xht[h]=mod1.addVar(vtype=GRB.CONTINUOUS,name="xht")
                                            xt[h]=mod1.addVar(vtype=GRB.CONTINUOUS,name="xt")
                                            mod1.addConstr(xht==X[h,pd,c+1,g+1] *zgrade[c,g])
                                            mod1.addConstr(xt==X[h,pd,c+1,g+1] * 1.0)
                                            for i in range(len(trimholdconst)):
                                                if trimholddegree in range(1,9):
                                                    xtrm=mod1.addGenConstrPoly(xt, xht, trimholdconst[i])
                                                    HLOADMOM.append(xtrm)
                                                elif trimholddegree == 0:
                                                    xtrm=mod1.addGenConstrPoly(xt * trimholdconst[0])
                                                elif trimholddegree == 99:
                                                    nsize = len(volumestart)
                                                    y=mod1.addVar(range(1,(nsize)+1),vtype=GRB.BINARY, name="y")
                                                    mod1.addConstr(gp.quicksum(y[i] * volumestart[i] for i in range(1,(nsize)+1)) <= X[
                                                            h, pd, c+1, g+1] * zgrade[c, g], "volumestart_constraint")
                                                    mod1.addConstr(
                                                        gp.quicksum(y[i] * volumeend[i] for i in range(1,(nsize)+1)) >= X[
                                                            h, pd, c+1, g+1] * zgrade[c, g], "volumeend_constraint")
                                                    mod1.addConstr(gp.quicksum(y[i] for i in range(1,(nsize)+1)) == 1,
                                                                   "sum_y_constraint")

                                                    # Define expressions
                                                    lcgx = mod1.addConstr(gp.quicksum(y[i] * lcg[i] for i in range(1,(nsize)+1)))
                                                    xtrm = mod1.addConstr(X[h, pd, c+1, g+1] * lcgx)
                                                    HLOADMOM.append(xtrm)
                                    if p == len(pschedule):  # Arrival
                                        pol = getpolforpod(cargodetails, p, listofCargo[c], listofgrade[g])

                                        for pL in pol:
                                            mod1.addConstr(xht == X[h, p+1, c+1, g+1] * xsfgrade)
                                            mod1.addConstr(xt == X[h, p+1, c+1, g+1] * 1.0)
                                            if trimholddegree in range(1, 9):
                                                xtrm = mod1.addGenConstrPoly(xt, xht, trimholdconst[i])
                                                HLOADMOM.append(xtrm)
                                            elif trimholddegree == 0:
                                                xtrm = mod1.addGenConstrPoly(xt * trimholdconst[0])
                                            elif trimholddegree == 99:
                                                nsize = len(volumestart)
                                                y = mod1.addVar(range(1, (nsize) + 1), vtype=GRB.BINARY, name="y")

                                                mod1.addConstr(gp.quicksum(y[i] * volumestart[i] for i in range(1, (nsize) + 1)) <= X[h, p+1, c+1, g+1] * xsfgrade, "volumestart_constraint")
                                                mod1.addConstr(gp.quicksum(y[i] * volumeend[i] for i in range(1, (nsize) + 1)) >= X[h, p+1, c+1, g+1] * xsfgrade, "volumeend_constraint")
                                                mod1.addConstr(gp.quicksum(y[i] for i in range(1, (nsize) + 1)) == 1, "sum_y_constraint")

                                                lcgx = mod1.addConstr(gp.quicksum(y[i] * lcg[i] for i in range(1, (nsize) + 1)))
                                                xtrm = mod1.addConstr(X[h, p+1, c + 1, g + 1] * lcgx)
                                                HLOADMOM.append(xtrm)
                                    if p >1 and p < len(pschedule) and tt==1:
                                        prepol, prepod = getpreviousPODPOL(cargodetails, p - 1)
                                        for pl in prepol:
                                            pod12 = getpodforpol(cargodetails, pl, listofCargo[c], listofgrade[g])
                                            for d11 in pod12:
                                                if d11 >= p:

                                                    mod1.addConstr(xht == X[h, d11,c+1, g+1] * xsfgrade,
                                                                   name=f"xht_constraint_{h}_{d11}_{c}_{g}")
                                                    mod1.addConstr(xt == X[h, d11, c+1, g+1] * 1.0,
                                                                   name=f"xt_constraint_{h}_{d11}_{c}_{g}")
                                                    if trimholddegree in range(1, 9):
                                                        xtrm = mod1.addGenConstrPoly(xt, xht, trimholdconst[i])
                                                        HLOADMOM.append(xtrm)
                                                    elif trimholddegree == 0:
                                                        xtrm = mod1.addGenConstrPoly(xt * trimholdconst[0])
                                                    elif trimholddegree == 99:
                                                        nsize = len(volumestart)
                                                        y = mod1.addVar(range(1, (nsize) + 1), vtype=GRB.BINARY,
                                                                        name="y")

                                                        mod1.addConstr(gp.quicksum(y[i] * volumestart[i] for i in range(1, (nsize) + 1)) <= X[h, p + 1, c + 1, g + 1] * xsfgrade,"volumestart_constraint")
                                                        mod1.addConstr(gp.quicksum(y[i] * volumeend[i] for i in range(1, (nsize) + 1)) >= X[h, p + 1, c + 1, g + 1] * xsfgrade,"volumeend_constraint")
                                                        mod1.addConstr(
                                                            gp.quicksum(y[i] for i in range(1, (nsize) + 1)) == 1,
                                                            "sum_y_constraint")

                                                        lcgx = mod1.addConstr(
                                                            gp.quicksum(y[i] * lcg[i] for i in range(1, (nsize) + 1)))
                                                        xtrm = mod1.addConstr(X[h, p + 1, c + 1, g + 1] * lcgx)
                                                        HLOADMOM.append(xtrm)

                                    if p > 1 and p < len(pschedule) and tt==2:
                                        prepol, prepod = getpreviousPODPOL(cargodetails, p - 1)
                                        for pl in prepol:
                                            pod12 = getpodforpol(cargodetails, pl, listofCargo[c], listofgrade[g])
                                            for d11 in pod12:
                                                if d11 > p:

                                                    mod1.addConstr(xht == X[h, d11, c+1, g+1] * xsfgrade,
                                                                   name=f"xht_constraint_{h}_{d11}_{c}_{g}")
                                                    mod1.addConstr(xt == X[h, d11, c+1, g+1] * 1.0,
                                                                   name=f"xt_constraint_{h}_{d11}_{c}_{g}")
                                                    if trimholddegree in range(1, 9):
                                                        xtrm = mod1.addGenConstrPoly(xt, xht, trimholdconst[i])
                                                        HLOADMOM.append(xtrm)
                                                    elif trimholddegree == 0:
                                                        xtrm = mod1.addGenConstrPoly(xt * trimholdconst[0])
                                                    elif trimholddegree == 99:
                                                        nsize = len(volumestart)
                                                        y = mod1.addVar(range(1, (nsize) + 1), vtype=GRB.BINARY,
                                                                        name="y")

                                                        mod1.addConstr(gp.quicksum(y[i] * volumestart[i] for i in range(1, (nsize) + 1)) <= X[
                                                            h, p + 1, c + 1, g + 1] * xsfgrade, "volumestart_constraint")
                                                        mod1.addConstr(gp.quicksum(y[i] * volumeend[i] for i in range(1, (nsize) + 1)) >= X[
                                                            h, p + 1, c + 1, g + 1] * xsfgrade, "volumeend_constraint")
                                                        mod1.addConstr(
                                                            gp.quicksum(y[i] for i in range(1, (nsize) + 1)) == 1,
                                                            "sum_y_constraint")

                                                        lcgx = mod1.addConstr(
                                                            gp.quicksum(y[i] * lcg[i] for i in range(1, (nsize) + 1)))
                                                        xtrm = mod1.addConstr(X[h, p + 1, c + 1, g + 1] * lcgx)
                                                        HLOADMOM.append(xtrm)
#
#                   #creating hold moments NL expression for trim constraint
                    HLOADMOMS=0
                    if len(cargodetails) > 0  and first_pass==False:
                        for h in range(1,len(noOfHolds)+1):
                            trimholddegree= find_trim_value(exp_Trim, h, "trimholddegree")
                            trimhc=find_trim_value(exp_Trim, h, "trimholdconst")
                            xht = 0.0
                            xt = 0.0
                            for c in range(len(cargo)):
                                for g in range(len(grade)):
                                    xsfgrade=1/SFCargoGrade.get(str(listofCargo[c]).upper(),str(listofgrade[g]).upper(),1)
                                    if p==1:
                                        dis = getpodforpol(cargodetails, p, listofCargo[c], listofgrade[g])
                                        for pd in dis:
                                            xht = xtemp[h, pd, c, g] * zgrade[c, g]
                                            xt = xtemp[h, pd, c, g]
                                            if trimholddegree in range(1, 9):
                                                xtrm = mod1.addGenConstrPoly(xt, xht, trimhc[i])
                                                HLOADMOM.append(xtrm)
                                            elif trimholddegree == 99:
                                                soundData = vesseldata.get( "SoundingData", [])
                                                LcgData = get_souding_lcg_and_vcg(f"HOLD{h}", round(xht, 2), soundData)
                                                lcg = LcgData.get(f"HOLD{h}LCG", 0)
                                                xtrm = xt * lcg
                                                HLOADMOMS = HLOADMOMS + xtrm
                                            else:
                                                xtrm = xt * trimhc[0]
                                                HLOADMOMS = HLOADMOMS + xtrm
                                    if p== len(pschedule):
                                        pol = getpolforpod(cargodetails, p, listofCargo[c], listofgrade[g])
                                        for pL in pol:
                                            xht = xtemp[h, pL, c, g] * xsfgrade
                                            xt = xtemp[h, pL, c, g]
                                            if trimholddegree in range(1, 9):
                                                xtrm = mod1.addGenConstrPoly(xt, xht, trimhc[i])
                                                HLOADMOM.append(xtrm)
                                            elif trimholddegree == 99:
                                                soundData = vesseldata.get( "SoundingData", [])
                                                LcgData = get_souding_lcg_and_vcg(f"HOLD{h}", round(xht, 2), soundData)
                                                lcg = LcgData.get(f"HOLD{h}LCG", 0)
                                                xtrm = xt * lcg
                                                HLOADMOMS = HLOADMOMS + xtrm
                                            else:
                                                xtrm = xt * trimhc[0]
                                                HLOADMOMS = HLOADMOMS + xtrm
                                    if p > 1 and p < len(pschedule) and tt==1 :#Arrival
                                        prepol, prepod = getpreviousPODPOL(cargodetails, p - 1)
                                        for pl in prepol:
                                            pod12 = getpodforpol(cargodetails, pl, listofCargo[c], listofgrade[g])
                                            for d11 in pod12:
                                                if d11 > p:
                                                    xht = xtemp[h, d11, c, g] * xsfgrade
                                                    xt = xtemp[h, d11, c, g]
                                                    if trimholddegree in range(1, 9):
                                                        xtrm = mod1.addGenConstrPoly(xt, xht, trimhc[i])
                                                        HLOADMOM.append(xtrm)
                                                    elif trimholddegree == 99:
                                                        soundData = vesseldata.get( "SoundingData", [])
                                                        LcgData = get_souding_lcg_and_vcg(f"HOLD{h}", round(xht, 2), soundData)
                                                        lcg = LcgData.get(f"HOLD{h}LCG", 0)
                                                        xtrm = xt * lcg
                                                        HLOADMOMS = HLOADMOMS + xtrm
                                                    else:
                                                        xtrm = xt * trimhc[0]
                                                        HLOADMOMS = HLOADMOMS + xtrm
                                    if p >1 and p < len(pschedule) and tt==2:
                                        prepol, prepod = getpreviousPODPOL(cargodetails, p - 1)
                                        for pl in prepol:
                                            pod12 = getpodforpol(cargodetails, pl, listofCargo[c], listofgrade[g])
                                            for d11 in pod12:
                                                if d11 > p:
                                                    xht = xtemp[h, d11, c, g] * xsfgrade
                                                    xt = xtemp[h, d11, c, g]
                                                    if trimholddegree in range(1, 9):
                                                        xtrm = mod1.addGenConstrPoly(xt, xht, trimhc[i])
                                                        HLOADMOM.append(xtrm)
                                                    elif trimholddegree == 99:
                                                        soundData = vesseldata.get( "SoundingData", [])
                                                        LcgData = get_souding_lcg_and_vcg(f"HOLD{h}", round(xht, 2),
                                                                                          soundData)
                                                        lcg = LcgData.get(f"HOLD{h}LCG", 0)
                                                        xtrm = xt * lcg
                                                        HLOADMOMS = HLOADMOMS + xtrm
                                                    else:
                                                        xtrm = xt * trimhc[0]
                                                        HLOADMOMS = HLOADMOMS + xtrm
                                    # light ship moments
                                    LightshipMOM = getLightShipLMOM(WtItem)
                                    WCMOM=0.0
                                    # Assuming vesselData, pschedule, p, and tt are already defined

                                    if p == 0:  # depart p (adjusted for 0-based indexing)
                                        tankdataxx = vesseldata.get("TankData", [])
                                        WCMOM = getWeightConstantLMOM(tankdataxx, pschedule[p])

                                    if p == len(pschedule) - 1:  # Arrival p (adjusted for 0-based indexing)
                                        ArrivaltankD = vesseldata.get("ArrivaltankData", [])
                                        WCMOM = getWeightConstantLMOM(ArrivaltankD, pschedule[p])

                                    if 0 < p < len(pschedule) - 1 and tt == 1:  # arrival p
                                        ArrivaltankD = vesseldata.get("ArrivaltankData", [])
                                        WCMOM = getWeightConstantLMOM(ArrivaltankD, pschedule[p])

                                    if 0 < p < len(pschedule) - 1 and tt == 2:  # depart p
                                        tankdataxx = vesseldata.get("TankData", [])
                                        WCMOM = getWeightConstantLMOM(tankdataxx, pschedule[p])


                                    # Assuming WBlist, pschedule, p, tank, exp_Trim, BTnk, and tt are already defined

                                    holdtank = getHoldBallastTank(WBlist, pschedule[p])
                                    WB3BHMOM = []
                                    # print(f"8002=holdtank=={holdtank}")
                                    hlen = len(holdtank)
                                    for t in range(hlen):
                                        zz3 = getTankWeight(tank, holdtank[t])
                                        hh1 = 1
                                        zz2 = getholdbalLCB(exp_Trim, hh1)
                                        WB = mod1.addVar(name=f"WB_{p}_{t}")
                                        # print(f"8008=zz3weight=={zz3}=zz2lcb=={zz2}")
                                        if p == 0:  # depart (adjusted for 0-based indexing)

                                            mod1.addConstr(WB == zz3 * BTnk[p, t] * zz2[t],
                                                           name=f"WB_constraint_{p}_{t}")
                                            WB3BHMOM.append(WB)
                                        if p == len(pschedule) - 1:  # Arrival (adjusted for 0-based indexing)

                                            mod1.addConstr(WB == zz3 * BTnk[p - 1, t] * zz2[t],
                                                           name=f"WB_constraint_{p - 1}_{t}")
                                            WB3BHMOM.append(WB)
                                        if 0 < p < len(pschedule) - 1 and tt == 1:  # Arrival

                                            mod1.addConstr(WB == zz3 * BTnk[p - 1, t] * zz2[t],
                                                           name=f"WB_constraint_{p - 1}_{t}")
                                            WB3BHMOM.append(WB)
                                        if 0 < p < len(pschedule) - 1 and tt == 2:  # depart

                                            mod1.addConstr(WB == zz3 * BTnk[p, t] * zz2[t],
                                                           name=f"WB_constraint_{p}_{t}")
                                            WB3BHMOM.append(WB)
                                        HLOADMOM_f = 0
                                        if first_pass==True:
                                            hlemn = len(HLOADMOM)
                                            if hlemn>=1:
                                                mod1.addConstr(HLOADMOM_f == gp.quicksum(HLOADMOM[yy] for yy in range(hlemn)),name="HLOADMOM_f_constraint")
                                        elif first_pass == False:
                                            HLOADMOM_f = HLOADMOMS
                                        WB3BHMOM_f = 0
                                        wblen = len(WB3BHMOM)
                                        if wblen>=1:
                                            mod1.addConstr(WB3BHMOM_f == gp.quicksum(WB3BHMOM[yy] for yy in range(wblen)),name="WB3BHMOM_f_constraint")
                                        WBMOM_f=0
                                        wblen=len(WBMOM)
                                        if wblen>=1:
                                            mod1.addConstr(WBMOM_f == gp.quicksum(WBMOM[yy] for yy in range(wblen)),name="WBMOM_f_constraint")
                                        mod1.addConstr(
                                            LightshipMOM +  # lightship
                                            HLOADMOM_f +  # hold
                                            WBMOM_f +  # ballast
                                            WCMOM +  # tanks
                                            WB3BHMOM_f  # hold tank
                                            == -100 * TRIM * MCTC + LCB,
                                            name="nonlinear_constraint"
                                        )







                                            # Optimize the model if needed
                                    # mod3.optimize()
    except Exception as e:
        print("The Exception in trim constraint formation:", e)
        # Capture the current stack trace
        bt = traceback.extract_stack()

        # Print the file name, line number, and function for each frame in the stack trace
        for frame in bt:
            print(f"File: {frame.filename}, Line: {frame.lineno}, Function: {frame.name}")
        return -1

    ##################################################################################################################
    ############################################################ #########################################################
    # trim constraint formulation end
    ##################################################################################################################
    ############################################################ #########################################################
def stressflag(fmStation,parameter,mod1,DISPL,pschedule,FmStLcgvalue,vesseldata,CargoHold,FmStWeightRatio,FmStItems,X,tank,Btnk,first_pass,tnk_ballast,xtemp,exp_BMSF,WBlist,bmsf_objects,cargo,grade,listofgrade,listofCargo,cargodetails,tankdata):
    ##################################################################################################################
    #####################################################################################################################
    # Shear force constraint formulation start
    ##################################################################################################################
    #####################################################################################################################
    try:
        for p in range(pschedule):
            if (stressflag):
                HLOADSF = []
                HLOADSF_ff = 0
                # Array for ballast tank weights for all frames
                tankWB20 = []
                # Array for hold as ballast tank weights for all frames
                tankHoldWB = []
                # size or number of frame stations
                fsIndex = len(fmStation)
                for f in reversed(range(1,fsIndex)):
                    # if stress flag is of at port p
                    if getTargetTrim_value(pschedule[p], parameter) != 0:
                        frameno :float =fmStation[f]["frame"]

                        SFPosLim = frame_col(fmStation, frameno, "limitsfpos")
                        SFPortPosLim =frame_col(fmStation,frameno, "limitSFposHRB")
                        # polindex
                        polIdx = pschedule[p]
                        # frame used for SF

                        SFusedFrame = find_Frame_value(bmsf_objects, frameno)
                        # array of frames stations above frameno
                        # frame_col(fmStation, fmStation["frame"], col2)
                        frameStation = getAboveframeStation(frameno, fmStation)
                        # List of non ballast tank
                        listofWCTank = getWCTankList(tankdata, polIdx)
                        # dict of hold as ballast tanks
                        holdtank = getHoldBallastTank(WBlist, polIdx)
                        # println("8115=holdtank==$holdtank")
                        # weight ratio of holds at frame frameno

                        Holdsframe = polynomial_frame(bmsf_objects, frameno,"Holdsatframe")
                        # Weight ratio of ballast tank at frameno
                        WtRatio_blst_tan = polynomial_frame(exp_BMSF, frameno,"WtRatio_blst_tank")
                        Hold_tanks_list = polynomial_frame(exp_BMSF,frameno,"Hold_tanks_list")
                        Htank_Weight_Ration =polynomial_frame(exp_BMSF, frameno,"Htank_Weight_Ratio")
                        Holdbsttankweight=polynomial_frame(exp_BMSF, frameno,"Holdbsttankweight")
                        xx = [i for i, x in enumerate(Holdsframe) if x > 0.0]
                        # weight of lightship at frameno
                        if first_pass:
                            if len(xx) >= 1:
                                if p == 1:  # depart
                                    for c in range(len(cargo)):
                                        for g in range(len(grade)):
                                            dis = getpodforpol(cargodetails, p, listofCargo[c], listofgrade[g])
                                            if len(dis) >= 1:
                                                for pd in dis:
                                                    xsf = gp.quicksum(X[h, pd, c+1, g+1] * Holdsframe[h] * 0.001 for h in xx)
                                                    HLOADSF.append(xsf)
                                if p == len(pschedule):  # Arrival
                                    for c in range(len(cargo)):
                                        for g in range(len(grade)):
                                            pol = getpolforpod(cargodetails, p, listofCargo[c], listofgrade[g])
                                            if len(pol) >= 1:
                                                for pL in pol:
                                                    xsf = gp.quicksum(X[h, p, c+1, g+1] * Holdsframe[h] * 0.001 for h in xx)
                                                    HLOADSF.append(xsf)
                                if 1 < p < len(pschedule) and tt == 1:  # Arrival
                                    for c in range(len(cargo)):
                                        for g in range(len(grade)):
                                            prepol, prepod = getpreviousPODPOL(cargodetails, p - 1)
                                            for pl in prepol:
                                                pod12 = getpodforpol(cargodetails, pl, listofCargo[c], listofgrade[g])
                                                for d11 in pod12:
                                                    if d11 >= p and tt == 1:
                                                        xsf = gp.quicksum(X[h, d11, c+1, g+1] * Holdsframe[h] * 0.001 for h in xx)
                                                        HLOADSF.append(xsf)
                                if 1 < p < len(pschedule) and tt == 2:  # depart
                                    for c in range(len(cargo)):
                                        for g in range(len(grade)):
                                            prepol, prepod = getpreviousPODPOL(cargodetails, p)
                                            for pl in prepol:
                                                pod12 = getpodforpol(cargodetails, pl, listofCargo[c], listofgrade[g])
                                                for d11 in pod12:
                                                    if d11 > p:
                                                        xsf = gp.quicksum(X[h, d11, c+1, g+1] * Holdsframe[h] * 0.001 for h in xx)
                                                        HLOADSF.append(xsf)
                        else:
                            if len(xx) >= 1:
                                if p == 1:  # depart
                                    for c in range(len(cargo)):
                                        for g in range(len(grade)):
                                            dis = getpodforpol(cargodetails, p, listofCargo[c], listofgrade[g])
                                            if len(dis) >= 1:
                                                for pd in dis:
                                                    for h in xx:
                                                        HLOADSF_ff += xtemp[h, pd, c+1, g+1] * Holdsframe[h] * 0.001
                                if p == len(pschedule):  # Arrival
                                    for c in range(len(cargo)):
                                        for g in range(len(grade)):
                                            pol = getpolforpod(cargodetails, p, listofCargo[c], listofgrade[g])
                                            if len(pol) >= 1:
                                                for pL in pol:
                                                    for h in xx:
                                                        HLOADSF_ff += xtemp[h, p, c+1, g+1] * Holdsframe[h] * 0.001
                                if 1 < p < len(pschedule) and tt == 1:  # Arrival
                                    for c in range(len(cargo)):
                                        for g in range(len(grade)):
                                            prepol, prepod = getpreviousPODPOL(cargodetails, p - 1)
                                            for pl in prepol:
                                                pod12 = getpodforpol(cargodetails, pl, listofCargo[c], listofgrade[g])
                                                for d11 in pod12:
                                                    if d11 >= p and tt == 1:
                                                        for h in xx:
                                                            HLOADSF_ff += xtemp[h, d11, c+1, g+1] * Holdsframe[h] * 0.001
                                if 1 < p < len(pschedule) and tt == 2:  # depart
                                    for c in range(len(cargo)):
                                        for g in range(len(grade)):
                                            prepol, prepod = getpreviousPODPOL(cargodetails, p)
                                            for pl in prepol:
                                                pod12 = getpodforpol(cargodetails, pl, listofCargo[c], listofgrade[g])
                                                for d11 in pod12:
                                                    if d11 > p:
                                                        for h in xx:
                                                            HLOADSF_ff += xtemp[h, d11, c+1, g+1] * Holdsframe[h] * 0.001

                        if not getMaxDischarge(cargodetails):
                            if len(xx) >= 1:
                                if p == 1:  # depart
                                    xl = gp.quicksum(tnk_ballast[p, t] * WtRatio_blst_tan[t] * 0.001 for t in xx)
                                    tankWB20.append(xl)
                                if p == len(pschedule):  # arrival
                                    xl = gp.quicksum(tnk_ballast[p - 1, t] * WtRatio_blst_tan[t] * 0.001 for t in xx)
                                    tankWB20.append(xl)
                                if 1 < p < len(pschedule) and tt == 1:  # Arrival
                                    xl = gp.quicksum(tnk_ballast[p - 1, t] * WtRatio_blst_tan[t] * 0.001 for t in xx)
                                    tankWB20.append(xl)
                                if 1 < p < len(pschedule) and tt == 2:  # depart
                                    xl = gp.quicksum(tnk_ballast[p, t] * WtRatio_blst_tan[t] * 0.001 for t in xx)
                                    tankWB20.append(xl)
                                # holdtank is a list or array

                                if len(holdtank) >= 1:
                                    if p == 1:  # depart
                                        for th in range(len(holdtank)):
                                            zz3 = getTankWeight(tank, holdtank[th])
                                            if Htank_Weight_Ration[th] > 0.0:
                                                xl = Btnk[p, th] * zz3 * Htank_Weight_Ration[th] * 0.001
                                                tankHoldWB.append(xl)
                                                # mod3.addConstr(tankHoldWBvar[f, portcounter, th] == xl)
                                    if p == len(pschedule):  # Arrival
                                        for th in range(len(holdtank)):
                                            zz3 = getTankWeight(tank, holdtank[th])
                                            if Htank_Weight_Ration[th] > 0.0:
                                                xl = Btnk[p - 1, th] * zz3 * Htank_Weight_Ration[th] * 0.001
                                                tankHoldWB.append(xl)
                                                # mod3.addConstr(tankHoldWBvar[f, portcounter, th] == xl)
                                    if 1 < p < len(pschedule) and tt == 1:  # Arrival
                                        for th in range(len(holdtank)):
                                            zz3 = getTankWeight(tank, holdtank[th])
                                            if Htank_Weight_Ration[th] > 0.0:
                                                xl = Btnk[p - 1, th] * zz3 * Htank_Weight_Ration[th] * 0.001
                                                tankHoldWB.append(xl)
                                                # mod3.addConstr(tankHoldWBvar[f, portcounter, th] == xl)
                                    if 1 < p < len(pschedule) and tt == 2:  # depart
                                        for th in range(len(holdtank)):
                                            zz3 = getTankWeight(tank, holdtank[th])
                                            if Htank_Weight_Ration[th] > 0.0:
                                                xl = Btnk[p, th] * zz3 * Htank_Weight_Ration[th] * 0.001
                                                tankHoldWB.append(xl)
                                                # mod3.addConstr(tankHoldWBvar[f, portcounter, th] == xl)
                                # get hold number ,weight ration and items dict and weight ratio and lcg dict before frameno
                        holdno, FmStWeight, FmStLcg = getMaxHoldNoAtEachFrame(frameno,fmStation,FmStItems,CargoHold,FmStWeightRatio,FmStLcgvalue)
                        # looping all items of dictonary FmStWeight=Dict(itemsFramenumber=>WeightRatio)
                        # Weight const weight at frameno
                        sigmaWc1 = 0
                        # tankdata2=nothing
                        tankname = ""
                        if p == 1 and tt == 1:  # depart
                            tankdataxx = vesseldata.get("TankData", [])
                            listofWCTank = getWCTankList(tankdataxx, pschedule[p])

                            for k, v in FmStWeight.items():
                                if k in listofWCTank:
                                    for f in range(len(frameStation)):
                                        tankvalue = [row for row in tankdataxx if row['tankname'] == k and row['POLIndex'] == p]
                                        if len(tankvalue) >= 1:
                                            sigmaWc1 += (FmStWeightRatio.get(f"{k}{frameStation[f]}", 0) * tankvalue[0]['weight']) * 0.001
                        # Assuming vesselData, pschedule, FmStWeight, frameStation, FmStWeightRatio, p, tt, sigmaWc1 are already defined

                        if p == len(pschedule) and tt == 1:  # arrival
                            ArrivaltankD = vesseldata.get("ArrivaltankData", [])
                            listofWCTank = getWCTankList(ArrivaltankD, pschedule[p])

                            for k, v in FmStWeight.items():
                                if k in listofWCTank:
                                    for f in range(len(frameStation)):
                                        tankvalue = [row for row in ArrivaltankD if row['tankname'] == k and row['POLIndex'] == p]
                                        if len(tankvalue) >= 1:
                                            sigmaWc1 += (FmStWeightRatio.get(f"{k}{frameStation[f]}", 0) * tankvalue[0]['weight']) * 0.001

                        if 1 < p < len(pschedule) and tt == 1:  # Arrival
                            ArrivaltankD = vesseldata.get("ArrivaltankData", [])
                            listofWCTank = getWCTankList(ArrivaltankD, pschedule[p])

                            for k, v in FmStWeight.items():
                                if k in listofWCTank:
                                    for f in range(len(frameStation)):
                                        tankvalue = [row for row in ArrivaltankD if row['tankname'] == k and row['POLIndex'] == p]
                                        if len(tankvalue) >= 1:
                                            sigmaWc1 += (FmStWeightRatio.get(f"{k}{frameStation[f]}", 0) * tankvalue[0]['weight']) * 0.001

                        if 1 < p < len(pschedule) and tt == 2:  # depart
                            tankdataxx = vesseldata.get("TankData", [])
                            listofWCTank = getWCTankList(tankdataxx, pschedule[p])

                            for k, v in FmStWeight.items():
                                if k in listofWCTank:
                                    for f in range(len(frameStation)):
                                        tankvalue = [row for row in tankdataxx if row['tankname'] == k and row['POLIndex'] == p]
                                        if len(tankvalue) >= 1:
                                            sigmaWc1 += (FmStWeightRatio.get(f"{k}{frameStation[f]}", 0) * tankvalue[0]['weight']) * 0.001

                        # SF positive at sea
                        SFPosLim = frame_col(fmStation, frameno, "limitsfpos")
                        SFPortPosLim = frame_col(fmStation, frameno, "limitSFposHRB")
                        SF201postiveLimit=getPostiveSFLimit(fmStation["frame"],pschedule[p],parameter,SFPosLim,SFPortPosLim)
                        # SF Negative at sea

                        SFNegLim =frame_col(fmStation, frameno, "limitSFnegSEA")
                        # SF Negative at port
                        SFPortNegLim = frame_col(fmStation, frameno, "limitSFnegHRB")
                        # SF Negative limit based upon percentage and sea/port from parameter json
                        SF201NegativeLimit =getNegativeSFLimit(fmStation["frame"],pschedule[p],parameter,SFNegLim,SFPortNegLim)
                        # SF base value correction polynomial degree
                        SFBaseDraftDegree =  find_Frame_value(exp_BMSF, frameno,"SFBaseDraftDegree")
                        # SF base value correction polynomial constant
                        SFBaseConst=polynomial_frame(exp_BMSF, frameno,"SFBaseConst")
                        # SF trim value correction polynomial degree
                        SFTrimCorDegree=find_Frame_value(exp_BMSF, frameno,"SFTrimCorDegree")
                        # SF trim value correction polynomial constant
                        SFBaseTrimConst=polynomial_frame(exp_BMSF, frameno,"SFBaseTrimConst")


                        xsfbase = mod1.addVar(vtype=GRB.CONTINUOUS,name="xsfbase")
                        xtrim = mod1.addVar(vtype=GRB.CONTINUOUS,name="xsfbase")
                        if SFusedFrame>=1:
                            if len(SFBaseConst) >=1:
                                if SFBaseDraftDegree in range(1,9):
                                    mod1.addGenConstrPoly(DISPL,xsfbase,SFBaseConst[i])
                                else:
                                    mod1.addConstr(xsfbase==SFBaseConst[0])

                                if SFTrimCorDegree in range(1,9):
                                    mod1.addGenConstrPoly(DISPL,xtrim,SFBaseTrimConst[i])
                                else:
                                    mod1.addConstr(xtrim==SFBaseTrimConst[0])
                        HLOADSF_1=0
                        if first_pass==True:
                            zsf=len(HLOADSF)
                            if zsf >=1:
                                HLOADSF_1=mod1.addConstr(gp.quicksum(tankHoldWB[i] for i in range(1,zsf)))
                        else:
                            HLOADSF_1 = HLOADSF_ff
                        zh=len(tankHoldWB)
                        tankHoldWB_1 = 0
                        # Define the expression for tankHoldWB_1 if zh >= 1
                        if zh >= 1:
                            tankHoldWB_1_expr = gp.quicksum(tankHoldWB[i] for i in range(zh))
                            tankHoldWB_1 = mod1.addVar(vtype=GRB.CONTINUOUS,name="tankHoldWB_1")
                            mod1.addConstr(tankHoldWB_1 == tankHoldWB_1_expr, name="tankHoldWB_1_constr")

                        # Define the expression for tankWB20_1
                        zt = len(tankWB20)
                        tankWB20_1 = 0
                        if zt >= 1:
                            tankWB20_1_expr = gp.quicksum(tankWB20[i] for i in range(zt))
                            tankWB20_1 = mod1.addVar(vtype=GRB.CONTINUOUS,name="tankWB20_1")
                            mod1.addConstr(tankWB20_1 == tankWB20_1_expr, name="tankWB20_1_constr")




















    # mod1.display()
    # mod1.computeIIS()
    # mod2.write("mod2_TIR_CHECK.ilp")
    # mod1.write("D:/BCAP_python/Bcap_12.ilp")
    # print("polIdxs=====",polIdxs)


    # for var in mod1.getVars():
    #     print(var)
    # set_chartedparty_constraints(mod1, inputs_flags,polIdxs,podIdxs,cargo,grade,HoldNos,CargoDetails,ChartedParty,VesselParticulars,pschedule )

    # mod1.display()



