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
```

---

## Running the GUI
### Step 1: Open Terminal
```bash
cd /path/to/pyHazCat
python xgui.py
```
This will launch the GUI.

---

## Using pyHazCat GUI

### 1️⃣ Selecting Radionuclides
- Click **"Radionuclides (select multiple)"**.
- Type & select radionuclides (e.g., `Co-60`).
- They appear in the **Selected List**.

### 2️⃣ Entering Inventory & Release Fraction
- Enter **Inventory** (in Curies).
- (Optional) Enter **Release Fractions** for HC2 & HC3.

### 3️⃣ Specify Output File
- Provide a filename (e.g., `hazcat_results.txt`).
- If left blank, the default `hazcat_out.txt` is used.

### 4️⃣ Run HazCat Computation
- Click **"Run HazCat"**.
- Results appear in the output window.

### 5️⃣ Save Results
- **Text Report:** `{output_filename}.txt`
- **CSV Report:** `hazcat_output.csv`

### 6️⃣ Load Previous Configurations
- Click **"Load Config File"**.
- Select a **JSON config file**.
- The GUI autofills data.

### 7️⃣ Remove Radionuclides
- Select radionuclides in **Selected List**.
- Click **"Remove Selected"**.

---

## Configuration File (`.json`)

**pyHazCat GUI** automatically saves & loads input data using JSON files.

### Example Config (`your_input.json`)
```json
{
    "consider_progeny": false,
    "ignore_half_life": null,
    "rads_list": ["Kr-81", "Kr-83m"],
    "inventories": [1.0, 1.0],
    "Rs_HC2": null,
    "Rs_HC3": null,
    "output_filename": "hazcat_out.txt"
}
```

### JSON Fields Explained:
| Key                | Type      | Description |
|--------------------|----------|-------------|
| `consider_progeny` | `boolean` | Consider progeny radionuclides (`true/false`). |
| `ignore_half_life` | `null/float` | Ignore radionuclides with half-lives below this value (in seconds). |
| `rads_list`        | `list[str]` | Selected radionuclides. |
| `inventories`      | `list[float]` | Inventory values (Curies). |
| `Rs_HC2`          | `list/float/null` | Release fractions for HC2. |
| `Rs_HC3`          | `list/float/null` | Release fractions for HC3. |
| `output_filename`  | `str` | Output filename. |

---

## Using Configuration Files

### 🔄 **Loading an Existing Config File**
1. Open **pyHazCat GUI**.
2. Click **"Load Config File"**.
3. Select a JSON file (e.g., `your_input.json`).
4. Click **"Run HazCat"**.

### 💾 **Creating a Config File via GUI**
1. Manually enter radionuclides & inventory in the GUI.
2. Click **"Run HazCat"**.
3. Inputs are **saved automatically** in `your_input.json`.

---

## Understanding the Output
### **Generated Files**
1. **Text Report (`hazcat_out.txt`)**  
   - Threshold Quantities (TQ) for HC2 & HC3.
   - Hazard classification.
   - Dominant pathway analysis.

2. **CSV Report (`hazcat_output.csv`)**  
   - Tabular format for easy processing.

### **Example Output**
```
Radionuclide: Co-60
  HazCat Computed TQ (HC2): 0.5 Ci
  DOE-STD-1027-2018 TQ (HC2): 0.6 Ci
  HazCat Computed TQ (HC3): 1.2 Ci
  DOE-STD-1027-2018 TQ (HC3): 1.3 Ci
  Hazard Category: HC-3
  Dominant Pathway: Inhalation
```

---

## Troubleshooting

### ❌ **GUI does not open**
✅ Install Tkinter:
```bash
sudo dnf install python3-tkinter
```
✅ Run with:
```bash
python3 xgui.py
```

### ❌ **Output file not generated**
✅ Check permissions or specify output:
```bash
python3 xgui.py --output hazcat_out.txt
```

---

## Summary
- **pyHazCat GUI** simplifies hazard categorization.
- Users can **manually enter** radionuclides or **load a config file**.
- Results are **automatically saved** in text & CSV formats.
- **JSON config files allow easy reuse of inputs**.
- GUI is **interactive & user-friendly**.

---

## Next Steps 🚀
Want additional features? Open an **issue** or contribute to the repo! 🎯

