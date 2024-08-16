from Vesselinfo.VesselParticulars import readVesselParticulars
from Vesselinfo.VesselMain import readVesselMain
from Vesselinfo.Lightship import readLightShip
from Tankinfo.Tank import readTank
from Tankinfo.TankMapping import readTankMapping
from Tankinfo.BallastWeight import readBallastDetail
from Tankinfo.TankPosition import readTankPostion
from StabilityInfo.AllowableMassforHold import readAllowableMassforHold
from StabilityInfo.HydroStaticData import readHydroStatic
from StabilityInfo.SoundingData import readSoundingData
from StabilityInfo.FrameStation import readFrameStation
from StabilityInfo.StressTable import readSTable
from StabilityInfo.SFandBMFrameStation import readSFandBMFrameStation

# from VesselParticulars import readVesselParticulars

def readVesselData(vesselcode,localpath):
    vesselData={}
    try:
        vessel = readVesselParticulars(localpath)
        vesselMain = readVesselMain(localpath)
        WtItem = readLightShip(localpath)
        tank = readTank(localpath)
        tankmapping = readTankMapping(localpath)
        ballastwt = readBallastDetail(localpath)
        tankPosition = readTankPostion(localpath)
        allowablemass = readAllowableMassforHold(localpath)
        Hydro_value = readHydroStatic(localpath)
        soundData = readSoundingData(localpath)
        fmStation = readFrameStation(localpath)
        svalue = readSTable(localpath)
        SFBMFrames = readSFandBMFrameStation(localpath)

        vesselData["vessel"] = vessel
        vesselData["vesselMain"] = vesselMain
        vesselData["LightShip"] = WtItem
        vesselData["Tank"] = tank
        vesselData["tankmapping"] = tankmapping
        vesselData["BallastDetail"] = ballastwt
        vesselData["TankPostion"] = tankPosition
        vesselData["allowablemass"] = allowablemass
        vesselData["HydroStatic"] = Hydro_value
        vesselData["SoundingData"] = soundData
        vesselData["fmStation"] = fmStation
        vesselData["svalue"] = svalue
        vesselData["SFBMFrames"] = SFBMFrames
    except Exception as e:
        print("The exception in readVesselData:", e)

    return vesselData




