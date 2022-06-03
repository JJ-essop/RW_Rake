import requests
import pandas as pd

def get_run_pressure_data(run_id):
    CLIO_API_BASE_URL = "http://en-cliows-prod/api"
    url = f"{CLIO_API_BASE_URL}/pressurecoefficient/{run_id}"
    api_out = query_api(url)
    return api_out


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
        r'G:\01 - Aero Projects\15 - WT Data\WTRakes\RW Onset Flow Rake\22D_v4.01_Clio_table.csv',
        usecols=[1, 2, 5, 6, 7])
    return clio_table
