import pandas as pd
from CommonInfo.CommonInfo import setWeightItems
from Tankinfo.Tank import getTankWtItemName,getTankDensity,getTankWeight
import numpy as np
from Vesselinfo.VesselParticulars import getHoldVolumeMaxBounds
from NonlinearInfo.commonfunction import getpodforpol,getpolforpod
from StabilityInfo.SoundingData import get_souding_lcg_and_vcg
from InputInfo.CargoDetail import getpreviousPODPOL
from Tankinfo.WNTankList import getHoldBallastTank
from NonlinearInfo.Nonlinear_modelling_printing_SF_BM import extract_integer

def getVesselCalculatorInput(
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
        # print("9273-pl===$pl")
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




































