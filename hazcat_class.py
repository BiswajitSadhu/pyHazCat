import numpy as np
import os
import pandas as pd
os.getcwd()
import logging

pd.reset_option('display.float_format')

class HAZCAT():
    def __init__(self, config):
        super().__init__()

        self.lambda_of_rads = None
        self.config = config
        self.inventories = config['inventories']
        self.rads_list = config['rads_list']
        self.f = config['output_filename']

    def get_dcfs_for_radionuclides(self):
        """
        Computes max DCF values for a list of radionuclides.

        Parameters:
        rads_list (list): List of radionuclides to process.

        Returns:
        dict: Dictionary with radionuclides as keys and their DCF dictionaries as values.
        """
        return {rad: self.compute_max_dcf(rad) for rad in self.rads_list}

        # Example usage:
        #rads_list = ['Cs-137', 'Co-60', 'Sr-90']
        #dcfs_dicts_rads_list = get_dcfs_for_radionuclides(rads_list)

        #print(dcfs_dicts_rads_list)

    def screen_Annex_G_ICRP119_dcf_inh_public_for_radionuclide(self, file_path, radionuclide):
        """
        Reads an Excel file and returns rows that match the given radionuclide.

        Parameters:
            file_path (str): Path to the Excel file.
            radionuclide (str): Radionuclide name (e.g., "Cs-137").

        Returns:
            DataFrame: Filtered rows containing the specified radionuclide.
        """
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            # df.columns = df.columns.str.strip()
            df.columns = ['Nuclide', 'Half-life', 'Type', 'f1', 'inh_infant', 'f1_age_g_gt_1a',
                          'inh_1_year', 'inh_5_years', 'inh_10_years', 'inh_15_years',
                          'inh_adult']

            if "Nuclide" in df.columns:
                df_filtered = df[df["Nuclide"].astype(str).str.strip().str.upper() == radionuclide.upper()]
                return df_filtered if not df_filtered.empty else "No data found"
            else:
                return "No 'Nuclide' column found"

        except Exception as e:
            return f"Error: {e}"

    def screen_Annex_H_ICRP119_dcf_inhal_reactive_soluble_gases_public_for_radionuclide(self, file_path, radionuclide):
        """
        Reads a CSV file, ignores the first column (index), and returns rows matching the given radionuclide.

        Parameters:
            file_path (str): Path to the CSV file.
            radionuclide (str): Radionuclide name (e.g., "H-3").

        Returns:
            DataFrame: Filtered rows containing the specified radionuclide.
        """
        try:
            df = pd.read_csv(self, file_path, skiprows=1, index_col=0)
            df.columns = ['Nuclide', 'Half-life', 'Type', 'f1', 'inh_infant', 'f1_age_g_gt_1a',
                          'inh_1_year', 'inh_5_years', 'inh_10_years', 'inh_15_years', 'inh_adult',
                          'VAPOUR_FORM']

            df.columns = df.columns.str.strip()

            if "Nuclide" in df.columns:
                df_filtered = df[df["Nuclide"].astype(str).str.strip().str.upper() == radionuclide.upper()]
                return df_filtered if not df_filtered.empty else "No data found"
            else:
                return "No 'Nuclide' column found"

        except Exception as e:
            return f"Error: {e}"

    def screen_Table_A2_DOE_STD_1196_2011_dcf_inhal_by_radionuclide(self, file_path, radionuclide):
        """
        Reads a cleaned CSV file and extracts rows containing the specified radionuclide.

        Parameters:
            file_path (str): Path to the cleaned CSV file.
            radionuclide (str): Radionuclide name (e.g., "Cs-137").

        Returns:
            DataFrame: Filtered rows containing the specified radionuclide.
        """
        try:
            # Read CSV, treating the first row as the header
            df = pd.read_csv(file_path, skiprows=0)
            df.columns = ['Index', 'Nuclide', 'Type', 'f1', 'inh_infant', 'inh_1_year',
                          'inh_5_year', 'inh_10_year', 'inh_15_year', 'inh_adult', 'Reference Person']
            # first column index is removed
            df = df.iloc[:, 1:]

            # Ensure "Nuclide" column exists
            if "Nuclide" in df.columns:
                # Filter rows where Nuclide matches the input (case insensitive)
                df_filtered = df[df["Nuclide"].astype(str).str.strip().str.upper() == radionuclide.upper()]
                return df_filtered if not df_filtered.empty else "No data found for the given radionuclide."
            else:
                return "No 'Nuclide' column found in the file."

        except Exception as e:
            return f"Error: {e}"

    def screen_Table_5_JAERI_dcf_inh_particulates_public_by_radionuclide(self, file_path, radionuclide):
        """
        Reads a cleaned CSV file and extracts rows containing the specified radionuclide.

        Parameters:
            file_path (str): Path to the cleaned CSV file.
            radionuclide (str): Radionuclide name (e.g., "Cs-137").

        Returns:
            DataFrame: Filtered rows containing the specified radionuclide.
        """
        try:
            # Read CSV, treating the first row as the header
            df = pd.read_csv(file_path, skiprows=0)
            # df.columns = ['Index', 'Nuclide', 'Type', 'f1',  'Newborn', '1-year' ,'5-year', '10-year',
            #      '15-year', 'Adult','Reference Person']
            # first column index is removed
            # print(df)
            df.columns = ['Index', 'Nuclide', 'Half-life', 'Type', 'f1', 'inh_infant', 'f1_age_g_gt_1a',
                          'inh_1_year', 'inh_5_years', 'inh_10_years', 'inh_15_years', 'inh_adult']

            df = df.iloc[:, 1:]
            # print(df)

            # Ensure "Nuclide" column exists
            if "Nuclide" in df.columns:
                # Filter rows where Nuclide matches the input (case insensitive)
                df_filtered = df[df["Nuclide"].astype(str).str.strip().str.upper() == radionuclide.upper()]
                return df_filtered if not df_filtered.empty else "No data found for the given radionuclide."
            else:
                return "No 'Nuclide' column found in the file."

        except Exception as e:
            return f"Error: {e}"

    def screen_Table_7_JAERI_dcf_inh_Public_Soluble_Reactive_Gases_Vapours_public_by_radionuclide(self, file_path,
                                                                                                  radionuclide):
        """
        Reads a cleaned CSV file and extracts rows containing the specified radionuclide.

        Parameters:
            file_path (str): Path to the cleaned CSV file.
            radionuclide (str): Radionuclide name (e.g., "Cs-137").

        Returns:
            DataFrame: Filtered rows containing the specified radionuclide.
        """
        try:
            # Read CSV, treating the first row as the header
            df = pd.read_csv(file_path, header=0)
            # df.columns = ['Index', 'Nuclide', 'Type', 'f1',  'Newborn', '1-year' ,'5-year', '10-year',
            #      '15-year', 'Adult','Reference Person']
            df.columns = ['Index', 'Nuclide', 'Chemical Form', 'Half-life', 'Type', 'percent_deposit', 'f1',
                          'inh_infant', 'f1_age_g_gt_1a', 'inh_1_year', 'inh_5_years',
                          'inh_10_years', 'inh_15_years', 'inh_adult']

            # first column index is removed
            df = df.iloc[:, 1:]
            # print(df)
            # Ensure "Nuclide" column exists
            if "Nuclide" in df.columns:
                # Filter rows where Nuclide matches the input (case insensitive)
                df_filtered = df[df["Nuclide"].astype(str).str.strip().str.upper() == radionuclide.upper()]
                return df_filtered if not df_filtered.empty else "No data found for the given radionuclide."
            else:
                return "No 'Nuclide' column found in the file."

        except Exception as e:
            return f"Error: {e}"

    def screen_Table_4_6_FGR_15_dcf_ecerman_submersion(self, file_path, radionuclide,
                                                       sheet_name='submersion_dose'):
        """
        Return Dose Conversion Factors (Submersion) specific to radionuclide.

        This function retrieves dose conversion factors (DCF) for submersion exposure from the specified Excel file.
        It filters the data based on the given radionuclide.

        Args:
            file_path (str): The path to the Excel file containing submersion DCF data.
            radionuclide (str): The name of the radionuclide to filter data for.
            sheet_name (str, optional): The sheet name in the Excel file containing the data. Defaults to 'submersion_dose'.

        Returns:
            pd.DataFrame: A DataFrame containing DCF values for the specified radionuclide.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the radionuclide is not found in the dataset.
        """
        try:
            # Load Excel sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

            # Drop fully empty rows
            df.dropna(axis=0, how='all', inplace=True)

            # Rename columns (ensure they exist before renaming)
            expected_columns = ['Nuclide', 'sub_infant', 'sub_1_year', 'sub_5_years',
                                'sub_10_years', 'sub_15_years', 'sub_adult']

            if len(df.columns) >= len(expected_columns):
                df.columns = expected_columns  # Assign column names if they match expected structure

            # Filter rows based on the radionuclide
            df_filtered = df[df['Nuclide'] == radionuclide]

            if df_filtered.empty:
                raise ValueError(f"No data found for radionuclide: {radionuclide}")

            return df_filtered

        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def screen_Table_A3_DOE_STD_1196_2011_dcf_submersion(self, file_path, radionuclide):
        """
        Return Dose Conversion Factors (Submersion) for a specific radionuclide from the DOE-STD-1196-2011 dataset.

        This function reads an Excel file, extracts submersion dose conversion factor (DCF) data,
        and filters rows based on the given radionuclide.

        Args:
            file_path (str): The path to the Excel file containing the submersion DCF data.
            radionuclide (str): The name of the radionuclide to filter data for.
            sheet_name (str, optional): The sheet name in the Excel file. Defaults to the first sheet if None.

        Returns:
            pd.DataFrame: A DataFrame containing DCF values for the specified radionuclide.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the radionuclide is not found in the dataset.
        """
        try:
            # Load Excel file
            df = pd.read_excel(file_path, engine="openpyxl")

            # Merge 2nd and 3rd columns (Col2 and Col3) with a space separator
            df["Merged_Col2_Col3"] = df.iloc[:, 1].astype(str) + " " + df.iloc[:, 2].astype(str)

            # Drop the original columns if needed
            df.drop(df.columns[[1, 2]], axis=1, inplace=True)
            # print(df)
            # Drop fully empty rows
            # df.dropna(axis=0, how='all', inplace=True)
            df.columns = ["Nuclide", "sub_adult", "Half-life"]

            # Ensure "Nuclide" column exists before filtering
            if 'Nuclide' not in df.columns:
                raise ValueError("Expected column 'Nuclide' not found in dataset.")

            # Filter rows for the specified radionuclide
            df_filtered = df[df['Nuclide'] == radionuclide]

            if df_filtered.empty:
                raise ValueError(f"No data found for radionuclide: {radionuclide}")

            return df_filtered

        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def screen_annex_a_icrp119_dcf_inhal_worker(self, file_path, radionuclide, sheet_name=0):
        """
        Reads the given Excel file, filters rows based on the radionuclide,
        merges the 2nd and 3rd columns with space separation, and returns the result.

        Args:
            file_path (str): Path to the Excel file.
            radionuclide (str): Radionuclide name to filter (e.g., "Cs-137").
            sheet_name (str or int): Name or index of the sheet to read.

        Returns:
            pd.DataFrame or str: Filtered DataFrame with merged columns, or an error message.
        """
        try:
            # Load the Excel file
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Drop fully empty rows
            df.dropna(axis=0, how='all', inplace=True)

            # Ensure we have the expected number of columns before renaming
            expected_cols = 9  # Adjust this if needed
            if df.shape[1] < expected_cols:
                return f"Error: Expected at least {expected_cols} columns, found {df.shape[1]}."

            # Rename columns
            df.columns = ['Element', 'Nuclide', 'Half-life', 'Type', 'inh_f1', 'inh_adult_1mu_m',
                          'inh_adult_5mu_m', 'ing_f1', 'ing_adult']

            # Drop the first column (Element)
            df.drop(columns=['Element'], axis=1, inplace=True)

            # Filter based on the radionuclide
            df_filtered = df[df['Nuclide'].fillna('').astype(str).str.startswith(radionuclide)]

            # If no rows match, return a message
            return df_filtered if not df_filtered.empty else "No matching data found for the given radionuclide."

        except Exception as e:
            return f"Error: {e}"

    def screen_Annex_B_ICRP119_dcf_inhal_reactive_soluble_gases_worker(self, file_path, radionuclide):
        """
        Reads a CSV file, ignores the first column (index), and returns rows matching the given radionuclide.

        Parameters:
            file_path (str): Path to the CSV file.
            radionuclide (str): Radionuclide name (e.g., "H-3").

        Returns:
            DataFrame or str: Filtered rows containing the specified radionuclide, or an error message.
        """
        try:
            # Read the CSV, skipping the first row and detecting delimiter
            df = pd.read_csv(file_path, skiprows=1, sep=None, engine="python")

            # Ensure the correct number of columns before renaming
            expected_cols = 4  # Adjust if the actual file has a different structure
            if df.shape[1] < expected_cols:
                return f"Error: Expected at least {expected_cols} columns, found {df.shape[1]}."

            # Rename columns appropriately
            df.columns = ['Nuclide', 'Chemical Form', 'Half-life', 'inh_adult']

            # Drop rows where Nuclide is NaN
            df.dropna(subset=["Nuclide"], inplace=True)

            # Standardize radionuclide search (strip spaces and convert to uppercase)
            df_filtered = df[df["Nuclide"].astype(str).str.strip().str.upper() == radionuclide.upper()]

            return df_filtered if not df_filtered.empty else "No data found for the given radionuclide."

        except Exception as e:
            return f"Error: {e}"

    def screen_Table_3_JAERI_dcf_inh_ing_particulates_worker_by_radionuclide(self, file_path, radionuclide):
        """
        Reads a cleaned CSV file and extracts rows containing the specified radionuclide.

        Parameters:
            file_path (str): Path to the cleaned CSV file.
            radionuclide (str): Radionuclide name (e.g., "Cs-137").

        Returns:
            DataFrame or str: Filtered rows containing the specified radionuclide, or an error message.
        """
        try:
            # Read CSV
            df = pd.read_csv(file_path, skiprows=0)

            # Check if at least 9 columns exist
            expected_cols = 9  # Adjust if necessary
            if df.shape[1] < expected_cols:
                return f"Error: Expected at least {expected_cols} columns, found {df.shape[1]}."

            # Rename columns
            df.columns = ['Element', 'Nuclide', 'Half-life', 'Type', 'inh_f1', 'inh_adult_1mu_m',
                          'inh_adult_5mu_m', 'ing_f1', 'ing_adult']

            # Drop the first column ("Element")
            df = df.iloc[:, 1:]

            # Ensure "Nuclide" column exists
            if "Nuclide" not in df.columns:
                return "Error: No 'Nuclide' column found in the file."

            # Filter rows where Nuclide starts with the input (case insensitive)
            df_filtered = df[df["Nuclide"].str.startswith(radionuclide, na=False)]

            # If no rows match, return a message
            return df_filtered if not df_filtered.empty else "No data found for the given radionuclide."

        except Exception as e:
            return f"Error: {e}"

    def screen_Table_6_JAERI_dcf_inh_public_soluble_reactive_gases_vapours_workers_by_radionuclide(self, file_path,
                                                                                                   radionuclide):
        """
        Reads a cleaned CSV file and extracts rows containing the specified radionuclide.

        Parameters:
            file_path (str): Path to the cleaned CSV file.
            radionuclide (str): Radionuclide name (e.g., "Cs-137").

        Returns:
            DataFrame or str: Filtered rows containing the specified radionuclide, or an error message.
        """
        try:
            # Read CSV with the first row as header
            df = pd.read_csv(file_path, header=0)

            # Ensure we have enough columns before renaming
            expected_cols = 5  # Adjust this if necessary
            if df.shape[1] < expected_cols:
                return f"Error: Expected at least {expected_cols} columns, but found {df.shape[1]}."

            # Rename columns
            df.columns = ['Index', 'Nuclide', 'Chemical Form', 'Half-life', 'inh_adult']

            # Drop the first column ("Index")
            df.drop(columns=['Index'], inplace=True, errors='ignore')

            # Ensure "Nuclide" column exists
            if "Nuclide" not in df.columns:
                return "Error: No 'Nuclide' column found in the file."

            # Filter rows where Nuclide matches the input (case insensitive)
            df_filtered = df[df["Nuclide"].astype(str).str.strip().str.upper() == radionuclide.upper()]

            return df_filtered if not df_filtered.empty else "No data found for the given radionuclide."

        except Exception as e:
            return f"Error: {e}"


    def merge_dataframes_with_source_hc2(self, **dfs):
        """
        Merges multiple DataFrames while adding a column to specify their source.

        Parameters:
            **dfs: Dictionary of named DataFrames (e.g., result_tab7="Table 7")

        Returns:
            Merged DataFrame or an error message if no valid DataFrames exist.
        """
        valid_dfs = []

        for name, df in dfs.items():
            if isinstance(df, pd.DataFrame):  # Check if it's a valid DataFrame
                df = df.copy()  # Avoid modifying the original
                df["Reference"] = name  # Add source column
                df["Valid for"] = 'Public'
                valid_dfs.append(df)

        if not valid_dfs:
            return "No valid DataFrames to merge."

        return pd.concat(valid_dfs, ignore_index=True, sort=False)

    def merge_dataframes_with_source_hc3(self, **dfs):
        """
        Merges multiple DataFrames while adding a column to specify their source.

        Parameters:
            **dfs: Dictionary of named DataFrames (e.g., result_tab7="Table 7")

        Returns:
            Merged DataFrame or an error message if no valid DataFrames exist.
        """
        valid_dfs = []

        for name, df in dfs.items():
            if isinstance(df, pd.DataFrame):  # Check if it's a valid DataFrame
                df = df.copy()  # Avoid modifying the original
                df["Reference"] = name  # Add source column
                df["Valid for"] = 'Worker'
                valid_dfs.append(df)

        if not valid_dfs:
            return "No valid DataFrames to merge."

        return pd.concat(valid_dfs, ignore_index=True, sort=False)

    def filter_max_value_by_reference(self, df, radionuclide, nuclide_col, value_col, reference_col):
        """
        Filters the dataframe for the given radionuclide and selects the maximum value based on priority order:
        1. 'ICRP119' or 'FGR' (take the maximum among these).
        2. If none found, take the maximum from 'DOE-STD'.
        3. If still none found, take the maximum from 'JAERI'.
        4. If no data is available after filtering, return a message.

        Args:
            df (pd.DataFrame): Input dataframe.
            radionuclide (str): Radionuclide name to filter.
            nuclide_col (str): Column name for radionuclide.
            value_col (str): Column name for values (e.g., "inh_adult").
            reference_col (str): Column name for reference.

        Returns:
            pd.DataFrame or str: Filtered row(s) with the maximum value, or a message if no data is found.
        """
        # Ensure column names exist in the dataframe
        required_cols = [nuclide_col, value_col, reference_col]
        # print(required_cols)
        for col in required_cols:
            if col not in df.columns:
                return f"Error: Column '{col}' not found in dataframe."

        # Convert all columns to string to avoid issues
        # print(df[nuclide_col] )
        df[nuclide_col] = df[nuclide_col].astype(str).str.strip().str.upper()
        df[reference_col] = df[reference_col].astype(str)

        # Filter rows for the given radionuclide
        df_filtered = df[df[nuclide_col] == radionuclide.upper()]
        if df_filtered.empty:
            return f"No data available for radionuclide: {radionuclide}"

        # Function to check if reference contains specific keywords
        def contains_keyword(df, keywords):
            return df[df[reference_col].str.contains('|'.join(keywords), case=False, na=False)]

        # Step 1: Look for 'ICRP119' or 'FGR' and get max value
        df_priority1 = contains_keyword(df_filtered, ["ICRP_119", "FGR"])
        if not df_priority1.empty:
            df_priority1.loc[:, value_col] = pd.to_numeric(df_priority1[value_col], errors='coerce')

            # df_priority1[value_col] = pd.to_numeric(df_priority1[value_col], errors='coerce')
            print(f"DCF (max) taken from {df_priority1['Reference'].iloc[0]}".format())
            return df_priority1[value_col].max()

        # Step 2: If no 'ICRP119' or 'FGR', look for 'DOE-STD'
        df_priority2 = contains_keyword(df_filtered, ["DOE_STD"])
        if not df_priority2.empty:
            df_priority2.loc[:, value_col] = pd.to_numeric(df_priority2[value_col], errors='coerce')

            # df_priority2[value_col] = pd.to_numeric(df_priority2[value_col], errors='coerce')
            print(f"DCF (max) taken from DOE-STD-1196-2011 {df_priority2['Reference']}".format())
            return df_priority2[value_col].max()

        # Step 3: If no 'DOE-STD', look for 'JAERI'
        df_priority3 = contains_keyword(df_filtered, ["JAERI"])
        if not df_priority3.empty:
            df_priority3.loc[:, value_col] = pd.to_numeric(df_priority3[value_col], errors='coerce')
            print("DCF (max) taken from JAERI-Data/Code 2002-013")
            # df_priority3[value_col] = pd.to_numeric(df_priority3[value_col], errors='coerce')
            return df_priority3[value_col].max(skipna=True)

        # Step 4: If no data found after filtering, return message
        return f"No data available for radionuclide: {radionuclide}"

    def compute_max_dcf(self, radionuclide):

        dict_dcf = {}
        # INH_HC2
        result_annexg = self.screen_Annex_G_ICRP119_dcf_inh_public_for_radionuclide(
            "library/inhalation_HC2/Annex_G_ICRP119_dcf_inh_public.xlsx",
            radionuclide)
        result_annexh = self.screen_Annex_H_ICRP119_dcf_inhal_reactive_soluble_gases_public_for_radionuclide(
            "library/inhalation_HC2/Annex_H_ICRP119_dcf_inhal_reactive_soluble_gases_public.csv",
            radionuclide)
        result_tab_a2 = self.screen_Table_A2_DOE_STD_1196_2011_dcf_inhal_by_radionuclide(
            "library/inhalation_HC2/Table_A2-DOE-STD-1196-2011_dcf_inhal.csv",
            radionuclide)
        result_tab5 = self.screen_Table_5_JAERI_dcf_inh_particulates_public_by_radionuclide(
            "library/inhalation_HC2/Table_5_JAERI_dcf_inh_particulates_public.csv",
            radionuclide)
        result_tab7 = self.screen_Table_7_JAERI_dcf_inh_Public_Soluble_Reactive_Gases_Vapours_public_by_radionuclide(
            "library/inhalation_HC2/Table_7_JAERI_dcf_inh_Public_Soluble_Reactive_Gases_Vapours.csv",
            radionuclide)

        # SUB HC2
        result_sub_fgr15_hc2 = self.screen_Table_4_6_FGR_15_dcf_ecerman_submersion(
            "library/submersion_HC2/Dose_Table_4_6_ecerman_final_FGR15.xlsx",
            radionuclide)
        result_sub_dcf_doe_std = self.screen_Table_A3_DOE_STD_1196_2011_dcf_submersion(
            "library/submersion_HC2/Table_A3_DOE_STD_1196_2011_dcf_submersion.xlsx",
            radionuclide)

        # INH_HC3
        result_annexa = self.screen_annex_a_icrp119_dcf_inhal_worker(
            "library/inhalation_HC3/AnnexA_ICRP119_dcf_inhal_Worker.xlsx",
            radionuclide)
        result_annexb = self.screen_Annex_B_ICRP119_dcf_inhal_reactive_soluble_gases_worker(
            "library/inhalation_HC3/AnnexB_ICRP119_dcf_inh_soluble_reactive_gas_worker.csv",
            radionuclide)
        result_tab3 = self.screen_Table_3_JAERI_dcf_inh_ing_particulates_worker_by_radionuclide(
            "library/inhalation_HC3/Table3_JAERI_dcf_ing_inh_PARTICULATES_Worker.csv",
            radionuclide)
        result_tab6 = self.screen_Table_6_JAERI_dcf_inh_public_soluble_reactive_gases_vapours_workers_by_radionuclide(
            "library/inhalation_HC3/Table6_JAERI_dcf_Soluble_Reactive_Gases_Worker.csv",
            radionuclide)

        # Merge dataframes
        merged_df_inh_hc2 = self.merge_dataframes_with_source_hc2(
            Table_7_JAERI_DATA_CODE_2002_013=result_tab7,
            Table_5_JAERI_DATA_CODE_2002_013=result_tab5,
            Annex_G_ICRP_119=result_annexg,
            Annex_H_ICRP_119=result_annexh
        )

        merged_df_sub_hc2 = self.merge_dataframes_with_source_hc2(
            Table_4_6_FGR15=result_sub_fgr15_hc2,
            Table_A3_DOE_STD_1196_2011=result_sub_dcf_doe_std
        )

        merged_df_inh_hc3 = self.merge_dataframes_with_source_hc3(
            Annex_A_ICRP_119=result_annexa,
            Annex_B_ICRP_119=result_annexb,
            Table_3_JAERI_DATA_CODE_2002_013=result_tab3,
            Table_6_JAERI_DATA_CODE_2002_013=result_tab6
        )

        merged_df_ing_hc3 = self.merge_dataframes_with_source_hc3(
            Annex_A_ICRP_119=result_annexa,
            Annex_B_ICRP_119=result_annexb,
            Table_6_JAERI_DATA_CODE_2002_013=result_tab6
        )

        # Get max DCF values
        max_dcf_inh_hc2 = self.filter_max_value_by_reference(merged_df_inh_hc2, radionuclide, "Nuclide", "inh_adult",
                                                        "Reference")
        max_dcf_sub_hc2 = self.filter_max_value_by_reference(merged_df_sub_hc2, radionuclide, "Nuclide", "sub_adult",
                                                        "Reference")
        max_dcf_inh_hc3 = self.filter_max_value_by_reference(merged_df_inh_hc3, radionuclide, "Nuclide", "inh_adult_1mu_m",
                                                        "Reference")
        max_dcf_ing_hc3 = self.filter_max_value_by_reference(merged_df_ing_hc3, radionuclide, "Nuclide", "ing_adult",
                                                        "Reference")

        dict_dcf['max_dcf_inh_hc2'] = max_dcf_inh_hc2
        dict_dcf['max_dcf_sub_hc2'] = max_dcf_sub_hc2
        dict_dcf['max_dcf_inh_hc3'] = max_dcf_inh_hc3
        dict_dcf['max_dcf_ing_hc3'] = max_dcf_ing_hc3

        return dict_dcf

    def find_aws(self):
        xls = pd.ExcelFile("library/AWS.xls")
        df_tq = pd.read_excel(xls)
        df_tq.dropna(axis=0, how='all', inplace=True)
        # rads_list = ['Ir-192', 'Co-60']
        AWS = []
        for rad in self.rads_list:
            rad = rad.split('-')[0]
            if not df_tq[df_tq['Symbol'] == rad]['AW'].empty:
                val = df_tq[df_tq['Symbol'] == rad]['AW'].item()
            else:
                val = None
                raise ValueError(f"Information on atomic weight for %s is not available"%rad)
            AWS.append(np.float32(val))
        return AWS
    
    def get_bv(self):
        xls = pd.ExcelFile("library/doe_haz_cat_excel.xlsx")
        df_tq = pd.read_excel(xls, sheet_name='r_bv')
        df_tq.dropna(axis=0, how='all', inplace=True)
        BV = []
        for rad in self.rads_list:
            rad = rad.split('-')[0]
            val = df_tq[df_tq['Symbol'] == rad]['Soil to Plant Concentration Factor\n(Bv)'].item()
            BV.append(val)
        return BV

    def get_R_HC3(self):
        xls = pd.ExcelFile("library/doe_haz_cat_excel.xlsx")
        df_tq = pd.read_excel(xls, sheet_name='r_bv')
        df_tq.dropna(axis=0, how='all', inplace=True)
        R = []
        for rad in self.rads_list:
            rad = rad.split('-')[0]
            val = df_tq[df_tq['Symbol'] == rad]['Release Fraction (R)'].item()
            R.append(val)
        return R
    
    def get_R_HC2(self):
        Rs = []
        for rad in self.rads_list:
            rad = rad.split('-')[0]
            if rad in ['H', 'Kr', 'Xe', 'Ar', 'Rn', 'Ne', 'Cl', 'F', 'N', 'O']:
                R = 1.0
                Rs.append(R)
            elif rad in ['P', 'S', 'K', 'I', 'Na', 'Br']:
                R = 0.5
                Rs.append(R)
            elif rad in ['Se', 'Hg', 'Cs', 'Po', 'Te', 'Ru', 'C']:
                R = 1e-02
                Rs.append(R)
            else:
                R = 1e-03
                Rs.append(R)
        return Rs
    '''
    def convert_half_life_to_seconds(self, half_life):
        units = {"ls": 1e-6, "ms": 1e-3, "s": 1, "m": 60, "h": 3600, "d": 86400, "y": 31536000}
        for unit, factor in units.items():
            if half_life.endswith(unit):
                try:
                    value = float(half_life.replace(unit, "").strip())
                    return value * factor
                except ValueError:
                    return half_life  # Return as is if conversion fails
        return half_life  # Return as is if no unit matches
    '''

    def get_nuclide_info(self, nuclide_name):
        """Retrieve nuclide information from primary or JAERI dataset."""
        primary_file = "library/radionuclides_halflife_complete.csv"
        jaeri_file = "library/JAERI-Data-Code 2002-Table4_CSV_FINAL.xlsx"

        def convert_half_life_to_seconds(half_life):
            units = {"ls": 1e-6, "ms": 1e-3, "s": 1, "m": 60, "h": 3600, "d": 86400, "y": 31536000}
            for unit, factor in units.items():
                if half_life.endswith(unit):
                    try:
                        value = float(half_life.replace(unit, "").strip())
                        return value * factor
                    except ValueError:
                        return half_life  # Return as is if conversion fails
            return half_life  # Return as is if no unit matches

        # Load primary dataset
        df = pd.read_csv(primary_file)
        nuclide_data = df[df["Nuclide"] == nuclide_name]

        if nuclide_data.empty:
            print("Fetching from JAERI dataset...")
            try:
                jaeri_df = pd.read_excel(jaeri_file, sheet_name="JAERI-IngestionDCF")
                jaeri_df = jaeri_df.dropna()
                nuclide_data = jaeri_df[jaeri_df["Nuclide"] == nuclide_name]
                if nuclide_data.empty:
                    return f"Nuclide {nuclide_name} not found."
                if "Hg" in nuclide_name:
                    raise ValueError("refined JAERI dataset (JAERI-Data-Code 2002-Table4_CSV_FINAL.xlsx) does not "
                                     "have half-life information for Mercury (Hg) nuclides. Please update it manually")
            except Exception as e:
                return f"Error loading JAERI file: {e}"

        half_life = convert_half_life_to_seconds(nuclide_data["Half-life"].values[0])
        decay_constant = 0.693 / half_life if isinstance(half_life, (int, float)) and half_life > 0 else "N/A"

        result = {
            "Nuclide": nuclide_name,
            "Half-life (s)": half_life,
            "Decay Constant (s^-1)": decay_constant
        }

        # Include all additional columns from either dataset
        for column in nuclide_data.columns[1:]:  # Skip 'Nuclide' column
            result[column] = nuclide_data[column].values[0]

        return result

    # Example usage:
    # print(get_nuclide_info("Ir-179"))

    def halflives_lambda_rads_from_rads_list(self):
        half_lives = []
        lambda_of_rads = []
        for nuclide_name in self.rads_list:
            nuclide_info = self.get_nuclide_info(nuclide_name)
            half_lives.append(nuclide_info['Half-life (s)'])
            lambda_of_rads.append(nuclide_info['Decay Constant (s^-1)'])

        half_lives = np.array(half_lives)

        # unit: /second
        self.lambda_of_rads = lambda_of_rads

        # unit: second
        self.list_half_life = half_lives

        return self.list_half_life, self.lambda_of_rads

    def find_half_life_and_decay_const_radionuclides(self):
        """
            Find the half-life and decay constant for radionuclides.

            This method reads data from the "RadioToxicityMaster.xls" file to find the half-life and decay constant
            (lambda) for each radionuclide in the `rads_list`.

            Returns:
                tuple: A tuple containing two lists: `list_half_life`, which contains the half-life of each radionuclide in
                    seconds, and `lambda_of_rads`, which contains the decay constant (lambda) of each radionuclide in
                    per second.
            Raises:
                ValueError: If the unit of half-life is not recognized. It should be 'a' or 'y' for year, 'd' for days, 'h'
                    for hours, 'm' for minutes, or 's' for seconds.
        """
        # lambda
        xls = pd.ExcelFile("library/RadioToxicityMaster.xls")
        name = pd.read_excel(xls, "Inhalation CED Sv per Bq Public")
        name.dropna(axis=0, how='all', inplace=True)

        # calculate half-life in second
        lambda_of_rads = []
        list_half_life = []
        for rad in self.rads_list:
            search_string = '|'.join([rad])
            df = name[name['Nuclide'].str.contains(search_string, na=False)]
            if str('d') in df['Hal-life'].iloc[0]:
                x = float(df['Hal-life'].iloc[0][:-1])
                x = x * 3600 * 24
                lambda_of_rad = (0.693 / x)
                lambda_of_rads.append(lambda_of_rad)
                # unit second
                list_half_life.append(x)

            elif str('a') in df['Hal-life'].iloc[0] or str('y') in df['Hal-life'].iloc[0]:
                x = float(df['Hal-life'].iloc[0][:-1])
                x = x * 3600 * 24 * 365
                lambda_of_rad = (0.693 / x)
                lambda_of_rads.append(lambda_of_rad)
                list_half_life.append(x)

            elif str('h') in df['Hal-life'].iloc[0]:
                x = float(df['Hal-life'].iloc[0][:-1])
                x = x * 3600
                lambda_of_rad = (0.693 / x)
                lambda_of_rads.append(lambda_of_rad)
                list_half_life.append(x)

            elif str('m') in df['Hal-life'].iloc[0]:
                x = float(df['Hal-life'].iloc[0][:-1])
                x = x * 60
                lambda_of_rad = (0.693 / x)
                lambda_of_rads.append(lambda_of_rad)
                list_half_life.append(x)

            elif str('s') in df['Hal-life'].iloc[0]:
                x = float(df['Hal-life'].iloc[0][:-1])
                lambda_of_rad = (0.693 / x)
                lambda_of_rads.append(lambda_of_rad)
                list_half_life.append(x)

            else:
                raise ValueError('Unit of half-life not recognized. It should be (a or y) for year, d for days, '
                                 'h for hours, m for minutes and s for seconds.')
        # unit: /second
        self.lambda_of_rads = lambda_of_rads
        # unit: second
        self.list_half_life = list_half_life

        return self.list_half_life, self.lambda_of_rads
    
    def inhalation_dcf_list(self, master_file='library/RadioToxicityMaster.xls',
                            sheet_name='Inhalation CED Sv per Bq Public',
                            age=18):
        """
        Return Dose conversion Factors (Inhalation) specific to age and radionuclide.

        This method reads data from the specified Excel file and sheet to find the dose conversion factors (DCFs) for
        inhalation exposure, considering the age of the public.

        Args:
            master_file (str): The path to the Excel file containing data with DCF.
            sheet_name (str): The name of the sheet in the Excel file containing the respective data.
            age (int): The age of the public.

        Returns:
            numpy.ndarray: An array containing Dose conversion Factors (DCFs) specific to each radionuclide.

        Raises:
            ValueError: If the age of the recipient is not a number.
        """
        xls = pd.ExcelFile(master_file)
        name = pd.read_excel(xls, sheet_name)
        name.dropna(axis=0, how='all', inplace=True)
        dcfs = []

        for ndx, rad in enumerate(self.rads_list):
            
            search_string = '|'.join([rad])
            df = name[name['Nuclide'] == search_string]
            # consider all types: F, M, S and take the max value as dcf
            search_string_type = '|'.join(['F', 'M', 'S'])
            df = df[df['Type'].str.contains(search_string_type, na=False)]
            if age > 17:
                dcf = df['e_g_age_g_gt_17a_Sv/Bq'].max()
            elif 12 < age <= 17:
                dcf = df['e_g_age_g_12_17a_Sv/Bq'].max()
            elif 7 < age <= 12:
                dcf = df['e_g_age_g_7_12a_Sv/Bq'].max()
            elif 2 < age <= 7:
                dcf = df['e_g_age_g_2_7a_Sv/Bq'].max()
            elif 1 < age <= 2:
                dcf = df['e_g_age_g_1_2a_Sv/Bq'].max()
            elif age <= 1:
                dcf = df['e_g_age_g_lt_1a_Sv/Bq'].max()
            else:
                raise ValueError('The age of recipient must be a number.')

            dcfs.append(dcf)

        self.inhalation_dcf = np.array(dcfs)
        return self.inhalation_dcf
    
    def inhalation_dcf_list_worker(self, master_file='library/worker_icrp119.xlsx',
                            sheet_name='Sheet1'):
        """
        Return Dose conversion Factors (Inhalation) specific to age and radionuclide.

        This method reads data from the specified Excel file and sheet to find the dose conversion factors (DCFs) for
        inhalation exposure, considering the age of the public.

        Args:
            master_file (str): The path to the Excel file containing data with DCF.
            sheet_name (str): The name of the sheet in the Excel file containing the respective data.
            age (int): The age of the public.

        Returns:
            numpy.ndarray: An array containing Dose conversion Factors (DCFs) specific to each radionuclide.

        Raises:
            ValueError: If the age of the recipient is not a number.
            
        # DO NOT ACCURATELY WORK FOR H-3, C-11, C-14, S-35 as these are having many chemical forms. Its in TO-DO tasks
        """
        xls = pd.ExcelFile(master_file)
        name = pd.read_excel(xls, sheet_name)
        name.dropna(axis=0, how='all', inplace=True)
        dcfs = []

        for ndx, rad in enumerate(self.rads_list):
            
            search_string = '|'.join([rad])
            df = name[name['nuclide'] == search_string]
            # consider all types: F, M, S and take the max value as dcf
            search_string_type = '|'.join(['F', 'M', 'S'])
            df = df[df['Type'].str.contains(search_string_type, na=False)]
            print('df inhal:', df)
            dcf = df['inh_e_sv_per_bq_1μm'].max()
            dcfs.append(dcf)

        inhalation_dcf = np.array(dcfs)
        return inhalation_dcf
    
    def ingestion_dcf_list_worker(self, master_file='library/worker_icrp119.xlsx',
                        sheet_name='Sheet1'):
        """
        Return Dose conversion Factors (ingestion) specific to age and radionuclide.

        This method reads data from the specified Excel file and sheet to find the dose conversion factors (DCFs) for
        ingestion exposure, considering the age of the public.

        Args:
            master_file (str): The path to the Excel file containing data with DCF.
            sheet_name (str): The name of the sheet in the Excel file containing the respective data.
            age (int): The age of the public.

        Returns:
            numpy.ndarray: An array containing Dose conversion Factors (DCFs) specific to each radionuclide.

        Raises:
            ValueError: If the age of the recipient is not a number.

        # DO NOT ACCURATELY WORK FOR H-3, C-11, C-14, S-35 as these are having many chemical forms. Its in TO-DO tasks
        """
        xls = pd.ExcelFile(master_file)
        name = pd.read_excel(xls, sheet_name)
        name.dropna(axis=0, how='all', inplace=True)
        dcfs = []

        for ndx, rad in enumerate(self.rads_list):

            search_string = '|'.join([rad])
            df = name[name['nuclide'] == search_string]
            # consider all types: F, M, S and take the max value as dcf
            search_string_type = '|'.join(['F', 'M', 'S'])
            df = df[df['Type'].str.contains(search_string_type, na=False)]
            dcf = df['ing_e_sv_per_bq'].max()
            dcfs.append(dcf)

        ingestion_dcf = np.array(dcfs)
        return ingestion_dcf
    
    def find_progeny_name_and_yield_f(self, rad, master_file="library/dcf_corr.xlsx"):
        """
            Return the names and fractional yields of progeny radionuclides for a given radionuclide.

            This method reads data from the specified Excel file to find the names and fractional yields of progeny radionuclides
            for a given radionuclide. It allows users to specify a threshold (in seconds) to ignore progeny with half-lives
            shorter than the threshold.

            Args:
                rad (str): The name of the radionuclide.
                master_file (str): The path to the Excel file containing data with progeny radionuclides and fractional yields.

            Returns:
                tuple: A tuple containing two numpy arrays:
                    - An array of strings representing the names of progeny radionuclides.
                    - An array of floats representing the fractional yields of progeny radionuclides.

            Raises:
                ValueError: If the unit of half-life for radionuclides is not recognized.
        """

        xls = pd.ExcelFile(master_file)
        name = pd.read_excel(xls, sheet_name=0,
                             names=['Element', 'Nuclide', 'halflife_and_daughters', 'decaymode_and_yield',
                                    'alpha_energy', 'electron_energy', 'photon_energy', 'total_mev_per_nt'], skiprows=0)
        name.dropna(axis=0, how='all', inplace=True)
        # 30 minute (default)
        if self.config['consider_progeny']:
            ignore_half_life = self.config['ignore_half_life']
        else:
            ignore_half_life = 0
        daughter_list = []
        frac_yield = []
        lambda_of_rads = []
        search_string = '|'.join([rad])
        df = name[name['Nuclide'] == search_string]
        index = df.index[0]
        i = 1
        while name.iloc[[index + i]].isnull().any()['Nuclide']:
            search_string = '|'.join(name.iloc[[index + i]]['halflife_and_daughters'])
            df1 = name[name['Nuclide'].str.contains(search_string, na=False)]
            for _, ndx in zip(df1['Nuclide'].values, df1['Nuclide'].index):
                if str(_) == search_string:
                    hlf = name.iloc[[ndx]]['halflife_and_daughters'].values[0]
                    if str('s') in hlf:
                        x = float(hlf[:-1])

                    elif str('m') in hlf:
                        x = float(hlf[:-1])
                        x = x * 60

                    elif str('d') in hlf:
                        x = float(hlf[:-1])
                        x = x * 3600 * 24

                    elif str('a') in hlf or str('y') in hlf:
                        x = float(hlf[:-1])
                        x = x * 3600 * 24 * 365

                    elif str('h') in hlf:
                        x = float(hlf[:-1])
                        x = x * 3600
                        lambda_of_rad = (0.693 / x)
                        lambda_of_rads.append(lambda_of_rad)

                    else:
                        raise ValueError('the unit of half-life for radionuclides should be in format a (annual),'
                                         'd (day), h (hour), m (minute), s (second)')

                    if x <= ignore_half_life:
                        daughter_list.append(name.iloc[[ndx]]['Nuclide'].values)
                        frac_yield.append(name.iloc[[index + i]]['decaymode_and_yield'].values)
            i += 1

        daughter_list = np.array(daughter_list).flatten()
        frac_yield = np.array(frac_yield).flatten()
        return daughter_list, frac_yield

    def get_dcf_sub_inert_gas_same_for_worker_and_public(self):
        """
        Creates a DataFrame containing effective dose rate coefficients for exposure
        of workers or adult members of the public to airborne concentration of inert gases.
        Converts the unit of dcf from Sv/day per Bq/m^3 to Sv/sec per Bq/m^3.

        SOURCE: A) ICRP Pub-119: ANNEX C. EFFECTIVE DOSE RATES FOR EXPOSURE OF WORKERS OR
        ADULT MEMBERS OF THE PUBLIC TO INERT GASES
        Table C.1. Effective dose rate coefficients ð_eÞ for exposure of workers or adult mem-
        bers of the public to airborne concentration of inert gases

        B) JAERI-Data/Code 2002-013: Table 8: Effective Dose Rates for Exposure of Adults – Inert Gases (Class SR-0)
        Returns:
        pd.DataFrame: DataFrame containing nuclide data.
        """
        data = [
            ("Argon", "Ar-37", "35.02 d", 4.1E-15),
            ("Argon", "Ar-39", "269 y", 1.1E-11),
            ("Argon", "Ar-41", "1.827 h", 5.3E-09),
            ("Argon", "Ar-42", "32.9 y", 1.3E-11),
            ("Argon", "Ar-44", "11.87 m", 8.1E-09),
            ("Krypton", "Kr-74", "11.50 m", 4.5E-09),
            ("Krypton", "Kr-75", "4.29 m", 5.1E-09),
            ("Krypton", "Kr-76", "14.8 h", 1.6E-09),
            ("Krypton", "Kr-77", "74.7 m", 3.9E-09),
            ("Krypton", "Kr-79", "35.04 h", 9.7E-10),
            ("Krypton", "Kr-81", "2.1E5 y", 2.1E-11),
            ("Krypton", "Kr-81m", "13 s", 4.8E-10),
            ("Krypton", "Kr-83m", "1.83 h", 2.1E-13),
            ("Krypton", "Kr-85", "10.72 y", 2.2E-11),
            ("Krypton", "Kr-85m", "4.48 h", 5.9E-10),
            ("Krypton", "Kr-87", "76.3 m", 3.4E-09),
            ("Krypton", "Kr-88", "2.84 h", 8.4E-09),
            ("Krypton", "Kr-89", "3.15 m", 8.3E-09),
            ("Xenon", "Xe-120", "40 m", 1.5E-09),
            ("Xenon", "Xe-121", "40.1 m", 7.5E-09),
            ("Xenon", "Xe-122", "20.1 h", 1.9E-10),
            ("Xenon", "Xe-123", "2.08 h", 2.4E-09),
            ("Xenon", "Xe-125", "17.0 h", 9.3E-10),
            ("Xenon", "Xe-127", "36.41 d", 9.7E-10),
            ("Xenon", "Xe-127m", "1.15333 m", 6.0E-10),
            ("Xenon", "Xe-129m", "8.0 d", 8.1E-11),
            ("Xenon", "Xe-131m", "11.9 d", 3.2E-11),
            ("Xenon", "Xe-133", "5.245 d", 1.2E-10),
            ("Xenon", "Xe-133m", "2.188 d", 1.1E-10),
            ("Xenon", "Xe-135", "9.09 h", 9.6E-10),
            ("Xenon", "Xe-135m", "15.29 m", 1.6E-09),
            ("Xenon", "Xe-137", "3.818 m", 9.4E-10),
            ("Xenon", "Xe-138", "14.17 m", 4.7E-09),
        ]

        df = pd.DataFrame(data, columns=["Element", "Nuclide", "Half-life", "dcf_sub (Sv/day per Bq/m^3)"])
        df["dcf_sub (Sv/sec per Bq/m^3)"] = df["dcf_sub (Sv/day per Bq/m^3)"].astype(float) / 86400
        return df

    def dcf_list_ecerman_submersion_include_progeny(self, master_file="library/Dose_ecerman_final.xlsx",
                                                    sheet_name="submersion_dose",
                                                    age=18):

        """
        Return Dose Conversion Factors (Submersion) specific to age and radionuclide, including progeny contribution.

        This method computes dose conversion factors (DCF) for submersion exposure from the specified Excel file.
        It accounts for the age of the individual and returns the maximum DCF available for the given radionuclide and age
        group. Additionally, it includes the contribution from progeny radionuclides based on the specified decay data.
        The details of nuclear decay data is obtained from SRS 19 based on ICRP 107.

        Args:
            master_file (str): The path to the Excel file containing data with DCF for submersion exposure.
            sheet_name (str): The name of the sheet in the Excel file containing the DCF data.
            age (int): The age of the individual for whom DCF is being calculated.

        Returns:
            list of tuples: A list containing tuples of DCF values for submersion exposure specific to each radionuclide
            in the `rads_list`, including the contribution from progeny radionuclides if `consider_progeny` is True.
            Each tuple contains two DCF values: the corrected DCF considering progeny and the original DCF.

        Raises:
            ValueError: If the age of the recipient is not a valid number.
        """

        # consider_progeny = self.config['consider_progeny']
        consider_progeny = False
        xls = pd.ExcelFile(master_file)
        name = pd.read_excel(xls, sheet_name)
        name.dropna(axis=0, how='all', inplace=True)
        dcfs = []
        dcf_corr_list = []
        for rad in self.rads_list:

            search_string = '|'.join([rad])
            df = name[name['Nuclide'] == search_string]
            if age > 17:
                dcf = df['Adult'].max()
            elif 12 < age <= 17:
                dcf = df['15-yr-old'].max()
            elif 7 < age <= 12:
                dcf = df['10-yr-old'].max()
            elif 2 < age <= 7:
                dcf = df['5-yr-old'].max()
            elif 1 < age <= 2:
                dcf = df['1-yr-old'].max()
            elif age <= 1:
                dcf = df['Newborn'].max()
            else:
                raise ValueError('The age of recipient must be a number.')
            
            dcf_corr = dcf
            if consider_progeny:
                daughter_list, frac_yield = self.find_progeny_name_and_yield_f(rad, master_file="library/dcf_corr.xlsx")
                for d, y in zip(daughter_list, frac_yield):
                    search_string = '|'.join([d])
                    df = name[name['Nuclide'].str.contains(search_string, na=False)]
                    if age > 17:
                        dcf_d = df['Adult'].max()
                    elif 12 < age <= 17:
                        dcf_d = df['15-yr-old'].max()
                    elif 7 < age <= 12:
                        dcf_d = df['10-yr-old'].max()
                    elif 2 < age <= 7:
                        dcf_d = df['5-yr-old'].max()
                    elif 1 < age <= 2:
                        dcf_d = df['1-yr-old'].max()
                    elif age <= 1:
                        dcf_d = df['Newborn'].max()
                    else:
                        raise ValueError('The age of recipient must be a number.')
                    dcf_corr += dcf_d * y

            dcfs.append(dcf)
            dcf_corr_list.append(dcf_corr)

        if consider_progeny:
            self.dcf_list_submersion_corr = np.array(dcf_corr_list)
            self.dcf_list_submersion = np.array(dcfs)
            dcfs_combo = []
            for i, j in zip(self.dcf_list_submersion_corr, self.dcf_list_submersion):
                t = tuple([i, j])
                dcfs_combo.append(t)
            return dcfs_combo
        else:
            self.dcf_list_submersion = np.array(dcfs)
            dcfs_combo = []
            for i, j in zip(self.dcf_list_submersion, self.dcf_list_submersion):
                t = tuple([i, j])
                dcfs_combo.append(t)
            return dcfs_combo

    def dcf_list_ecerman_ground_shine(self, master_file="library/Dose_ecerman_final.xlsx", sheet_name="surface_dose",
                                      age=18):
        """
        Return Dose conversion Factors (Ground Shine) specific to age and radionuclide.

        This method reads data from the specified Excel file and sheet to find the dose conversion factors (DCFs) for
        ground shine exposure, considering the age of the public.

        Args:
            master_file (str): The path to the Excel file containing data with DCF.
            sheet_name (str): The name of the sheet in the Excel file containing the respective data.
            age (int): The age of the public.

        Returns:
            numpy.ndarray: An array containing Dose conversion Factors (DCFs) specific to each radionuclide.

        Raises:
            ValueError: If the age of the recipient is not a number.
        """
        xls = pd.ExcelFile(master_file)
        name = pd.read_excel(xls, sheet_name)
        name.dropna(axis=0, how='all', inplace=True)
        dcfs = []

        for rad in self.rads_list:
            search_string = '|'.join([rad])
            df = name[name['Nuclide'] == search_string]
            if age > 17:
                dcf = df['Adult'].max()
            elif 12 < age <= 17:
                dcf = df['15-yr-old'].max()
            elif 7 < age <= 12:
                dcf = df['10-yr-old'].max()
            elif 2 < age <= 7:
                dcf = df['5-yr-old'].max()
            elif 1 < age <= 2:
                dcf = df['1-yr-old'].max()
            elif age <= 1:
                dcf = df['Newborn'].max()
            else:
                raise ValueError('The age of recipient must be a number.')

            dcfs.append(dcf)

        self.dcfs_gs = np.array(dcfs)

        return self.dcfs_gs

    def dcf_list_ecerman_ground_shine_include_progeny(self, master_file="library/Dose_ecerman_final.xlsx",
                                                      sheet_name='surface_dose',
                                                      age=18, consider_progeny=True):
        """
            Return Dose conversion Factors (Ground Shine) specific to age and radionuclide, considering progeny contribution.

            This method reads data from the specified Excel file and sheet to find the dose conversion factors (DCFs) for
            ground shine exposure, considering the age of the public. It allows users to choose whether to include the progeny
            contribution in the calculation. DCF values in SRS 19 does not include progeny contribution. This function
            facilitates the computation of DCFs that includes progeny contribution. The details of nuclear decay data
            is obtained from SRS 19 based on ICRP 107.

            Args:
                master_file (str): The path to the Excel file containing data with DCF.
                sheet_name (str): The name of the sheet in the Excel file containing the respective data.
                age (int): The age of the public.
                consider_progeny (bool): A boolean flag indicating whether to include progeny contribution (default is True).

            Returns:
                list of tuples: A list containing tuples of Dose conversion Factors (DCFs) specific to each radionuclide.
                    Each tuple contains two DCFs: one with progeny contribution included and one without.

            Raises:
                ValueError: If the age of the recipient is not a number.
        """
        xls = pd.ExcelFile(master_file)
        name = pd.read_excel(xls, sheet_name)
        name.dropna(axis=0, how='all', inplace=True)

        dcfs = []
        dcf_corr_list = []
        for rad in self.rads_list:

            search_string = '|'.join([rad])
            df = name[name['Nuclide'] == search_string]
            if age > 17:
                dcf_ = df['Adult'].max()
            elif 12 < age <= 17:
                dcf_ = df['15-yr-old'].max()
            elif 7 < age <= 12:
                dcf_ = df['10-yr-old'].max()
            elif 2 < age <= 7:
                dcf_ = df['5-yr-old'].max()
            elif 1 < age <= 2:
                dcf_ = df['1-yr-old'].max()
            elif age <= 1:
                dcf_ = df['Newborn'].max()
            else:
                raise ValueError('The age of recipient must be a number.')
            dcf_corr = dcf_
            daughter_list, frac_yield = self.find_progeny_name_and_yield_f(rad, master_file='library/dcf_corr.xlsx')

            if consider_progeny:
                for d, y in zip(daughter_list, frac_yield):
                    search_string = '|'.join([d])
                    df = name[name['Nuclide'].str.contains(search_string, na=False)]
                    if age > 17:
                        dcf_d = df['Adult'].max()
                    elif 12 < age <= 17:
                        dcf_d = df['15-yr-old'].max()
                    elif 7 < age <= 12:
                        dcf_d = df['10-yr-old'].max()
                    elif 2 < age <= 7:
                        dcf_d = df['5-yr-old'].max()
                    elif 1 < age <= 2:
                        dcf_d = df['1-yr-old'].max()
                    elif age <= 1:
                        dcf_d = df['Newborn'].max()
                    else:
                        raise ValueError('The age of recipient must be a number.')

                    dcf_corr += dcf_d * y
            dcfs.append(dcf_)
            dcf_corr_list.append(dcf_corr)

        if consider_progeny:
            self.dcfs_gs_corr = np.array(dcf_corr_list)
            self.dcfs_gs = np.array(dcfs)
            dcfs_combo = []
            for i, j in zip(self.dcfs_gs_corr, self.dcfs_gs):
                t = tuple([i, j])
                dcfs_combo.append(t)
            return dcfs_combo
        else:
            self.dcfs_gs = np.array(dcfs)
            dcfs_combo = []
            for i, j in zip(self.dcfs_gs, self.dcfs_gs):
                t = tuple([i, j])
                dcfs_combo.append(t)
            return dcfs_combo
        
    def dcf_list_ingestion(self, master_file="library/Dose_ecerman_final.xlsx", sheet_name="ingestion_gsr3", age=18):
        """
        Return Dose Conversion Factors (Ingestion) specific to age and radionuclide.

        This method computes dose conversion factors (DCF) for ingestion exposure from the specified Excel file.
        It accounts for the age of the individual and returns the maximum DCF available for the given radionuclide and age
        group. For tritium (H-3), it returns separate DCF values for HTO and OBT forms.

        Args:
            master_file (str): The path to the Excel file containing data with DCF for ingestion exposure.
            sheet_name (str): The name of the sheet in the Excel file containing the DCF data.
            age (int): The age of the individual for whom DCF is being calculated.

        Returns:
            numpy.ndarray: An array containing DCF values for ingestion exposure specific to each radionuclide in the
            `rads_list`. For H-3, it contains an array with two DCF values for HTO and OBT forms.

        Raises:
            ValueError: If the age of the recipient is not a valid number.
        """
        xls = pd.ExcelFile(master_file)
        name = pd.read_excel(xls, sheet_name)
        name.dropna(axis=0, how='all', inplace=True)
        dcfs = []
        for rad in self.rads_list:
            if rad != 'H-3':
                search_string = '|'.join([rad])
                df = name[name['Nuclide'] == search_string]
                if age > 17:
                    dcf = df['e_g_age_g_gt_17a_Sv/Bq'].max()
                elif 12 < age <= 17:
                    dcf = df['e_g_age_g_12_17a_Sv/Bq'].max()
                elif 7 < age <= 12:
                    dcf = df['e_g_age_g_7_12a_Sv/Bq'].max()
                elif 2 < age <= 7:
                    dcf = df['e_g_age_g_2_7a_Sv/Bq'].max()
                elif 1 < age <= 2:
                    dcf = df['e_g_age_g_1_2a_Sv/Bq'].max()
                elif age <= 1:
                    dcf = df['e_g_age_g_lt_1a_Sv/Bq'].max()
                else:
                    raise ValueError('The age of recipient must be a number.')
                dcfs.append(dcf)
            else:
                dcfs_tritium = []
                for _ in ['HTO', 'OBT']:
                    search_string = '|'.join([_])
                    df = name[name['Nuclide'] == search_string]
                    if age > 17:
                        dcf = df['e_g_age_g_gt_17a_Sv/Bq'].max()
                    elif 12 < age <= 17:
                        dcf = df['e_g_age_g_12_17a_Sv/Bq'].max()
                    elif 7 < age <= 12:
                        dcf = df['e_g_age_g_7_12a_Sv/Bq'].max()
                    elif 2 < age <= 7:
                        dcf = df['e_g_age_g_2_7a_Sv/Bq'].max()
                    elif 1 < age <= 2:
                        dcf = df['e_g_age_g_1_2a_Sv/Bq'].max()
                    elif age <= 1:
                        dcf = df['e_g_age_g_lt_1a_Sv/Bq'].max()
                    else:
                        raise ValueError('The age of recipient must be a number.')
                    dcfs_tritium.append(dcf)
                dcfs.append(dcfs_tritium)
        self.dcfs_ingestion = np.array(dcfs, dtype=object)

        return self.dcfs_ingestion

    def read_us_doe_std_1027_2018(self, rad):
        xls = pd.ExcelFile("library/doe_haz_cat_excel.xlsx")
        df_tq = pd.read_excel(xls, sheet_name='thresholds')
        df_tq.dropna(axis=0, how='all', inplace=True)
        search_string = '|'.join([str(rad)])
        df_tq = df_tq[df_tq['Radionuclide'] == search_string]
        return df_tq 
    
    def sum_of_ratio(self):
        
        if len(self.rads_list) > 1:
            sor_hc2 = 0
            sor_hc3 = 0
            text = ''
            # DOE STANDARD HAZARD CATEGORIZATION OF DOE NUCLEAR FACILITIES; 
            text += 'Following Table 1-1: THRESHOLDS FOR RADIONUCLIDES (ref. DOE-STD-1027-2018 (Jan 2019)):\n'
            for inv, rad in zip(self.inventories, self.rads_list):
                xls = pd.ExcelFile("library/doe_haz_cat_excel.xlsx")
                df_tq = pd.read_excel(xls, sheet_name='thresholds')
                df_tq.dropna(axis=0, how='all', inplace=True)
                search_string = '|'.join([str(rad)])
                df_tq = df_tq[df_tq['Radionuclide'] == search_string] 
                sor_hc2 += inv/df_tq.HC2_Curies.item()
                sor_hc3 += inv/df_tq.HC3_Curies.item()
            if sor_hc2 > 1:
                print("Based on Sum of Ratio Method The facility is categorized as HC-2")
                text += '\n'
                text += f"SOR (HC2): {sor_hc2}\n"
                text += "Based on Sum of Ratio Method The facility is categorized as HC-2"
            elif sor_hc3 > 1:
                text += '\n'
                text += f"SOR (HC2): {sor_hc2} and SOR (HC3): {sor_hc3}\n"
                print("Based on Sum of Ratio Method The facility is categorized as HC-3")
                text += "Based on Sum of Ratio Method The facility is categorized as HC-3"
            elif min(sor_hc2, sor_hc3) < 1:
                text += '\n'
                text += f"SOR (HC2): {sor_hc2} and SOR (HC3): {sor_hc3}\n"
                print("Based on Sum of Ratio Method The facility maybe categorized as BELOW HC-3")
                text += "Based on Sum of Ratio Method The facility is categorized as BELOW HC-3"

            return sor_hc2, sor_hc3, text
 
    def sum_of_ratio_hazcat(self, HC2_Curies, HC3_Curies):
        
        if len(self.rads_list) > 1:
            sor_hc2 = 0
            sor_hc3 = 0
            text = ''
            # DOE STANDARD HAZARD CATEGORIZATION OF DOE NUCLEAR FACILITIES; 
            text += '\n\nUsing HazCat Computed TQ:\n'
            for ndx, (inv, rad) in enumerate(zip(self.inventories, self.rads_list)):
                sor_hc2 += inv/HC2_Curies[ndx]
                sor_hc3 += inv/HC3_Curies[ndx]
            if sor_hc2 > 1:
                print("Based on Sum of Ratio Method The facility is categorized as HC-2.")
                text += '\n'
                text += f"SOR (HC2): {sor_hc2}\n"
                text += "Based on Sum of Ratio Method The facility is categorized as HC-2."
            elif sor_hc3 > 1:
                text += '\n'
                text += f"SOR (HC2): {sor_hc2} and SOR (HC3): {sor_hc3}\n"
                print("Based on Sum of Ratio Method The facility is categorized as HC-3.")
                text += "Based on Sum of Ratio Method The facility is categorized as HC-3."
            elif min(sor_hc2, sor_hc3) < 1:
                text += '\n'
                text += f"SOR (HC2): {sor_hc2} and SOR (HC3): {sor_hc3}\n"
                print("Based on Sum of Ratio Method The facility maybe categorized as BELOW HC-3.")
                text += "Based on Sum of Ratio Method The facility is categorized as BELOW HC-3."

            return sor_hc2, sor_hc3, text
   
        
    
    # On-site consequence analysis
    def point_source_dose(self, gamma_energy =  None,g_yield =  None, activity_curie = None,\
                               dist_list = [10, 20, 40, 50, 100, 200, 400, 600, 800, 1000], \
                               exposed_fraction=[1,1e-03, 5e-04, 1e-05], unit='mSv/hr'):

        """
        gamma_energy: in MeV unit
        """
        if gamma_energy == None:
            raise ValueError("gamma energies not found")

        if g_yield == None:
            raise ValueError("information on emission probabilities not found.")

        if dist_list == None:
            raise ValueError("distance in meter should be provided in array format.")

        if activity_curie == None:
            raise ValueError("Total acitivity of the radionuclide (in curie) is not provided.")

        if exposed_fraction == None:
            raise ValueError("Please mention the exposed fractions (for multiple scenario) of the inventory in array format")

        dose_dict = {}
        for ef in exposed_fraction:

            if unit == 'mSv/hr':
                for distance in dist_list:
                    dose = 0 
                    for ge, y in zip(gamma_energy, g_yield):
                        # unit mSv/hr
                        distance_feet = distance * 3.28084
                        dose += (1000 * (1/114) * (6 * y  * activity_curie * ge)/(distance_feet**2)) 
                        # dose += 1000 * (0.01 * 0.53 * y  * activity_curie * ge)/(distance**2) 
                    dose_after_dr_Corr = dose * ef 
                    if distance not in dose_dict:
                        dose_dict[distance] = []
                    #dose_after_dr_Corr = round(dose_after_dr_Corr, 5)
                    dose_dict[distance].append(dose_after_dr_Corr) 

            if unit == 'mR/hr':
                for distance in dist_list:
                    distance_feet = distance * 3.28084
                    dose = 0 
                    for ge, y in zip(gamma_energy, g_yield):
                        # unit mSv/hr
                        dose += (1000 * (6 * y  * activity_curie * ge)/(distance_feet**2)) 
                        # dose += 1000 * (0.53 * y  * activity_curie * ge)/(distance**2) 
                    dose_after_dr_Corr = dose * ef
                    if distance not in dose_dict:
                        dose_dict[distance] = []
                    #dose_after_dr_Corr = round(dose_after_dr_Corr, 5)
                    dose_dict[distance].append(dose_after_dr_Corr) 

        df_dose = pd.DataFrame([dose_dict])
        return dose_dict, df_dose

    def gamma_energy_abundaces(self, master_file="library/Dose_ecerman_final.xlsx",
                           sheet_name="gamma_energy_radionuclide"):

        """
        taken from following database:
        https://www-nds.iaea.org/xgamma_standards/genergies1.htm
        THE FINAL output is energies,emission_prob for selected radionuclides
        :param master_file:
        :param sheet_name:
        :return: energies, emission probability, a dictionary with energy and emission probability.
        """
        if self.rads_list == None:
            raise ValueError("radionuclide name is missing. Please provide it in array format e.g. ['Ir-192']")
        
        
        logging.getLogger("main").info("Data source of gamma energy and abundances: {weblk}".format(
            weblk="www-nds.iaea.org/xgamma_standards/genergies1.htm"))
        xls = pd.ExcelFile(master_file)
        colnames = ['nuclide', 'energy_kev', 'std_energy_kev', 'emmission_prob', 'std_emmission_prob', 'type']
        name = pd.read_excel("library/Dose_ecerman_final.xlsx",
                           sheet_name="gamma_energy_radionuclide", header=0, names= colnames)
        name.dropna(axis=0, how='all', inplace=True)
        name = name.iloc[:, :-1]
        energies = []
        emmission_prob = []
        all_dicts_lst = []
        neglected_energies = {}
        for rad in self.rads_list:
            en_dict = {}
            energies_per_rad = []
            emmission_prob_per_rad = []
            search_string = '|'.join([rad])
            df = name[name['nuclide'].str.contains(search_string, na=False)]
            if df.empty:
                emmission_prob_per_rad = [0]
                energies_per_rad = [0]
                print("gamma energy not available for {}. This either means the radionuclide is pure-beta emitter or " 
                      "the data of gamma energy not available in the current database (ref: www-nds.iaea.org/xgamma_standards/genergies1.htm)".format(rad))

                logging.getLogger("gamma energies").info("gamma energy not available for {}. This either means the radionuclide is pure-beta emitter or " 
                      "the data of gamma energy not available in the current database (ref: www-nds.iaea.org/xgamma_standards/genergies1.htm)".format(
                    rad))

            df_e = df['energy_kev'].items()
            df_p = df['emmission_prob'].items()
            for (column_e, content_e), (c, content_p) in zip(df_e, df_p):
                # neglected based on cutoff criteria (below 5 kev or abundance below 1e-03)
                if content_e / 1000 < 0.05 or content_p < 0.001:
                    # converted to MeV unit
                    neglected_energies[rad] = (content_e / 1000, content_p)
                # above 5 kev and abundance above 1e-03
                else:
                    energies_per_rad.append(content_e / 1000)
                    emmission_prob_per_rad.append(content_p)
                    en_dict[content_e / 1000] = content_p

                # converted to MeV unit
                #energies_per_rad.append(content_e / 1000)
                #emmission_prob_per_rad.append(content_p)
                #en_dict[content_e / 1000] = content_p
            all_dicts_lst.append(en_dict)
            energies.append(energies_per_rad)
            emmission_prob.append(emmission_prob_per_rad)
        return energies, emmission_prob, all_dicts_lst, neglected_energies, df

    def get_E1(self, gamma):
        ###
        # E1 = Sum of the products of the photon energies and the photon fraction or
        # intensities [MeV];
        ###
        E1s = []
        for ndx, rad in enumerate(self.rads_list):
            sum_ep = 0
            for k, v in gamma[2][ndx].items():
                sum_ep += k * v
            E1s.append(sum_ep)
        return E1s

    def get_E1_from_TableA1_ICRP_107(self):

        ###
        # ANNEX A.RADIONUCLIDES  OF THE ICRP - 07 COLLECTION
        # E1 = Sum of the products of the photon energies and the photon fraction or
        # intensities [MeV];
        # IN ALL OCCASIONS, INDIVIDUAL RADIONUCLIDE IS CONSIDERED FOR GAMMA ENERGY
        # FOR EX. Cs-137 IS CONSIDERED BUT BA-137m is not consIdired for gamma if Cs-137 IS THE RAD
        # this follows USA HAZ CAT FORMULATION
        ###
        E1s = []
        for ndx, rad in enumerate(self.rads_list):
            sum_ep = float(self.get_nuclide_info(rad)['Photon'])
            E1s.append(sum_ep)

        # print('E1s', E1s)
        return E1s
    
    def compute_threshold_quantity_HC2_in_gram_and_curie(self,
                                                         Rs, aws, half_lives,
                                                         dcfs_dicts_rads_list,
                                                         CHI_BY_Q = 1e-04):
        # NRC approach
        # HC-2: 1 rem (i.e. 10 mSv) at 100 m distance
        # Q = Quantity of material used as threshold (grams)
        # R = Release fraction for material of concern (unitless)
        # H_I = Effective dose equivalent from inhalation (rem/gm-released)
        # H_G = Effective dose equivalent from ground contamination (rem/gm-released)
        # H_CS = Effective dose equivalent from cloud shine (rem/gm-released)

        # Q = 1/(R*(H_I+H_G+H_CS))

        # DOE approach
        # TQ_HC2 = Quantity of material used as threshold (grams)
        # R = release fraction of material averaged over an entire facility (unitless)
        # SA = Specific activity of radionuclide released (Ci/gm)
        # chi_by_Q = Meteorological dispersion coefficient (1E-4 sec/m 3 ) 
        # CHI_BY_Q = 1e-04
        # DCF inhalation = Inhalation Dose Coefficient (Sv/Bq)
        # BR = Respiration rate (3.3333E-4 m 3 /sec)
        BR = 3.3333E-4
        # DC_submersion = Air Submersion Dose Coefficient (Sv/sec per Bq/m 3 )
        # AW = Atomic weight
        # t_half = halflife (in second)
        # calculate specific activity
        N_0 = 6.022E+23
        TQ_HC2s_gram = []
        TQ_HC2s_curie = []

        for ndx, rad in enumerate(self.rads_list):
            AW = aws[ndx]
            t_half = half_lives[ndx]
            DCF_inhalation = dcfs_dicts_rads_list[rad]['max_dcf_inh_hc2']
            DCF_submersion = dcfs_dicts_rads_list[rad]['max_dcf_sub_hc2']
            R = Rs[ndx]
            # unit Ci/gm; for Ir-192 ~ 9220 Ci/gm
            SA = (np.log(2) * N_0)/(AW * t_half * 3.7E+10)
            print("DCF_inhalationsss:", DCF_inhalation)
            if np.isnan(DCF_inhalation):
                print(f"WARNING: Inhalation DCF not found for {rad} during HC2 TQ calculation".format(rad))
                DCF_inhalation = 0

            # gm 
            TQ_HC2 = np.array(1/(R * SA * CHI_BY_Q * ((DCF_inhalation * BR) + DCF_submersion)))
            # unit conversion factor
            factor = (0.01/3.7e10) 
            TQ_HC2_gram = TQ_HC2 * factor
            TQ_HC2_curie = TQ_HC2_gram * SA
            TQ_HC2s_gram.append(TQ_HC2_gram)
            TQ_HC2s_curie.append(TQ_HC2_curie)
        return TQ_HC2s_curie, TQ_HC2s_gram 
    
    def compute_inhalation_threshold_quantity_HC3_in_gram_and_curie(self, Rs, aws, BVs,
                                                                    half_lives, E1s,
                                                                    dcfs_dicts_rads_list,
                                                                    r_factor_hc3 = None,
                                                                    CHI_BY_Q = 7.2e-02):
        # NRC approach
        # HC-2: 1 rem (i.e. 10 mSv) at 100 m distance
        # Q = Quantity of material used as threshold (grams)
        # R = Release fraction for material of concern (unitless)
        # H_I = Effective dose equivalent from inhalation (rem/gm-released)
        # H_G = Effective dose equivalent from ground contamination (rem/gm-released)
        # H_CS = Effective dose equivalent from cloud shine (rem/gm-released)
        # Q = 1/(R*(H_I+H_G+H_CS))
        # DOE approach
        # TQ_HC2 = Quantity of material used as threshold (grams)
        # R = release fraction of material averaged over an entire facility (unitless)
        # SA = Specific activity of radionuclide released (Ci/gm)
        # chi_by_Q = Meteorological dispersion coefficient (1E-4 sec/m 3 ) 
        # CHI_BY_Q = 1e-04
        # DCF inhalation = Inhalation Dose Coefficient (Sv/Bq)
        # BR = Respiration rate (3.3333E-4 m 3 /sec)
        BR = 3.3333E-4
        # DC_submersion = Air Submersion Dose Coefficient (Sv/sec per Bq/m 3 )
        # AW = Atomic weight
        # t_half = halflife (in second)
        N_0 = 6.022E+23
        TQ_HC3s_curie = []
        TQ_HC3s_gram = []
        dominant_pathway_text_list = []
        for ndx, rad in enumerate(self.rads_list):
            AW = np.float32(aws[ndx])
            t_half = half_lives[ndx]
            DCF_inhalation = dcfs_dicts_rads_list[rad]['max_dcf_inh_hc3']
            # DCF_submersion = sub_dcfs[ndx][0]
            DCF_ingestion = dcfs_dicts_rads_list[rad]['max_dcf_ing_hc3']
            R = Rs[ndx]
            E1 = E1s[ndx]
            # unit Ci/gm; for Ir-192 ~ 9220 Ci/gm
            SA = (np.log(2) * N_0)/(AW * t_half * 3.7E+10)
            
            #inhalation only
            # gm 
            iTQ_HC3 = np.array(10/(R * SA * CHI_BY_Q * DCF_inhalation * BR))
            # unit conversion factor
            factor = (0.01/3.7e10) 
            iTQ_HC3_gram = iTQ_HC3 * factor
            iTQ_HC3_curie = iTQ_HC3_gram * SA
                               
            # TQHC3,food = Food ingestion pathway threshold quantity [Ci];
            # DF = Dilution factor accounting for the transfer of radionuclides from air to
            # vegetation (Ci/kg of vegetables at the point of exposure per curies released
            # to the atmosphere, [kg-1 ]);
            # BV = Concentration ratio for the transfer of the element to the edible portion of a
            # crop from dry soil (dimensionless)
            B_v = BVs[ndx]
            DF = 1e-04 + (3.5e-06 * B_v)
            # FC = Food (i.e., leafy vegetable) consumption rate of reference man [0.175
            # kg/day];
            FC = 0.175 
            # CT = Contact Time (effective time over which contaminated vegetables are
            # ingested [days];
            # λI = Radionuclide decay constant [day-1 ] = ln(2)/t 1/2 ;
            # t 1/2 = Radionuclide half-life [days];
            lambda_i = (86400 * np.log(2))/t_half
            # λW = Weathering decay constant [day-1 ] = ln(2)/14 days; and
            lambda_w = np.log(2)/14
            # t_g = Growing season time [60 days]
            t_g = 60
            # unit = days               
            CT = (1-np.exp(-(lambda_i+lambda_w)*t_g))/(lambda_i+lambda_w)
            # R = Release fraction [dimensionless]; and
            # DC ingest = Ingestion dose coefficient [Sv/Bq]
            
            # Food ingestion pathway
            
            fing_TQ_HC3 = np.array(10/(DF * FC * CT * R * DCF_ingestion))
            # unit conversion factor
            factor = (0.01/3.7e10) 
            fing_TQ_HC3_curie = fing_TQ_HC3 * factor
            fing_TQ_HC3_gram = fing_TQ_HC3_curie * SA
                                       
            # water ingestion pathway
            # CT contact time: 9 days
            contact_time = 9
            ctfac = (1-np.exp(-lambda_i*contact_time))/lambda_i
            # water consumption for reference man 2 L/day
            WC = 2
            # Retardation factor (1 day)
            R_d = 1
            # DF; t_half in day
            DF = 7.6e-8 * np.exp((-4.2*86400*R_d)/t_half)
            wing_TQ_HC3 = np.array(10/(DF * ctfac * WC * DCF_ingestion))
            # unit conversion factor
            factor = (0.01/3.7e10) 
            wing_TQ_HC3_curie = wing_TQ_HC3 * factor
            wing_TQ_HC3_gram = wing_TQ_HC3_curie * SA
                                       
            ##### External Exposure #######
            # duration of exposure : 1 day
            exposure_time = 1
            expofac = (1-np.exp(-lambda_i*exposure_time))/lambda_i
            # equation coefficient
            C_gamma = 6.41e-05
            # mu_a (cm-1) = Linear energy absorption coefficient for gamma rays in air
            mu_a = 3.7e-05
            # distance from point source in metre
            S = 30
            numerator = (10*S**2* C_gamma)     
            denominator = (E1 * mu_a * 24 * expofac * np.exp(-100*mu_a *S))                    
            print('E1_:', E1, mu_a)
            direct_expo_TQ_HC3 = (numerator/denominator)
                                   
            # air exposure: submersion dose

            def get_dcf_by_nuclide(nuclide_name):
                """
                Retrieves the effective dose rate coefficient (dcf_sub) for a given nuclide.

                Args:
                nuclide_name (str): The name of the nuclide (e.g., "Ar-37").

                Returns:
                float: The dcf_sub value in Sv/sec per Bq/m^3, or None if nuclide is not found.
                """
                df = self.get_dcf_sub_inert_gas_same_for_worker_and_public()
                result = df[df["Nuclide"] == nuclide_name]["dcf_sub (Sv/sec per Bq/m^3)"].values
                return result[0] if len(result) > 0 else None

            def compute_submersion_TQ_HC3(rad):
                """
                Computes submersion_TQ_HC3_curie using the given DCF_submersion value.

                Parameters:
                DCF_submersion (float): The dose conversion factor for submersion.
                # unit is Sv-sec/Bq-m3

                Returns:
                float: The computed submersion_TQ_HC3_curie value.
                """

                DCF_submersion = get_dcf_by_nuclide(rad)
                CHI_BY_Q_hc3 = 7.2e-02
                factor = (0.01 / 3.7e10)
                denominator_sub = CHI_BY_Q_hc3 * float(DCF_submersion)
                submersion_TQ_HC3_curie = (10 / denominator_sub) * factor

                return submersion_TQ_HC3_curie

            # CONSOLIDATED list from ICRP 103, TABLE ANNEX C, AND JAERI-DATA/CODE-2002-013 TABLE 8
            inert_gas_lists = ['Ar-37', 'Ar-39', 'Ar-41', 'Kr-74', 'Kr-76', 'Kr-77', 'Kr-79',
                               'Kr-81', 'Kr-81m', 'Kr-83m', 'Kr-85', 'Kr-85m', 'Kr-87', 'Kr-88',
                                'Xe-120', 'Xe-121', 'Xe-122', 'Xe-123', 'Xe-125', 'Xe-127', 'Xe-129m',
                                'Xe-131m', 'Xe-133', 'Xe-133m', 'Xe-135', 'Xe-135m', 'Xe-138',
                               'N-13', 'O-14', 'O-15', 'Ar-42', 'Ar-44', 'Kr-75', 'Kr-89', 'Xe-127m',
                                'Xe-137']

            if rad in inert_gas_lists:
                submersion_TQ_HC3_curie = compute_submersion_TQ_HC3(rad)
            else:
                print(f"NOTE: The submersion dose is not computed during HC3 TQ computation "
                      f"for {rad} as it is not an inert gas".format())
                submersion_TQ_HC3_curie = np.inf
                # print(f"Computed submersion_TQ_HC3_curie: {submersion_TQ_HC3_curie}")
            '''
            # Meteorological dispersion coefficient 30 meters 
            # from ground level releas[7.2x10-2 s/m3];
            CHI_BY_Q_hc3 = 7.2e-02
            factor = (0.01 / 3.7e10)
            print('DCF_submersion:', DCF_submersion)
            denominator_sub = CHI_BY_Q_hc3 * DCF_submersion
            submersion_TQ_HC3_curie = (10/denominator_sub) * factor
            '''
                                   
            dominant_pathway_text = ''

            if np.isnan(iTQ_HC3_curie):
                iTQ_HC3_curie = np.inf
            if np.isnan(fing_TQ_HC3_curie):
                fing_TQ_HC3_curie = np.inf
            if np.isnan(wing_TQ_HC3_curie):
                wing_TQ_HC3_curie = np.inf
            if np.isnan(direct_expo_TQ_HC3):
                direct_expo_TQ_HC3 = np.inf
            if np.isnan(submersion_TQ_HC3_curie):
                submersion_TQ_HC3_curie = np.inf

            stack_all_tq_hc3_curie = [iTQ_HC3_curie, fing_TQ_HC3_curie, 
                                 wing_TQ_HC3_curie, direct_expo_TQ_HC3,
                                  submersion_TQ_HC3_curie]

            
            #if r_factor_hc3 is not None:
            #    x = r_factor_hc3[ndx]
            #    stack_all_tq_hc3_curie = [x * i if ndx != 3 else i for ndx, i in enumerate(stack_all_tq_hc3_curie)]
  
            #else:
            #    stack_all_tq_hc3_curie = stack_all_tq_hc3_curie
            
            # in gram
            stack_all_tq_hc3_in_gram = stack_all_tq_hc3_curie/SA
            pathways = ['  Inhalation', '  Food ingestion', '  Water ingestion',
                       '  Direct exposure', '  Submersion']
            # print('Dominant pathway:', pathways[np.argmin(stack_all_dose_hc3)])
            #dominant_pathway_text = 'TQ-HC3: '
            dominant_pathway_text += '\n'
            for p, s in zip(pathways, stack_all_tq_hc3_curie):
                dominant_pathway_text += '  ' + str(p) + ':' + ' ' + str(s) + ' Ci. ' 
                dominant_pathway_text += '\n'
            dominant_pathway_text += '  ' + 'Dominant Pathway (TQ HC-3):' + ' ' + str(pathways[np.argmin(stack_all_tq_hc3_curie)])
            # if np.argmin(stack_all_tq_hc3_curie) == 3:
            dominant_pathway_text_list.append(dominant_pathway_text)
            
            TQ_HC3s_curie.append(min(stack_all_tq_hc3_curie))
            TQ_HC3s_gram.append(min(stack_all_tq_hc3_in_gram))
            
        return TQ_HC3s_curie, TQ_HC3s_gram, dominant_pathway_text_list
    
    def write_hazcat_classification_and_dose(self, df_tq, inv, rad):
        """
        Writes HAZCAT classification and dose information to a file.

        Args:
          f (file): The file object to write to.
          ndx (int): Index for accessing data from lists.
          inv (float): Inventory value.
          rad (str): Radionuclide name.
        """
        # f = self.f
        
        text = ""
        short_note = ""
        def get_limiting_pathway_note(limiting_pathway):
            """
            Returns a note based on the limiting pathway code.

            Args:
              limiting_pathway (str): The limiting pathway code (e.g., "C", "E", "Inhalation-D").

            Returns:
              str: The note corresponding to the limiting pathway code.
            """
            notes = {
              'C': "NOTE: At the recommendation of the Tritium Focus Group, the HC-2 and HC-3 tritium threshold "
                  "values were provided by the Tritium Focus Group (TFG) and are not calculated using the "
                  "methodology in this Standard.",
              'E': "NOTE: The HC-3 TQ is set to be equal to the HC-2 TQ for the following nine radionuclides:"
                  " Bi-212n, Po-213, Po-214, Po-216, Po-218, Rn-215, Rn-216, Rn-217, and U-235m.",
              'Inhalation-D': "NOTE: To be used only if segmentation or the nature of the process precludes the potential for"
                  " criticality. Otherwise, the “Single-Parameter Limits for Fissile Nuclides” in Section 5 of"
                  " ANSI/ANS-8.1-2014 are evaluated consistent with Section 3.1.6 of this Standard."
                    }
            return notes.get(limiting_pathway, "")  # Return empty string if code not found

        # Write notes about specific limiting pathways (if applicable)
        if df_tq.Limiting_Pathway.item() in ['C', 'E', 'Inhalation-D']:
            text += get_limiting_pathway_note(df_tq.Limiting_Pathway.item()) + '\n'

            # f.write(get_limiting_pathway_note(df_tq.Limiting_Pathway.item()) + '\n')
            
        # haz cat 2    
        if inv > df_tq.HC2_Curies.item():
            short_note += "HAZARD CATEGORY 2"
            text += "\n"
            text += "### TQs from look-up table of DOE-STD-1027-2018 document ###"
            text += "\n"
            text += f"DOE-STD-1027-2018 TQ (HC2): {df_tq.HC2_Curies.item()} Ci \n"
            text += f"DOE-STD-1027-2018 TQ (HC3): {df_tq.HC3_Curies.item()} Ci \n"
            text += "Based on US-DOE-std-1027-2018 based precomputed values and inventory = {} curie,".format(inv)
            text += " the case with {} belong to HAZARD CATEGORY 2\n".format(rad)
            text += "\n"
            text += "Definition: Hazard Analysis shows the potential for significant on-site consequences.\n"
            text += "\n"
            text += "Interpretation: DOE nonreactor nuclear facilities with the potential for nuclear"
            text += " criticality events or DOE nuclear facility, including Category B"
            text += " reactors, with sufficient quantities of hazardous radioactive material"
            text += " and energy (i.e., greater than HC-2 TQs in Attachment 1), which"
            text += " would require on-site emergency planning activities.\n"
            text += "\n"
            #f.write("Based on US-DOE-std-1027-2018 based precomputed values and inventory = {} curie,"
            #        " the case with {} belong to HAZARD CATEGORY 2".format(inv, rad))
            #f.write('\n')
            #f.write("Definition: Hazard Analysis shows the potential for significant on-site consequences.")
            #f.write('\n')
            #f.write("Interpretation: DOE nonreactor nuclear facilities with the potential for nuclear"
            #        " criticality events or DOE nuclear facility, including Category B"
            #        " reactors, with sufficient quantities of hazardous radioactive material"
            #        " and energy (i.e., greater than HC-2 TQs in Attachment 1), which"
            #        " would require on-site emergency planning activities.") 
            #f.write('\n')
            
        # below haz cat 3    
        if inv < df_tq.HC3_Curies.item():
            short_note += "BELOW HAZARD CATEGORY 3"
            text += "\n"
            text += "### TQs from look-up table of DOE-STD-1027-2018 document ###"
            text += "\n"
            text += f"DOE-STD-1027-2018 TQ (HC2): {df_tq.HC2_Curies.item()} Ci \n"
            text += f"DOE-STD-1027-2018 TQ (HC3): {df_tq.HC3_Curies.item()} Ci \n"
            
            text += "Based on US-DOE-std-1027-2018 based precomputed values and inventory = {} curie,".format(inv)
            text += " the case with {} belong to BELOW HAZARD CATEGORY 3\n".format(rad)
            text += "\n"
            text += "Definition: A nuclear facility with radiological materials, but in quantities"
            text += " determined as part of an initial or final hazard categorization to be less"
            text += " than Hazard Category 3 thresholds"
            text += "\n"
            text += "Interpretation: nonreactor nuclear facilities with quantities of hazardous"
            text += " radioactive materials less than the HC-3 TQ values in Attachment 1."
            text += " These facilities are not required to comply with the requirements of 10"
            text += " CFR Part 830, Subpart B."
            text += "\n"
            #f.write('\n')
            #f.write("Interpretation: nonreactor nuclear facilities with quantities of hazardous"
            #        " radioactive materials less than the HC-3 TQ values in Attachment 1."
            #        " These facilities are not required to comply with the requirements of 10"
            #        " CFR Part 830, Subpart B.")

    
            #f.write("Based on US-DOE-std-1027-2018 based precomputed values and inventory = {} curie,"
            #        " the case with {} belong to BELOW HAZARD CATEGORY 3".format(inv, rad))
            #f.write('\n')
            #f.write("Definition: A nuclear facility with radiological materials, but in quantities"
            #        " determined as part of an initial or final hazard categorization to be less"
            #        " than Hazard Category 3 thresholds")
            # f.write('\n')
            # f.write("Interpretation: nonreactor nuclear facilities with quantities of hazardous"
            #        " radioactive materials less than the HC-3 TQ values in Attachment 1."
            #        " These facilities are not required to comply with the requirements of 10"
            #        " CFR Part 830, Subpart B.")

        # haz cat 3    
        if df_tq.HC2_Curies.item() > inv > df_tq.HC3_Curies.item():
            short_note += "HAZARD CATEGORY 3"
            
            text += "\n"
            text += "### TQs from look-up table of DOE-STD-1027-2018 document ###"
            text += "\n"
            text += f"DOE-STD-1027-2018 TQ (HC2): {df_tq.HC2_Curies.item()} Ci \n"
            text += f"DOE-STD-1027-2018 TQ (HC3): {df_tq.HC3_Curies.item()} Ci \n"
            text += "Based on US-DOE-std-1027-2018 based precomputed values and inventory = {} curie,".format(inv)
            text += " the case with {} belong to HAZARD CATEGORY 3\n".format(rad)
            text += "\n"
            text += "Definition: Hazard Analysis shows the potential for significant localized consequences."
            text += "\n"
            text += "Interpretation: DOE nonreactor nuclear facilities with quantities of hazardous"
            text += " radioactive materials which meet or exceed the HC-3 TQs in"
            text += " Attachment 1. (ref. US-DOE-std-1027-2018)"

            #f.write("Based on US-DOE-std-1027-2018 based precomputed values and inventory = {} curie,"
            #        " the case with {} belong to HAZARD CATEGORY 3".format(inv, rad))
            #f.write('\n')
            #f.write("Definition: Hazard Analysis shows the potential for significant localized consequences.")
            #f.write('\n')
            #f.write("Interpretation: DOE nonreactor nuclear facilities with quantities of hazardous"
            #        " radioactive materials which meet or exceed the HC-3 TQs in"
            #        " Attachment 1. (ref. US-DOE-std-1027-2018)")
        text += "\n"
        text += "NOTE: The limiting exposure pathways used for determining the HC-3 threshold value are: (1)"
        text += " inhalation, (2) ingestion of food, (3) ingestion of water, (4) direct exposure, and (5) air"
        text += " submersion"
        text += "\n"
        text += "\n"
        
        return text, short_note
    
    def inventory_based_hazard_classification(self):
        if self.inventories == None:
            raise ValueError("Please provide the radionuclide-wise inventory of the facility in array format." 
                  " For ex. if two radionuclides are being handled with inventory A curie and B curie at the facility. "
                  "Provide the inventory values of these radionuclides sequentially i.e. [A, B].")
        if self.rads_list == None:
            raise ValueError("Please provide the name of the radionuclides of the facility in array format." 
                  " For ex. if two radionuclides are being handled with inventory H-3 and Co-60 at the facility. "
                  "Provide the name of these radionuclides sequentially i.e. ['H-3', 'Co-60']")

        print("NOTE: The limiting exposure pathways used for determining the HC-3 threshold value are: (1)"
                  " inhalation, (2) ingestion of food, (3) ingestion of water, (4) direct exposure, and (5) air"
                  " submersion\n")

        return

    



