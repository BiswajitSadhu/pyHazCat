# pyHazCat GUI - Hazard Categorization Tool

## Introduction
**pyHazCat** is a graphical user interface (GUI) tool for **hazard categorization (HazCat)** of radionuclides. It enables users to:
- ✅ Select radionuclides for analysis.
- ✅ Specify inventory values and release fractions.
- ✅ Compute threshold quantities (TQ) for HC2 & HC3.
- ✅ Automatically generate reports in text and CSV formats.
- ✅ Save and load configurations using JSON files.

---

## Prerequisites

### System Requirements
- **OS:** Fedora (or any Linux distro with Python)
- **Python Version:** 3.x (Recommended: Python 3.8+)
- **Required Packages:**  
  - `tkinter` (for GUI)  
  - `numpy` (for numerical calculations)  
  - `pandas` (for data handling)  
  - `json` (for config file storage)  

### Installation
Run the following commands:
```bash
sudo dnf install python3-tkinter
pip install numpy pandas

---
### Running the GUI
Step 1: Open Terminal

'''bash
cd /path/to/pyHazCat
python xgui.py

### USING pyHazCat GUI

1️⃣ Selecting Radionuclides
Click "Radionuclides (select multiple)".
Type & select radionuclides (e.g., Co-60).
They appear in the Selected List.
2️⃣ Entering Inventory & Release Fraction
Enter Inventory (in Curies).
(Optional) Enter Release Fractions for HC2 & HC3.
3️⃣ Specify Output File
Provide a filename (e.g., hazcat_results.txt).
If left blank, the default hazcat_out.txt is used.
4️⃣ Run HazCat Computation
Click "Run HazCat".
Results appear in the output window.
5️⃣ Save Results
Text Report: {output_filename}.txt
CSV Report: hazcat_output.csv
6️⃣ Load Previous Configurations
Click "Load Config File".
Select a JSON config file.
The GUI autofills data.
7️⃣ Remove Radionuclides
Select radionuclides in Selected List.
Click "Remove Selected".

