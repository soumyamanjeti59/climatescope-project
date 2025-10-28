import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io

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
    sel_countries = st.sidebar.multiselect("Countries (compare multiple!)", countries, default=countries[:1])
    variable_options = [col for col in ["temperature_celsius", "precip_mm", "humidity", "wind_mps"] if col in df.columns]
    variable = st.sidebar.selectbox("Variable", variable_options)
    years = sorted(df['year'].unique())
    yr_min, yr_max = min(years), max(years)
    yr_range = st.sidebar.slider("Year range", yr_min, yr_max, (yr_min, yr_max))

    chart_type = st.sidebar.radio("Trend Chart Type", ["Line", "Bar", "Heatmap"])

    filtered = df[(df['year'] >= yr_range[0]) & (df['year'] <= yr_range[1])]
    if sel_countries:
        filtered = filtered[filtered['country'].isin(sel_countries)]

    extremes = None
    if os.path.exists("analysis/extremes.csv"):
        ex = pd.read_csv("analysis/extremes.csv")
        if sel_countries:
            ex = ex[ex['country'].isin(sel_countries)]
        extremes = ex

    # Choropleth section
    st.markdown("## Average Climate Measures by Country")
    st.markdown(
        "This choropleth map visualizes the average value of the selected variable across the chosen countries and time period."
    )
    if not filtered.empty:
        country_avg = filtered.groupby('country')[variable].mean().reset_index()
        fig = px.choropleth(
            country_avg,
            locations='country',
            locationmode='country names',
            color=variable,
            title=f"{variable} Average by Country",
            template="plotly_dark"
        )
        fig.update_layout(
            coloraxis_colorbar=dict(title=variable.replace("_"," ").title())
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for choropleth.")

    # Trend section
    st.markdown("## Climate Trends Over Time")
    st.markdown(
        "Interactive trend charts allow you to compare how the selected variable changes over months and years among selected countries. "
        "Switch between line, bar, and heatmap views."
    )
    if not filtered.empty:
        if chart_type == "Heatmap":
            filtered['month_num'] = pd.to_datetime(filtered['month']).dt.month
            pivot = filtered.pivot_table(
                index='country',
                columns='month_num',
                values=variable,
                aggfunc='mean',
                fill_value=None
            )
            fig2 = px.imshow(
                pivot,
                labels=dict(x="Month", y="Country", color=variable),
                aspect="auto",
                title=f"{variable} Heatmap (Country vs Month)",
                template="plotly_dark"
            )
        else:
            if chart_type == "Line":
                fig2 = px.line(
                    filtered,
                    x='month',
                    y=variable,
                    color='country',
                    title=f"{variable} Trend Comparison ({yr_range[0]}-{yr_range[1]})",
                    template="plotly_dark"
                )
            elif chart_type == "Bar":
                fig2 = px.bar(
                    filtered,
                    x='month',
                    y=variable,
                    color='country',
                    title=f"{variable} Bar Comparison ({yr_range[0]}-{yr_range[1]})",
                    template="plotly_dark"
                )

            if extremes is not None and not extremes.empty and chart_type in ("Line", "Bar"):
                for country in sel_countries:
                    df_ext = extremes[(extremes['country'] == country)]
                    fig2.add_trace(go.Scatter(
                        x=df_ext['month'],
                        y=df_ext[variable],
                        mode='markers',
                        name=f'Extreme ({country})',
                        marker=dict(color='red', size=12, symbol='x'),
                        showlegend=True
                    ))

        st.plotly_chart(fig2, use_container_width=True)

        # Download Chart as PNG button
        buf = io.BytesIO()
        fig2.write_image(buf, format="png")
        st.download_button(
            label="Download Chart as PNG",
            data=buf,
            file_name="chart.png",
            mime="image/png"
        )
    else:
        st.info("No data for selected chart.")

    # Download filtered data as CSV button
    if not filtered.empty:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv",
        )

    # Extremes section
    st.markdown("## Detected Extreme Weather Events and Outliers")
    st.markdown(
        "The following table displays detected extreme temperature and precipitation events within your current filter settings."
    )
    if extremes is not None:
        st.subheader("Detected Extremes")
        st.dataframe(extremes)
