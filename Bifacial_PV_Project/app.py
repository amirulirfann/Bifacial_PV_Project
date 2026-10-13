import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Bifacial PV Performance Assessment",
    page_icon="☀️",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("☀️ Bifacial PV Performance Assessment")

st.write(
    "This application is developed to assess the performance "
    "of a bifacial photovoltaic (PV) system under different "
    "ground surface conditions."
)

st.divider()

# --------------------------------------------------
# GROUND SURFACE
# --------------------------------------------------

st.header("1. Ground Surface Condition")

surface = st.selectbox(
    "Select Ground Surface",
    ["Grass", "Tar", "Tarpaulin"]
)

# Default albedo values
default_albedo = {
    "Grass": 0.20,
    "Tar": 0.10,
    "Tarpaulin": 0.80
}

st.info(
    f"Selected ground surface: **{surface}**"
)

# --------------------------------------------------
# PV SYSTEM PARAMETERS
# --------------------------------------------------

st.header("2. PV System Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    rated_power = st.number_input(
        "Rated Power (W)",
        min_value=0.0,
        value=100.0,
        step=10.0
    )

with col2:
    module_efficiency = st.number_input(
        "Module Efficiency (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0
    )

with col3:
    module_area = st.number_input(
        "Module Area (m²)",
        min_value=0.01,
        value=0.50,
        step=0.05
    )

# --------------------------------------------------
# BIFACIAL PARAMETERS
# --------------------------------------------------

st.header("3. Bifacial Parameters")

col1, col2 = st.columns(2)

with col1:
    bifaciality = st.number_input(
        "Bifaciality Factor (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=5.0
    )

with col2:
    albedo = st.number_input(
        "Ground Albedo",
        min_value=0.0,
        max_value=1.0,
        value=default_albedo[surface],
        step=0.05
    )

st.caption(
    "Albedo can be adjusted based on the actual ground surface "
    "or experimental/literature data."
)

# --------------------------------------------------
# ENVIRONMENTAL DATA
# --------------------------------------------------

st.header("4. Environmental Data")

col1, col2 = st.columns(2)

with col1:
    irradiance = st.number_input(
        "Solar Irradiance (W/m²)",
        min_value=0.0,
        value=800.0,
        step=50.0
    )

with col2:
    pv_temperature = st.number_input(
        "PV Temperature (°C)",
        min_value=-20.0,
        max_value=100.0,
        value=25.0,
        step=1.0
    )

# --------------------------------------------------
# MEASURED PV DATA
# --------------------------------------------------

st.header("5. Measured PV Data")

col1, col2 = st.columns(2)

with col1:
    measured_voltage = st.number_input(
        "Measured Voltage (V)",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

with col2:
    measured_current = st.number_input(
        "Measured Current (A)",
        min_value=0.0,
        value=0.0,
        step=0.01
    )

# --------------------------------------------------
# CALCULATION
# --------------------------------------------------

if st.button("⚡ Calculate PV Performance", type="primary"):

    # Measured PV output
    pv_power = measured_voltage * measured_current

    # Front-side incident power
    incident_power = irradiance * module_area

    # Measured efficiency
    if incident_power > 0:
        measured_efficiency = (pv_power / incident_power) * 100
    else:
        measured_efficiency = 0

    # Simplified bifacial contribution
    rear_contribution = (
        irradiance
        * albedo
        * (bifaciality / 100)
    )

    # Effective irradiance estimation
    effective_irradiance = irradiance + rear_contribution

    # Estimated available PV power
    estimated_power = (
        effective_irradiance
        * module_area
        * (module_efficiency / 100)
    )

    # Bifacial gain
    if irradiance > 0:
        bifacial_gain = (
            rear_contribution / irradiance
        ) * 100
    else:
        bifacial_gain = 0

    # --------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------

    result = {
        "Ground Surface": surface,
        "Albedo": albedo,
        "Irradiance (W/m²)": irradiance,
        "PV Temperature (°C)": pv_temperature,
        "Voltage (V)": measured_voltage,
        "Current (A)": measured_current,
        "Measured Power (W)": pv_power,
        "Measured Efficiency (%)": measured_efficiency,
        "Estimated Power (W)": estimated_power,
        "Bifacial Gain (%)": bifacial_gain
    }

    st.session_state["latest_result"] = result

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    st.divider()

    st.header("6. Results")

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.metric(
            "PV Output Power",
            f"{pv_power:.2f} W"
        )

    with r2:
        st.metric(
            "PV Efficiency",
            f"{measured_efficiency:.2f}%"
        )

    with r3:
        st.metric(
            "Estimated Bifacial Gain",
            f"{bifacial_gain:.2f}%"
        )

    with r4:
        st.metric(
            "Ground Albedo",
            f"{albedo:.2f}"
        )

    # --------------------------------------------------
    # RESULT SUMMARY
    # --------------------------------------------------

    st.subheader("Performance Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.write("**Ground Surface:**", surface)
        st.write("**Solar Irradiance:**", f"{irradiance:.2f} W/m²")
        st.write("**PV Temperature:**", f"{pv_temperature:.2f} °C")
        st.write("**Measured Voltage:**", f"{measured_voltage:.2f} V")
        st.write("**Measured Current:**", f"{measured_current:.2f} A")

    with summary_col2:

        st.write("**Measured PV Power:**", f"{pv_power:.2f} W")
        st.write(
            "**Measured PV Efficiency:**",
            f"{measured_efficiency:.2f}%"
        )
        st.write(
            "**Estimated Bifacial Contribution:**",
            f"{rear_contribution:.2f} W/m²"
        )
        st.write(
            "**Estimated Effective Irradiance:**",
            f"{effective_irradiance:.2f} W/m²"
        )

# --------------------------------------------------
# COMPARISON SECTION
# --------------------------------------------------

st.divider()

st.header("7. Ground Surface Comparison")

st.write(
    "Enter measured results for each ground surface to compare "
    "the bifacial PV performance."
)

comparison_data = pd.DataFrame({
    "Ground Surface": ["Grass", "Tar", "Tarpaulin"],
    "Albedo": [0.20, 0.10, 0.80],
    "Measured Power (W)": [0.0, 0.0, 0.0],
    "Efficiency (%)": [0.0, 0.0, 0.0]
})

edited_data = st.data_editor(
    comparison_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Albedo": st.column_config.NumberColumn(
            "Albedo",
            min_value=0.0,
            max_value=1.0,
            step=0.05
        ),
        "Measured Power (W)": st.column_config.NumberColumn(
            "Measured Power (W)",
            min_value=0.0,
            step=0.1
        ),
        "Efficiency (%)": st.column_config.NumberColumn(
            "Efficiency (%)",
            min_value=0.0,
            step=0.1
        )
    }
)

# --------------------------------------------------
# GRAPH 1 - POWER COMPARISON
# --------------------------------------------------

st.subheader("PV Output Power Comparison")

power_chart = edited_data.set_index(
    "Ground Surface"
)[["Measured Power (W)"]]

st.bar_chart(power_chart)

# --------------------------------------------------
# GRAPH 2 - EFFICIENCY COMPARISON
# --------------------------------------------------

st.subheader("PV Efficiency Comparison")

efficiency_chart = edited_data.set_index(
    "Ground Surface"
)[["Efficiency (%)"]]

st.bar_chart(efficiency_chart)

# --------------------------------------------------
# GRAPH 3 - ALBEDO
# --------------------------------------------------

st.subheader("Ground Surface Albedo Comparison")

albedo_chart = edited_data.set_index(
    "Ground Surface"
)[["Albedo"]]

st.bar_chart(albedo_chart)

# --------------------------------------------------
# FINAL INTERPRETATION
# --------------------------------------------------

st.divider()

st.header("8. Performance Interpretation")

max_power_row = edited_data.loc[
    edited_data["Measured Power (W)"].idxmax()
]

max_eff_row = edited_data.loc[
    edited_data["Efficiency (%)"].idxmax()
]

st.success(
    f"Highest measured PV power: **{max_power_row['Ground Surface']}** "
    f"({max_power_row['Measured Power (W)']:.2f} W)"
)

st.info(
    f"Highest measured PV efficiency: **{max_eff_row['Ground Surface']}** "
    f"({max_eff_row['Efficiency (%)']:.2f}%)"
)

st.caption(
    "Note: Bifacial contribution is presented as an estimation based "
    "on irradiance, ground albedo and bifaciality factor. Actual rear-side "
    "irradiance should be measured when available for more accurate analysis."
)