# pyHazCat GUI – Hazard Categorization Tool

## Introduction

**pyHazCat** is a graphical user interface (GUI)–based tool for **Hazard Categorization (HazCat)** of radionuclides, developed for applications in **nuclear and radiological facilities**.  
It implements hazard screening and categorization consistent with **DOE-STD-1027-2018–style methodologies**, with extensions and refinements implemented in the pyHazCat framework.

pyHazCat supports **two interchangeable GUI frontends**:

- 🖥️ **Tkinter-based Desktop GUI** (offline, lightweight)
- 🌐 **Streamlit-based Web GUI** (modern, scalable, browser-based)

Both interfaces use the **same computational backend**, ensuring identical results and full traceability.

---

## Key Features

- Selection of single or multiple radionuclides  
- Inventory specification and optional release fractions  
- Computation of **Threshold Quantities (TQ)** for **HC-2** and **HC-3**  
- Pathway-wise HC-3 breakdown  
  (Inhalation, Food ingestion, Water ingestion, Direct exposure, Submersion)  
- Automatic identification of **dominant pathway**  
- Sum-of-Ratio (SOR) evaluation for multi-radionuclide inventories  
- Structured output tables (CSV) and detailed text reports  
- Save / load configurations using **JSON**  
- Publication- and regulatory-ready outputs  

---

## GUI Options

### 1. Tkinter-based GUI (Desktop)

**Recommended for**
- Offline systems  
- Minimal dependencies  
- Legacy environments  

**Characteristics**
- Desktop application  
- Lightweight  
- Form-based inputs  
- Scrollable, text-style detailed output  

---

### 2. Streamlit-based GUI (Web)

**Recommended for**
- Large radionuclide inventories (20–50+)  
- VM / HPC / AnuNet deployment  
- Browser-based and collaborative workflows  

**Characteristics**
- Web-based interface (local or server-hosted)  
- **Tabular / row-wise input** using `st.data_editor`  
- Scales cleanly to large inventories  
- Side-by-side HC-2 / HC-3 plots  
- Structured pathway tables  
- Modern UI with background theming and branding  

---

## Prerequisites

### System Requirements
- **OS:** Linux (Fedora / Ubuntu recommended)
- **Python Version:**  
  - Tkinter GUI: Python ≥ 3.7  
  - Streamlit GUI: Python ≥ 3.8 recommended  

---

## Installation

### Common Backend Dependencies

```bash
sudo dnf install python3-tkinter
pip install numpy pandas matplotlib streamlit

'''bash
cd /path/to/pyHazCat
python xgui.py

'''bash
cd /path/to/pyHazCat
streamlit run streamlit_app.py




