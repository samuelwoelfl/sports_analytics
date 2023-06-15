import streamlit as st
import sys 
import os
sys.path.append(os.path.abspath("C:\\Users\\Time\\Sports Analytics"))
from fit_data import *
import plotly_express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager
from highlight_text import fig_text
# import pandas as pd
# import numpy as np


st.set_page_config(layout="wide")

st.title('Comparison')


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
selection_session_1 = st.selectbox("Which Sessions would you like to compare?", options=fit_df["file_id"].unique())
selection_session_2 = st.selectbox("vs.", options=fit_df["file_id"].unique())

session_1_df = fit_df.query(
    "sport == @selection_sport & file_id == @selection_session_1"
)

session_1_df = session_1_df.reset_index().melt('timestamp_x', value_vars= ["heart_rate", "enhanced_speed", "enhanced_altitude", "power"], var_name='metric', value_name='value')

nearest = alt.selection_point(nearest=True, on='mouseover',
                        fields=['timestamp_x'], empty=False)

line = alt.Chart(session_1_df).mark_line(interpolate='basis').encode(
    x='timestamp_x:T',
    y='value:Q',
    color='metric:N'
)

selectors = alt.Chart(session_1_df).mark_point().encode(
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

rules = alt.Chart(session_1_df).mark_rule(color='gray').encode(
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

session_2_df = fit_df.query(
    "sport == @selection_sport & file_id == @selection_session_2"
)

session_2_df = session_2_df.reset_index().melt('timestamp_x', value_vars= ["heart_rate", "enhanced_speed", "enhanced_altitude", "power"], var_name='metric', value_name='value')

nearest = alt.selection_point(nearest=True, on='mouseover',
                        fields=['timestamp_x'], empty=False)

line = alt.Chart(session_2_df).mark_line(interpolate='basis').encode(
    x='timestamp_x:T',
    y='value:Q',
    color='metric:N'
)

selectors = alt.Chart(session_2_df).mark_point().encode(
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

rules = alt.Chart(session_2_df).mark_rule(color='gray').encode(
    x='timestamp_x:T',
).transform_filter(
    nearest
)

line_chart_2 = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=1000, height=500
)

st.write(line_chart_2)


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

radar_df_1 = fit_df[["file_id", "heart_rate", "enhanced_speed", "power", "enhanced_altitude"]]
radar_df_1 = radar_df_1.groupby("file_id").aggregate({"heart_rate":"mean", "enhanced_speed":"mean", "power":"mean", "enhanced_altitude":"sum"})
radar_df_1["Percentile_Rank_hr"] = 100 - (radar_df_1.heart_rate.rank(pct = True)*100)
radar_df_1["Percentile_Rank_pace"] = radar_df_1.enhanced_speed.rank(pct = True)*100
radar_df_1["Percentile_Rank_power"] = radar_df_1.power.rank(pct = True)*100
radar_df_1["Percentile_Rank_alt"] = radar_df_1.enhanced_altitude.rank(pct = True)*100

radar_df_1 = radar_df_1.query(
    "file_id == @selection_session_1"
)
radar_df_1=radar_df_1.reset_index()

radar_df_1 = radar_df_1.drop(["heart_rate", "enhanced_speed", "power", "enhanced_altitude"], axis=1)

radar_df_1 = pd.melt(radar_df_1, id_vars="file_id", value_vars= ["Percentile_Rank_hr", "Percentile_Rank_pace", "Percentile_Rank_power", "Percentile_Rank_alt"], var_name='metric', value_name='value')

radar_df_1 = radar_df_1.drop(["file_id"], axis=1)

radar_df_1 = radar_df_1.round(0)


#---

radar_df_2 = fit_df[["file_id", "heart_rate", "enhanced_speed", "power", "enhanced_altitude"]]
radar_df_2 = radar_df_2.groupby("file_id").aggregate({"heart_rate":"mean", "enhanced_speed":"mean", "power":"mean", "enhanced_altitude":"sum"})
radar_df_2["Percentile_Rank_hr"] = 100 - (radar_df_2.heart_rate.rank(pct = True)*100)
radar_df_2["Percentile_Rank_pace"] = radar_df_2.enhanced_speed.rank(pct = True)*100
radar_df_2["Percentile_Rank_power"] = radar_df_2.power.rank(pct = True)*100
radar_df_2["Percentile_Rank_alt"] = radar_df_2.enhanced_altitude.rank(pct = True)*100

radar_df_2 = radar_df_2.query(
    "file_id == @selection_session_2"
)
radar_df_2=radar_df_2.reset_index()

radar_df_2 = radar_df_2.drop(["heart_rate", "enhanced_speed", "power", "enhanced_altitude"], axis=1)

radar_df_2 = pd.melt(radar_df_2, id_vars="file_id", value_vars= ["Percentile_Rank_hr", "Percentile_Rank_pace", "Percentile_Rank_power", "Percentile_Rank_alt"], var_name='metric', value_name='value')

radar_df_2 = radar_df_2.drop(["file_id"], axis=1)

radar_df_2 = radar_df_2.round(0)



#---

values_session_1 = radar_df_1.value.values.tolist()
values_session_2 = radar_df_2.value.values.tolist()

#Pizza Plot

font_normal = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/roboto/'
                          'Roboto%5Bwdth,wght%5D.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/roboto/'
                          'Roboto-Italic%5Bwdth,wght%5D.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                        'RobotoSlab%5Bwght%5D.ttf')
# parameter and values list
# The values are taken from the excellent fbref website (supplied by StatsBomb)
params = [
    "Average Heartrate", "Average Pace", "Average Power", "Total Altitude"
]

# instantiate PyPizza class
baker = PyPizza(
    params=params,                  # list of parameters
    background_color="#EBEBE9",     # background color
    straight_line_color="#222222",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    last_circle_color="#222222",    # color of last circle
    other_circle_ls="-.",           # linestyle for other circles
    other_circle_lw=1               # linewidth for other circles
)

# plot pizza
fig, ax = baker.make_pizza(
    values_session_1,                     # list of values
    compare_values=values_session_2,    # comparison values
    figsize=(8, 8),             # adjust figsize according to your need
    kwargs_slices=dict(
        facecolor="#1AB0B0", edgecolor="#222222",
        zorder=2, linewidth=1
    ),                          # values to be used when plotting slices
    kwargs_compare=dict(
        facecolor="#8676FE", edgecolor="#222222",
        zorder=2, linewidth=1,
    ),
    kwargs_params=dict(
        color="#000000", fontsize=12,
        fontproperties=font_normal.prop, va="center"
    ),                          # values to be used when adding parameter
    kwargs_values=dict(
        color="#000000", fontsize=12,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="#1AB0B0",
            boxstyle="round,pad=0.2", lw=1
        )
    ),                          # values to be used when adding parameter-values labels
    kwargs_compare_values=dict(
        color="#000000", fontsize=12, fontproperties=font_normal.prop, zorder=3,
        bbox=dict(edgecolor="#000000", facecolor="#8676FE", boxstyle="round,pad=0.2", lw=1)
    ),                          # values to be used when adding parameter-values labels
)


# add title
fig_text(
    0.515, 0.99, "<Session> "+str(selection_session_1)+" vs <Session> "+str(selection_session_2), size=17, fig=fig,
    highlight_textprops=[{"color": '#1AB0B0'}, {"color": '#8676FE'}],
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

fig.text(
    0.515, 0.942,
    "Percentile Rank vs all Sessions | "+selection_sport,
    size=15,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)


st.write(fig)



#fig = px.line_polar(radar_df, r='value', theta='metric', line_close=True)
#fig.update_traces(fill='toself')

#st.write(fig)
