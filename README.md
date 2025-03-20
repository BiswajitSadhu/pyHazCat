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



