✔ Milestone 4 – Testing Checklist
A. Local Setup Testing
pip install -r requirements.txt
streamlit run app_prototype.py


Verify app loads at:
http://localhost:8501

B. Functionality Testing
Filters:

⬜ Country multiselect works

⬜ Year slider filters data

⬜ Calendar date filter works

⬜ Variable selector updates chart

⬜ Drill down by year works

⬜ Drill down by country works

Visualizations:

⬜ Choropleth plot loads

⬜ Trend line/bar/heatmap switches correctly

⬜ Extreme event markers appear correctly

⬜ Time series chart updates

⬜ Scatter plot updates

Downloads:

⬜ Chart downloads as PNG

⬜ Filtered data CSV downloads

C. Data Accuracy Testing

Check:

df[df['country']=='India'].groupby('year')['temperature_celsius'].mean()


Compare results with the choropleth and trend chart.

D. UI/UX Testing

⬜ Background theme loads

⬜ Sidebar UI works

⬜ No overlapping elements

⬜ App responsive on laptop/mobile

⬜ Buttons clickable

E. Edge Case Testing

Empty filter selection

Single country vs multiple countries

Extreme date filters

Missing data handling