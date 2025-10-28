import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="ClimateScope Prototype")
st.title("🌍 ClimateScope — Milestone 3 Prototype")

DATA_PATH = "data/processed/monthly_agg.parquet"
REQUIRED_COLS = ["country", "year", "month", "temperature_celsius", "precip_mm", "humidity", "wind_mps"]

if not os.path.exists(DATA_PATH):
    st.warning("Run scripts/aggregate_daily_to_monthly.py first to generate data.")
else:
    df = pd.read_parquet(DATA_PATH)
    st.write("Columns present in DataFrame:", df.columns.tolist())

    missing = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()

    st.sidebar.header("Filters")
    countries = sorted(df['country'].dropna().unique())
    # Replace selectbox with multiselect
    sel_countries = st.sidebar.multiselect("Countries (compare multiple!)", countries, default=countries[:1])
    variable_options = [col for col in ["temperature_celsius", "precip_mm", "humidity", "wind_mps"] if col in df.columns]
    variable = st.sidebar.selectbox("Variable", variable_options)
    years = sorted(df['year'].unique())
    yr_min, yr_max = min(years), max(years)
    yr_range = st.sidebar.slider("Year range", yr_min, yr_max, (yr_min, yr_max))

    # Filter using selected countries
    filtered = df[(df['year'] >= yr_range[0]) & (df['year'] <= yr_range[1])]
    if sel_countries:
        filtered = filtered[filtered['country'].isin(sel_countries)]

    # Choropleth (now handles multiple countries correctly)
    if not filtered.empty:
        country_avg = filtered.groupby('country')[variable].mean().reset_index()
        fig = px.choropleth(
            country_avg,
            locations='country',
            locationmode='country names',
            color=variable,
            title=f"{variable} Average by Country"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for choropleth.")

    # Time-series (compare countries via different line color)
    if not filtered.empty:
        fig2 = px.line(
            filtered,
            x='month',
            y=variable,
            color='country',
            title=f"{variable} Trend Comparison ({yr_range[0]}-{yr_range[1]})"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data for time-series plot.")

    # Extremes
    if os.path.exists("analysis/extremes.csv"):
        st.subheader("Detected Extremes")
        ex = pd.read_csv("analysis/extremes.csv")
        if sel_countries:
            ex = ex[ex['country'].isin(sel_countries)]
        st.dataframe(ex)
