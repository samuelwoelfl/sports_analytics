import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data as vega_data
import random
from datetime import date

#py -m streamlit run Streamlit_Files_Samuel\dashboard.py
# ----------------------------- Page Config --------------------------------- #
st.set_page_config(layout="wide")

# -------------------------------- Title ------------------------------------ #
st.title('Your stats for this week')
st.subheader('Dashboard')

# ------------------------------- Custom CSS --------------------------------- #

st.markdown(
    """
    <style>
    canvas {
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------ Init Data ---------------------------------- #
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


# -------------------------------- Load Data --------------------------------- #
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("")

# ---------------------------------- Main Layout --------------------------------- #
col_main_left, col_main_right = st.columns([3, 1])

# -------------------------------- Main Column Left ------------------------------ #
col_stats_1, col_stats_2, col_stats_3 = col_main_left.columns([1, 1, 1])

# ------------------------------- First section left ----------------------------- #
# Widget 1
fitness_chart = alt.Chart(vega_data.stocks(), title="Fitness", height=200).transform_filter(
    'datum.symbol==="GOOG"'
).mark_area(
    line={'color': 'white'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='#1AB0B0', offset=0),
               alt.GradientStop(color='white', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
).encode(
    x=alt.X('date:T', axis=None),
    y=alt.Y('price:Q', axis=None)
).configure(
    background='#1AB0B0',
    padding={"left": 50, "top": 50, "right": 50, "bottom": 50}  # ! padding seems to not work right now
)

col_stats_1.altair_chart(fitness_chart, use_container_width=True)

# Widget 2
fatigue_chart = alt.Chart(vega_data.stocks(), title="Fatigue", height=200).transform_filter(
    'datum.symbol==="MSFT"'
).mark_area(
    line={'color': 'white'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='#8676FE', offset=0),
               alt.GradientStop(color='white', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
).encode(
    x=alt.X('date:T', axis=None),
    y=alt.Y('price:Q', axis=None)
).configure(
    background='#8676FE',
    padding={"left": 50, "top": 50, "right": 50, "bottom": 50}
)

col_stats_2.altair_chart(fatigue_chart, use_container_width=True)

# Widget 3
form_chart = alt.Chart(vega_data.stocks(), title="Form", height=200).transform_filter(
    'datum.symbol==="AAPL"'
).mark_area(
    line={'color': 'white'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='#FF844B', offset=0),
               alt.GradientStop(color='white', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
).encode(
    x=alt.X('date:T', axis=None),
    y=alt.Y('price:Q', axis=None)
).configure(
    background='#FF844B',
    padding={"left": 50, "top": 50, "right": 50, "bottom": 50}
)

col_stats_3.altair_chart(form_chart, use_container_width=True)

# -------------------------------------- Second Section left ------------------------------------- #
col_activity, col_parts = col_main_left.columns([2, 1])

# Widget Activity
activity_data = pd.DataFrame({
    'Tag': ['Mon', 'Die', 'Mit', 'Don', 'Fre', 'Sam', 'Son'],
    'b': [28, 55, 43, 91, 81, 53, 19]
})
activity_chart = alt.Chart(activity_data, title="Activity", height=300).mark_bar(
    line={'color': 'white'},
    color='#E8F1FD'
).encode(
    x=alt.X('Tag'),
    y=alt.Y('b', axis=None)
).configure(
    background='#FFFFFF',
    padding={"left": 50, "top": 50, "right": 50, "bottom": 50}
)

col_activity.altair_chart(activity_chart, use_container_width=True)

# Widget Aufteilung
parts_data = pd.DataFrame({
    "sport": ['Laufen', 'Fahrrad', 'Schwimmen'],
    "value": [4, 6, 8],
    "color": ['#1AB0B0', '#FF844B', '#8676FE'],
})

parts_chart = alt.Chart(parts_data, title="Aufteilung", height=300).mark_arc(innerRadius=50).encode(
    theta="value",
    color='value:N'
    # color=alt.Color('value:N', scale=alt.Scale(
    #     domain=['Laufen', 'Fahrrad', 'Schwimmen'],
    #     range=['#1AB0B0', '#FF844B', '#8676FE']
    # ))
).configure(
    background='#FFFFFF',
    padding={"left": 50, "top": 50, "right": 50, "bottom": 50}
)

col_parts.altair_chart(parts_chart, use_container_width=True)

# -------------------------------------- Third section left ---------------------------------- #

col_main_left.subheader("Sessions")

sessions_data = pd.DataFrame(
    {
        "name": ["🏃 Laufen", "🚴 Fahhrad", "🏊‍♂️ Schwimmen", "🏃 Laufen", "🏃 Laufen", "🚴 Fahhrad"],
        "date": [date(1980, 1, 1), date(1980, 1, 1), date(1980, 1, 1), date(1980, 1, 1), date(1980, 1, 1), date(1980, 1, 1)],
        "distance": ["12.2 km", "12.2 km", "12.2 km", "12.2 km", "12.2 km", "12.2 km"],
        "track_data": [[random.randint(0, 5000) for _ in range(30)] for _ in range(6)],
    }
)

st.dataframe(sessions_data,
             column_config={
                 "name": "App name",
                 "date": st.column_config.DateColumn(
                     "Datum",
                     min_value=date(1900, 1, 1),
                     max_value=date(2005, 1, 1),
                     format="DD.MM.YYYY",
                     step=1,
                 ),
                 "distance": "Distanz",
                 "track_data": st.column_config.LineChartColumn(
                     "Streckenverlauf", y_min=0, y_max=5000
                 ),
             },
                hide_index=True,
                use_container_width=True
             )

# ----------------------------------------- Sidebar right ------------------------------------ #

# Add content to the second column
col_main_right.header("Your Goals")
col_main_right.write("Running")

# ------------------------------------------ Old stuff --------------------------------------- #

# with st.sidebar:
#     st.image('media/Logo.png')
#     st.text("Hello Bar")

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)


# hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
# st.subheader(f'Map of all pickups at {hour_to_filter}:00')
# st.map(filtered_data)


# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour <= hour_to_filter, bins=24, range=(0, 24))[0]
# st.line_chart(hist_values)
