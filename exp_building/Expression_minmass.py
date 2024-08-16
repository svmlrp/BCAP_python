# import pandas as pd
#
#
# def readexp_minmass(localpath):
#     try:
#
#         df=pd.read_csv(localpath)
#         return df
#     except Exception as e:
#         print("The Exception in readexp_minmass Method:", e)
#
# def find_minmass_value(df,Frame_number,cols):
#     output=0
#     try:
#         for i,row in df.iterrows():
#             if row["Hold Number"]== Frame_number:
#                 output=row[cols]
#                 break
#         return output
#     except Exception as e:
#         print(f"The Exception in find_minmass_value{cols} Method:", e)
#         return -1
#
# def polynomial_minmass(df,Frame_number,cols):
#     output=[]
#     try:
#         for i,row in df.iterrows():
#             if row["Hold Number"]== Frame_number:
#                 output=row[cols]
#                 const=list(map(float, output.split(',')))
#                 break
#         return const
#     except Exception as e:
#         print(f"The Exception in polynomial_minmass{cols} Method:", e)
#         return -1


import csv

class Minimass:
    def __init__(self, vessel, hold_number, weight_degree, weight_const, use_ballast, ballast_tank_no):
        self.vessel = vessel
        self.hold_number = hold_number
        self.weight_degree = weight_degree
        self.weight_const = weight_const
        self.use_ballast = use_ballast
        self.ballast_tank_no = ballast_tank_no

    @classmethod
    def from_csv(cls, csv_file):
        instances = []
        try:
            with open(csv_file, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    try:
                        weight_const = tuple(map(float, row['WeightConst'].split(',')))
                        instance = cls(
                            vessel=row['Vessel'],
                            hold_number=int(row['Hold Number']),
                            weight_degree=int(row['WeightDegree']),
                            weight_const=weight_const,
                            use_ballast=int(row['UseBallast']),
                            ballast_tank_no=int(row['BallasttankN0'])
                        )
                        instances.append(instance)
                    except ValueError as e:
                        print(f"Error converting row {row}: {e}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return instances

    def to_dict(self):
        return {
            'vessel': self.vessel,
            'HoldNumber': self.hold_number,
            'WeightDegree': self.weight_degree,
            'weightConst': self.weight_const,
            'UseBallast': self.use_ballast,
            'Ballast_tank_No': self.ballast_tank_no
        }

    @staticmethod
    def get_weight_info_by_hold_number(instances, hold_number):
        try:
            for instance in instances:
                if instance.hold_number == hold_number:
                    return instance.weight_degree, instance.weight_const
            raise ValueError(f"Hold number {hold_number} not found")
        except Exception as e:
            print(f"Error: {e}")
            return None, None

# Reading the content from the CSV file and storing it in a dictionary
csv_file_path = "C:/Users/deenadayalan.pu/bcap_octeract_dependacy/bcap_optimizer/BCAP project/FWA/files/Minimass.csv"
minimass_objects = Minimass.from_csv(csv_file_path)

# Get weightDegree and weightConst for a given hold number
hold_number_to_find = 10  # specify the hold number you want to find
weight_degree, weight_const = Minimass.get_weight_info_by_hold_number(minimass_objects, hold_number_to_find)

if weight_degree is not None and weight_const is not None:
    print(f"WeightDegree: {weight_degree}, WeightConst: {weight_const}")
else:
    print(f"Could not find weight info for hold number {hold_number_to_find}")
