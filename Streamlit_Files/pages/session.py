import streamlit as st
import sys 
import os
sys.path.append(os.path.abspath("C:\\Users\\Time\\Sports Analytics"))
from fit_data import *
import plotly_express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager
# import pandas as pd
# import numpy as np


st.set_page_config(layout="wide")

st.title('Session')


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

selection_sport = st.selectbox("Which sport would you like to select?", options=fit_df["sport"].unique())
fit_df = fit_df[fit_df["sport"] == selection_sport]
selection_session = st.selectbox("Which Session would you like to select?", options=fit_df["file_id"].unique())
selection_metric = st.multiselect(
    "What metrics would you like display?",
    ["heart_rate", "enhanced_speed", "enhanced_altitude","power"],
    default="heart_rate"
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
    width=1000, height=500
)

st.write(line_chart_1)


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

df = pd.DataFrame(dict(
    r=[1, 5, 2, 2, 3],
    theta=['processing cost','mechanical properties','chemical stability',
           'thermal stability', 'device integration']))

fig = px.line_polar(df, r='r', theta='theta', line_close=True)
fig.update_traces(fill='toself')

st.write(fig)
