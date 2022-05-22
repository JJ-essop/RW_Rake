import requests
import pandas as pd
import numpy as np

def get_run_pressure_data(run_id):
    url = f"{CLIO_API_BASE_URL}/pressurecoefficient/{run_id}"
    result = query_api(url)
    return result


def query_api(url, timeout=30, **kwargs):
    response = requests.get(url, timeout=timeout, **kwargs)
    if response.ok:
        return response.json()
    response.raise_for_status()

def read_tap_map():
    tap_map = pd.read_csv(
        r'G:\01 - Aero Projects\15 - WT Data\WTRakes\RW Onset Flow Rake\RW_Tap_Map.csv')
    return tap_map

def read_clio_table():
    clio_table = pd.read_csv(
        r'G:\01 - Aero Projects\15 - WT Data\WTRakes\RW Onset Flow Rake\22C_v3.01_Clio_table.csv', usecols=[1, 2, 5, 6, 7])
    return clio_table


CLIO_API_BASE_URL = "http://en-cliows-prod/api"
run_no = 104612

result = get_run_pressure_data(run_no)

tap_map = read_tap_map()
clio_table = read_clio_table()

set_points = list(range(len(result)))

for sp in set_points:
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

    filename = f"FRH_{clio_table.Frh_tgt[sp]}__RRH_{clio_table.Rrh_tgt[sp]}__Yaw_{clio_table.Yaw_tgt[sp]}__Steer_{clio_table.Steer_tgt[sp]}__Roll_{clio_table.Roll_tgt[sp]}"

    print(filename)

    output.to_csv(r"G:\01 - Aero Projects\15 - WT Data\WTRakes\RW Onset Flow Rake\WT Results\22W18\JJ\R109080\%s.csv" % filename, sep=",", index=False)