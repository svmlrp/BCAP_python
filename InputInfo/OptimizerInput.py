def getSchedule(ScheduleData):

    schedule=[]
    try:
        for i in len(ScheduleData):
            schedule.append(ScheduleData[i].get( "servicecode", ""))
            schedule.append(ScheduleData[i].get("vesselName", ""))
            schedule.append(ScheduleData[i].get("voyageno", ""))
            schedule.append(ScheduleData[i].get("portcode", ""))
            schedule.append(ScheduleData[i].get("portname", ""))
            schedule.append(ScheduleData[i].get("bound", ""))
            schedule.append(ScheduleData[i].get("shortportcode", ""))
            schedule.append(ScheduleData[i].get("terminalcode", ""))
            schedule.append(ScheduleData[i].get("arrivaldate", ""))
            schedule.append(ScheduleData[i].get("departuredate", ""))
            schedule.append(ScheduleData[i].get("currentport", "N"))
            schedule.append(ScheduleData[i].get("Portindex", "1"))
            schedule.append(ScheduleData[i].get("portcolor", "255,255,255"))

        return schedule
    except Exception as e:
        print(f"The Exception in getSchedule Method:", e)
        return -1

def getMTPerMeterCubeFromCubicFT(cubicfeet):
    MTperMeterCubic: float=0.0
    try:
        cubicFTperLT: float=0.0
        meterCubicperLT: float=0.0
        meterCubicperMT: float=0.0
        cubicFTperLT=round(cubicfeet * 1.016047, 3)
        meterCubicperLT=round(cubicFTperLT / 35.3147, 3)
        meterCubicperMT=round(meterCubicperLT * 0.984206, 3)
        MTperMeterCubic=round(1 / meterCubicperMT, 3)
        return MTperMeterCubic
    except Exception as e:
        print(f"The Exception in getMTPerMeterCubeFromCubicFT Method:", e)
        return -1

def getCargoDetails(CargoDetailsData):
    cargodetails=[]
    try:
        for i in range(len(CargoDetailsData)):
            cargodetails.append(CargoDetailsData[i].get("pol", ""),
                                CargoDetailsData[i].get("polIdx", "1"),
                                CargoDetailsData[i].get("pod", ""),
                                CargoDetailsData[i].get("podIdx", "2"),
                                CargoDetailsData[i].get("name", ""),
                                CargoDetailsData[i].get("grade", ""),
                                CargoDetailsData[i].get("weight", 0),
                                getMTPerMeterCubeFromCubicFT(float(CargoDetailsData[i].get("stowagefactor", 1))),
                                CargoDetailsData[i].get("maxdischarge", "N"))
        return CargoDetailsData
    except Exception as e:
        print(f"The Exception in getCargoDetails Method:", e)
        return -1


def getUserAllocation(useralloc):
    userallocation=[]
    try:
        for i in range(len(useralloc)):
            userallocation.append(useralloc[i].get("pol", ""),
                                  useralloc[i].get("polIdx", int(1)),
                                  str(useralloc[i].get("pod", "")),
                                  useralloc[i].get("podIdx", int(2)),
                                  useralloc[i].get("cargotype", ""),
                                  useralloc[i].get("grade", ""),
                                  useralloc[i].get("holdno", int(0)),
                                  useralloc[i].get("useralloc", int(1)),
                                  useralloc[i].get("quantity",1)

                                )
            return userallocation
    except Exception as e:
        print(f"The Exception in getUserAllocation Method:", e)
        return -1


def getCharterPartyAssumption(ChartedPartyAssumptionData):
    chartedPartyAssumption=[]
    try:
        for i in range(len(ChartedPartyAssumptionData)):
            chartedPartyAssumption.append(ChartedPartyAssumptionData[i].get("cargo", ""),
                                          ChartedPartyAssumptionData[i].get("techname", ""),
                                          ChartedPartyAssumptionData[i].get("grade", ""),
                                          getMTPerMeterCubeFromCubicFT(ChartedPartyAssumptionData[i].get("stowagefactor", 1)),
                                          ChartedPartyAssumptionData[i].get("terms", ""),
                                          ChartedPartyAssumptionData[i].get("contract_qty", 0),
                                          ChartedPartyAssumptionData[i].get("customer_request", 0),
                                          ChartedPartyAssumptionData[i].get("plusorminus", 0),
                                          ChartedPartyAssumptionData[i].get("pol", ""),
                                          ChartedPartyAssumptionData[i].get("polIdx", 1),
                                          ChartedPartyAssumptionData[i].get("pol_terminal", ""),
                                          ChartedPartyAssumptionData[i].get("pol_berth", ""),
                                          ChartedPartyAssumptionData[i].get("pod", ""),
                                          ChartedPartyAssumptionData[i].get("podIdx", ""),
                                          ChartedPartyAssumptionData[i].get("pod_terminal", ""),
                                          ChartedPartyAssumptionData[i].get("pod_berth", "")







                                          )
            return ChartedPartyAssumptionData
    except Exception as e:
        print(f"The Exception in getCharterPartyAssumption Method:", e)
        return -1

def getParameter(TargetTrimData):
    targettrim=[]
    try:
        for i in range(len(TargetTrimData)):
            targettrim.append(TargetTrimData[i].get("pol",""),
                              TargetTrimData[i].get("polidx",0),
                              TargetTrimData[i].get("trim", 0),
                              TargetTrimData[i].get("meandraft", 0),
                              TargetTrimData[i].get("ballast", 0),
                              TargetTrimData[i].get("deballast", 0),
                              TargetTrimData[i].get("tankwt", 0),
                              TargetTrimData[i].get("SFValue", ""),
                              TargetTrimData[i].get("BMValue", ""),
                              TargetTrimData[i].get("seaWaterDensity", 1.025),
                              TargetTrimData[i].get("draftlimit", -1),
                              TargetTrimData[i].get("hogorsag", "Hog"),
                              TargetTrimData[i].get("hogorsagvalue", -1),
                              TargetTrimData[i].get("stress", 0),
                              TargetTrimData[i].get("arrivaldraft", 0),
                              TargetTrimData[i].get("seaport", 0),
                              TargetTrimData[i].get("arrivalswdensity", 1.025),
                              TargetTrimData[i].get("loadwaterline", "Tropical Draft"),
                              TargetTrimData[i].get("draft", 10),
                              TargetTrimData[i].get("airdraft", 0),
                              TargetTrimData[i].get("NumberofHatchCovers", 0),
                              TargetTrimData[i].get("airdraftHatchcover", 0)


                              )
            return targettrim
    except Exception as e:
        print(f"The Exception in getParameter Method:", e)
        return -1


def getTankData(TankInput):
    tankdata=[]
    try:
        for i in range(len(TankInput)):
            tankdata.append(TankInput[i].get("vslcode", ""),
                            TankInput[i].get("tankcategory", ""),
                            TankInput[i].get("tankname", ""),
                            TankInput[i].get("density", 1),
                            TankInput[i].get("capacity", 0),
                            TankInput[i].get("weight", 0),
                            TankInput[i].get("lcglpp", 0),
                            TankInput[i].get("vcgbl", 0),
                            TankInput[i].get("tcgcl", 0.0),
                            TankInput[i].get("fsm", 0.0),0.0,0.0,0.0,0.0,
                            TankInput[i].get("port", ""),
                            TankInput[i].get("portindex", 0)
                            )
            return tankdata
    except Exception as e:
        print(f"The Exception in getTankData Method:", e)
        return -1

def getWBTankList(wbTankList):
    tanklist=[]
    try:
        for i in range(len(wbTankList)):
            tanklist.append(wbTankList[i].get("port", ""),
                            wbTankList[i].get("portindex", 0),
                            wbTankList[i].get("tankindex", 0),
                            wbTankList[i].get("tankname", ""),
                            wbTankList[i].get("volincube", 0),
                            wbTankList[i].get("maxper", 100),
                            wbTankList[i].get("unpumpableweight", 0),
                            wbTankList[i].get("holdtank", "N")

                            )
        sorted_tanklist = sorted(tanklist, key=lambda p: p['tankindex'])
        return sorted_tanklist
    except Exception as e:
        print(f"The Exception in getWBTankList Method:", e)
        return -1


