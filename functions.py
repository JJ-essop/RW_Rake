import requests
import pandas as pd
import numpy as np


# API for extracting pressure coefficient data from a given run
def get_run_pressure_data(run_id):
    CLIO_API_BASE_URL = "http://en-cliows-prod/api"
    url = f"{CLIO_API_BASE_URL}/pressurecoefficient/{run_id}"
    api_out = query_api(url)
    return api_out


# Checks to see if API call was successful
def query_api(url, timeout=30, **kwargs):
    response = requests.get(url, timeout=timeout, **kwargs)
    if response.ok:
        return response.json()
    response.raise_for_status()


# Returns the tapping map for a given rake - currently hard coded
def read_tap_map():
    tap_map = pd.read_csv(
        r'G:\01 - Aero Projects\15 - WT Data\WTRakes\Diffuser Rake\Diffuser_Rake_Tap_Map.csv')
    return tap_map


# Creates a data frame of X, Y, Z locations of pressure probes and teh Cp value for each probe

# Iterates through the API output of all pressure channels and takes the Cp value for each channel
# specified in the tapping map
def generate_Cp_dataframe(result, tap_map):
    for sp in list(range(len(result))):
        Cp = []

        for channel in tap_map.CHANNEL:
            Cp.append(result[sp][channel])

        output = pd.DataFrame([
            list(tap_map.X),
            list(tap_map.Y),
            list(tap_map.Z),
            Cp
        ])

        output = np.transpose(output)
        output.columns = ["X", "Y", "Z", "TotalPressureCoefficient"]
        output.head()

        filename = f"FRH_{result[sp]['frh_tgt']}__RRH_{result[sp]['rrh_tgt']}__Yaw_{result[sp]['yaw_tgt']}__Steer_{result[sp]['steer_tgt']}__Roll_{result[sp]['roll_tgt']}"
        print(filename)

        output.to_csv(
            r"G:\01 - Aero Projects\15 - WT Data\WTRakes\Diffuser Rake\WT Results\22W36\R110612\%s.csv" % filename,
            sep=",", index=False)