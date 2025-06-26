import streamlit as st
import pandas as pd
import altair as alt

# --- Configuration ---
st.set_page_config(layout="wide", page_title="UK Offshore Wind CfD Analysis")

# --- Data Definition (based on research report tables) ---
# Table 1: Detailed CfD Allocation Round Data (Offshore Wind Projects)
cfd_data =
df_cfd = pd.DataFrame(cfd_data)

# CPI Data (from Table 4)
cpi_dec_2012 = 97.6 # [1]
cpi_may_2025 = 138.4 # [1, 2, 3]

# Exchange Rates (as assumed in the report, and a reasonable EUR rate)
exchange_rates = {
    "GBP_to_USD": 1.25, #
    "GBP_to_EUR": 1.18 # Assumed for this example
}

# Average UK Offshore Wind Capacity Factor (from research)
capacity_factor = 0.422 # [4]

# --- Calculations ---

# Calculate Estimated Annual Production (MWh)
df_cfd["Estimated Annual Production (MWh)"] = df_cfd["Capacity (MW)"] * capacity_factor * 8760

# Calculate Estimated Annual Revenue (GBP, 2012 prices)
df_cfd = df_cfd["Estimated Annual Production (MWh)"] * df_cfd

# Normalize Strike Price to 2025 (GBP)
df_cfd = df_cfd * (cpi_may_2025 / cpi_dec_2012)

# Calculate Estimated Annual Revenue (GBP, 2025 prices)
df_cfd = df_cfd["Estimated Annual Production (MWh)"] * df_cfd

# Convert Normalized Strike Prices to USD and EUR
df_cfd = df_cfd * exchange_rates
df_cfd = df_cfd * exchange_rates

# Convert Estimated Annual Revenue to USD and EUR (2025 prices)
df_cfd = df_cfd * exchange_rates
df_cfd = df_cfd * exchange_rates

# Convert Production to TWh
df_cfd = df_cfd["Estimated Annual Production (MWh)"] / 1_000_000

# --- Streamlit App Layout ---

st.title("UK Offshore Wind CfD Project Analysis")
st.markdown("Explore Contracts for Difference (CfD) strike prices, estimated production, and revenue for UK offshore wind projects from Allocation Round 1 to 6.")

# Sidebar for user inputs
st.sidebar.header("Visualization Options")
selected_currency = st.sidebar.radio(
    "Choose Currency for Strike Prices and Revenue:",
    ("GBP (£)", "USD ($)", "EUR (€)")
)
selected_price_year = st.sidebar.radio(
    "Choose Price Year for Strike Prices:",
    ("2012 (Original)", "2025 (Inflation Adjusted)")
)

# Determine the column names based on user selection
currency_symbol = ""
strike_price_col = ""
revenue_col = ""

if selected_currency == "GBP (£)":
    currency_symbol = "£"
    if selected_price_year == "2012 (Original)":
        strike_price_col = "Strike Price (£/MWh, 2012 prices)"
    else:
        strike_price_col = "Normalized Strike Price (£/MWh, 2025 GBP)"
    revenue_col = "Estimated Annual Revenue (£, 2025 prices)"
elif selected_currency == "USD ($)":
    currency_symbol = "$"
    strike_price_col = "Normalized Strike Price ($/MWh, 2025 USD)"
    revenue_col = "Estimated Annual Revenue ($, 2025 USD)"
else: # EUR (€)
    currency_symbol = "€"
    strike_price_col = "Normalized Strike Price (€/MWh, 2025 EUR)"
    revenue_col = "Estimated Annual Revenue (€, 2025 EUR)"

# --- Chart 1: CfD Strike Prices by Project ---
st.header(f"CfD Strike Prices by Offshore Wind Project ({selected_price_year} in {selected_currency})")

# Filter out AR4 and AR5 for project-specific charts as they had no offshore wind projects/bids
df_chart1 = df_cfd.isin()].copy()

if not df_chart1.empty:
    chart1 = alt.Chart(df_chart1).mark_bar().encode(
        x=alt.X(strike_price_col, title=f"Strike Price ({currency_symbol}/MWh)"),
        y=alt.Y("Project Name", sort="-x", title="Project Name"),
        color=alt.Color("Allocation Round", title="Allocation Round"),
        tooltip=
    ).properties(
        title=f"CfD Strike Prices by Offshore Wind Project ({selected_price_year} in {selected_currency})"
    ).interactive()
    st.altair_chart(chart1, use_container_width=True)
else:
    st.write("No offshore wind projects found for the selected criteria to display strike prices.")

# --- Chart 2: Estimated Annual Production and Revenue ---
st.header(f"Estimated Annual Production (TWh) and Revenue ({currency_symbol}, 2025 Value) per Project")

# Filter out AR4 and AR5 for project-specific charts
df_chart2 = df_cfd.isin()].copy()

if not df_chart2.empty:
    # Melt the DataFrame for combined bar chart
    df_melted = df_chart2.melt(
        id_vars=,
        value_vars=,
        var_name="Metric",
        value_name="Value"
    )

    # Create the combined chart
    chart2 = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X("Value", title="Value"),
        y=alt.Y("Project Name", sort="-x", title="Project Name"),
        color=alt.Color("Metric", title="Metric"),
        column=alt.Column("Metric", header=alt.Header(titleOrient="bottom", labelOrient="bottom")),
        tooltip=
    ).properties(
        title=f"Estimated Annual Production and Revenue ({currency_symbol}, 2025 Value) per Project"
    ).interactive()
    st.altair_chart(chart2, use_container_width=True)
else:
    st.write("No offshore wind projects found for the selected criteria to display production and revenue.")

st.markdown("---")
st.markdown(f"""
**Notes:**
*   Capacity factor of 42.2% is used for production calculations.[4]
*   CPI for 2012 (December) is 97.6 and for 2025 (May) is 138.4.[1]
*   Assumed exchange rates: 1 GBP = {exchange_rates} USD, 1 GBP = {exchange_rates} EUR.
*   "Number of Turbines" data is generally not available in public CfD results documents.
*   Allocation Round 4 (AR4) did not have specific offshore wind projects listed in the provided research snippets.
*   Allocation Round 5 (AR5) had no offshore wind bids submitted.
""")
