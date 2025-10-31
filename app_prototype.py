import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io

# Add cohesive climate-themed background and UI style
def add_cohesive_climate_style():
    st.markdown(
        """
        <style>
        /* Full app background with subtle dark overlay */
        .stApp {
            background: linear-gradient(rgba(15, 32, 39, 0.8), rgba(15, 32, 39, 0.8)), 
                        url('https://images.unsplash.com/photo-1435224654926-ecc9f7fa028c?auto=format&fit=crop&w=1470&q=80');
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
            color: #f0f6f8;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: rgba(20, 40, 50, 0.85) !important;
            border-radius: 0 20px 20px 0;
            font-size: 16px;
            color: #d1d9e6 !important;
        }
        /* Sidebar spacing */
        .css-1v3fvcr {
            margin-bottom: 14px;
        }
        /* Sidebar labels */
        .css-1a4t5cm {
            color: #e0e6f2 !important;
        }
        /* Main content container styling */
        .css-18e3th9 {
            background-color: rgba(0, 0, 0, 0.6);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        }
        /* Headings glow */
        h1, h2, h3, h4 {
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.15);
        }
        /* Streamlit dataframe style */
        .stDataFrame div[data-testid="stDataFrame"] {
            border-radius: 12px !important;
            box-shadow: 0 4px 8px rgba(255,255,255,0.1);
            background-color: rgba(255, 255, 255, 0.1);
        }
        /* Buttons style */
        .stButton > button {
            background-color: #3e6fc1;
            color: white;
            border-radius: 8px;
            border: none;
            box-shadow: 0 2px 6px rgba(62,111,193,0.6);
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #2c4a8f;
            box-shadow: 0 4px 12px rgba(44,74,143,0.8);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

add_cohesive_climate_style()

st.set_page_config(layout="wide", page_title="ClimateScope Prototype")
st.title("🌍 Global Weather Monitor")

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

    yr_range = st.sidebar.slider("Year range", 2000, 2025,
                                 (min(df['year'].min(), 2000), max(df['year'].max(), 2000)))

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

    # ========================
    # Choropleth Visualization
    # ========================
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

        # Remove dark outer container (keep dark map)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
             coloraxis_colorbar=dict(title=variable.replace("_", " ").title()),
             height=600,     # increase map height (default ~450)
             width=1100,     # increase width for wide display
             # # remove extra padding

        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for choropleth.")

    # ========================
    # Climate Trends Over Time
    # ========================
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

    if not filtered.empty:
        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv",
        )

    # ========================
    # Extreme Weather Events
    # ========================
    st.markdown("## Detected Extreme Weather Events and Outliers")
    st.markdown(
        "The following table displays detected extreme temperature and precipitation events within your current filter settings."
    )
    if extremes is not None:
        st.subheader("Detected Extremes")
        st.dataframe(extremes)