#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from hazcat_class import *
from tkinter import ttk
from tkinter import *


# Copyright and Acknowledgment
COPYRIGHT = "Copyright (c) 2024 Bhabha Atomic Research Centre, Mumbai, India"
ACKNOWLEDGMENT = "This code is developed by Dr. Biswajit Sadhu, RS & ESS, HPD and supervised by Dr. S. Anand, Head, RS & ESS, HPD."

# Custom AutocompleteCombobox class
class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self._handle_keyrelease)
        self['values'] = self._completion_list

    def _autocomplete(self, delta=0):
        if delta:
            self.delete(self.position, tk.END)
        else:
            self.position = len(self.get())

        _hits = [item for item in self._completion_list if item.lower().startswith(self.get().lower())]

        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits

        if _hits:
            self._hit_index = (self._hit_index + delta) % len(_hits)
            self.delete(0, tk.END)
            self.insert(0, _hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def _handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down'):
            if event.keysym == 'BackSpace':
                self.delete(self.index(tk.INSERT), tk.END)
                self.position = self.index(tk.END)
            return
        if event.keysym == 'Return':
            self._autocomplete()
        else:
            self._autocomplete()
            
            
def get_float_list(RF_HC2_list_text):
    """Retrieves text from Text widget, validates and converts to float list."""
    text = RF_HC2_list_text.get("1.0", "end-1c").strip()
    float_list = []
    for item in text.splitlines():  # Split by newlines for multi-line input
        try:
            float_list.append(float(item))
        except ValueError:
            pass  # Ignore invalid elements
    return float_list

def print_hazcat_output(rads_list, half_lives, inh_dcfs_public_hc2, inh_dcfs_worker_hc3, sub_dcfs, dcfs_ingestion, aws, Rs_HC2, 
                        Rs_HC3, BVs, E1s, tq_hc2s, TQ_HC2s_gram,
                                                  tq_hc3, TQ_HC3s_gram, dominant_pathway_text_list_hc3):
    """
    Calculates and displays radioisotope-specific output for all entries.

    Args:
      rads_list (list): List of radioisotope names (strings).
      half_lives (list): List of corresponding half-life values (numbers).
      inh_dcfs (list): List of inhalation dose conversion factors (numbers).
      sub_dcfs (list): List of submersion dose conversion factors (numbers).
      dcfs_ingestion (list): List of ingestion dose conversion factors (numbers).
      aws (list): List of airborne release fractions (numbers).
      Rs (list): List of release fractions (numbers).
      BVs (list): List of breathing volumes (numbers).
      E1s (list): List of gamma energy per disintegration values (numbers).
      tq_hc2s (list): List of threshold quantities for HC2 (numbers).
      tq_hc3 (list): List of threshold quantities for HC3 (numbers).

    Raises:
      ValueError: If the lengths of any lists don't match.
    """
    output_text = ""
    print('half_lives::::', half_lives)
    for i in range(len(rads_list)):
        isotope = rads_list[i]
        output_text += f"Radionuclide: {isotope}\n"
        output_text += f"  Half life (second): {half_lives[i]}\n"
        output_text += f"  Inhalation dose conversion factor (Public) (Sv/Bq): {inh_dcfs_public_hc2[i]}\n"
        output_text += f"  Inhalation dose conversion factor (Worker) (Sv/Bq): {inh_dcfs_worker_hc3[i]}\n"
        output_text += f"  Air Submersion Dose Coefficient (Sv/sec per Bq/m3) (progeny ignored DCFs are in bracket): {sub_dcfs[i]}\n"
        output_text += f"  Ingestion dose coefficient [Sv/Bq]: {dcfs_ingestion[i]}\n"     
        output_text += f"  Atomic Weight: {aws[i]}\n"
        output_text += f"  Release fraction for computing Threshold for HC2: {Rs_HC2[i]}\n"
        output_text += f"  Release fraction for computing Threshold for HC3: {Rs_HC3[i]}\n"
        output_text += f"  Soil to Plant Concentration Factor: {BVs[i]}\n"
        output_text += f"  Sum of the products of the photon energies and the photon fraction or intensities [MeV]: {E1s[i]}\n"
        output_text += f"  Threshold quantity for HC2 (Curie): {tq_hc2s[i]}\n"
        output_text += f"  Threshold quantity for HC2 (Gram): {TQ_HC2s_gram[i]}\n"
        output_text += f"  Threshold quantity across all pathways for HC3 (Curie): {dominant_pathway_text_list_hc3[i]}\n"
        output_text += f"  Threshold quantity for HC3 (Curie): {tq_hc3[i]}\n"
        output_text += f"  Threshold quantity for HC3 (Gram): {TQ_HC3s_gram[i]}\n\n"

    print(output_text)  # Or display the output text using your preferred method
    return output_text


def display_results(window, rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies, sortext=None, sortext_hz = None):
    """
    Displays TQ (HC2) and TQ (HC3) information using Tkinter widgets.

    Args:
      window (tk.Tk): The main application window.
      rads_list (list): List of radionuclide names.
      tq_hc2s (list): List of TQ (HC2) values in Curies.
      tq_hc3s (list): List of TQ (HC3) values in Curies.
      short_notes (list): List of results on HC classification.
    """

    output_label = ttk.Label(window, text="Results")
    output_label.grid(row=6, columnspan=len(rads_list))  # Position the label

    # Combine text for both HC2 and HC3 in a single loop
    combined_text = ""
    for rad, hc2, hc3, sn, doehc2, doehc3 in zip(rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies):
        combined_text += f"Radionuclide: {rad}\n"
        combined_text += f"  HazCat Computed TQ (HC2): {hc2:.1f} Ci\n"
        combined_text += f"  DOE-STD-1027-2018 TQ (HC2): {doehc2} Ci\n"
        combined_text += f"  HazCat Computed TQ (HC3): {hc3:.1f} Ci\n"
        combined_text += f"  DOE-STD-1027-2018 TQ (HC3): {doehc3} Ci\n"
        combined_text += f"  Hazard Category: {sn} \n\n"
    if sortext:
        combined_text += f"  SOR (DOE-STD-1027-2018):{sortext} \n\n"
        combined_text += f"  SOR (HazCat):{sortext_hz} \n\n"

    output_label.config(text=combined_text)  # Update label with combined text

import tkinter as tk
from tkinter import ttk
from tkinter import font  # Import the font module

def display_results_with_scrollbar(window, rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies, sortext=None, sortext_hz=None):
    """
    Displays TQ (HC2) and TQ (HC3) information using Tkinter widgets with a scrollbar.

    Args:
        window (tk.Tk): The main application window.
        rads_list (list): List of radionuclide names.
        tq_hc2s (list): List of TQ (HC2) values in Curies.
        tq_hc3s (list): List of TQ (HC3) values in Curies.
        short_notes (list): List of results on HC classification.
        doe_tqhc2_curies (list): List of DOE TQ (HC2) values in Curies.
        doe_tqhc3_curies (list): List of DOE TQ (HC3) values in Curies.
        sortext (str): Optional; String of SOR for DOE-STD-1027-2018.
        sortext_hz (str): Optional; String of SOR for HazCat.
    """

    # Label for the output
    output_label = ttk.Label(window, text="Results:")
    output_label.grid(row=6, column=0, padx=5, pady=5, sticky='w')

    # Create a frame for the text widget and scrollbar
    frame = ttk.Frame(window)
    frame.grid(row=7, column=0, columnspan=6, padx=5, pady=5, sticky='nsew')

    # Configure the grid row and column to make the text widget expandable
    window.grid_rowconfigure(7, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Create a custom font with size 16
    custom_font = font.Font(family="Comic Sans MS", size=16)

    # Create a text widget for displaying the results
    text_widget = tk.Text(frame, wrap='word', width=80, height=20, font=custom_font)
    text_widget.grid(row=0, column=0, sticky='nsew')

    # Create a scrollbar for the text widget
    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text_widget.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    text_widget['yscrollcommand'] = scrollbar.set

    # Configure the frame to expand with the window
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Combine text for both HC2 and HC3 in a single loop
    combined_text = ""
    for rad, hc2, hc3, sn, doehc2, doehc3 in zip(rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies):
        combined_text += f"Radionuclide: {rad}\n"
        combined_text += f"  HazCat Computed TQ (HC2): {hc2:.1f} Ci\n"
        combined_text += f"  DOE-STD-1027-2018 TQ (HC2): {doehc2} Ci\n"
        combined_text += f"  HazCat Computed TQ (HC3): {hc3:.1f} Ci\n"
        combined_text += f"  DOE-STD-1027-2018 TQ (HC3): {doehc3} Ci\n"
        combined_text += f"  Hazard Category: {sn} \n\n"
    if sortext:
        combined_text += f"  SOR (DOE-STD-1027-2018): {sortext} \n\n"
        combined_text += f"  SOR (HazCat): {sortext_hz} \n\n"

    # Insert combined text into the text widget
    text_widget.insert(tk.END, combined_text)
    text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

'''
def display_results_with_scrollbar(window, rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies, sortext=None, sortext_hz=None):
    """
    Displays TQ (HC2) and TQ (HC3) information using Tkinter widgets with a scrollbar.

    Args:
        window (tk.Tk): The main application window.
        rads_list (list): List of radionuclide names.
        tq_hc2s (list): List of TQ (HC2) values in Curies.
        tq_hc3s (list): List of TQ (HC3) values in Curies.
        short_notes (list): List of results on HC classification.
        doe_tqhc2_curies (list): List of DOE TQ (HC2) values in Curies.
        doe_tqhc3_curies (list): List of DOE TQ (HC3) values in Curies.
        sortext (str): Optional; String of SOR for DOE-STD-1027-2018.
        sortext_hz (str): Optional; String of SOR for HazCat.
    """

    # Label for the output
    output_label = ttk.Label(window, text="Results:")
    output_label.grid(row=6, column=0, padx=5, pady=5, sticky='w')

    # Create a frame for the text widget and scrollbar
    frame = ttk.Frame(window)
    frame.grid(row=7, column=1, columnspan=6, padx=5, pady=5, sticky='nsew')

    # Configure the grid row and column to make the text widget expandable
    window.grid_rowconfigure(7, weight=1)
    window.grid_columnconfigure(0, weight=1)
    
    # Create a custom font with size 16
    #custom_font = font.Font(family="Helvetica", size=16)

    # Create a text widget for displaying the results
    text_widget = tk.Text(frame, wrap='word', width=120, height=20)
    text_widget.grid(row=0, column=0, sticky='nsew')

    # Create a scrollbar for the text widget
    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text_widget.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    text_widget['yscrollcommand'] = scrollbar.set
    
    # Configure the frame to expand with the window
    #frame.grid_rowconfigure(0, weight=1)
    #frame.grid_columnconfigure(0, weight=1)

    # Combine text for both HC2 and HC3 in a single loop
    combined_text = ""
    for rad, hc2, hc3, sn, doehc2, doehc3 in zip(rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies):
        combined_text += f"Radionuclide: {rad}\n"
        combined_text += f"  HazCat Computed TQ (HC2): {hc2:.1f} Ci\n"
        combined_text += f"  DOE-STD-1027-2018 TQ (HC2): {doehc2} Ci\n"
        combined_text += f"  HazCat Computed TQ (HC3): {hc3:.1f} Ci\n"
        combined_text += f"  DOE-STD-1027-2018 TQ (HC3): {doehc3} Ci\n"
        combined_text += f"  Hazard Category: {sn} \n\n"
    if sortext:
        combined_text += f"  SOR (DOE-STD-1027-2018): {sortext} \n\n"
        combined_text += f"  SOR (HazCat): {sortext_hz} \n\n"

    # Insert combined text into the text widget
    text_widget.insert(tk.END, combined_text)
    text_widget.config(state=tk.DISABLED)  # Make the text widget read-only



'''
def get_RVs_for_GUI():
    user_config = get_user_input()
    print('Configuration:', user_config)
    
    rads_list = user_config['rads_list']
    inventories = user_config['inventories']
    filename = user_config['output_filename']
    
    # Integrate HAZCAT calculations
    hazcat = HAZCAT(user_config)
    Rs_HC2 = hazcat.get_R_HC2()
    Rs_HC3 = hazcat.get_R_HC3()
    return Rs_HC2, Rs_HC3

def write_hazcat_logo(f):
    
    letters = {
                'A': [' *** ', '*   *', '*****', '*   *', '*   *'],
                'B': ['**** ', '*   *', '**** ', '*   *', '**** '],
                'C': [' ****', '*    ', '*    ', '*    ', ' ****'],
                'D': ['**** ', '*   *', '*   *', '*   *', '**** '],
                'E': ['*****', '*    ', '*****', '*    ', '*****'],
                'F': ['*****', '*    ', '***  ', '*    ', '*    '],
                'G': [' ****', '*    ', '*  **', '*   *', ' ****'],
                'H': ['*   *', '*   *', '*****', '*   *', '*   *'],
                'I': ['*****', '  *  ', '  *  ', '  *  ', '*****'],
                'J': ['*****', '    *', '    *', '*   *', ' *** '],
                'K': ['*   *', '*  * ', '**   ', '*  * ', '*   *'],
                'L': ['*    ', '*    ', '*    ', '*    ', '*****'],
                'M': ['*   *', '** **', '* * *', '*   *', '*   *'],
                'N': ['*   *', '**  *', '* * *', '*  **', '*   *'],
                'O': [' *** ', '*   *', '*   *', '*   *', ' *** '],
                'P': ['**** ', '*   *', '**** ', '*    ', '*    '],
                'Q': [' *** ', '*   *', '*   *', '*  **', ' ** *'],
                'R': ['**** ', '*   *', '**** ', '*  * ', '*   *'],
                'S': [' ****', '*    ', '**** ', '    *', '**** '],
                'T': ['*****', '  *  ', '  *  ', '  *  ', '  *  '],
                'U': ['*   *', '*   *', '*   *', '*   *', ' *** '],
                'V': ['*   *', '*   *', '*   *', ' * * ', '  *  '],
                'W': ['*   *', '*   *', '* * *', '** **', '*   *'],
                'X': ['*   *', ' * * ', '  *  ', ' * * ', '*   *'],
                'Y': ['*   *', ' * * ', '  *  ', '  *  ', '  *  '],
                'Z': ['*****', '   * ', '  *  ', ' *   ', '*****'],
            }

    string = "HazCat"
    f.write('\n')
    f.write(
        '###############################################################################################################################\n')
    # f.write('\n')
    for i in range(5):
        for word in range(len(string)):
            current_word = string[word].upper()
            if word == len(string) - 1:
                print(letters[current_word][i], file=f)

            else:
                print(letters[current_word][i], end='  ', file=f)
    f.write(
        '###############################################################################################################################\n')

def calculate_hazcat():
    """Placeholder function for HAZCAT calculations. Replace with actual logic
    and display results using Tkinter widgets or other methods."""
    
    # Prepare output string
    ack_text = f"{COPYRIGHT}\n\n{ACKNOWLEDGMENT}\n\n"

    user_config = get_user_input()
    print('Configuration:', user_config) 
    
    rads_list = user_config['rads_list']
    
    inventories = user_config['inventories']
    
    filename = user_config['output_filename']
    if not filename:  # Check if the entry is empty
        filename = "hazcat_out.txt"
        
    Rs_HC2 = user_config['Rs_HC2']
    
    Rs_HC3 = user_config['Rs_HC3']
    # Integrate HAZCAT calculations
    hazcat = HAZCAT(user_config)
    # NOW USES ICRP 103 RADIONUCLIDE DATA
    half_lives = hazcat.halflives_lambda_rads_from_rads_list()[0]
    print('half_lives:', half_lives)
    # half_lives = hazcat.find_half_life_and_decay_const_radionuclides()[0]
    # half_lives = np.array(half_lives)
    inh_dcfs_public_hc2 = hazcat.inhalation_dcf_list()
    inh_dcfs_worker_hc3 = hazcat.inhalation_dcf_list_worker()
    # THIS IS FOR HC2 only (FGR 15), in HC3, submersion is only for inert gas.
    sub_dcfs = hazcat.dcf_list_ecerman_submersion_include_progeny()
    aws = hazcat.find_aws()

    if Rs_HC2 is None:
        tq_hc2_revise = False
        Rs_HC2 = hazcat.get_R_HC2()
    else:
        tq_hc2_revise = True
        Rs_HC2_ini = hazcat.get_R_HC2()
        r_factor_hc2 = np.array(Rs_HC2_ini)/np.array(Rs_HC2)
        
    if Rs_HC3 is None:
        tq_hc3_revise = False
        r_factor_hc3 = None
        Rs_HC3 = hazcat.get_R_HC3()
    else:
        tq_hc3_revise = True
        Rs_HC3_ini = hazcat.get_R_HC3()
        r_factor_hc3 = np.array(Rs_HC3_ini)/np.array(Rs_HC3)
        # print('rfactor:', np.array(Rs_HC3_ini), np.array(Rs_HC3), r_factor_hc3)

    BVs = hazcat.get_bv()
    # dcfs_ingestion = hazcat.dcf_list_ingestion()
    dcfs_ingestion = hazcat.ingestion_dcf_list_worker()
    # gamma = hazcat.gamma_energy_abundaces()
    # E1s = hazcat.get_E1(gamma)
    E1s = hazcat.get_E1_from_TableA1_ICRP_107()
    # inha_dcfs = hazcat.inhalation_dcf_list()
    
    ###### HAZCAT COMPUTED VALUES ##########################
    # print('half_lives:::', half_lives)
    
    # COMPUTE TQ-HC2 with HazCat code
    tq_hc2s, TQ_HC2s_gram = hazcat.compute_threshold_quantity_HC2_in_gram_and_curie(Rs_HC2, aws, half_lives, 
                                                                                    inh_dcfs_public_hc2, sub_dcfs)
    # COMPUTE TQ-HC3 with HazCat code
    tq_hc3, TQ_HC3s_gram, dominant_pathway_text_list_hc3 = hazcat.compute_inhalation_threshold_quantity_HC3_in_gram_and_curie(Rs_HC3, aws, 
                                                                       BVs, half_lives, 
                                                                       E1s, inh_dcfs_worker_hc3, dcfs_ingestion, r_factor_hc3 = r_factor_hc3,
                                                                       CHI_BY_Q = 7.2e-02)
    
    
    
    ######## US-DOE-TABLE BASED CLASSIFICATION ############
    with open(filename, "w") as output_file:      
        write_hazcat_logo(output_file)
        # acknowledgement
        output_file.write(ack_text)
        # table check
        short_notes = []
        doe_tqhc2_curies = []
        doe_tqhc3_curies = []
        for odx, (inv, rad) in enumerate(zip(inventories, rads_list)):
            df_tq = hazcat.read_us_doe_std_1027_2018(rad)
            doe_tqhc2_curie, doe_tqhc2_gm, doe_tqhc3_curie, doe_tqhc3_gm = df_tq.HC2_Curies.item(), df_tq.HC2_Grams.item(), df_tq.HC3_Curies.item(),  df_tq.HC3_Grams.item()  
            doe_tqhc2_curies.append(doe_tqhc2_curie)
            doe_tqhc3_curies.append(doe_tqhc3_curie)
            # Perform hazard classification based on inventory and precomputed values
            notes, short_note = hazcat.write_hazcat_classification_and_dose(df_tq, inv, rad)
            output_file.write(notes)
            short_notes.append(short_note)
        
        #######################################################
        out_all = print_hazcat_output(rads_list, half_lives, inh_dcfs_public_hc2, inh_dcfs_worker_hc3, sub_dcfs, 
                                      dcfs_ingestion, aws, Rs_HC2, Rs_HC3, BVs, E1s, tq_hc2s, TQ_HC2s_gram,
                                                  tq_hc3, TQ_HC3s_gram, dominant_pathway_text_list_hc3)
    
        output_file.write(out_all)
        # US-DOE-TABLE based Sum of Ratio output
        ## SUM OF RATIO ###
        if len(rads_list) > 1:
            sorhc2, sorhc3, sortext = hazcat.sum_of_ratio()
            print('DOE_SOR:', sorhc2, sorhc3, sortext)
            output_file.write(sortext)
            sorhc2_hz, sorhc3_hz, sortext_hz = hazcat.sum_of_ratio_hazcat(tq_hc2s, tq_hc3)
            print('HazCat_SOR:', sorhc2_hz, sorhc3_hz, sortext_hz)
            output_file.write(sortext_hz)
        print(f"Results saved to: {filename}")
    
    # Example usage (assuming window is a Tk() instance):
    
    if len(rads_list) > 1:
        display_results_with_scrollbar(window, rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies, sortext=sortext, sortext_hz = sortext_hz)
        #display_results(window, rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies, sortext=sortext, sortext_hz = sortext_hz)
    else:
        display_results_with_scrollbar(window, rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies, sortext=None, sortext_hz = None)    
        #display_results(window, rads_list, tq_hc2s, tq_hc3, short_notes, doe_tqhc2_curies, doe_tqhc3_curies, sortext=None, sortext_hz = None)    
    
# Radionuclide list
def get_rads_list_from_doe():
    xls = pd.ExcelFile("library/doe_haz_cat_excel.xlsx")
    df_tq = pd.read_excel(xls, sheet_name='thresholds')
    df_tq.dropna(axis=0, how='all', inplace=True)
    list_of_rads = df_tq['Radionuclide'].to_list()
    return list_of_rads

def get_selected_radionuclides():
    return [selected_list_box.get(i) for i in range(selected_list_box.size())]

# Function to retrieve user input
def get_user_input():
    """Retrieves user input from rads_list_text and inv_list_text, validates it, 
    and returns a dictionary with configuration data. Handles errors and displays messages."""
    
    #rads_list = get_selected_radionuclides()
    #rads_list = [rad.strip() for rad in rads_list]  # Ensure rads_list elements are strings

    inventories_dict, output_filename, rf2_dict, rf3_dict = get_inventory_inputs()
    inventories_text = list(inventories_dict.values())
    rads_list = list(inventories_dict.keys())
    
    rf_list_hc2_val =  list(rf2_dict.values())
    if list(set(rf_list_hc2_val)) == [None]:
        rf_list_hc2_val = None
    elif None in rf_list_hc2_val:
        raise ValueError("Release fraction values (for HC2) must be provided "
                         "for all chosen radionculides, if mentioned for atleast one radionuclides.")
        
    rf_list_hc3_val = list(rf3_dict.values())
    if list(set(rf_list_hc3_val)) == [None]:
        rf_list_hc3_val = None
    elif None in rf_list_hc3_val:
        raise ValueError("Release fraction values (for HC3) must be provided "
                         "for all chosen radionculides, if mentioned for atleast one radionuclides.")
        
    print('outfilename_dict:', output_filename, rf_list_hc2_val, rf_list_hc3_val)
    if inventories_text == "":
        print("Inventory list is empty. Please enter the inventory values.")
        return None
    
    print('inventories_text:', inventories_text, inv_list_text)
    
    # Check Release fraction is provided by USER or not
    if rf_list_hc2_val == ['']:
        rf_list_hc2_val = None
    else:
        # rf_list_hc2_val = np.array([float(x) for x in rf_list_hc2 if x.isdigit()])
        rf_list_hc2_val = rf_list_hc2_val
    
    if rf_list_hc3_val == ['']:
        rf_list_hc3_val = None
    else:
        # rf_list_hc3_val = np.array([float(x) for x in rf_list_hc3 if x.isdigit()])
        rf_list_hc3_val = rf_list_hc3_val
    
    inventories = []
            
    error_message = ""
            
    for inv_str in inventories_text:
        try:
            inventories.append(float(inv_str.strip()))  # Convert to float, strip spaces
        except ValueError:
            error_message = "Invalid inventory value: Please enter comma-separated numbers."
            break  # Stop processing on first error
    

    # Check if all lists have the same length
    if len(rads_list) != len(inventories):
        # Handle length mismatch (e.g., display error message)
        print("Error: Lists must have the same number of entries.")
        raise ValueError("Error: Radionuclides and inventories must have the same number of entries.")

    if error_message:
        # Display error message (replace with your preferred method)
        print(error_message)
        # Optionally, clear the entry field to encourage re-entry
        inv_list_text.delete(0, tk.END)
        return None
    else:
        # DO NOT ALLOW CONSIDER PROGENY = True as the individual radionuclide needs to be considered not its progeny
        # Create radio buttons for consider_progeny
        if consider_progeny_var.get() == 1:  # If consider progeny is selected
            #
            progeny = False
            ignore_half_life = None
            # unit: second
            # ignore_half_life = 1800
            # ignore_half_life_entry.config(state='normal')
        else:
            progeny = False
            ignore_half_life = None
        
        # Inventories successfully converted to floats
        return {'consider_progeny': progeny, 'ignore_half_life': ignore_half_life, 
                'rads_list': rads_list, 'inventories': inventories,
                'Rs_HC2': rf_list_hc2_val, 'Rs_HC3': rf_list_hc3_val,'output_filename': output_filename}


inventory_widgets = {}
filename_widgets = {}
rf2_widgets = {}
rf3_widgets = {}

def create_row(window, row_index=None, rad=None):
    """Creates the fixed Output row (if not created) and adds Inventory rows dynamically."""
    height = 1.5

    # Ensure the Output File row is always at row 0
    if "output_file" not in filename_widgets:
        f_label = ttk.Label(window, text="Output file (Optional):")
        f_label.grid(row=0, column=5, columnspan=2,padx=1, pady=1)
        f_text = tk.Text(window, width=15, height=height)
        f_text.grid(row=0, column=6, columnspan=2, padx=1, pady=1)
        filename_widgets["output_file"] = f_text  # Store reference

    # If rad is None, just return after creating the output row
    if rad is None:
        return

    # Start inventory rows from row 1
    if row_index is None:
        row_index = len(inventory_widgets) + 1  # Dynamically determine row position

    inv_list_label = ttk.Label(window, text=f"Inventory for {rad}:")
    inv_list_label.grid(row=row_index, column=0, padx=5, pady=5)
    inv_list_text = tk.Text(window, width=30, height=height)
    inv_list_text.grid(row=row_index, column=1, padx=5, pady=5)
    inventory_widgets[rad] = inv_list_text  # Store reference

    RF_HC2_list_label = ttk.Label(window, text="Release Fraction for HC-2 (Optional):")
    RF_HC2_list_label.grid(row=row_index, column=2, padx=5, pady=5)
    RF_HC2_list_text = tk.Text(window, width=30, height=height)
    RF_HC2_list_text.grid(row=row_index, column=3, padx=5, pady=5)
    rf2_widgets[rad] = RF_HC2_list_text

    RF_HC3_list_label = ttk.Label(window, text="Release Fraction for HC-3 (Optional):")
    RF_HC3_list_label.grid(row=row_index, column=4, padx=5, pady=5)
    RF_HC3_list_text = tk.Text(window, width=30, height=height)
    RF_HC3_list_text.grid(row=row_index, column=5, padx=5, pady=5)
    rf3_widgets[rad] = RF_HC3_list_text

    return inv_list_text, filename_widgets["output_file"]  # Return output text reference

'''
def create_row(window, row_index, rad):
    """Helper function to create a row for inventory and release fractions input."""
    height = 1.5
    inv_list_label = ttk.Label(window, text=f"Inventory for {rad}:")
    inv_list_label.grid(row=row_index, column=0, padx=5, pady=5)
    inv_list_text = tk.Text(window, width=30, height=height)
    inv_list_text.grid(row=row_index, column=1, padx=5, pady=5)
    
    # Store the Text widget reference in the dictionary with rad as the key
    inventory_widgets[rad] = inv_list_text

    RF_HC2_list_label = ttk.Label(window, text="Release Fraction for HC-2 (Optional):")
    RF_HC2_list_label.grid(row=row_index, column=2, padx=5, pady=5)
    RF_HC2_list_text = tk.Text(window, width=30, height=height)
    RF_HC2_list_text.grid(row=row_index, column=3, padx=5, pady=5)
    # Store the Text widget reference in the dictionary with rad as the key
    rf2_widgets[rad] = RF_HC2_list_text

    RF_HC3_list_label = ttk.Label(window, text="Release Fraction for HC-3 (Optional):")
    RF_HC3_list_label.grid(row=row_index, column=4, padx=5, pady=5)
    RF_HC3_list_text = tk.Text(window, width=30, height=height)
    RF_HC3_list_text.grid(row=row_index, column=5, padx=5, pady=5)
    # Store the Text widget reference in the dictionary with rad as the key
    rf3_widgets[rad] = RF_HC3_list_text

    output_row = row_index+1
    f_label = ttk.Label(window, text="Output file (Optional):")
    f_label.grid(row=output_row, column=0, padx=5, pady=5)
    f_text = tk.Text(window, width=30, height=height)
    f_text.grid(row=output_row, column=1, padx=5, pady=5)
    # Store the Text widget reference in the dictionary with rad as the key
    filename_widgets['output_file'] = f_text
    
    # Ensure the output row is created only once
    #if "output_file" not in filename_widgets:
    #    output_row = row_index + 1
    #    f_label = ttk.Label(window, text="Output file (Optional):")
    #    f_label.grid(row=output_row, column=0, padx=5, pady=5)
    #    f_text = tk.Text(window, width=30, height=height)
    #    f_text.grid(row=output_row, column=1, padx=5, pady=5)
    #    filename_widgets["output_file"] = f_text  # Store it to avoid re-creation
    # filename_widgets["output_file"]
    
    return inv_list_text, f_text
'''
def get_inventory_inputs():
    """Retrieve the input from all inventory Text widgets."""
    inventories = {}
    for rad, widget in inventory_widgets.items():
        inventories[rad] = widget.get("1.0", "end-1c").strip()
        
    outfilename = {}
    for filename, widget in filename_widgets.items():
        outfilename[filename] = widget.get("1.0", "end-1c").strip()
        
    rf2 = {}
    for rad, widget in rf2_widgets.items():
        if widget.get("1.0", "end-1c").strip() != '':
            rf2[rad] = float(widget.get("1.0", "end-1c").strip())
        else:
            rf2[rad] = None
    
    rf3 = {}
    for rad, widget in rf3_widgets.items():
        if widget.get("1.0", "end-1c").strip() != '':
            rf3[rad] = float(widget.get("1.0", "end-1c").strip()) 
        else:
            rf3[rad] = None
    return inventories, outfilename['output_file'], rf2, rf3
      
# Function to generate input rows dynamically based on the selected radionuclides
def generate_input_rows():
    # Clear previous rows (if any)
    for widget in window.grid_slaves():
        if int(widget.grid_info()["row"]) > 1:
            widget.grid_forget()
    selected_rads = get_selected_radionuclides()
    for i, rad in enumerate(selected_rads):
        row_index = i + 1  # Start rows from index 1
        inv_list_text = create_row(window, row_index, rad)     
    return row_index, inv_list_text

def update_selected_list(event):
    # Get the current selected value from the AutocompleteCombobox
    selected_value = rads_listbox.get()
    if selected_value and selected_value not in selected_list_box.get(0, tk.END):
        selected_list_box.insert(tk.END, selected_value)
        row_index, inv_list_text = generate_input_rows()
        run_row_index = row_index+2
        calculate_button = ttk.Button(window, text="Run HazCat", command=calculate_hazcat)
        calculate_button.grid(row=run_row_index, column=2, padx=55, pady=55)  # Specify grid location

# Function to get the output filename (consider placing this elsewhere if used globally)
def get_output_filename():
    filename = f_entry.get().strip()  # Get the text from the entry field and remove leading/trailing whitespaces
    if not filename:  # Check if the entry is empty
        filename = "hazcat_out.txt"  # Use default filename if empty
    return filename

###
window = tk.Tk()
window.title("HazCat v1.0")
style = ttk.Style(window)
style.theme_use('classic')

# Set the font size for ttk widgets
style.configure('TLabel', font=('Times', 14))  # Increase font size for TLabel
style.configure('TButton', font=('Times', 14))  # Increase font size for TButton
style.configure('TEntry', font=('Times', 14))  # Increase font size for TEntry


inv_list_text = tk.Text(window, width=30, height=3)
RF_HC2_list_text = tk.Text(window, width=30, height=3)
RF_HC3_list_text = tk.Text(window, width=30, height=3)
consider_progeny_var = tk.IntVar()

# Radionuclide selection label and AutocompleteCombobox (multiple selection)
rads_list_label = ttk.Label(window, text="Radionuclides (select multiple):")
rads_list_label.grid(row=0, column=0, padx=1, pady=1)

# AutocompleteCombobox for radionuclide selection
rads_listbox = AutocompleteCombobox(window)
radionuclide_list = get_rads_list_from_doe()
rads_listbox.set_completion_list(radionuclide_list)
rads_listbox.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# Label for the selected list display
selected_list_label = ttk.Label(window, text="Selected List:")
selected_list_label.grid(row=0, column=3, padx=1, pady=1)
# Listbox to display the selected radionuclides; len(radionuclide_list)
selected_list_box = tk.Listbox(window, selectmode=tk.MULTIPLE, height=10)
selected_list_box.grid(row=0, column=4, columnspan=2, padx=1, pady=1)

# Bind selection change event to the AutocompleteCombobox
rads_listbox.bind("<<ComboboxSelected>>", update_selected_list)

# Run the main event loop
window.mainloop()


# In[ ]:




