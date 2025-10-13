import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="ClimateScope Prototype")
st.title("🌍 ClimateScope — Milestone 2 Prototype")

DATA_PATH = "data/processed/monthly_agg.parquet"
REQUIRED_COLS = ["country", "year", "month", "temperature_c", "precip_mm", "humidity", "wind_speed_mps"]

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
    countries = ["All"] + sorted(df['country'].dropna().unique())
    sel_country = st.sidebar.selectbox("Country", countries)
    variable_options = [col for col in ["temperature_c","precip_mm","humidity","wind_speed_mps"] if col in df.columns]
    variable = st.sidebar.selectbox("Variable", variable_options)
    years = sorted(df['year'].unique())
    yr_min, yr_max = min(years), max(years)
    yr_range = st.sidebar.slider("Year range", yr_min, yr_max, (yr_min, yr_max))

    filtered = df[(df['year'] >= yr_range[0]) & (df['year'] <= yr_range[1])]
    if sel_country != "All":
        filtered = filtered[filtered['country'] == sel_country]

    # Choropleth
    if not filtered.empty:
        country_avg = filtered.groupby('country')[variable].mean().reset_index()
        fig = px.choropleth(country_avg, locations='country', locationmode='country names', color=variable)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for choropleth.")

    # Time-series
    if not filtered.empty:
        trend = filtered.groupby('month')[variable].mean().reset_index()
        fig2 = px.line(trend, x='month', y=variable, title=f"{variable} Trend ({yr_range[0]}-{yr_range[1]})")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data for time-series plot.")

    # Extremes
    if os.path.exists("analysis/extremes.csv"):
        st.subheader("Detected Extremes")
        ex = pd.read_csv("analysis/extremes.csv")
        if sel_country != "All":
            ex = ex[ex['country'] == sel_country]
        st.dataframe(ex)
