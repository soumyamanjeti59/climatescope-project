Final Project Report – ClimateScope Dashboard (Milestone 4)
1. Introduction

ClimateScope is an interactive climate analytics dashboard built using Streamlit, Pandas, and Plotly.
It allows users to visualize global and regional climate patterns, including:

Temperature trends

Precipitation changes

Humidity levels

Wind speed

Pressure

Solar radiation

Extreme weather events

The dashboard enables deep filtering, drill-downs, comparison between countries, extreme event detection, scatter-plot analysis, and downloadable outputs.

This project contributes to understanding climate variability and trends in a visually rich environment.

2. Dataset & Methodology
2.1 Data Source

Processed dataset stored at:

data/processed/monthly_agg.parquet


This file contains monthly aggregated weather metrics for all countries.

2.2 Required Columns

The dashboard requires:

country

year

month

temperature_celsius

precip_mm

humidity

wind_mps

Additional synthetic fields (generated automatically for demo/demo completeness):

pressure_hPa

solar_radiation

cloud_cover

dew_point

visibility_km

heat_index

snow_mm

thunderstorm_days

min_temperature_celsius

max_temperature_celsius

2.3 Tools & Libraries

Streamlit (UI Framework)

Plotly Express + Graph Objects (Charts)

Pandas (Data processing)

NumPy (Synthetic feature generation)

2.4 Data Processing

Steps executed:

Load .parquet dataset using Pandas

Validate required columns

Add synthetic climate variables (for dashboard richness)

Create a date column for time-series plots

Apply filters based on:

Countries

Year range

Calendar date range

Drill by year

Drill by country

Calculate country-level averages for choropleth map

Detect extreme values (loaded from analysis/extremes.csv)

3. Dashboard Features
🔹 1. Side Filters

Country multiselect

Variable selector

Year range slider

Calendar date range

Drill-down settings:

Drill by year

Drill by country

🔹 2. Choropleth Climate Map

Shows mean value of selected variable by country.

🔹 3. Trend Analysis Module

Supports:

Line Chart

Bar Chart

Heatmap

With extreme-event markers highlighted using red X.

🔹 4. Time-Series Explorer

Visualizes monthly data using actual dates.

🔹 5. Scatter-Plot Relationship Explorer

Plots correlation between any two variables.

🔹 6. Extreme Weather Table

Shows detected extreme data events.

🔹 7. Downloadable Outputs

Chart PNG

Filtered CSV export

4. Key Insights (Sample — customize based on your results)
4.1 Global Trends

Temperature anomalies show consistent warming over the years.

Precipitation patterns fluctuate significantly between regions.

Humidity and wind speeds demonstrate seasonal trends.

Extreme weather events show notable peaks in specific years.

4.2 Regional Trends

Regions like Asia, Europe, North America show strong warming signals.

Variability in rainfall is pronounced in equatorial regions.

Extreme temperature spikes noted in 2012, 2016, 2020 (example values).

5. Conclusion

ClimateScope successfully visualizes global and regional climate data through a highly interactive dashboard.
The Streamlit interface, combined with Plotly, allows users to explore trends, compare countries, detect anomalies, and download filtered outputs.

6. Future Enhancements

See details in future_enhancements.md.