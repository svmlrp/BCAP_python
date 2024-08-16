import json
from typing import List


class Schedule:
    def __init__(self, portcode, portname, terminalcode, currentport, arrivaldate, departuredate, terminaltime,
                 Portindex, servicecode, voyageno, bound, terminalTime, shortportcode, vesselName, portcolor):
        self.portcode = portcode
        self.portname = portname
        self.terminalcode = terminalcode
        self.currentport = currentport
        self.arrivaldate = arrivaldate
        self.departuredate = departuredate
        self.terminaltime = terminaltime
        self.Portindex = Portindex
        self.servicecode = servicecode
        self.voyageno = voyageno
        self.bound = bound
        self.terminalTime = terminalTime
        self.shortportcode = shortportcode
        self.vesselName = vesselName
        self.portcolor = portcolor


class CargoDetails:
    def __init__(self, pol, polIdx, pod, podIdx, name, grade, weight, stowagefactor, maxdischarge):
        self.pol = pol
        self.polIdx = polIdx
        self.pod = pod
        self.podIdx = podIdx
        self.name = name
        self.grade = grade
        self.weight = weight
        self.stowagefactor = stowagefactor
        self.maxdischarge = maxdischarge


class Parameter:
    def __init__(self, pol, trim, ballast, deballast, tankwt, hogorsag, hogorsagvalue, stress, loadwaterline, draft,
                 airdraft, seaWaterDensity, seaport, draftlimit, arrivalairdraft, arrivalswdensity, arrivaldraft,
                 NumberofHatchCovers, airdraftHatchcover, meandraft, polidx, SFValue, BMValue, hatchAirDraft):
        self.pol = pol
        self.trim = trim
        self.ballast = ballast
        self.deballast = deballast
        self.tankwt = tankwt
        self.hogorsag = hogorsag
        self.hogorsagvalue = hogorsagvalue
        self.stress = stress
        self.loadwaterline = loadwaterline
        self.draft = draft
        self.airdraft = airdraft
        self.seaWaterDensity = seaWaterDensity
        self.seaport = seaport
        self.draftlimit = draftlimit
        self.arrivalairdraft = arrivalairdraft
        self.arrivalswdensity = arrivalswdensity
        self.arrivaldraft = arrivaldraft
        self.NumberofHatchCovers = NumberofHatchCovers
        self.airdraftHatchcover = airdraftHatchcover
        self.meandraft = meandraft
        self.polidx = polidx
        self.SFValue = SFValue
        self.BMValue = BMValue
        self.hatchAirDraft = hatchAirDraft


class WaterBallast:
    def __init__(self, scenarioid, port, portindex, tankcategory, tankname, volincube, vesselcode, density, capacity,
                 weight, lcglpp, vcgbl, tcgcl, fsm, select, maxper, partialyfilled, fullyfilled, unpumpableweight,
                 holdtank, bmax, sounding, volinpercent):
        self.scenarioid = scenarioid
        self.port = port
        self.portindex = portindex
        self.tankcategory = tankcategory
        self.tankname = tankname
        self.volincube = volincube
        self.vesselcode = vesselcode
        self.density = density
        self.capacity = capacity
        self.weight = weight
        self.lcglpp = lcglpp
        self.vcgbl = vcgbl
        self.tcgcl = tcgcl
        self.fsm = fsm
        self.select = select
        self.maxper = maxper
        self.partialyfilled = partialyfilled
        self.fullyfilled = fullyfilled
        self.unpumpableweight = unpumpableweight
        self.holdtank = holdtank
        self.bmax = bmax
        self.sounding = sounding
        self.volinpercent = volinpercent


class Tank:
    def __init__(self, scenarioid, port, portindex, tankcategory, tankname, volincube, vesselcode, density, capacity,
                 weight, lcglpp, vcgbl, tcgcl, fsm, select, maxper, partialyfilled, fullyfilled, unpumpableweight,
                 holdtank, bmax, sounding, volinpercent):
        self.scenarioid = scenarioid
        self.port = port
        self.portindex = portindex
        self.tankcategory = tankcategory
        self.tankname = tankname
        self.volincube = volincube
        self.vesselcode = vesselcode
        self.density = density
        self.capacity = capacity
        self.weight = weight
        self.lcglpp = lcglpp
        self.vcgbl = vcgbl
        self.tcgcl = tcgcl
        self.fsm = fsm
        self.select = select
        self.maxper = maxper
        self.partialyfilled = partialyfilled
        self.fullyfilled = fullyfilled
        self.unpumpableweight = unpumpableweight
        self.holdtank = holdtank
        self.bmax = bmax
        self.sounding = sounding
        self.volinpercent = volinpercent

class ArrivalTank:
    def __init__(self, scenarioid, port, portindex, tankcategory, tankname, volincube, vesselcode, density, capacity,
                 weight, lcglpp, vcgbl, tcgcl, fsm, select, maxper, partialyfilled, fullyfilled, unpumpableweight,
                 holdtank, bmax, sounding, volinpercent):
        self.scenarioid = scenarioid
        self.port = port
        self.portindex = portindex
        self.tankcategory = tankcategory
        self.tankname = tankname
        self.volincube = volincube
        self.vesselcode = vesselcode
        self.density = density
        self.capacity = capacity
        self.weight = weight
        self.lcglpp = lcglpp
        self.vcgbl = vcgbl
        self.tcgcl = tcgcl
        self.fsm = fsm
        self.select = select
        self.maxper = maxper
        self.partialyfilled = partialyfilled
        self.fullyfilled = fullyfilled
        self.unpumpableweight = unpumpableweight
        self.holdtank = holdtank
        self.bmax = bmax
        self.sounding = sounding
        self.volinpercent = volinpercent


class ChartedPartyAssumption:
    def __init__(self, cargo, techname, grade, stowagefactor, contract_qty, customer_request, plusorminus, pol, polIdx,
                 pol_terminal, pol_berth, pod, podIdx, pod_terminal, pod_berth, terms):
        self.cargo = cargo
        self.techname = techname
        self.grade = grade
        self.stowagefactor = stowagefactor
        self.contract_qty = contract_qty
        self.customer_request = customer_request
        self.plusorminus = plusorminus
        self.pol = pol
        self.polIdx = polIdx
        self.pol_terminal = pol_terminal
        self.pol_berth = pol_berth
        self.pod = pod
        self.podIdx = podIdx
        self.pod_terminal = pod_terminal
        self.pod_berth = pod_berth
        self.terms = terms

# class Input_flags:
#     def  __init__(self):
#         if self.data:
#             self.errorFlag = self.data.get('errorFlag', None)
#             self.BendingFlag = self.data.get('BendingFlag', None)
#             self.stressflag = self.data.get('stressflag', None)
#             self.VolumeFlag = self.data.get('VolumeFlag', None)
#             self.TrimFlag = self.data.get('TrimFlag', None)
#             self.AdjacentCargoFlag = self.data.get('AdjacentCargoFlag', None)
#             self.chartedPartyFlag = self.data.get('chartedPartyFlag', None)
#             self.LoadableFlag = self.data.get('LoadableFlag', None)
#             self.weightFlag = self.data.get('weightFlag', None)
#             self.propellerFlag = self.data.get('propellerFlag', None)
#             self.PreferedFlag = self.data.get('PreferedFlag', None)
#             self.mixedCargoFlag = self.data.get('mixedCargoFlag', None)
#             self.BallestTankWTFlag = self.data.get('BallestTankWTFlag', None)
#             self.DeflectionFlag = self.data.get('DeflectionFlag', None)
#             self.HatchCoverFlag = self.data.get('HatchCoverFlag', None)
#             self.FirstPass = self.data.get('FirstPass', None)
#             self.MinimumMassflag = self.data.get('MinimumMassflag', None)
#             self.ArrivalDeaparture = self.data.get('ArrivalDeaparture', None)
#             self.TrimConstFlag = self.data.get('TrimConstFlag', None)
#             self.autoallocationFlag = self.data.get('autoallocationFlag', None)
#         else:
#             self.errorFlag = None
#             self.BendingFlag = None
#             self.stressflag = None
#             self.VolumeFlag = None
#             self.TrimFlag = None
#             self.AdjacentCargoFlag = None
#             self.chartedPartyFlag = None
#             self.LoadableFlag = None
#             self.weightFlag = None
#             self.propellerFlag = None
#             self.PreferedFlag = None
#             self.mixedCargoFlag = None
#             self.BallestTankWTFlag = None
#             self.DeflectionFlag = None
#             self.HatchCoverFlag = None
#             self.FirstPass = None
#             self.MinimumMassflag = None
#             self.ArrivalDeaparture = None
#             self.TrimConstFlag = None
#             self.autoallocationFlag = None


class VesselData:
    def __init__(self, username, Vesselcode, speed, version, chartedpartyRefNo, remarks, Propelleraftmindraft,
                 Propellerfwdmindraft,
                 Schedule: List[Schedule], CargoDetails: List[CargoDetails], Parameter: List[Parameter],
                 WaterBallast: List[WaterBallast],
                 Tank: List[Tank],ArrivalTank:List[ArrivalTank],errorFlag,BendingFlag,stressflag,VolumeFlag,TrimFlag,AdjacentCargoFlag,chartedPartyFlag,
                 LoadableFlag,weightFlag, propellerFlag,PreferedFlag,mixedCargoFlag,BallestTankWTFlag,DeflectionFlag,HatchCoverFlag
                 ,FirstPass,MinimumMassflag,ArrivalDeaparture,TrimConstFlag,autoallocationFlag,ChartedPartyAssumption: List[ChartedPartyAssumption]):
        self.username = username
        self.Vesselcode = Vesselcode
        self.speed = speed
        self.version = version
        self.chartedpartyRefNo = chartedpartyRefNo
        self.remarks = remarks
        self.Propelleraftmindraft = Propelleraftmindraft
        self.Propellerfwdmindraft = Propellerfwdmindraft
        self.Schedule = Schedule
        self.CargoDetails = CargoDetails
        self.Parameter = Parameter
        self.WaterBallast = WaterBallast
        self.Tank = Tank
        self.ArrivalTank = ArrivalTank
        self.errorFlag=errorFlag
        self.BendingFlag = BendingFlag
        self.stressflag=stressflag
        self.VolumeFlag = VolumeFlag
        self.TrimFlag = TrimFlag
        self.AdjacentCargoFlag = AdjacentCargoFlag
        self.chartedPartyFlag = chartedPartyFlag
        self.LoadableFlag = LoadableFlag
        self.weightFlag = weightFlag
        self.propellerFlag = propellerFlag
        self.PreferedFlag=PreferedFlag
        self.mixedCargoFlag = mixedCargoFlag
        self.BallestTankWTFlag = BallestTankWTFlag
        self.DeflectionFlag = DeflectionFlag
        self.HatchCoverFlag = HatchCoverFlag
        self.FirstPass=FirstPass
        self.MinimumMassflag = MinimumMassflag
        self.ArrivalDeaparture=ArrivalDeaparture
        self.TrimConstFlag=TrimConstFlag
        self.autoallocationFlag=autoallocationFlag
        self.ChartedPartyAssumption = ChartedPartyAssumption

    @classmethod
    def from_json(cls, data):
        schedule = [Schedule(**item) for item in data['Schedule']]
        cargo_details = [CargoDetails(**item) for item in data['CargoDetails']]
        parameter = [Parameter(**item) for item in data['Parameter']]
        water_ballast = [WaterBallast(**item) for item in data['WaterBallast']]
        tank = [Tank(**item) for item in data['Tank']]
        arrivalTank = [ArrivalTank(**item) for item in data['ArrivalTank']]
        charted_party_assumption = [ChartedPartyAssumption(**item) for item in data['ChartedPartyAsswumption']]
        # input_flag={data["errorFlag"],data["BendingFlag"],data["stressflag"],data["VolumeFlag"],data["TrimFlag"],data["AdjacentCargoFlag"],data["chartedPartyFlag"],
        #          data["LoadableFlag"],data["weightFlag"], data["propellerFlag"],data["PreferedFlag"],data["mixedCargoFlag"],data["BallestTankWTFlag"],data["DeflectionFlag"],data["HatchCoverFlag"]
        #          ,data["FirstPass"],data["MinimumMassflag"],data["ArrivalDeaparture"],data["TrimConstFlag"],data["autoallocationFlag"]}

        return cls(
            username=data['username'],
            Vesselcode=data['Vesselcode'],
            speed=data['speed'],
            version=data['version'],
            chartedpartyRefNo=data['chartedpartyRefNo'],
            remarks=data['remarks'],
            Propelleraftmindraft=data['Propelleraftmindraft'],
            Propellerfwdmindraft=data['Propellerfwdmindraft'],
            Schedule=schedule,
            CargoDetails=cargo_details,
            Parameter=parameter,
            WaterBallast=water_ballast,
            Tank=tank,
            ArrivalTank=arrivalTank,
            errorFlag=data["errorFlag"],
            BendingFlag= data["BendingFlag"],
            stressflag= data["stressflag"],
            VolumeFlag= data["VolumeFlag"],
            TrimFlag=data["TrimFlag"],
            AdjacentCargoFlag=data["AdjacentCargoFlag"],
            chartedPartyFlag=data["chartedPartyFlag"],
            LoadableFlag= data["LoadableFlag"],
            weightFlag=data["weightFlag"],
            propellerFlag=data["propellerFlag"],
            PreferedFlag=data["PreferedFlag"],
            mixedCargoFlag=data["mixedCargoFlag"],
            BallestTankWTFlag=data["BallestTankWTFlag"],
            DeflectionFlag= data["DeflectionFlag"],
            HatchCoverFlag=data["HatchCoverFlag"],
            FirstPass=data["FirstPass"],
            MinimumMassflag=data["MinimumMassflag"],
            ArrivalDeaparture= data["ArrivalDeaparture"],
            TrimConstFlag=data["TrimConstFlag"],
            autoallocationFlag=data["autoallocationFlag"],
            ChartedPartyAssumption=charted_party_assumption
        )

    def to_dict(self):
        return {
            'username': self.username,
            'Vesselcode': self.Vesselcode,
            'speed': self.speed,
            'version': self.version,
            'chartedpartyRefNo': self.chartedpartyRefNo,
            'remarks': self.remarks,
            'Propelleraftmindraft': self.Propelleraftmindraft,
            'Propellerfwdmindraft': self.Propellerfwdmindraft,
            'Schedule': [vars(s) for s in self.Schedule],
            'CargoDetails': [vars(c) for c in self.CargoDetails],
            'Parameter': [vars(p) for p in self.Parameter],
            'WaterBallast': [vars(w) for w in self.WaterBallast],
            'Tank': [vars(t) for t in self.Tank],
            'ArrivalTank': [vars(t) for t in self.ArrivalTank],
            'errorFlag':self.errorFlag,
            'BendingFlag':self.BendingFlag,
            'stressflag':self.stressflag,
            'VolumeFlag':self.VolumeFlag,
            'TrimFlag':self.TrimFlag,
            'AdjacentCargoFlag':self.AdjacentCargoFlag,
            'chartedPartyFlag':self.chartedPartyFlag,
            'LoadableFlag': self.LoadableFlag,
            'weightFlag':self.weightFlag,
            'propellerFlag':self.propellerFlag,
            'PreferedFlag':self.PreferedFlag,
            'mixedCargoFlag':self.mixedCargoFlag,
            'BallestTankWTFlag':self.BallestTankWTFlag,
            'DeflectionFlag':self.DeflectionFlag,
            'HatchCoverFlag':self.HatchCoverFlag,
            'FirstPass':self.FirstPass,
            'MinimumMassflag':self.MinimumMassflag,
            'ArrivalDeaparture':self.ArrivalDeaparture,
            'TrimConstFlag':self.TrimConstFlag,
            'autoallocationFlag':self.autoallocationFlag,
            'ChartedPartyAssumption': [vars(c) for c in self.ChartedPartyAssumption]
        }


# Load JSON file
with open("C:/Users/deenadayalan.pu/Downloads/PMM Singleport 023 JSON.json", 'r') as file:
    data = json.load(file)
    # print("data====",data)

# Create VesselData object
vessel_data = VesselData.from_json(data)

# Convert to dictionary
data_dict = vessel_data.to_dict()

# Example usage: print the dictionary for Schedule
print(data_dict['Schedule'])
print(data_dict["CargoDetails"])
print(data_dict["Parameter"])
print(data_dict['WaterBallast'])
print(data_dict["Tank"])
print(data_dict["ArrivalTank"])
print(data_dict)

