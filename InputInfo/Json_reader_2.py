import json
from typing import List, Dict
from NonlinearInfo.NonlinearModeling import PMMOptimizer
from InputInfo.OptimizerInput import getMTPerMeterCubeFromCubicFT
# from NonlinearInfo.NonlinearModeling import P
import pandas as pd
# from Vesselinfo.VesselParticulars import readVesselParticulars
# Define the classes as previously provided
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
        self.name = name.upper()
        self.grade = grade
        self.weight = weight
        self.stowagefactor = getMTPerMeterCubeFromCubicFT(stowagefactor)
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
        self.cargo = cargo.upper()
        self.techname = techname.upper()
        self.grade = grade
        self.stowagefactor = getMTPerMeterCubeFromCubicFT(stowagefactor)
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


class VesselData:
    def __init__(self, username, Vesselcode, speed, version, chartedpartyRefNo, remarks, Propelleraftmindraft,
                 Propellerfwdmindraft,
                 Schedule: List[Schedule], CargoDetails: List[CargoDetails], Parameter: List[Parameter],
                 WaterBallast: List[WaterBallast],
                 Tank: List[Tank], ArrivalTank: List[ArrivalTank], Input_Flags: Dict[str, bool],
                 ChartedPartyAssumption: List[ChartedPartyAssumption]):
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
        self.Input_Flags = Input_Flags
        self.ChartedPartyAssumption = ChartedPartyAssumption

    @classmethod
    def from_json(cls, data: str):
        json_data = json.loads(data)

        Schedule_list = [Schedule(**schedule) for schedule in json_data.get("Schedule", [])]
        CargoDetails_list = [CargoDetails(**cargo) for cargo in json_data.get("CargoDetails", [])]
        Parameter_list = [Parameter(**param) for param in json_data.get("Parameter", [])]
        WaterBallast_list = [WaterBallast(**wb) for wb in json_data.get("WaterBallast", [])]
        Tank_list = [Tank(**tank) for tank in json_data.get("Tank", [])]
        ArrivalTank_list = [ArrivalTank(**arrival) for arrival in json_data.get("ArrivalTank", [])]
        ChartedPartyAssumption_list = [ChartedPartyAssumption(**assumption) for assumption in
                                       json_data.get("ChartedPartyAsswumption", [])]

        Input_Flags = {key: json_data[key] for key in json_data.keys() if key.endswith("Flag") or key == "FirstPass"}

        return cls(
            json_data["username"],
            json_data["Vesselcode"],
            json_data["speed"],
            json_data["version"],
            json_data["chartedpartyRefNo"],
            json_data["remarks"],
            json_data["Propelleraftmindraft"],
            json_data["Propellerfwdmindraft"],
            Schedule_list,
            CargoDetails_list,
            Parameter_list,
            WaterBallast_list,
            Tank_list,
            ArrivalTank_list,
            Input_Flags,
            ChartedPartyAssumption_list
        )

    def to_dict(self):
        return {
            "username": self.username,
            "Vesselcode": self.Vesselcode,
            "speed": self.speed,
            "version": self.version,
            "chartedpartyRefNo": self.chartedpartyRefNo,
            "remarks": self.remarks,
            "Propelleraftmindraft": self.Propelleraftmindraft,
            "Propellerfwdmindraft": self.Propellerfwdmindraft,
            "Schedule": [vars(s) for s in self.Schedule],
            "CargoDetails": [vars(c) for c in self.CargoDetails],
            "Parameter": [vars(p) for p in self.Parameter],
            "WaterBallast": [vars(wb) for wb in self.WaterBallast],
            "Tank": [vars(t) for t in self.Tank],
            "ArrivalTank": [vars(at) for at in self.ArrivalTank],
            "Input_Flags": self.Input_Flags,
            "ChartedPartyAssumption": [vars(cpa) for cpa in self.ChartedPartyAssumption]
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


# Reading JSON file and creating the object
json_file_path = "D:/BCAP_python/PMM MP 002 JSON.json"

with open(json_file_path, 'r') as f:
    json_content = f.read()

vessel_data = VesselData.from_json(json_content)

# Print the classes and the final dictionary representation
# print("Vessel Data Classes:")
# print(f"Username: {vessel_data.username}")
# print(f"Vessel Code: {vessel_data.Vesselcode}")
# print(f"Speed: {vessel_data.speed}")
# print(f"Version: {vessel_data.version}")
# print(f"Charted Party Ref No: {vessel_data.chartedpartyRefNo}")
# print(f"Remarks: {vessel_data.remarks}")
# print(f"Propeller Aft Min Draft: {vessel_data.Propelleraftmindraft}")
# print(f"Propeller Fwd Min Draft: {vessel_data.Propellerfwdmindraft}")
#
# print("\nSchedule:")
# for schedule in vessel_data.Schedule:
#     print(vars(schedule))
#
# print("\nCargo Details:")
# for cargo in vessel_data.CargoDetails:
#     print(vars(cargo))
#
# print("\nParameter:")
# for param in vessel_data.Parameter:
#     print(vars(param))
#
# print("\nWater Ballast:")
# for wb in vessel_data.WaterBallast:
#     print(vars(wb))
#
# print("\nTank:")
# for tank in vessel_data.Tank:
#     print(vars(tank))
#
# print("\nArrival Tank:")
# for arrival in vessel_data.ArrivalTank:
#     print(vars(arrival))
#
# print("\nCharted Party Assumption:")
# for cpa in vessel_data.ChartedPartyAssumption:
#     print(vars(cpa))

# print("\nInput Flags:")
# if vessel_data.Input_Flags:
#     for key, value in vessel_data.Input_Flags.items():
#         print(f"{key}: {value}")
# else:
#     print("No flags present")

data_dict = vessel_data.to_dict()

# Example usage: print the dictionary for Schedule
print(data_dict['Schedule'])
print(data_dict["CargoDetails"])
print(data_dict["Parameter"])
print(data_dict['WaterBallast'])
print(data_dict["Tank"])
print(data_dict["ArrivalTank"])
print(data_dict["Input_Flags"])

class VesselAPI:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.api_dict = self._create_api_dict()

    def _create_api_dict(self):
        api_dict = {}
        for index, row in self.data.iterrows():
            api_dict[row['vesselcode']] = row['apiURL']
        return api_dict

    def get_api_url(self, vesselcode):
        return self.api_dict.get(vesselcode, "Vessel code not found")

# Initialize the class with the CSV file
vessel_api = VesselAPI("D:/BCAP_python/apiurl.csv")


# Example usage
api_url = vessel_api.get_api_url('XXX')
print(api_url)

# def apiurl(localpath,vsl):
#     df=pd.read_csv(localpath)
#     df=df[df['vesselcode']==vsl]
#     df1=df["apiURL"]
#     return df

class LocalPathReader:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.path_dict = self._create_path_dict()

    def _create_path_dict(self):
        path_dict = {}
        for index, row in self.data.iterrows():
            path_dict[index] = row['localpath']
        return path_dict

    def get_local_path(self, index):
        return self.path_dict.get(index, "Index not found")

# Initialize the class with the CSV file
def read_local_path_test(vscode,localpath1):
    # Read the CSV into a DataFrame
    df = pd.read_csv(localpath1)
    # Extract the path from the first cell in the first row
    path = df.iloc[0, 0]
    # Construct the local path by appending the vscode string and "/files/"
    localpath = f"{path}{vscode}/files/"
    # Uncomment the line below to print the local path for debugging
    # print("localpath==", localpath)
    return localpath

    # print("local_path=========",path)
local_path=read_local_path_test("PMM","D:/BCAP_python/localfilePath.csv")
# print("local_path_inside",local_path)
first_pass=True

# vesselparticulars=readVesselParticulars(local_path)
# print("vesselparticulars",vesselparticulars)

PMMOptimizer(data_dict,api_url,local_path,first_pass)


