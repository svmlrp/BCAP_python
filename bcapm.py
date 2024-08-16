import pandas as pd
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
vessel_api = VesselAPI("C:/Users/deenadayalan.pu/bcap_octeract_dependacy/bcap_optimizer/apiurl.csv")


# Example usage
api_url = vessel_api.get_api_url('XXX')
print(api_url)

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
local_path_reader = LocalPathReader("C:/Users/deenadayalan.pu/bcap_octeract_dependacy/bcap_optimizer/localfilePath.csv")

# Example usage
local_path = local_path_reader.get_local_path(0)
print(local_path)