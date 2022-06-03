from functions import get_run_pressure_data, read_tap_map, read_clio_table
import pandas as pd
import numpy as np

def export_to_csv():
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

        # output.to_csv(
        #     r"G:\01 - Aero Projects\15 - WT Data\WTRakes\RW Onset Flow Rake\WT Results\22W20\R109418\%s.csv" % filename,
        #     sep=",", index=False)


# run_no = 104950
run_no = input('Enter Clio RunID: ')

result = get_run_pressure_data(run_no)

print(len(result))

tap_map = read_tap_map()
clio_table = read_clio_table()

print(len(clio_table))

export_to_csv()