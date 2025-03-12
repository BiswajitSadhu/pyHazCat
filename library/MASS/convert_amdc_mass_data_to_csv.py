import pandas as pd
import re

def convert_mass_data_to_csv(txt_file_path, csv_file_path):
    """
    Reads a nuclear mass data file, processes it, and saves it as a CSV.

    Parameters:
        txt_file_path (str): Path to the input .txt file.
        csv_file_path (str): Path to the output .csv file.
    """
    # Read the text file
    with open(txt_file_path, "r") as file:
        lines = file.readlines()

    # Extract valid data lines (skip headers and empty lines)
    data_lines = [line.strip() for line in lines if line.strip() and not line.startswith("1")]

    # Define column headers
    columns = ['Nuclide', 'N', 'Z', 'A', 'El', 'Atomic Mass']

    processed_data = []

    for line in data_lines:
        # Use regex or whitespace splitting to extract values
        parts = re.split(r"\s+", line, maxsplit=20)  # Ensure proper splitting

        # Remove "#" but keep the actual numerical values
        parts = [x.replace("#", "") if x else x for x in parts]

        # Handle missing values represented as "*"
        parts = [None if x == "*" else x for x in parts]

        # Extract N, Z, A, and El (Element)
        if not parts[2].isdigit():  # Case when N is present but A is missing
            N, Z = int(parts[0]), int(parts[1])
            A = N + Z
            El = parts[2]  # Element symbol
            data_offset = 2
        elif not parts[4].isdigit():  # Case when A is explicitly present
            N, Z, A = int(parts[1]), int(parts[2]), int(parts[3])
            El = parts[4]  # Element symbol
            data_offset = 4
        else:
            continue  # Skip rows that don't fit expected format

        # Merge atomic mass values
        atomic_mass_combined = f"{parts[-3]}.{parts[-2]}"

        # Generate Nuclide identifier: "El-A" (e.g., Cs-137)
        nuclide = f"{El}-{A}"

        # Append row to processed data
        row = [nuclide, N, Z, A, El, atomic_mass_combined]
        processed_data.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(processed_data, columns=columns)

    # Save as CSV
    df.to_csv(csv_file_path, index=False)

    print(f"Data successfully saved to {csv_file_path}")

# Example usage:
txt_file_path = "/home/biswajit/Documents/HAZCAT_CODE/HazCat/pyHazCat/library/MASS/massround.mas20.txt"
csv_file_path = "massround_data_final.csv"

convert_mass_data_to_csv(txt_file_path, csv_file_path)

