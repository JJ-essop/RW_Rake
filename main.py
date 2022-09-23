from functions import get_run_pressure_data, read_tap_map, generate_Cp_dataframe

# run_no = 104950
run_no = input('Enter Clio RunID: ')

result = get_run_pressure_data(run_no)
print(result[15])

tap_map = read_tap_map()

generate_Cp_dataframe(result, tap_map)