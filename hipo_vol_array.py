# CREATES A PKL FILE WITH THE TIME ARRAY AND VOLUME ARRAY

import pandas as pd
import pickle

df = pd.read_excel("Diagnosis_FS_prog_HippoVol.xlsx")

time_array = {}
value_array = {}


def initialize_lists():
    """
    Initializes the lists

    """

    for index, row in df.iterrows():
        time_array[row["OASISID"]] = []
        value_array[row["OASISID"]] = []


def fill_initial_values():
    """
    Fills the lists with the initial values of the time and value arrays

    """

    for index, row in df.iterrows():
        if len(time_array[row["OASISID"]]) != 0 and time_array[row["OASISID"]][len(time_array[row["OASISID"]]) - 1] == \
                row["years_to_Visit"]:
            continue
        time_array[row["OASISID"]].append(row["years_to_Visit"])
        value_array[row["OASISID"]].append(row["TOTAL_HIPPOCAMPUS_VOLUME"])


def filter_initial_values():
    """
    Remove patients with one data point

    """

    to_remove = []

    for patient in time_array:
        if len(time_array[patient]) == 1:
            to_remove.append(patient)

    for removing in to_remove:
        time_array.pop(removing)
        value_array.pop(removing)


def fill_missing_values():
    """
    Fill missing values with linear interpolation

    """

    for patient in time_array:
        for i in range(len(time_array[patient]) - 1, -1, -1):
            if i == 0 and time_array[patient][i] != 0:
                time_array[patient].insert(0, 0)
                interpolated_val = value_array[patient][0] + (value_array[patient][0] - value_array[patient][1]) / (
                        time_array[patient][2] - time_array[patient][1]) * (time_array[patient][1])
                value_array[patient].insert(0, interpolated_val)
                break


def export_to_excel(data, output_path):
    """
    Export a dictionary to an Excel file
    :param data: Dictionary to export
    :param output_path: Path to save the Excel file

    """

    df = pd.DataFrame(columns=['Key', 'Value1', 'Value2', 'Value3', 'Value4'])

    for key, values in data.items():
        row = {'Key': key}
        for i, value in enumerate(values):
            row[f'Value{i + 1}'] = value
        df = df._append(row, ignore_index=True)

    df.to_excel(output_path, index=False)


def excel_to_txt(input_excel_file, output_txt_file, delimiter='\t'):
    """
    Convert an Excel file to a TXT file
    :param input_excel_file: Path to the Excel file
    :param output_txt_file: Path to save the TXT file
    :param delimiter: Delimiter to use between columns

    """

    try:

        # Read the Excel file into a DataFrame, replace empty cells with NaN
        df = pd.read_excel(input_excel_file).fillna('NaN')

        # Write the DataFrame to a TXT file with the specified delimiter
        df.to_csv(output_txt_file, sep=delimiter, index=False)

        print(f"Conversion successful. Data saved to {output_txt_file}")
    except Exception as e:
        print(f"Error: {str(e)}")


def save_data_as_pkl(x_file_path, y_file_path, pkl_file_path):
    """
    Save data from two text files to a .pkl file
    :param x_file_path: Time array path
    :param y_file_path: Volume array path
    :param pkl_file_path: pkl file path

    """

    with open(x_file_path, "r") as file_x, open(y_file_path, "r") as file_y:
        data = {
            "XA": file_x.read(),
            "YA": file_y.read()
        }

    # Save the data to a .pkl file
    with open(pkl_file_path, "wb") as pkl_file:
        pickle.dump(data, pkl_file)


def remove_first_row_and_columns(file_path):
    """
    Remove the first row and columns from a text file
    :param file_path: Path to TXT file

    """

    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = lines[1:]

    for i in range(len(lines)):
        lines[i] = lines[i].split()[1:]

    with open(file_path, 'w') as file:
        for line in lines:
            file.write(' '.join(line) + '\n')


def print_xa_and_ya_from_pkl(pkl_file_path):
    with open(pkl_file_path, "rb") as pkl_file:
        data = pickle.load(pkl_file)

    if "XA" in data and "YA" in data:
        print("Contents of XA:")
        print(data["XA"])
        print("\nContents of YA:")
        print(data["YA"])


# Clean excel data
initialize_lists()
fill_initial_values()
filter_initial_values()
fill_missing_values()

# Export to excel time array and volume array
export_to_excel(time_array, "time_array.xlsx")
export_to_excel(value_array, "volume_array.xlsx")

# Convert excel to txt
excel_to_txt("time_array.xlsx", "time_array.txt")
excel_to_txt("volume_array.xlsx", "volume_array.txt")

# Remove first row and columns (OASISID and headers)
file_path_time = 'time_array.txt'
file_path_volume = 'volume_array.txt'

remove_first_row_and_columns(file_path_time)
remove_first_row_and_columns(file_path_volume)

# Save data as pkl
save_data_as_pkl("time_array.txt", "volume_array.txt", "data.pkl")

# Print XA and YA from pkl
print_xa_and_ya_from_pkl("data.pkl")
