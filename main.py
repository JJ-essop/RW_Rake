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


CLIO_API_BASE_URL = "http://en-cliows-prod/api"

result = get_run_pressure_data(104612)

tap_map = read_tap_map()

Cp = []
for channel in tap_map.CHANNEL:
    Cp.append(result[3][channel])

output = pd.DataFrame([
    list(tap_map.X),
    list(tap_map.Y),
    list(tap_map.Z),
    Cp
])

output = np.transpose(output)
output.columns = ["X", "Y", "Z", "TotalPressureCoefficient"]
output.head()

print(output)

output.to_csv(r"G:\01 - Aero Projects\15 - WT Data\WTRakes\RW Onset Flow Rake\run_no.csv", sep=",", index=False)