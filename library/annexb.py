import pandas as pd

# Define the final dataset
data = {
    "Nuclide": [
        "H-3", "H-3", "H-3", "H-3",
        "C-11", "C-11", "C-11", "C-11",
        "C-14", "C-14", "C-14", "C-14",
        "S-35",
        "Ni-56", "Ni-57", "Ni-59", "Ni-63", "Ni-65", "Ni-66",
        "Ru-94", "Ru-97", "Ru-103", "Ru-105", "Ru-106",
        "Te-116", "Te-121", "Te-121m", "Te-123", "Te-123m", "Te-125m", "Te-127", "Te-127m", "Te-129",
        "Te-129m", "Te-131", "Te-131m", "Te-132", "Te-133", "Te-133m", "Te-134",
        "I-120", "I-120", "I-120m", "I-120m", "I-121", "I-121", "I-123", "I-123",
        "I-124", "I-124", "I-125", "I-125", "I-126", "I-126", "I-128", "I-128",
        "I-129", "I-129", "I-130", "I-130", "I-131", "I-131", "I-132", "I-132",
        "I-132m", "I-132m", "I-133", "I-133", "I-134", "I-134", "I-135", "I-135",
        "Hg-193", "Hg-193m", "Hg-194", "Hg-195", "Hg-195m", "Hg-197", "Hg-197m",
        "Hg-199m", "Hg-203"
    ],
    "Chemical Form": [
        "Organically bound tritium", "Tritium gas", "Tritiated methane", "Tritiated water",
        "CO2", "CO", "Methane", "Organic gases/vapours",
        "CO2", "CO", "Methane", "Organic gases/vapours",
        "dioxide",
        "carbonyl", "carbonyl", "carbonyl", "carbonyl", "carbonyl", "carbonyl",
        "tetroxide", "tetroxide", "tetroxide", "tetroxide", "tetroxide",
        "vapour", "vapour", "vapour", "vapour", "vapour", "vapour", "vapour", "vapour", "vapour",
        "vapour", "vapour", "vapour", "vapour", "vapour", "vapour", "vapour",
        "CH3I", "I2", "CH3I", "I2", "CH3I", "I2", "CH3I", "I2",
        "CH3I", "I2", "CH3I", "I2", "CH3I", "I2", "CH3I", "I2",
        "CH3I", "I2", "CH3I", "I2", "CH3I", "I2", "CH3I", "I2",
        "CH3I", "I2", "CH3I", "I2", "CH3I", "I2", "CH3I", "I2",
        "vapour", "vapour", "vapour", "vapour", "vapour", "vapour", "vapour",
        "vapour", "vapour"
    ],
    "T½": [
        "12.35 y", "", "", "",
        "20.38 m", "", "", "",
        "5730 y", "", "", "",
        "87.44 d",
        "6.10 d", "36.08 h", "7.5E4 y", "96 y", "2.520 h", "54.6 h",
        "51.8 m", "2.9 d", "39.28 d", "4.44 h", "368.2 d",
        "2.49 h", "17 d", "154 d", "1E13 y", "119.7 d", "58 d", "9.35 h", "109 d", "69.6 m",
        "33.6 d", "25.0 m", "30 h", "78.2 h", "12.45 m", "55.4 m", "41.8 m",
        "81.0 m", "", "53 m", "", "2.12 h", "", "13.2 h", "",
        "4.18 d", "", "60.14 d", "", "13.02 d", "", "24.99 m", "",
        "1.57E7 y", "", "12.36 h", "", "8.04 d", "", "2.30 h", "",
        "83.6 m", "", "20.8 h", "", "52.6 m", "", "6.61 h", "",
        "3.5 h", "11.1 h", "260 y", "9.9 h", "41.6 h", "64.1 h", "23.8 h",
        "42.6 m", "46.60 d"
    ],
    "e (Sv/Bq)": [
        "4.1E-11", "1.8E-15", "1.8E-13", "1.8E-11",
        "2.2E-12", "1.2E-12", "2.7E-14", "3.2E-12",
        "6.5E-12", "8.0E-13", "2.9E-12", "5.8E-10",
        "1.2E-10",
        "1.2E-09", "5.6E-10", "8.3E-10", "2.0E-09", "3.6E-10", "1.6E09",
        "5.6E-11", "1.2E-10", "1.1E-09", "1.8E-10", "1.8E-08",
        "8.7E-11", "5.1E-10", "5.5E-09", "1.2E-08", "2.9E-09", "1.5E-09", "7.7E-11", "4.6E-09", "3.7E-11",
        "3.7E-09", "6.8E-11", "2.4E-09", "5.1E-09", "5.6E-11", "2.2E-10", "8.4E-11",
        "2.0E-10", "3.0E-10", "1.0E-10", "1.8E-10", "5.6E-11", "8.6E-11", "1.5E-10", "2.1E-10",
        "9.2E-09", "1.2E-08", "1.1E-08", "1.4E-08", "2.0E-08", "2.6E-08", "1.3E-11", "6.5E-11",
        "7.4E-08", "9.6E-08", "1.4E-09", "1.9E-09", "1.5E-08", "2.0E-08", "1.9E-10", "3.1E-10",
        "1.6E-10", "2.7E-10", "3.1E-09", "4.0E-09", "5.0E-11", "1.5E-10", "6.8E-10", "9.2E-10",
        "1.1E-09", "3.1E-09", "4.0E-08", "1.4E-09", "8.2E-09", "4.4E-09", "5.8E-09",
        "1.8E-10", "7.0E-09"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv("AnnexB_icrp119_dcf_inh_soluble_reactive_gas_worker.csv", index=False)

# Print confirmation
print("CSV file 'final_nuclide_data.csv' has been saved.")

