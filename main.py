import streamlit as st
import pandas as pd
import altair as alt

# --- Configuration ---
st.set_page_config(layout="wide", page_title="UK Offshore Wind CfD Analysis")

# --- Data Definition (based on research report tables) ---
# Table 1: Detailed CfD Allocation Round Data (Offshore Wind Projects)
# Data populated from Table 1 of the markdown analysis document.
cfd_data = [
    {"Allocation Round": "AR1", "Project Name": "Neart Na Gaoithe", "Strike Price (£/MWh, 2012 prices)": 114.39, "Capacity (MW)": 448, "Delivery Year": "2018/19", "Number of Turbines": None},
    {"Allocation Round": "AR1", "Project Name": "East Anglia ONE", "Strike Price (£/MWh, 2012 prices)": 119.89, "Capacity (MW)": 714, "Delivery Year": "2017/18", "Number of Turbines": None},
    {"Allocation Round": "AR2", "Project Name": "Triton Knoll Offshore Wind Farm", "Strike Price (£/MWh, 2012 prices)": 74.75, "Capacity (MW)": 860, "Delivery Year": "2021/22", "Number of Turbines": None},
    {"Allocation Round": "AR2", "Project Name": "Hornsea Project 2", "Strike Price (£/MWh, 2012 prices)": 57.50, "Capacity (MW)": 1386, "Delivery Year": "2022/23", "Number of Turbines": None},
    {"Allocation Round": "AR2", "Project Name": "Moray Offshore Windfarm (East)", "Strike Price (£/MWh, 2012 prices)": 57.50, "Capacity (MW)": 950, "Delivery Year": "2022/23", "Number of Turbines": None},
    {"Allocation Round": "AR3", "Project Name": "Doggerbank Creyke Beck A P1", "Strike Price (£/MWh, 2012 prices)": 39.650, "Capacity (MW)": 1200, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR3", "Project Name": "Doggerbank Creyke Beck B P1", "Strike Price (£/MWh, 2012 prices)": 41.611, "Capacity (MW)": 1200, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR3", "Project Name": "Doggerbank Teeside A P1", "Strike Price (£/MWh, 2012 prices)": 41.611, "Capacity (MW)": 1200, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR3", "Project Name": "Seagreen Phase 1", "Strike Price (£/MWh, 2012 prices)": 41.611, "Capacity (MW)": 454, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR3", "Project Name": "Sofia Offshore Wind Farm Phase 1", "Strike Price (£/MWh, 2012 prices)": 39.650, "Capacity (MW)": 1400, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "Green Volt Offshore Windfarm (GV01) (Floating)", "Strike Price (£/MWh, 2012 prices)": 139.93, "Capacity (MW)": 400, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "Inch Cape A (Permitted Reduction)", "Strike Price (£/MWh, 2012 prices)": 54.23, "Capacity (MW)": 177.41, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "Inch Cape B (Permitted Reduction)", "Strike Price (£/MWh, 2012 prices)": 54.23, "Capacity (MW)": 88.70, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "Moray Offshore Windfarm (West) String 9 (Permitted Reduction)", "Strike Price (£/MWh, 2012 prices)": 54.23, "Capacity (MW)": 73.50, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "EA3B (Permitted Reduction)", "Strike Price (£/MWh, 2012 prices)": 54.23, "Capacity (MW)": 158.90, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "Hornsea Project Three Offshore Wind Farm AR6 A (Permitted Reduction)", "Strike Price (£/MWh, 2012 prices)": 54.23, "Capacity (MW)": 360, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "Hornsea Project Three Offshore Wind Farm AR6 C (Permitted Reduction)", "Strike Price (£/MWh, 2012 prices)": 54.23, "Capacity (MW)": 360, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "Hornsea Project Three Offshore Wind Farm AR6 B (Permitted Reduction)", "Strike Price (£/MWh, 2012 prices)": 54.23, "Capacity (MW)": 360, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "Hornsea Project Four Offshore Wind Farm", "Strike Price (£/MWh, 2012 prices)": 58.87, "Capacity (MW)": 2400, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR6", "Project Name": "East Anglia Two, Phase 1", "Strike Price (£/MWh, 2012 prices)": 58.87, "Capacity (MW)": 963.07, "Delivery Year": None, "Number of Turbines": None},
    # Add placeholders for AR4 and AR5 explicitly with 0 capacity/NaN price for calculations
    {"Allocation Round": "AR4", "Project Name": "No Offshore Wind Projects", "Strike Price (£/MWh, 2012 prices)": None, "Capacity (MW)": 0, "Delivery Year": None, "Number of Turbines": None},
    {"Allocation Round": "AR5", "Project Name": "No Offshore Wind Bids", "Strike Price (£/MWh, 2012 prices)": None, "Capacity (MW)": 0, "Delivery Year": None, "Number of Turbines": None},
]
df_cfd = pd.DataFrame(cfd_data)

# Ensure 'Capacity (MW)' and 'Strike Price' are numeric, coercing errors
df_cfd['Capacity (MW)'] = pd.to_numeric(df_cfd['Capacity (MW)'], errors='coerce')
df_cfd['Strike Price (£/MWh, 2012 prices)'] = pd.to_numeric(df_cfd['Strike Price (£/MWh, 2012 prices)'], errors='coerce')


# CPI Data (from Table 4)
cpi_dec_2012 = 97.6 # [1]
cpi_may_2025 = 138.4 # [1, 2, 3] # This value is from May 2025 as per the provided table.

# Exchange Rates (as assumed in the report, and a reasonable EUR rate)
exchange_rates = {
    "GBP_to_USD": 1.25, # Assumed for this example
    "GBP_to_EUR": 1.18 # Assumed for this example
}

# Average UK Offshore Wind Capacity Factor (from research)
capacity_factor = 0.422 # [4]

# --- Calculations ---

# Calculate Estimated Annual Production (MWh)
df_cfd["Estimated Annual Production (Mwh)"] = df_cfd["Capacity (MW)"] * capacity_factor * 8760

# Calculate Estimated Annual Revenue (GBP, 2012 prices)
df_cfd["Estimated Annual Revenue (£, 2012 prices)"] = df_cfd["Estimated Annual Production (Mwh)"] * df_cfd["Strike Price (£/MWh, 2012 prices)"]

# Normalize Strike Price to 2025 (GBP)
df_cfd["Normalized Strike Price (£/MWh, 2025 GBP)"] = df_cfd["Strike Price (£/MWh, 2012 prices)"] * (cpi_may_2025 / cpi_dec_2012)

# Calculate Estimated Annual Revenue (GBP, 2025 prices)
df_cfd["Estimated Annual Revenue (£, 2025 prices)"] = df_cfd["Estimated Annual Production (Mwh)"] * df_cfd["Normalized Strike Price (£/MWh, 2025 GBP)"]

# Convert Normalized Strike Prices to USD and EUR
df_cfd["Normalized Strike Price ($/MWh, 2025 USD)"] = df_cfd["Normalized Strike Price (£/MWh, 2025 GBP)"] * exchange_rates["GBP_to_USD"]
df_cfd["Normalized Strike Price (€/MWh, 2025 EUR)"] = df_cfd["Normalized Strike Price (£/MWh, 2025 GBP)"] * exchange_rates["GBP_to_EUR"]

# Convert Estimated Annual Revenue to USD and EUR (2025 prices)
df_cfd["Estimated Annual Revenue ($, 2025 USD)"] = df_cfd["Estimated Annual Revenue (£, 2025 prices)"] * exchange_rates["GBP_to_USD"]
df_cfd["Estimated Annual Revenue (€, 2025 EUR)"] = df_cfd["Estimated Annual Revenue (£, 2025 prices)"] * exchange_rates["GBP_to_EUR"]

# Convert Production to TWh
df_cfd["Estimated Annual Production (TWh)"] = df_cfd["Estimated Annual Production (Mwh)"] / 1_000_000

# Convert Estimated Annual Revenue to Millions (for display in Chart 2)
df_cfd["Estimated Annual Revenue (£M, 2025 prices)"] = df_cfd["Estimated Annual Revenue (£, 2025 prices)"] / 1_000_000
df_cfd["Estimated Annual Revenue ($M, 2025 USD)"] = df_cfd["Estimated Annual Revenue ($, 2025 USD)"] / 1_000_000
df_cfd["Estimated Annual Revenue (€M, 2025 EUR)"] = df_cfd["Estimated Annual Revenue (€, 2025 EUR)"] / 1_000_000

# --- Streamlit App Layout ---

st.title("UK Offshore Wind CfD Project Analysis")
st.markdown("Explore Contracts for Difference (CfD) strike prices, estimated production, and revenue for UK offshore wind projects from Allocation Round 1 to 6.")

# Sidebar for user inputs
st.sidebar.header("Visualization Options")
selected_currency = st.sidebar.radio(
    "Choose Currency for Strike Prices and Revenue:",
    ("GBP (£)", "USD ($)", "EUR (€)"),
    index=0 # Default to GBP
)
selected_price_year = st.sidebar.radio(
    "Choose Price Year for Strike Prices:",
    ("2012 (Original)", "2025 (Inflation Adjusted)"),
    index=0 # Default to 2012
)

# Determine the column names and symbols based on user selection
currency_symbol = ""
strike_price_col = ""
revenue_col = "" # For project-specific chart
revenue_col_m = "" # For chart in millions
revenue_label_unit = "" # Unit label for chart in millions

if selected_currency == "GBP (£)":
    currency_symbol = "£"
    if selected_price_year == "2012 (Original)":
        strike_price_col = "Strike Price (£/MWh, 2012 prices)"
    else:
        strike_price_col = "Normalized Strike Price (£/MWh, 2025 GBP)"
    revenue_col = "Estimated Annual Revenue (£, 2025 prices)"
    revenue_col_m = "Estimated Annual Revenue (£M, 2025 prices)"
    revenue_label_unit = "£M"
elif selected_currency == "USD ($)":
    currency_symbol = "$"
    strike_price_col = "Normalized Strike Price ($/MWh, 2025 USD)"
    revenue_col = "Estimated Annual Revenue ($, 2025 USD)"
    revenue_col_m = "Estimated Annual Revenue ($M, 2025 USD)"
    revenue_label_unit = "$M"
else: # EUR (€)
    currency_symbol = "€"
    strike_price_col = "Normalized Strike Price (€/MWh, 2025 EUR)"
    revenue_col = "Estimated Annual Revenue (€, 2025 EUR)"
    revenue_col_m = "Estimated Annual Revenue (€M, 2025 EUR)"
    revenue_label_unit = "€M"

# --- Chart 1: CfD Strike Prices by Project ---
st.header(f"CfD Strike Prices by Offshore Wind Project ({selected_price_year} in {selected_currency})")

# Filter out AR4 and AR5 for project-specific charts as they had no actual offshore wind projects/bids
# Filter out rows where Capacity (MW) is 0, which includes the AR4/AR5 placeholders
df_chart1 = df_cfd[df_cfd["Capacity (MW)"] > 0].copy()

if not df_chart1.empty:
    chart1 = alt.Chart(df_chart1).mark_bar().encode(
        x=alt.X(strike_price_col, title=f"Strike Price ({currency_symbol}/MWh)"),
        y=alt.Y("Project Name", sort="-x", title="Project Name"),
        color=alt.Color("Allocation Round", title="Allocation Round"),
        tooltip=[
            alt.Tooltip("Project Name"),
            alt.Tooltip("Allocation Round"),
            alt.Tooltip(strike_price_col, format=".2f", title=f"Strike Price ({currency_symbol}/MWh)"),
            alt.Tooltip("Capacity (MW)", format=".0f")
        ]
    ).properties(
        title=f"CfD Strike Prices by Offshore Wind Project ({selected_price_year} in {selected_currency})"
    ).interactive()
    st.altair_chart(chart1, use_container_width=True)
else:
    st.write("No offshore wind projects found for the selected criteria to display strike prices. AR4 and AR5 had no bids.")

# --- Chart 2: Estimated Annual Production and Revenue ---
st.header(f"Estimated Annual Production (TWh) and Revenue ({revenue_label_unit}, 2025 Value) per Project")

# Filter out AR4 and AR5 for project-specific charts (same as Chart 1)
df_chart2 = df_cfd[df_cfd["Capacity (MW)"] > 0].copy()

if not df_chart2.empty:
    # Melt the DataFrame for combined bar chart, using the million-unit revenue column
    df_melted = df_chart2.melt(
        id_vars=["Project Name", "Allocation Round"],
        value_vars=["Estimated Annual Production (TWh)", revenue_col_m],
        var_name="Metric",
        value_name="Value"
    )

    # Create the combined chart
    chart2 = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X("Value", title=alt.Title(f"Value (TWh / {revenue_label_unit})")),
        y=alt.Y("Project Name", sort=alt.EncodingSortField(field="Capacity (MW)", op="sum", order="descending"), title="Project Name"), # Modified sort
        color=alt.Color("Metric", title="Metric"),
        column=alt.Column("Metric", header=alt.Header(titleOrient="bottom", labelOrient="bottom")),
        tooltip=[
            alt.Tooltip("Project Name"),
            alt.Tooltip("Metric"),
            alt.Tooltip("Value", format=".2f")
        ]
    ).properties(
        title=f"Estimated Annual Production (TWh) and Revenue ({revenue_label_unit}, 2025 Value) per Project"
    ).interactive()
    st.altair_chart(chart2, use_container_width=True)
else:
    st.write("No offshore wind projects found for the selected criteria to display production and revenue. AR4 and AR5 had no bids.")

# --- Chart 3: Average CfD Strike Price and Total Capacity per Allocation Round ---
st.header(f"Average CfD Strike Price ({selected_price_year} {selected_currency}) and Total Capacity per Allocation Round")

# Prepare data for Chart 3: Group by Allocation Round
# Ensure all_rounds category is set for consistent ordering, including those with 0 capacity
all_rounds = ["AR1", "AR2", "AR3", "AR4", "AR5", "AR6"]

# Filter for projects with actual capacity for averaging strike price, but include all rounds for total capacity sum
# Use df_cfd directly for aggregation, as NaN capacity will result in 0 for sum
df_round_summary = df_cfd.groupby("Allocation Round").agg(
    Avg_Strike_Price_2012_GBP=('Strike Price (£/MWh, 2012 prices)', 'mean'),
    Avg_Strike_Price_2025_GBP=('Normalized Strike Price (£/MWh, 2025 GBP)', 'mean'),
    Avg_Strike_Price_2025_USD=('Normalized Strike Price ($/MWh, 2025 USD)', 'mean'),
    Avg_Strike_Price_2025_EUR=('Normalized Strike Price (€/MWh, 2025 EUR)', 'mean'),
    Total_Capacity_MW=('Capacity (MW)', 'sum') # Sum handles NaN/0 correctly
).reset_index()

# Ensure all_rounds are present for categorical ordering and fill missing (if any)
df_round_summary["Allocation Round"] = pd.Categorical(df_round_summary["Allocation Round"], categories=all_rounds, ordered=True)
df_round_summary = df_round_summary.sort_values("Allocation Round")
df_round_summary = df_round_summary.set_index("Allocation Round").reindex(all_rounds).reset_index()
# For rounds with no projects, Total_Capacity_MW will be NaN after reindex, fill with 0
df_round_summary["Total_Capacity_MW"] = df_round_summary["Total_Capacity_MW"].fillna(0)


# Determine the correct average strike price column based on user selection
avg_strike_price_col_name = ""
if selected_currency == "GBP (£)":
    if selected_price_year == "2012 (Original)":
        avg_strike_price_col_name = "Avg_Strike_Price_2012_GBP"
    else:
        avg_strike_price_col_name = "Avg_Strike_Price_2025_GBP"
elif selected_currency == "USD ($)":
    avg_strike_price_col_name = "Avg_Strike_Price_2025_USD"
else: # EUR (€)
    avg_strike_price_col_name = "Avg_Strike_Price_2025_EUR"

if not df_round_summary.empty:
    # Bar chart for Total Capacity
    bars = alt.Chart(df_round_summary).mark_bar(color='#a5d8ff').encode(
        x=alt.X("Allocation Round", sort=all_rounds, title=""), # No title here, common with line chart
        y=alt.Y("Total_Capacity_MW", title="Total Capacity (MW)"),
        tooltip=[
            alt.Tooltip("Allocation Round"),
            alt.Tooltip("Total_Capacity_MW", title="Total Capacity (MW)", format=".0f"),
            alt.Tooltip(avg_strike_price_col_name, title=f"Avg Strike Price ({currency_symbol}/MWh)", format=".2f")
        ]
    )

    # Line chart for Average Strike Price
    lines = alt.Chart(df_round_summary).mark_line(color='#ff6b6b', point=True).encode(
        x=alt.X("Allocation Round", sort=all_rounds),
        y=alt.Y(avg_strike_price_col_name, title=f"Average Strike Price ({currency_symbol}/MWh)"),
        tooltip=[
            alt.Tooltip("Allocation Round"),
            alt.Tooltip(avg_strike_price_col_name, title=f"Avg Strike Price ({currency_symbol}/MWh)", format=".2f"),
            alt.Tooltip("Total_Capacity_MW", title="Total Capacity (MW)", format=".0f")
        ]
    )

    # Combine charts with resolve_scale for independent Y-axes
    chart3 = alt.layer(bars, lines).resolve_scale(
        y='independent' # Ensures two separate Y-axes for different scales
    ).properties(
        title=f"Average CfD Strike Price ({selected_price_year} {selected_currency}) and Total Capacity per Round"
    ).interactive()
    st.altair_chart(chart3, use_container_width=True)
else:
    st.write("No round summary data available for plotting average strike prices and total capacity.")


st.markdown("---")
st.markdown(f"""
**Notes:**
* Capacity factor of 42.2% is used for production calculations.
* CPI for 2012 (December) is {cpi_dec_2012} and for 2025 (May) is {cpi_may_2025}.
* Assumed static exchange rates for conversion: 1 GBP = {exchange_rates["GBP_to_USD"]} USD, 1 GBP = {exchange_rates["GBP_to_EUR"]} EUR. Dynamic fetching from xe.com is not implemented.
* "Number of Turbines" data is generally not available in public CfD results documents.
* Allocation Round 4 (AR4) did not have specific offshore wind projects listed with awarded capacity.
* Allocation Round 5 (AR5) had no offshore wind bids submitted.
""")
