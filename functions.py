import requests
import pandas as pd
import numpy as np

# API for extracting oressure coefficient data from a given run
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
        r'G:\01 - Aero Projects\15 - WT Data\WTRakes\RW Onset Flow Rake\RW_Tap_Map.csv')
    return tap_map


# Creates a data frame of X, Y, Z locations of pressure probes and teh Cp value for each probe
# Iterates through the API output of all pressure channels and takes the Cp value for each channel specified in the tapping map
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

        return output


# Returns the clio table for the given map in order to get car conditions - currently hard coded until API is updated
def read_clio_table():
    clio_table = pd.read_csv(
        r'G:\01 - Aero Projects\15 - WT Data\WTRakes\RW Onset Flow Rake\22D_v4.01_Clio_table.csv',
        usecols=[1, 2, 5, 6, 7])
    return clio_table


# Exports Cp data frame to csv file for each set point, using the clio table for file naming convention
def export_to_csv(result, clio_table, output):
    for sp in list(range(len(result))):                     # iterate through all set points in the map
        filename = f"FRH_{clio_table.Frh_tgt[sp]}__RRH_{clio_table.Rrh_tgt[sp]}__Yaw_{clio_table.Yaw_tgt[sp]}__Steer_{clio_table.Steer_tgt[sp]}__Roll_{clio_table.Roll_tgt[sp]}"
        print(filename)

        output.to_csv(
            r"G:\01 - Aero Projects\15 - WT Data\WTRakes\RW Onset Flow Rake\WT Results\22W20\R109418\%s.csv" % filename,
            sep=",", index=False)