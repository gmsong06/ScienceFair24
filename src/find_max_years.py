import pandas as pd

# Replace 'your_excel_file.xlsx' with the actual path to your Excel file
excel_file_path = '../output_data/time_array.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

max_year_df = pd.DataFrame(columns=['Key', 'Max_Year'])

# Loop through rows in the DataFrame
for index, row in df.iterrows():
    max_year = 0

    for column in df.columns[1:]:
        cell_value = row[column]
        if pd.isna(cell_value):
            df.at[index, column] = 0
        else:
            df.at[index, column] = int(cell_value)

        max_year = max(max_year, df.at[index, column])

    max_year_df = max_year_df._append({'Key': row['Key'], 'Max_Year': max_year}, ignore_index=True)

output_excel_file = '../output_data/max_years.xlsx'  # Replace with your desired file path
max_year_df.to_excel(output_excel_file, index=False)
