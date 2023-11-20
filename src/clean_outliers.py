with open('../output_data/time_array.txt', 'r') as file:
    time_lines = file.readlines()

with open('../output_data/volume_array.txt', 'r') as file:
    volume_lines = file.readlines()

time_arrays = []
volume_arrays = []

# Parse time_lines
for time_line in time_lines:
    time_line = time_line.strip()
    time_array = time_line.split(' ')
    time_arrays.append(time_array)

# Parse volume_lines
for volume_line in volume_lines:
    volume_line = volume_line.strip()
    volume_array = volume_line.split(' ')
    volume_arrays.append(volume_array)

# Filter out undesired volume_arrays and corresponding time_arrays
filtered_time_arrays = []
filtered_volume_arrays = []

for time_array, volume_array in zip(time_arrays, volume_arrays):
    first_volume_point = float(volume_array[0])
    second_volume_point = float(volume_array[1])

    # Check conditions
    if first_volume_point < 0 or second_volume_point >= 1.2 * first_volume_point:
        continue  # Skip this time and volume arrays

    filtered_time_arrays.append(time_array)
    filtered_volume_arrays.append(volume_array)

filtered_time_file_path = '../output_data/filtered_time_array.txt'
filtered_volume_file_path = '../output_data/filtered_volume_array.txt'

# Write the filtered time arrays to the output file
with open(filtered_time_file_path, 'w') as time_output_file:
    for time_array in filtered_time_arrays:
        time_output_file.write('\t'.join(time_array) + '\n')

# Write the filtered volume arrays to the output file
with open(filtered_volume_file_path, 'w') as volume_output_file:
    for volume_array in filtered_volume_arrays:
        volume_output_file.write('\t'.join(volume_array) + '\n')
