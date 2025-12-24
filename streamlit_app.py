"""
MIT License

Copyright (c) 2024
Bhabha Atomic Research Centre (BARC), Mumbai, India

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

------------------------------------------------------------------------------

Developer:
Dr. Biswajit Sadhu
RS & ESS, HPD, HS & EG
Bhabha Atomic Research Centre (BARC), Mumbai
"""

# ============================================================
# Imports
# ============================================================
import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hazcat_class import HAZCAT
import base64
import os
import re
import numpy as np
import time
import random

def professional_funny_spinner():
    messages = [
        "Initializing deterministic hazard reasoning…",
        "Consulting DOE-STD-1027-2018 (again)…",
        "Persuading radionuclides to reveal their thresholds…",
        "Computing dose pathways with regulatory seriousness…",
        "Applying physics, not vibes…",
        "Almost there — no shortcuts taken.",
    ]
    return random.choice(messages)


def parse_hc3_pathways(pathway_text):
    """
    Parse HC-3 pathway string into structured values.
    Returns a dict with pathway values and dominant pathway.
    """

    pathways = {
        "Inhalation (Ci)": "-",
        "Food ingestion (Ci)": "-",
        "Water ingestion (Ci)": "-",
        "Direct exposure (Ci)": "-",
        "Submersion (Ci)": "-",
        "Dominant Pathway": "-"
    }

    if not pathway_text or not isinstance(pathway_text, str):
        return pathways

    # Extract numeric pathway values
    matches = re.findall(
        r"(Inhalation|Food ingestion|Water ingestion|Direct exposure|Submersion):\s*(inf|[\d.eE+-]+)",
        pathway_text
    )

    for key, value in matches:
        if value.lower() == "inf":
            pathways[f"{key} (Ci)"] = "-"
        else:
            pathways[f"{key} (Ci)"] = f"{float(value):.4e}"

    # Extract dominant pathway
    dom_match = re.search(r"Dominant Pathway.*?:\s*(\w+)", pathway_text)
    if dom_match:
        pathways["Dominant Pathway"] = dom_match.group(1)

    return pathways

# ============================================================
# MUST be first Streamlit call
# ============================================================
st.set_page_config(page_title="HazCat v1.0", layout="wide")

# ============================================================
# Background + Sidebar Styling
# ============================================================
def set_background(image_path="./back_pyhazcat.png", opacity=0.5):
    if not os.path.exists(image_path):
        return
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(
                rgba(0,0,0,{1-opacity}),
                rgba(0,0,0,{1-opacity})
            ),
            url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        .stApp * {{
            color: white;
            text-shadow: 1px 1px 2px black;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def set_sidebar_style(opacity=0.7):
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-color: rgba(0,0,0,{1-opacity});
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()
set_sidebar_style()

if os.path.exists("./back_pyhazcat.png"):
    st.sidebar.image("./back_pyhazcat.png", width=250)
    st.sidebar.markdown(
        "<p style='text-align:center;font-size:0.8rem;'>HazCat – BARC</p>",
        unsafe_allow_html=True
    )

st.markdown(
    """
    <style>
    /* Top horizontal header bar */
    header[data-testid="stHeader"] {
        background: linear-gradient(
            90deg,
            #1e3c72,
            #2a5298
        ) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }

    /* Ensure header text/icons stay visible */
    header[data-testid="stHeader"] * {
        color: white !important;
        text-shadow: 1px 1px 2px black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# Header
# ============================================================
st.markdown(
    "## pyHazCat v1.0 — Hazard Categorization Software for Nuclear Facilities",
    unsafe_allow_html=True
)
st.caption(
    "Developed at RS & ESS, Health Physics Division, Bhabha Atomic Research Centre (BARC), Mumbai"
)

#st.caption("Bhabha Atomic Research Centre, Mumbai")

# ============================================================
# Load Radionuclides
# ============================================================
@st.cache_data
def load_radionuclides():
    xls = pd.ExcelFile("library/doe_haz_cat_excel.xlsx")
    df = pd.read_excel(xls, sheet_name="thresholds")
    return sorted(df["Radionuclide"].dropna().tolist())

radionuclide_list = load_radionuclides()

# ============================================================
# Sidebar: Config Upload
# ============================================================
st.sidebar.header("Configuration")
uploaded_json = st.sidebar.file_uploader("Upload HazCat Input JSON", type=["json"])

loaded_config = None
if uploaded_json:
    loaded_config = json.load(uploaded_json)
    st.sidebar.success("Configuration loaded")

# ============================================================
# Radionuclide Selection
# ============================================================
selected_rads = st.multiselect(
    "Select Radionuclides",
    radionuclide_list,
    default=loaded_config["rads_list"] if loaded_config else []
)

if not selected_rads:
    st.warning("Select at least one radionuclide.")
    st.stop()

# ============================================================
# TABULAR INPUT (KEY CHANGE)
# ============================================================
st.subheader("Inventories and Release Fractions (Tabular Input)")

table_rows = []
for i, rad in enumerate(selected_rads):
    table_rows.append({
        "Radionuclide": rad,
        "Inventory (Ci)": float(loaded_config["inventories"][i]) if loaded_config else 0.0,
        "RF HC-2": float(loaded_config["Rs_HC2"][i]) if loaded_config and loaded_config.get("Rs_HC2") else np.nan,
        "RF HC-3": float(loaded_config["Rs_HC3"][i]) if loaded_config and loaded_config.get("Rs_HC3") else np.nan,
    })

df_input = pd.DataFrame(table_rows)

edited_df = st.data_editor(
    df_input,
    num_rows="fixed",
    height=400
)

# Convert table back to HazCat dictionaries
inventories = dict(zip(edited_df["Radionuclide"], edited_df["Inventory (Ci)"]))

rf_hc2 = {
    row["Radionuclide"]: row["RF HC-2"]
    if pd.notna(row["RF HC-2"]) and row["RF HC-2"] > 0
    else None
    for _, row in edited_df.iterrows()
}

rf_hc3 = {
    row["Radionuclide"]: row["RF HC-3"]
    if pd.notna(row["RF HC-3"]) and row["RF HC-3"] > 0
    else None
    for _, row in edited_df.iterrows()
}

# ============================================================
# Output Filename
# ============================================================
output_filename = st.text_input(
    "Output file name",
    value=loaded_config.get("output_filename", "hazcat_out.txt")
    if loaded_config else "hazcat_out.txt"
)

# ============================================================
# Legacy Detailed Display Builder
# ============================================================
def build_detailed_display(rads, tq2, tq3, dominant, hazcat):
    lines = []
    lines.append("HazCat – Detailed Hazard Categorization Report")
    lines.append("=" * 60)

    doe_hc2, doe_hc3, doe_path = [], [], []

    for rad in rads:
        df = hazcat.read_us_doe_std_1027_2018(rad)
        doe_hc2.append(df.HC2_Curies.item())
        doe_hc3.append(df.HC3_Curies.item())
        doe_path.append(df.Limiting_Pathway.item())

    for i, rad in enumerate(rads):
        lines.append(f"\nRadionuclide: {rad}")
        lines.append(f"  HazCat TQ HC-2 : {tq2[i]:.3e} Ci")
        lines.append(f"  DOE    TQ HC-2 : {doe_hc2[i]:.3e} Ci")
        lines.append(f"  HazCat TQ HC-3 : {tq3[i]:.3e} Ci")
        lines.append(f"  DOE    TQ HC-3 : {doe_hc3[i]:.3e} Ci")
        lines.append(f"  Dominant Pathway (HazCat): {dominant[i]}")
        lines.append(f"  Dominant Pathway (DOE):    {doe_path[i]}")
        lines.append("-" * 50)

    if len(rads) > 1:
        _, _, sortext = hazcat.sum_of_ratio()
        _, _, sortext_hz = hazcat.sum_of_ratio_hazcat(tq2, tq3)
        lines.append("\nSum of Ratios:")
        lines.append(sortext.strip())
        lines.append(sortext_hz.strip())

    return "\n".join(lines)

# ============================================================
# Run HazCat
# ============================================================
if st.button("Run HazCat", type="primary"):

    with st.spinner(professional_funny_spinner()):
        # Optional: small delay so the message is actually visible
        time.sleep(0.5)

        user_config = {
            "consider_progeny": False,
            "ignore_half_life": None,
            "rads_list": list(edited_df["Radionuclide"]),
            "inventories": list(edited_df["Inventory (Ci)"]),
            "Rs_HC2": list(rf_hc2.values()),
            "Rs_HC3": list(rf_hc3.values()),
            "output_filename": output_filename
        }

        hazcat = HAZCAT(user_config)

        tq_hc2, _ = hazcat.compute_threshold_quantity_HC2_in_gram_and_curie(
            hazcat.get_R_HC2(),
            hazcat.find_aws(),
            hazcat.halflives_lambda_rads_from_rads_list()[0],
            hazcat.get_dcfs_for_radionuclides()
        )

        tq_hc3, _, dominant = hazcat.compute_inhalation_threshold_quantity_HC3_in_gram_and_curie(
            hazcat.get_R_HC3(),
            hazcat.find_aws(),
            hazcat.get_bv(),
            hazcat.halflives_lambda_rads_from_rads_list()[0],
            hazcat.get_E1_from_TableA1_ICRP_107(),
            hazcat.get_dcfs_for_radionuclides()
        )


    # ========================================================
    # Visualization
    # ========================================================
    st.subheader("Threshold Quantity Comparison")

    col1, col2 = st.columns(2)

    # ---------------- HC-2 Plot ----------------
    with col1:
        st.markdown("### HC-2 Threshold Quantities")

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.bar(
            edited_df["Radionuclide"],
            tq_hc2,
        )
        ax2.set_ylabel("TQ HC-2 (Ci)")
        ax2.set_yscale("log")  # HC-2 almost always spans orders of magnitude
        ax2.set_xticklabels(
            edited_df["Radionuclide"],
            rotation=45,
            ha="right"
        )
        ax2.grid(axis="y", linestyle="--", alpha=0.4)

        st.pyplot(fig2)

    # ---------------- HC-3 Plot ----------------
    with col2:
        st.markdown("### HC-3 Threshold Quantities")

        fig3, ax3 = plt.subplots(figsize=(6, 4))
        ax3.bar(
            edited_df["Radionuclide"],
            tq_hc3,
        )
        ax3.set_ylabel("TQ HC-3 (Ci)")
        ax3.set_yscale("log")
        ax3.set_xticklabels(
            edited_df["Radionuclide"],
            rotation=45,
            ha="right"
        )
        ax3.grid(axis="y", linestyle="--", alpha=0.4)

        st.pyplot(fig3)

    # ========================================================
    # Results Table
    # ========================================================
    # ========================================================
    # Structured HC-3 Pathway Table
    # ========================================================

    rows = []

    for i, rad in enumerate(edited_df["Radionuclide"]):
        parsed = parse_hc3_pathways(dominant[i])

        row = {
            "Radionuclide": rad,
            "TQ HC-2 (Ci)": f"{tq_hc2[i]:.4e}",
            "TQ HC-3 (Ci)": f"{tq_hc3[i]:.4e}",
            **parsed
        }
        rows.append(row)

    df_results = pd.DataFrame(rows)

    st.subheader("Hazard Categorization Results (Structured Pathways)")
    st.dataframe(df_results, use_container_width=True)

    # df_results = pd.DataFrame({
    #     "Radionuclide": edited_df["Radionuclide"],
    #     "TQ HC-2 (Ci)": tq_hc2,
    #     "TQ HC-3 (Ci)": tq_hc3,
    #     "Dominant Pathway": dominant
    # })
    # 
    # st.dataframe(df_results)

    # ========================================================
    # Legacy Detailed Display
    # ========================================================
    detailed = build_detailed_display(
        list(edited_df["Radionuclide"]),
        tq_hc2,
        tq_hc3,
        dominant,
        hazcat
    )

    with st.expander("Detailed Report (Legacy HazCat Display)"):
        st.text_area("", detailed, height=450)

    st.success("HazCat calculation completed successfully.")

    # ========================================================
    # Downloads
    # ========================================================
    st.download_button(
        "Download CSV",
        df_results.to_csv(index=False),
        file_name="hazcat_output.csv"
    )

    st.download_button(
        "Download Input JSON",
        json.dumps(user_config, indent=4),
        file_name="hazcat_input.json"
    )

# ============================================================
# Footer
# ============================================================
# ============================================================
# Footer (MIT License – Streamlit-safe)
# ============================================================
st.markdown(
    """
    <style>
    .hazcat-footer {
        color: white;
        text-align: center;
        font-size: 0.9rem;
        padding: 14px 10px;
        margin-top: 30px;
        background: rgba(0, 0, 0, 0.60);
        border-radius: 8px;
        text-shadow: 1px 1px 2px black;
    }

    .hazcat-footer a {
        color: #aadfff;
        text-decoration: none;
    }

    .hazcat-footer a:hover {
        text-decoration: underline;
    }

    .hazcat-license {
        display: block;
        font-size: 0.75rem;
        margin-top: 6px;
        opacity: 0.85;
    }
    </style>

    <div class="hazcat-footer">
        <hr style="border: 0.5px solid rgba(255,255,255,0.4);">
        <b>Developed by Dr. Biswajit Sadhu</b><br>
        RS & ESS, HPD, HS & EG<br>
        Bhabha Atomic Research Centre (BARC)<br>
        Email: <a href="mailto:bsadhu@barc.gov.in">bsadhu@barc.gov.in</a>
        <span class="hazcat-license">
            © 2025 Bhabha Atomic Research Centre (BARC). Released under the <b>MIT License</b>.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)



