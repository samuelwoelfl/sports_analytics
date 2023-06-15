import streamlit as st
import sys 
import os
# sys.path.append(os.path.abspath("C:\\Users\\samue\\GitHub\\sports_analytics"))
from fit_data import *
import plotly_express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager
import pandas as pd
import folium
import numpy as np
from streamlit_folium import st_folium


# ----------------------------- Page Config --------------------------------- #
st.set_page_config(layout="wide")

# -------------------------------- Title ------------------------------------ #
st.title('Session Overview')
st.subheader('Single Session')


# ----------------------------- Custom Style -------------------------------- #
st.markdown('''
<style>

canvas {
  border-radius: 15px;
  overflow: hidden;
}

[title~="st.iframe"] {
  width: 100%;
}

.stats {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  border-radius: 12px 12px 0px 0px;
  padding: 16px 16px;
  gap: 3vh;
  height: 100%;
}

.stats#first {
  background-color: #F4F5F5;
}

.stats#second {
  background-color: #8676FE;
}

.stats * {
  margin: 0;
  padding: 0;
}

.stats .top .title {
  font-size: 18px;
  font-weight: 500;
}

.stats .top .subheading {
  font-size: 16px;
  opacity: .65;
}

.stats .bottom {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
}

.stats .data_elem {
  width: 49%;
  margin-bottom: 2vh;
}

.stats .label {
  font-size: 14px;
  opacity: .65;
}

.stats .text {
  font-size: 28px;
}
</style>
''', unsafe_allow_html=True)


# ----------------------------------------------- Selectors -------------------------------------------- #

col_select_1, col_select_2, col_select_3, col_select_4 = st.columns([4, 4, 4, 8])

selection_sport = col_select_1.selectbox("Which sport would you like to select?", options=fit_df["sport"].unique())
fit_df = fit_df[fit_df["sport"] == selection_sport]
selection_session = col_select_2.selectbox("Which Session would you like to select?", options=fit_df["file_id"].unique())


# ---------------------------------------------- Main Columns -------------------------------------------- #

col_main_left, col_main_right = st.columns([10, 3])

# ------------------------------------------------ Map -------------------------------------------------- #

df = pd.DataFrame(dict(
    r=[1, 5, 2, 2, 3],
    theta=['processing cost', 'mechanical properties', 'chemical stability', 'thermal stability', 'device integration']))

filtered_df = fit_df.query(
    "sport == @selection_sport & file_id == @selection_session"
)

test_df = filtered_df[['file_id', 'enhanced_altitude', 'position_lat', 'position_long', 'distance']]
test_df = test_df.iloc[::3]

# Create a Streamlit checkbox to toggle the markers
# show_markers = col_main_left.checkbox("Show Lap Markers", value=True)
show_markers = True

# @st.cache_data(experimental_allow_widgets=True)
def showMap():
    # Create the DataFrame
    map_df = pd.DataFrame(
        {
            "position_lat": [28.987727, 28.987758, 28.987793, 28.987831, 28.987865],
            "position_long": [-13.509858, -13.509848, -13.509825, -13.509798, -13.509771],
            "enhanced_altitude": [33.400002, 33.400002, 33.400002, 33.200001, 32.799999],
            "distance": ["digga", "kann", "ich", "hier", "schreiben text"]
        }
    )

    # Create the map
    m = folium.Map(location=[test_df['position_lat'].mean(), test_df['position_long'].mean()], zoom_start=12)

    # Create a list of coordinates from the DataFrame
    coordinates = list(zip(test_df['position_lat'], test_df['position_long']))

    # Create a polyline using the coordinates
    folium.PolyLine(
        locations=coordinates,
        color='red',
        weight=10
    ).add_to(m)

    # Add circle markers for each point in the DataFrame
    for _, row in test_df.iterrows():
        folium.CircleMarker(
            [row['position_lat'], row['position_long']],
            radius=6,
            fill=True,
            fill_color='blue',
            color='blue',
            fill_opacity=0,
            opacity=0,
            tooltip=f"Elevation: {row['enhanced_altitude']}<br><span style='white-space: pre;'>Distance: {row['distance']}</span>",
            popup=f"Elevation: {row['enhanced_altitude']}<br><span style='white-space: pre;'>Distance: {row['distance']}</span>",
        ).add_to(m)

    laps_df = pd.DataFrame(
        {
            "lat": [28.987727],
            "lon": [-13.509858]
        }
    )

    # Add markers to the map only if the checkbox is selected
    for _, row in laps_df.iterrows():
        if show_markers:
            folium.Marker([row['lat'], row['lon']]).add_to(m)

    # Call to render the Folium map in Streamlit
    with col_main_left:
        st_folium(m, width=1500, height=400)



showMap()


# --------------------------------------------- Line Chart ------------------------------------- #

selection_metric = col_main_left.multiselect(
    "What metrics would you like display?",
    ["heart_rate", "enhanced_speed", "enhanced_altitude","power"],
    default="heart_rate"
)


line_chart = alt.Chart(fit_df[(fit_df['timestamp_x'].dt.date == pd.to_datetime('2023-02-24').date())]).transform_fold(
    ["heart_rate", "enhanced_speed", "enhanced_altitude"],
    as_=["metric", "value"]
).mark_line().encode(
    x=alt.X('timestamp_x:T'),
    y=alt.Y('value:Q', scale = alt.Scale(zero=False)),
    color="metric:N"
).properties(
    width=800,
    height=400,
    title='Metriken im Verlauf'
)


metric_df = fit_df.query(
    "sport == @selection_sport & file_id == @selection_session"
)

metric_df = metric_df.reset_index().melt('timestamp_x', value_vars= metric_df[selection_metric], var_name='metric', value_name='value')

nearest = alt.selection_point(nearest=True, on='mouseover',
                        fields=['timestamp_x'], empty=False)

line = alt.Chart(metric_df).mark_line(interpolate='basis').encode(
    x='timestamp_x:T',
    y='value:Q',
    color='metric:N'
)

selectors = alt.Chart(metric_df).mark_point().encode(
    x='timestamp_x:T',
    opacity=alt.value(0),
).add_params(
    nearest
)

points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'value:Q', alt.value(' '))
)

rules = alt.Chart(metric_df).mark_rule(color='gray').encode(
    x='timestamp_x:T',
).transform_filter(
    nearest
)

line_chart_1 = alt.layer(
    line, selectors, points, rules, text
).properties(
    height=400
).configure(
    background='#FFFFFF',
    padding={"left": 50, "top": 50, "right": 50, "bottom": 50}
)

# st.write(line_chart_1)
col_main_left.altair_chart(line_chart_1, use_container_width=True)


# ----------------------------------------------- KPIs ---------------------------------------------------- #

session_2_name = 'Radfahren, 21.04.2023, 17:25-18:56'
session_2_distance = '114,56 km'
session_2_duration = '4:05:53 h'
session_2_avg_speed = '28 km/h'
session_2_elevation = '1.580 m'

col_main_right.markdown(
    f'''
    <div class="stats" id="first">
        <div class="top">
            <p class="title">Summary</p>
        </div>
        <div class="bottom">
            <div class="data_elem">
                <p class="label">Distanz</p>
                <p class="text">{session_2_distance}</p>
            </div>
            <div class="data_elem">
                <p class="label">Dauer</p>
                <p class="text">{session_2_duration}</p>
            </div>
            <div class="data_elem">
                <p class="label">Ø Geschwindigkeit</p>
                <p class="text">{session_2_avg_speed}</p>
            </div>
            <div class="data_elem">
                <p class="label">Anstieg Gesamt</p>
                <p class="text">{session_2_elevation}</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True
)


#KPIs
"""
total_distance=
total_time=
avg_pace=
total_altitude=
avg_power=
avg_heart_rate=
ef=power/hr
"""

radar_df = fit_df[["file_id", "heart_rate", "enhanced_speed", "power", "enhanced_altitude"]]
radar_df = radar_df.groupby("file_id").aggregate({"heart_rate":"mean", "enhanced_speed":"mean", "power":"mean", "enhanced_altitude":"sum"})
radar_df["Percentile_Rank_hr"] = radar_df.heart_rate.rank(pct = True)
radar_df["Percentile_Rank_pace"] = radar_df.enhanced_speed.rank(pct = True)
radar_df["Percentile_Rank_power"] = radar_df.power.rank(pct = True)
radar_df["Percentile_Rank_alt"] = radar_df.enhanced_altitude.rank(pct = True)

radar_df = radar_df.query(
    "file_id == @selection_session"
)
radar_df=radar_df.reset_index()
st.write(radar_df)
radar_df = radar_df.drop(["heart_rate", "enhanced_speed", "power", "enhanced_altitude"], axis=1)
st.write(radar_df)
radar_df = pd.melt(radar_df, id_vars="file_id", value_vars= ["Percentile_Rank_hr", "Percentile_Rank_pace", "Percentile_Rank_power", "Percentile_Rank_alt"], var_name='metric', value_name='value')
st.write(radar_df)
radar_df = radar_df.drop(["file_id"], axis=1)
st.write(radar_df)


col_main_right.dataframe(test_df)


fig = px.line_polar(df, r='r', theta='theta', line_close=True)
fig.update_traces(fill='toself')

st.write(fig)



