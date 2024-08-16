import pandas as pd
from InputInfo.ChartedPartyAssumption import getcharterpartyMinCargopol,getcharterpartyMinPercentageValue2
from InputInfo.CargoDetail import getTotalWeightOf_POL_POD_Cargo2
from Vesselinfo.VesselParticulars import getHoldVolumeMaxBounds,getHoldWeightMaxBounds
import gurobipy as gp
from gurobipy import GRB
from CommonInfo.CommonInfo import setWeightItems
from Tankinfo.Tank import getTankWtItemName,getTankDensity,getTankWeight
import numpy as np
from Vesselinfo.VesselParticulars import getHoldVolumeMaxBounds
# from NonlinearInfo.commonfunction import getpodforpol,getpolforpod
from StabilityInfo.SoundingData import get_souding_lcg_and_vcg
from InputInfo.CargoDetail import getpreviousPODPOL
from Tankinfo.WNTankList import getHoldBallastTank
from NonlinearInfo.Nonlinear_modelling_printing_SF_BM import extract_integer

def getVesselCalculatorInput(
        mod3,
        WtItems,
        tankdataxx,
        pl,
        listofPOL,
        soundingData,
        listofCargo,
        listofGrade,
        listofPOD,
        noOfHolds,
        WBlist,
        SFCargoGrade,
        vessel,
        AftDistfromAP,
        FwdDistfromAP,
        TankAptDist,
        TankFwdDist,
        tank,
        TankCategory,
        x,
        last_port,
        listofPOL2,
        listofTank,
        pschedule,
        cargodetails,
        Arrival,
        Tnktemp,
        BTnktemp,
):
    list=[]
    item={}
    rounddigit = 2
    try:
        print("9273-pl===$pl")
        # print(f"function getVesselCalculatorInput( pl==={pl}")
        for i,lightWt in WtItems.iterrows():
            item = setWeightItems(
                lightWt.weightid,
                lightWt.xaftap,
                lightWt.xfwdap,
                lightWt.weight,
                lightWt.lcgap,
                lightWt.vcgbl,
                lightWt.tcgcl,
            )
            list.append(item)
        # print("9287")
        pl3=0
        if pl==1:
            pl3=1
        elif pl > 1 and pl < len(pschedule):
            if Arrival==True:
                pl3=pl-1
            else:
                pl3=pl
        elif pl == len(pschedule):
            pl3=pl-1
        # print("=====9298=====")
        # print("12076==tankdataxx===",tankdataxx)
        for i,tankWt in tankdataxx.iterrows():
            if tankWt["POLIndex"]== pl:
                    print("tankWt.tankname===========>", tankWt["tankname"])
                    weightid = getTankWtItemName(tank, tankWt["tankname"])
                    aftDist = float(TankAptDist.get(str(tankWt.tankname), 0))
                    fwdDist = float(TankFwdDist.get(str(tankWt.tankname), 0))
                    item = setWeightItems(
                        weightid,
                        float(aftDist),
                        float(fwdDist),
                        float(tankWt.weight),
                        float(tankWt.lcglpp),
                        float(tankWt.vcgblpp),
                        float(tankWt.tcgclpp),
                    )
                    list.append(item)

        cargoTypesize = len(listofCargo)
        grade_size = len(listofGrade)
        zgrade = np.zeros(cargoTypesize, grade_size) #import numpy
        for c in range(cargoTypesize):
            for g in range(grade_size):
                haskey = f"{listofCargo[c]}{listofGrade[g]}"
                if haskey in SFCargoGrade:
                    value = SFCargoGrade[haskey]
                else:
                    value = 1
                zzg = 1 / value
                zgrade[c - 1, g - 1] = zzg

        if len(cargodetails) >=1:
            for h in range(noOfHolds):
                for c in range(cargoTypesize):
                    for g in range(grade_size):
                        if pl == 1:
                            dis = getpodforpol(cargodetails, pl, listofCargo[c], listofGrade[g])
                            for pd in dis:
                                if round(x[h, pd, c, g], 2) > 1.0:
                                    weight = 0
                                    weight = round(x[h, pd, c, g], 2)
                                    xsfgrade = SFCargoGrade.get(
                                        f"{listofCargo[c].upper()}{listofGrade[g].upper()}",
                                        1
                                    )
                                    volume=weight /xsfgrade
                                    soundingData2 = soundingData
                                    LcgData = get_souding_lcg_and_vcg(
                                        f"HOLD{h}",
                                        round(volume, 2),
                                        soundingData2
                                    )
                                    volumeper = (volume * 100) / getHoldVolumeMaxBounds(vessel, int(h))
                                    lcg = LcgData.get(f"HOLD{h}LCG", 0)
                                    vcg = LcgData.get(f"HOLD{h}VCG", 0)
                                    tcg = LcgData.get(f"HOLD{h}TCG", 0)
                                    volper = LcgData.get(f"HOLD{h}VOLPercentage", 0)
                                    fsm = LcgData.get(f"HOLD{h}FSM", 0)
                                    aftDist=float(AftDistfromAP.get(f"HOLD{h}",0))
                                    fwdDist=float(FwdDistfromAP.get(f"HOLD{h}",0))
                                    item = setWeightItems(
                                        f"BH{h}",
                                        float(aftDist),
                                        float(fwdDist),
                                        float(weight),
                                        float(lcg),
                                        float(vcg),
                                        float(tcg),)
                                    list.append(item)

                        if pl == len(pschedule):
                            pol = getpolforpod(cargodetails, pl, listofCargo[c], listofGrade[g])
                            for pL in pol:
                                if round(x[h, pl, c, g], 2) > 1.0:
                                    weight = 0
                                    weight = round(x[h, pl, c, g], 2)
                                    xsfgrade = SFCargoGrade.get(
                                        f"{listofCargo[c].upper()}{listofGrade[g].upper()}",
                                        1
                                    )
                                    volume=weight /xsfgrade
                                    soundingData2 = soundingData
                                    LcgData = get_souding_lcg_and_vcg(
                                        f"HOLD{h}",
                                        round(volume, 2),
                                        soundingData2
                                    )
                                    volumeper = (volume * 100) / getHoldVolumeMaxBounds(vessel, int(h))
                                    lcg = LcgData.get(f"HOLD{h}LCG", 0)
                                    vcg = LcgData.get(f"HOLD{h}VCG", 0)
                                    tcg = LcgData.get(f"HOLD{h}TCG", 0)
                                    volper = LcgData.get(f"HOLD{h}VOLPercentage", 0)
                                    fsm = LcgData.get(f"HOLD{h}FSM", 0)
                                    aftDist=float(AftDistfromAP.get(f"HOLD{h}",0))
                                    fwdDist=float(FwdDistfromAP.get(f"HOLD{h}",0))
                                    item = setWeightItems(
                                        f"BH{h}",
                                        float(aftDist),
                                        float(fwdDist),
                                        float(weight),
                                        float(lcg),
                                        float(vcg),
                                        float(tcg),)
                                    list.append(item)

                        if pl > 1 and pl < len(pschedule) and (Arrival == True):
                            prepol, prepod = getpreviousPODPOL(cargodetails, int(pl - 1))
                            for pll in prepol:
                                pod12 = getpodforpol(
                                    cargodetails,
                                    pll,
                                    listofCargo[c],
                                    listofGrade[g]
                                )
                                for d11 in pod12:
                                    if d11 >= pl and Arrival == True:
                                        if round(x[h, d11, c, g], 2) > 1.0:
                                            weight = 0
                                            weight = round(x[h, d11, c, g], 2)
                                            xsfgrade = SFCargoGrade.get(
                                                f"{listofCargo[c].upper()}{listofGrade[g].upper()}",
                                                1
                                            )
                                            volume=weight /xsfgrade
                                            soundingData2 = soundingData
                                            LcgData = get_souding_lcg_and_vcg(
                                                f"HOLD{h}",
                                                round(volume, 2),
                                                soundingData2
                                            )
                                            volumeper = (volume * 100) / getHoldVolumeMaxBounds(vessel, int(h))
                                            lcg = LcgData.get(f"HOLD{h}LCG", 0)
                                            vcg = LcgData.get(f"HOLD{h}VCG", 0)
                                            tcg = LcgData.get(f"HOLD{h}TCG", 0)
                                            volper = LcgData.get(f"HOLD{h}VOLPercentage", 0)
                                            fsm = LcgData.get(f"HOLD{h}FSM", 0)
                                            aftDist=float(AftDistfromAP.get(f"HOLD{h}",0))
                                            fwdDist=float(FwdDistfromAP.get(f"HOLD{h}",0))
                                            item = setWeightItems(
                                                f"BH{h}",
                                                float(aftDist),
                                                float(fwdDist),
                                                float(weight),
                                                float(lcg),
                                                float(vcg),
                                                float(tcg),)
                                            list.append(item)

                        if pl > 1 and pl < len(pschedule) and (Arrival == False):
                            prepol, prepod = getpreviousPODPOL(cargodetails, int(pl))
                            for pll in prepol:
                                pod12 = getpodforpol(
                                    cargodetails,
                                    pll,
                                    listofCargo[c],
                                    listofGrade[g]
                                )
                                for d11 in pod12:
                                    if d11 >= pl :
                                        if round(x[h, d11, c, g], 2) > 1.0:
                                            weight = 0
                                            weight = round(x[h, d11, c, g], 2)
                                            xsfgrade = SFCargoGrade.get(
                                                f"{listofCargo[c].upper()}{listofGrade[g].upper()}",
                                                1
                                            )
                                            volume = weight / xsfgrade
                                            soundingData2 = soundingData
                                            LcgData = get_souding_lcg_and_vcg(
                                                f"HOLD{h}",
                                                round(volume, 2),
                                                soundingData2
                                            )
                                            volumeper = (volume * 100) / getHoldVolumeMaxBounds(vessel, int(h))
                                            lcg = LcgData.get(f"HOLD{h}LCG", 0)
                                            vcg = LcgData.get(f"HOLD{h}VCG", 0)
                                            tcg = LcgData.get(f"HOLD{h}TCG", 0)
                                            volper = LcgData.get(f"HOLD{h}VOLPercentage", 0)
                                            fsm = LcgData.get(f"HOLD{h}FSM", 0)
                                            aftDist = float(AftDistfromAP.get(f"HOLD{h}", 0))
                                            fwdDist = float(FwdDistfromAP.get(f"HOLD{h}", 0))
                                            item = setWeightItems(
                                                f"BH{h}",
                                                float(aftDist),
                                                float(fwdDist),
                                                float(weight),
                                                float(lcg),
                                                float(vcg),
                                                float(tcg), )
                                            list.append(item)

        Tnk = Tnktemp
        pl3=0
        if pl==1:
            pl3==pl

        if pl == len(pschedule):
            pl3=pl-1

        if pl >1 and pl < len(pschedule) and Arrival == True:
            pl3=pl-1

        if pl > 1 and pl < len(pschedule) and Arrival == False:
            pl3 = pl

        for t in range(len(listofTank)):
            if round(Tnk[pl3,t],2) > 0:
                weight=round(Tnk[pl3,t],2)
                volume = weight / getTankDensity(tank, str(listofTank[t]))
                tankvalue = list(filter(lambda row: row.tankname == listofTank[t], tank))
                soundingData2=soundingData
                LcgData = get_souding_lcg_and_vcg(
                    f"listofTank{t}",
                    round(volume, 2),
                    soundingData2
                )
                lcg=LcgData.get(f"listofTank{t}LCG",0)
                vcg=LcgData.get(f"listofTank{t}VCG",0)
                tcg=LcgData.get(f"listofTank{t}TCG",0)
                volper=LcgData.get(f"listofTank{t}VOLPercentage",0)
                fsm=LcgData.get(f"listofTank{t}FSM",0)
                volumeper = (volume * 100) / tankvalue[0].capacity
                aftDist=float(AftDistfromAP.get(f"listofTank{t}",0))
                fwdDist=float(FwdDistfromAP.get(f"listofTank{t}",0))
                weightid = getTankWtItemName(tank, str(listofTank[t]))
                item = setWeightItems(
                    weightid,
                    float(aftDist),
                    float(fwdDist),
                    float(weight),
                    float(lcg),
                    float(vcg),
                    float(tcg),
                )
                list.append(item)


        holdtank = getHoldBallastTank(WBlist, pschedule[pl3])
        BTnk = 0
        if len(holdtank) > 0:
            BTnk = BTnktemp

        for t in range(len(holdtank)):
                if BTnk[pl3 ,t] >= 0.99:
                    if round(getTankWeight(tank, holdtank[t]) * BTnk[pl3, t],2) > 0:
                        weight = round(getTankWeight(tank, holdtank[t]) * BTnk[pl3, t], 2)

                        volume=weight/ getTankDensity(tank, holdtank[t])
                        tankvalue = [row for row in tank if row.tankname == holdtank[t]]
                        soundingData2 = soundingData
                        hold_num = extract_integer(holdtank[t])
                        LcgData = get_souding_lcg_and_vcg(
                            f"HOLD{hold_num}",
                            round(volume, 2),
                            soundingData2
                        )
                        lcg=LcgData.get(f"HOLD{hold_num}LCG",0)
                        vcg=LcgData.get(f"HOLD{hold_num}VCG",0)
                        tcg=LcgData.get(f"HOLD{hold_num}TCG",0)
                        volper=LcgData.get(f"HOLD{hold_num}VOLPercentage",0)
                        fsm=LcgData.get(f"HOLD{hold_num}FSM",0)
                        volumeper = (volume * 100) / tankvalue[0].capacity
                        aftDist=float(AftDistfromAP.get(f"holdtank{t}",0))
                        fwdDist=float(FwdDistfromAP.get(f"holdtank{t}",0))
                        print(f"holdtank[t]=={holdtank[t]}")
                        weightid = getTankWtItemName(tank, holdtank[t])
                        item = setWeightItems(
                            weightid,
                            float(aftDist),
                            float(fwdDist),
                            float(weight),
                            float(lcg),
                            float(vcg),
                            float(tcg),
                        )
                        list.append(item)


    except Exception as e:
        print(f"The exception in getVesselCalculatorInput method: {e}")
        import traceback
        bt = traceback.format_exc()

        for frame in bt:
            print(f"File: {frame.file}, Line: {frame.line}, Function: {frame.func}")

    return list


def get_ballast_tank_details(data,portindex,tankname):
    unpumpable = 0
    capacity=0
    for entry in data:
        if entry['portindex'] == portindex and entry['tankname'] == tankname:
            unpumpable = entry['unpumpableweight'] * entry["density"]
            capacity = entry['capacity'] * entry["density"]
            break
    return unpumpable,capacity

def get_holds_ballast_tank_name(data,portindex):
    holdasballast = []
    for entry in data:
        if entry['portindex'] == portindex and entry['holdtank']=="Y"  :
            holdasballast.append(entry['tankname'])
    return holdasballast

def get_holds_ballast_tank_weight(data,portindex,tankname):
    capacity=0
    for entry in data:
        if entry['portindex'] == portindex and entry['holdtank']=="Y" and entry['tankname']==tankname:
            capacity = entry['capacity'] * entry["density"]
    return capacity

# def get_total_weight_pol_pod_cargo(cargodetails,portindex,cargo,grade):

def set_chartedparty_constraints(mod1,X, chartedPartyFlag,polIdxs,podIdxs,cargo,grade,HoldNos,CargoDetails,ChartedParty,VesselParticulars,pschedule,listofCargo,listofgrade ):
    # print("pschedule,cargo,grade",pschedule,cargo,grade,listofCargo,listofgrade)
    # mod1.update()
    # print("cargo,grade11",listofCargo[0])
    try:
        for pl in range(len(pschedule)):
            for c in range(len(cargo)):
                for g in range(len(grade)):
                    # print("pl,cargo,grade",cargo[c])
                    minqty=0.0
                    maxqty=0.0
                    # print("pl+1,c+1, g+1", pl + 1, c + 1, g + 1)
                    # print("getTotalWeightOf_POL_POD_Cargo2(CargoDetails)",getTotalWeightOf_POL_POD_Cargo2(CargoDetails,pschedule[pl],cargo[c],grade[g]))
                    if getTotalWeightOf_POL_POD_Cargo2(CargoDetails,pschedule[pl],listofCargo[c],listofgrade[g]) > 0 :
                        minqtyall, minqty, podidxall =getcharterpartyMinPercentageValue2(pschedule[pl],listofCargo[c],listofgrade[g],ChartedParty)
                        maxqtyAll, maxqty =getmaxqty(CargoDetails, pschedule[pl], listofCargo[c],listofgrade[g], ChartedParty)
                        # print(minqtyall, minqty, podidxall)
                        if chartedPartyFlag:
                            # print("chartedPartyFlag",chartedPartyFlag)

                                # print("h, pl+1,c+1, g+1",h, pl+1,c+1, g+1)
                            mod1.addConstr(sum((X[h, pl+1,c+1, g+1] ) for h in range(1, len(HoldNos) + 1))<= maxqtyAll,"maxqtyAll")
                            mod1.addConstr(sum((X[h, pl+1, c+1, g+1] ) for h in range(1, len(HoldNos) + 1))>= minqtyall,"minqtyall")
                            dd=0
                            print("dd",len(podidxall),podidxall)
                            for d in podidxall:
                                # print()
                                print("maxqty[d]", maxqty[d], minqty[d], d)
                                print("maxqty[dd]", maxqty,minqty, dd)
                                mod1.addConstr(
                                    sum((X[h, d, c + 1, g + 1]) for h in range(1, len(HoldNos) + 1)) <= maxqty[dd],
                                    f"podmax{d}")
                                mod1.addConstr(
                                    sum((X[h, d, c + 1, g + 1]) for h in range(1, len(HoldNos) + 1)) >= minqty[dd],
                                    f"podmin{d}")
                                dd += 1
        #                         # else:
        #                         #     print(f"Warning: dd {dd} is out of range for maxqty list")
        #                         # print("dd",dd)
        #                         # print("podidxall",podidxall)
        #                         # print("sum((X[d, pl+1, c+1, g+1] ) for d in podidxall)",sum((X[d, pl+1, c+1, g+1] ) for d in podidxall))
        #
        #                 #     # except GurobiError as e:
        #                 #     #     print(f"GurobiError: {e}. Check Gurobi model and constraints.")
        #                 #         # print(chartedPartyFlag)
                        if len(podidxall) >= 1:
                            mod1.addConstr(sum((X[h, pl+1,c+1, g+1] ) for h in range(1, len(HoldNos) + 1))==sum((X[h, d,c+1, g+1] ) for d in podidxall for h in range(1, len(HoldNos) + 1)),"podidxall>=1")
                            mod1.update()
        #
        for p in polIdxs:
            # print("p",p)
            for c in range(len(cargo)):
                for g in range(len(grade)):
                    for h in range(1, len(HoldNos) + 1):
                        podall=getpodforpol(CargoDetails,p,listofCargo[c], listofgrade[g])
                        mod1.addConstr(X[h, p, c+1, g+1]==sum((X[h, pl, c+1, g+1] for pl in range(1,len(podall)+1 ))),"podall")
                        mod1.update()
    except Exception as e:
            print(f"The Exception in set_chartedparty_constraints Method", e)
    return mod1


def getVolumeConstraints(mod1,X,VesselParticulars,VolumeFlag,HoldNos,cargo,grade,polIdxs,podIdxs,listofCargo,listofgrade,CargoDetails):
    try:
        SFCargoGrade = {(item['name'], item['grade']): item['stowagefactor'] for item in CargoDetails}
        # print("SFCargoGrade",SFCargoGrade)
        if VolumeFlag:
            for h in range(1,len(HoldNos)+1):
                xvol = []
                for pl in range(1,len(polIdxs)+1):
                    for c in range(len(listofCargo)):
                        for g in range(len(listofgrade)):
                            key = (listofCargo[c], listofgrade[g])  # Form the key as a tuple
                            # value = SFCargoGrade.get(key, 1)
                            zz=1/SFCargoGrade.get(key, 1)
                            expr = gp.LinExpr()
                            # print("zz",zz)
                            expr+=X[h, pl, c+1, g+1] * zz
                            xvol.append(expr)
                ylen = len(xvol)
                # print(ylen)
                mod1.addConstr(sum( xvol[i] for i in range(ylen)) <= getHoldVolumeMaxBounds(VesselParticulars,h),"yy")
    except Exception as e:
        print(f"The Exception in getVolumeConstraints Method", e)
    return mod1


def getWeightConstraints(mod1,X,weightFlag,HoldNos,cargoTypesize,grade_size,polIdxs,VesselParticulars):
    try:
        if weightFlag:
            for h in range(1,len(HoldNos)+1):
                xvol = []
                for pl in range(1,len(polIdxs)+1):
                    for c in range(len(cargoTypesize)):
                        for g in range(len(grade_size)):
                            expr = gp.LinExpr()
                            expr+=X[h, pl, c+1, g+1]
                            xvol.append(expr)
                ylen = len(xvol)
                # print(" getHoldWeightMaxBounds(VesselParticulars,h)", getHoldWeightMaxBounds(VesselParticulars,h))
                mod1.addConstr(sum(xvol[i] for i in range(ylen)) <= getHoldWeightMaxBounds(VesselParticulars,h),"ww")
    except Exception as e:
        print(f"The Exception in getWeightConstraints Method", e)
    return mod1


def getadjacentMixedBinarylink(mod1,X,B,adjcargo2,mixedCargoFlag,AdjacentCargoFlag,HoldNos,cargo,grade,polIdxs,CargoDetails,VesselParticulars):
    try:
        if AdjacentCargoFlag==True:
            for pl in range(1,len(polIdxs)+1):
                for c in range(len(cargo)):
                    if len(grade) >=2 or len(cargo)>=2:
                        for g in range(len(grade)):
                            for h in range(1,len(HoldNos)):
                                # print("adan",adjcargo2[h, pl, c+1, g+1])
                                mod1.addConstr(B[h, pl, c+1, g+1] + B[h+1, pl, c+1, g+1] <= 1 + adjcargo2[h, pl, c+1, g+1],"AdjacentCargoFlag" )
                                mod1.update()
        if AdjacentCargoFlag == True or mixedCargoFlag== True:
            for pl in range(1,len(polIdxs)+1):
                for c in range(len(cargo)):
                    for g in range(len(grade)):
                        if len(grade) >= 2 or len(cargo) >= 2:
                            for h in range(1, len(HoldNos) + 1):
                                holdweight = getHoldWeightMaxBounds(VesselParticulars, h)
                                holdweight2 = holdweight * 3
                                mod1.addConstr(X[h, pl, c+1, g+1] >= 0 - holdweight2 * (1 - B[h, pl, c+1, g+1]))
                                mod1.addConstr(X[h, pl, c + 1, g + 1] <= 0 + holdweight2 * (B[h, pl, c + 1, g + 1]))
                                mod1.update()
        if mixedCargoFlag==True:
            if len(grade) >= 2 or len(cargo) >= 2:
                print("mixedCargoFlag", mixedCargoFlag)
                for h in range(1, len(HoldNos)+1):
                    # print("sinnjfb")
                    mod1.addConstr(sum(B[h, pl, c+1, g+1] for pl in range(1,len(polIdxs)+1) for g in range(len(grade)) for c in range(len(cargo))) <=1,"mixedCargoFlag")
                    mod1.update()
    except Exception as e:
        print(f"The Exception in getadjacentMixedBinarylink Method", e)
    return mod1

# def getUserAllocationmodel(mod1,X,Allocationdata,HoldNos,cargo,grade,listofCargo,listofgrade,pschedule,PreferedFlag):
#     try:
#         if PreferedFlag == True:
#             for obj in Allocationdata:
#                 for h in range(1,len(HoldNos)):
#                     if obj[]






def getmaxqty(loadlistcargo,polIdx,cargotype,grade,charterParty):
    try:
        weight = 0
        weightAll = []
        for app in loadlistcargo:
            for app1 in charterParty:
                if (
                        str(polIdx) + cargotype.upper() + grade.upper() ==
                        str(app['polIdx']) + app['name'].upper() + app['grade'].upper() and
                        str(polIdx) + cargotype.upper() + grade.upper() ==
                        str(app1['polIdx']) + app1['cargo'].upper() + app1['grade'].upper()
                ):
                    # print("str(polIdx) + cargotype.upper() + grade.upper()",str(polIdx) + cargotype.upper() + grade.upper())
                    weight += app["weight"]+app["weight"]*(app1["plusorminus"]/100)
                    weight2=app["weight"]+app["weight"]*(app1["plusorminus"]/100)
                    weightAll.append(weight2)
                    break
        return weight,weightAll
    except Exception as e:
        print("The Exception in getmaxqty Method:", e)
        return weight


def getmaxqtypod(loadlistcargo,polIdx,cargotype,grade,charterParty):
    try:
        weight = 0
        weightAll = []
        maxWeightCar = 0.0
        for app in loadlistcargo:
            for app1 in charterParty:
                if (
                        str(polIdx) + cargotype.upper() + grade.upper() ==
                        str(app['polIdx']) + app['name'].upper() + app['grade'].upper() and
                        str(polIdx) + cargotype.upper() + grade.upper() ==
                        str(app1['polIdx']) + app1['cargo'].upper() + app1['grade'].upper()
                ):
                    weight += app["weight"]+app["weight"]*(app1["plusorminus"]/100)
                    weight2=app["weight"]+app["weight"]*(app1["plusorminus"]/100)
                    weightAll.append(weight2)
                    break
        maxWeightCar = sum(weightAll)
        return maxWeightCar
    except Exception as e:
        print("The Exception in getmaxqtypod Method:", e)
        return maxWeightCar

def getpodforpol(loadlistcargo,polIdx,cargotype,grade):
    try:
        podlist=[]
        for app in loadlistcargo:
            if (
                        str(polIdx) + cargotype.upper() + grade.upper() ==
                        str(app['polIdx']) + app['name'].upper() + app['grade'].upper()
                ):
                podlist.append(app["pod"])

        return podlist
    except Exception as e:
        print("The Exception in getpodforpol Method:", e)
        return podlist

def getpolforpod(loadlistcargo,polIdx,cargotype,grade):
    try:
        polIdx=[]
        for app in loadlistcargo:
            if (
                        str(polIdx) + cargotype.upper() + grade.upper() ==
                        str(app['polIdx']) + app['name'].upper() + app['grade'].upper()
                ):
                polIdx.append(app["polIdx"])

        return polIdx
    except Exception as e:
        print("The Exception in getpolforpod Method:", e)
        return polIdx
def AutoAllocation5hold(mod1,X,B,HoldNos,cargo,grade,polIdxs,CargoDetails,ChartedParty,VesselParticulars,listofCargo,listofgrade):
    try:
        holdweighlimit = []
        holdvolimit = []
        # print("HoldNos",HoldNos)
        midhold = int((len(HoldNos) + 1) / 2)
        # print("midhold====", midhold)
        for i in range(1,len(HoldNos)+1):
            # zz = {int(item['Hold No.']): float(item['Max. Weight (MT)']) for item in VesselParticulars}
            zz=getHoldWeightMaxBounds(VesselParticulars,i)
            # print("zz",zz)
            # print("weight_by_hold",weight_by_hold)
            # yy = {int(item['Hold No.']): float(item['Volume without Hatch']) for item in VesselParticulars}
            yy=getHoldWeightMaxBounds(VesselParticulars,i)
            # print("yy",yy)
            holdweighlimit.append(zz)
            holdvolimit.append(yy)
        bmidhold = False
        btwohold = False
        bthreedhold = False
        bfourhold = False
        SFCargoGrade = {(item['name'], item['grade']): item['stowagefactor'] for item in CargoDetails}
        # X = mod1.getVarsByName("X")
        # B = mod1.getVarsByName("B")
        print("polIdxs",polIdxs)
        for p in polIdxs:
            for c in range(len(cargo)):
                for g in range(len(grade)):
                    # print(p,c,g,ChartedParty)
                    minqty=getcharterpartyMinCargopol(p,cargo[c],grade[g],ChartedParty)
                    # print("minqty",minqty)
                    sfgrade= 1 / (SFCargoGrade.get(f"{listofCargo[c]}{listofgrade[g]}", 1))
                    # print("sfgrade",sfgrade)
                    minvol = minqty * sfgrade
                    # print("minvol",minvol)
                    if minvol == 0:
                        for h in range(1,(len(HoldNos))+1):
                            # print("minvol",minvol)
                            mod1.addConstr(X[h,p,c+1,g+1]==0)
                            mod1.addConstr(B[h,p,c+1,g+1]==0)
                            mod1.update()
                    else:
                        if p ==1:
                            print("holdvolimit", holdvolimit[midhold])
                            if (holdvolimit[midhold]>= minvol and minvol>0 and holdweighlimit[midhold]>= minqty):
                        #         # print("minvol2",minvol)
                                mod1.addConstr(X[midhold,p,c+1,g+1] >= 1)
                                mod1.addConstr(B[midhold,p,c+1,g+1] >= 1)
                                mod1.update()
                                bmidhold=True
                            elif ( (holdvolimit[midhold-1] +holdvolimit[midhold+1] ) >= minvol and minvol>0
                                    and (holdweighlimit[midhold-1] +holdweighlimit[midhold+1])>= minqty):
                                    btwohold = True
                                    mod1.addConstr(X[midhold-1, p, c+1, g+1] >= 1)
                                    mod1.addConstr(B[midhold-1, p, c+1, g+1] >= 1)
                                    mod1.addConstr(X[midhold +1, p, c+1, g+1] >= 1)
                                    mod1.addConstr(B[midhold + 1, p, c+1, g+1] >= 1)
                                    mod1.update()
                            elif ( (holdvolimit[midhold-2] +holdvolimit[midhold+2]+holdvolimit[midhold-1]+holdvolimit[midhold+1]) >= minvol and minvol >0) and ((holdweighlimit[midhold-2]+holdvolimit[midhold+2]+holdvolimit[midhold-1]+holdweighlimit[midhold+1] >= minqty)):
                                bthreedhold = True
                                mod1.addConstr(X[midhold-2, p, c+1, g+1] >= 1)
                                mod1.addConstr(B[midhold-2, p, c+1, g+1] >= 1)
                                mod1.addConstr(X[midhold +2, p, c+1, g+1] >= 1)
                                mod1.addConstr(B[midhold + 2, p, c+1, g+1] >= 1)
                                mod1.addConstr(X[midhold-1, p, c+1, g+1] >= 1)
                                mod1.addConstr(B[midhold-1, p, c+1, g+1] >= 1)
                                mod1.addConstr(X[midhold +1, p, c+1, g+1] >= 1)
                                mod1.addConstr(B[midhold + 1, p, c+1, g+1] >= 1)


                            if p>1 and bmidhold==True:
                                mod1.addConstr(X[midhold, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold, p, c+1, g+1] == 0)
                                mod1.update()
                            elif p>1 and btwohold==True:
                                mod1.addConstr(X[midhold-1, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold-1, p, c+1, g+1] == 0)
                                mod1.addConstr(X[midhold + 1, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold + 1, p, c+1, g+1] == 0)
                                mod1.update()
                            elif p>1 and bthreedhold==True:
                                mod1.addConstr(X[midhold-2, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold-2, p, c+1, g+1] == 0)
                                mod1.addConstr(X[midhold + 2, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold + 2, p, c+1, g+1] == 0)
                                mod1.addConstr(X[midhold, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold, p, c+1, g+1] == 0)
                                mod1.update
                            elif p>1 and bfourhold==True:
                                mod1.addConstr(X[midhold-2, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold-2, p, c+1, g+1] == 0)
                                mod1.addConstr(X[midhold+2, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold+2, p, c+1, g+1] == 0)
                                mod1.addConstr(X[midhold - 1, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold - 1, p, c+1, g+1] == 0)
                                mod1.addConstr(X[midhold + 1, p, c+1, g+1] == 0)
                                mod1.addConstr(B[midhold + 1, p, c+1, g+1] == 0)
                                mod1.update
    except Exception as e:
        print(f"The Exception in AutoAllocation5hold Method", e)

def AutoAllocation7hold(mod1,X,B,HoldNos,cargo,grade,polIdxs,CargoDetails,ChartedParty,VesselParticulars,listofCargo,listofgrade):
    try:
        holdweighlimit = []
        holdvolimit = []
        midhold = int((len(HoldNos) + 1) / 2)

        for i in range(1,len(HoldNos)+1):
            zz = getHoldWeightMaxBounds(VesselParticulars, i)
            # print("zz",zz)
            # print("weight_by_hold",weight_by_hold)
            # yy = {int(item['Hold No.']): float(item['Volume without Hatch']) for item in VesselParticulars}
            yy = getHoldWeightMaxBounds(VesselParticulars, i)
            # print("yy",yy)
            holdweighlimit.append(zz)
            holdvolimit.append(yy)
        bmidhold = False
        btwohold = False
        bthreedhold = False
        bfourhold = False
        bfivehold = False
        bsixhold = False
        SFCargoGrade = {(item['name'], item['grade']): item['stowagefactor'] for item in CargoDetails}
        # X = mod1[:X]  # Assuming x is a list or array of variables
        # B = mod1[:B]
        for p in polIdxs:
            for c in range(len(cargo)):
                for g in range(len(grade)):
                    minqty = getcharterpartyMinCargopol(p, cargo[c], grade[g], ChartedParty)
                    sfgrade = 1 / (SFCargoGrade.get(f"{listofCargo[c]}{listofgrade[g]}", 1))
                    minvol = minqty * sfgrade
                    if minvol == 0:
                        for h in range(1,(len(HoldNos))+1):
                            mod1.addConstr(X[h,p,c+1,g+1]==0)
                            mod1.addConstr(B[h,p,c+1,g+1]==0)
                            mod1.update()
                    else:
                        if p ==1:
                            if (holdvolimit[midhold]>= minvol and minvol>0 and holdweighlimit[midhold]>= minqty):
                                mod1.addConstr(X[midhold,p,c+1,g+1]>=1)
                                mod1.addConstr(B[midhold,p,c+1,g+1]>=1)
                                bmidhold=True
                                mod1.update()
                            elif (((holdvolimit[midhold-1]+holdvolimit[midhold+1]) >= minvol and minvol>0) and ((holdweighlimit[midhold-1]+holdweighlimit[midhold+1])>=minqty)):
                                btwohold = True
                                mod1.addConstr(X[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold +1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 1, p, c+1, g+1]>=1)
                                mod1.update()
                            elif (((holdvolimit[midhold-2]+holdvolimit[midhold+2]+holdvolimit[midhold]) >= minvol and minvol>0) and ((holdweighlimit[midhold-2]+holdweighlimit[midhold+2]+holdweighlimit[midhold])>=minqty)):
                                bthreedhold = True
                                mod1.addConstr(X[midhold-2, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-2, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold + 2, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 2, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold, p, c+1, g+1]>=1)
                                mod1.update()
                            elif (((holdvolimit[midhold-3]+holdvolimit[midhold+3]+holdvolimit[midhold-1]+holdvolimit[midhold+1] )>=minvol and minvol>0) and ((holdweighlimit[midhold-3]+holdweighlimit[midhold+3]+holdweighlimit[midhold-1]+holdweighlimit[midhold+1])>=minqty)):
                                bfourhold = True
                                mod1.addConstr(X[midhold-3, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-3, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold+3, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold+3, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold + 1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 1, p, c+1, g+1]>=1)
                                mod1.update()
                            elif (((holdvolimit[midhold-3]+holdvolimit[midhold+3]+holdvolimit[midhold-1]+holdvolimit[midhold+1]+holdvolimit[midhold-2] +holdvolimit[midhold+2]  )>=minvol and minvol>0) and ((holdweighlimit[midhold-3]+holdweighlimit[midhold+3]+holdweighlimit[midhold-1]+holdweighlimit[midhold+1]+holdweighlimit[midhold-2] +holdweighlimit[midhold+2])>=minqty)):
                                bmsixhold = True
                                mod1.addConstr(X[midhold-3, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-3, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold+3, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold+3, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold + 1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 1, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold-2, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-2, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold + 2, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 2, p, c+1, g+1]>=1)
                                mod1.update()
                        if p>1 and bmidhold==True:
                            mod1.addConstr(X[midhold, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold, p, c+1, g+1] == 0)
                            mod1.update()
                        elif p>1 and btwohold == True:
                            mod1.addConstr(X[midhold-1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold-1, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold +1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold + 1, p, c+1, g+1] == 0)
                            mod1.update()
                        elif p>1 and bthreedhold==True:
                            mod1.addConstr(X[midhold-2, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold-2, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold + 2, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold + 2, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold, p, c+1, g+1] == 0)
                            mod1.update()
                        elif p>1 and bfourhold==True:
                            mod1.addConstr(X[midhold-3, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold-3, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold+3, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold+3, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold-1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold-1, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold + 1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold + 1, p, c+1, g+1] == 0)
                            mod1.update()
                        elif p>1 and bmsixhold==True:
                            mod1.addConstr(X[midhold-3, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold-3, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold+3, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold+3, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold-1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold-1, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold + 1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold + 1, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold-2, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold-2, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold + 2, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold + 2, p, c+1, g+1] == 0)
                            mod1.update()
    except Exception as e:
        print(f"The Exception in AutoAllocation7hold Method", e)


def AutoAllocation9hold(mod1,X,B,HoldNos,cargo,grade,polIdxs,CargoDetails,ChartedParty,VesselParticulars,listofCargo,listofgrade):
    try:
        holdweighlimit=[]
        holdvolimit=[]
        midhold=int((len(HoldNos) + 1) / 2)
        for i in range(1,len(HoldNos)+1):
            zz = getHoldWeightMaxBounds(VesselParticulars, i)
            yy = getHoldWeightMaxBounds(VesselParticulars, i)
            # print("yy",yy)
            holdweighlimit.append(zz)
            holdvolimit.append(yy)
        bmidhold = False
        btwohold = False
        bthreedhold = False
        bfourhold = False
        bfivehold = False
        SFCargoGrade = {(item['name'], item['grade']): item['stowagefactor'] for item in CargoDetails}
        # X=mod1[:X]
        # B=mod1[:B]
        for p in polIdxs:
            for c in range(len(cargo)):
                for g in range(len(grade)):
                    minqty=getcharterpartyMinCargopol(p,listofCargo[c], listofgrade[g],ChartedParty)
                    sfgrade = 1 / (SFCargoGrade.get(f"{listofCargo[c]}{listofgrade[g]}", 1))
                    minvol = minqty * sfgrade
                    if minvol == 0:
                        for h in range(1,len(HoldNos)):
                            mod1.addConstr(X[h, p, c+1, g+1] == 0)
                            mod1.addConstr(B[h, p, c+1, g+1] == 0)
                            mod1.update()
                    else:
                        if p==1:
                            if (holdvolimit[midhold]>= minvol and minvol>0  #1hold #4
                                    and (holdweighlimit[midhold]>= minqty)):
                                bmidhold = True
                                mod1.addConstr(X[midhold, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold, p, c+1, g+1]>=1)
                            elif (       ###2 hold  3,5
                                ( (holdvolimit[midhold-1] +holdvolimit[midhold+1] )
                                    >= minvol and  minvol>0)
                                    and
                                ( (holdweighlimit[midhold-1] +holdweighlimit[midhold+1])
                                    >= minqty)
                                    )  :
                                btwohold = True
                                mod1.addConstr(X[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold + 1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 1, p, c+1, g+1]>=1)
                                mod1.update()
                            elif (  ####3 hold 2, 4 ,6
                                    ( (holdvolimit[midhold-2] +holdvolimit[midhold+2] + holdvolimit[midhold] )
                                        >= minvol and  minvol>0)
                                        and
                                    ( (holdweighlimit[midhold-2] +holdweighlimit[midhold+2]+holdweighlimit[midhold] )
                                        >= minqty)
                                        ):
                                bthreedhold = True
                                mod1.addConstr(X[midhold-2, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-2, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold + 2, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 2, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold, p, c+1, g+1]>=1)
                                mod1.update()
                            elif (  ####4 hold 1,3,5,7
                                        ( (holdvolimit[midhold-3] +holdvolimit[midhold+3]
                                        + holdvolimit[midhold-1] +holdvolimit[midhold+1]  )
                                            >= minvol and  minvol>0)
                                            and
                                        ( (holdweighlimit[midhold-3] +holdweighlimit[midhold+3]

                                        +holdweighlimit[midhold-1] +holdweighlimit[midhold+1] )
                                            >= minqty)
                                            ):
                                bfourhold = True
                                mod1.addConstr(X[midhold-3, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-3, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold+3, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold+3, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-1, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold + 1, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 1, p, c+1, g+1]>=1)
                                mod1.update()
                            elif  (  ####5 hold 1,3,5,7
                                            ( (holdvolimit[midhold-2] +holdvolimit[midhold+2]
                                            + holdvolimit[midhold-4] +holdvolimit[midhold+4] + holdvolimit[midhold] )
                                                >= minvol and  minvol>0)
                                                and
                                            ( (holdweighlimit[midhold-2] +holdweighlimit[midhold+2]

                                            +holdweighlimit[midhold-4] +holdweighlimit[midhold+4] +holdweighlimit[midhold] )
                                                >= minqty)
                                                ):
                                bfivehold=True
                                mod1.addConstr(X[midhold-2, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-2, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold + 2, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 2, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold-4, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold-4, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold + 4, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold + 4, p, c+1, g+1]>=1)
                                mod1.addConstr(X[midhold, p, c+1, g+1]>=1)
                                mod1.addConstr(B[midhold, p, c+1, g+1]>=1)
                                mod1.update()
                        if p>1 and bmidhold==True:
                            mod1.addConstr(X[midhold , p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold , p, c+1, g+1] == 0)
                            mod1.update()
                        elif p>1 and btwohold==True:
                            mod1.addConstr(X[midhold - 1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold - 1, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold + 1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold + 1, p, c+1, g+1] == 0)
                            mod1.update()
                        elif p>1 and bthreedhold==True:
                            mod1.addConstr(X[midhold - 2, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold - 2, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold + 2, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold + 2, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold, p, c+1, g+1] == 0)
                            mod1.update()
                        elif p>1 and bfourhold==True:
                            mod1.addConstr(X[midhold - 2, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold - 2, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold + 2, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold + 2, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold - 1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold - 1, p, c+1, g+1] == 0)
                            mod1.addConstr(X[midhold + 1, p, c+1, g+1] == 0)
                            mod1.addConstr(B[midhold + 1, p, c+1, g+1] == 0)
                            mod1.update()
    except Exception as e:
        print(f"The Exception in AutoAllocation9hold Method", e)
def AutoAllocation11hold(mod1,X,B,HoldNos,cargo,grade,polIdxs,CargoDetails,ChartedParty,VesselParticulars,listofCargo,listofgrade):
    try:
        holdweighlimit = []
        holdvolimit = []
        midhold=int((len(HoldNos) + 1) / 2)
        for i in range(1,len(HoldNos)+1):
            zz=getHoldWeightMaxBounds(VesselParticulars,i)
            # print("weight_by_hold",weight_by_hold)
            yy=getHoldWeightMaxBounds(VesselParticulars,i)
            holdweighlimit.append(zz)
            holdvolimit.append(yy)
        bmidhold = False
        btwohold = False
        bthreedhold = False
        bfourhold = False
        bfivehold = False
        bsixhold = False
        SFCargoGrade = {(item['name'], item['grade']): item['stowagefactor'] for item in CargoDetails}
        # X = mod1[:X]  # Assuming x is a list or array of variables
        # B = mod1[:B]
        for p in polIdxs:
            for c in range(len(cargo)):
                for g in range(len(grade)):
                    minqty = getcharterpartyMinCargopol(p, cargo[c], grade[g], ChartedParty)
                    sfgrade = 1 / (SFCargoGrade.get(f"{listofCargo[c]}{listofgrade[g]}", 1))
                    minvol = minqty * sfgrade
                    if minvol == 0:
                        for h in range(1,len(HoldNos)+1):
                            mod1.addConstr(X[h,p,c+1,g+1]==0)
                            mod1.addConstr(B[h,p,c+1,g+1]==0)
                    else:
                        if p==1:
                            if (holdvolimit[midhold]>= minvol and minvol>0  #1hold #4
                                    and (holdweighlimit[midhold]>= minqty)):
                                mod1.addConstr(X[midhold,p,c+1,g+1]>=1)
                                mod1.addConstr(B[midhold,p,c+1,g+1]>=1)
                                bmidhold=True
                                mod1.update()
                            elif (       ###2 hold  3,5
                                ( (holdvolimit[midhold-1] +holdvolimit[midhold+1] )
                                    >= minvol and  minvol>0)
                                    and
                                ( (holdweighlimit[midhold-1] +holdweighlimit[midhold+1])
                                    >= minqty)
                                    )  :
                                btwohold=True
                                mod1.addConstr(X[midhold - 1, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold - 1, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold + 1, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold + 1, p, c+1,g+1]>=1)
                                mod1.update()
                            elif (  ####3 hold 2, 4 ,6
                                    ( (holdvolimit[midhold-2] +holdvolimit[midhold+2] + holdvolimit[midhold] )
                                        >= minvol and  minvol>0)
                                        and
                                    ( (holdweighlimit[midhold-2] +holdweighlimit[midhold+2]+holdweighlimit[midhold] )
                                        >= minqty)
                                        ):
                                bthreedhold=True
                                mod1.addConstr(X[midhold - 2, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold - 2, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold + 2, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold + 2, p,c+1,g+1]>=1)
                                mod1.addConstr(X[midhold, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold, p, c+1,g+1]>=1)
                                mod1.update()
                            elif (  ####4 hold 1,3,5,7
                                        ( (holdvolimit[midhold-3] +holdvolimit[midhold+3]
                                        + holdvolimit[midhold-1] +holdvolimit[midhold+1]  )
                                            >= minvol and  minvol>0)
                                            and
                                        ( (holdweighlimit[midhold-3] +holdweighlimit[midhold+3]

                                        +holdweighlimit[midhold-1] +holdweighlimit[midhold+1] )
                                            >= minqty)
                                            ):
                                bfourhold=True
                                mod1.addConstr(X[midhold - 3, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold - 3, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold + 3, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold + 3, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold - 1, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold - 1, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold + 1, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold + 1, p, c+1,g+1]>=1)
                                mod1.update()
                            elif (  ####5 hold 1,3,5,7
                                            ( (holdvolimit[midhold-2] +holdvolimit[midhold+2]
                                            + holdvolimit[midhold-4] +holdvolimit[midhold+4] + holdvolimit[midhold] )
                                                >= minvol and  minvol>0)
                                                and
                                            ( (holdweighlimit[midhold-2] +holdweighlimit[midhold+2]

                                            +holdweighlimit[midhold-4] +holdweighlimit[midhold+4] +holdweighlimit[midhold] )
                                                >= minqty)
                                                ):
                                bfivehold=True
                                mod1.addConstr(X[midhold - 2, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold - 2, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold + 2, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold + 2, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold - 4, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold - 4, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold + 4, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold + 4, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold, p, c+1,g+1]>=1)
                                mod1.update()
                            elif (  ####5 hold 1,3,5,7
                                                ( (holdvolimit[midhold-1] +holdvolimit[midhold+1]
                                                + holdvolimit[midhold-3] +holdvolimit[midhold+3] +
                                                holdvolimit[midhold-5] + holdvolimit[midhold+5] )
                                                    >= minvol and  minvol>0)
                                                    and
                                                ( (holdweighlimit[midhold-1] +holdweighlimit[midhold+1]

                                                +holdweighlimit[midhold-3] +holdweighlimit[midhold+3] +
                                                holdweighlimit[midhold-5] + holdweighlimit[midhold+5] )
                                                    >= minqty)
                                                    ):
                                bsixhold=True
                                mod1.addConstr(X[midhold - 1, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold - 1, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold + 1, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold + 1, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold - 3, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold - 3, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold + 3, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold + 3, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold + 5, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold + 5, p, c+1,g+1]>=1)
                                mod1.addConstr(X[midhold - 5, p, c+1,g+1]>=1)
                                mod1.addConstr(B[midhold - 5, p, c+1,g+1]>=1)
                                mod1.update()
                        if p > 1 and bmidhold ==True:
                            mod1.addConstr(X[midhold, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold, p, c+1,g+1] ==0)
                            mod1.update()
                        elif p > 1 and btwohold ==True:
                            mod1.addConstr(X[midhold - 1, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold - 1, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold + 1, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold + 1, p, c+1,g+1] ==0)
                            mod1.update()
                        elif p>1 and bthreedhold==True:
                            mod1.addConstr(X[midhold - 2, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold - 2, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold + 2, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold + 2, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold, p, c+1,g+1] ==0)
                            mod1.update()
                        elif p>1 and bfourhold == True:
                            mod1.addConstr(X[midhold - 3, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold - 3, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold + 3, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold + 3, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold - 1, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold - 1, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold + 1, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold + 1, p, c+1,g+1] ==0)
                            mod1.update()
                        elif p>1 and bfivehold == True:
                            mod1.addConstr(X[midhold - 2, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold - 2, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold + 2, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold + 2, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold - 4, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold - 4, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold + 4, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold + 4, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold , p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold , p, c+1,g+1] ==0)
                        elif p >1 and bsixhold == True:
                            mod1.addConstr(X[midhold - 1, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold - 1, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold + 1, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold + 1, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold - 3, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold - 3, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold + 3, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold + 3, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold + 5, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold + 5, p, c+1,g+1] ==0)
                            mod1.addConstr(X[midhold - 5, p, c+1,g+1] ==0)
                            mod1.addConstr(B[midhold - 5, p, c+1,g+1] ==0)
                            mod1.update()


    except Exception as e:
        print(f"The Exception in AutoAllocation11hold Method", e)










