from functions import get_run_pressure_data, read_tap_map, generate_Cp_dataframe
import subprocess

# run_no = 104950
run_no = input('Enter Clio RunID: ')

result = get_run_pressure_data(run_no)
print(result[15])

tap_map, ptap_path = read_tap_map()

export_path = generate_Cp_dataframe(result, tap_map, ptap_path, run_no)

subprocess.Popen(r'explorer /select,"%s"' %export_path)