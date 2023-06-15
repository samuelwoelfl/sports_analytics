import streamlit as st
import datetime
# import pandas as pd
# import numpy as np


# ----------------------------- Page Config --------------------------------- #
st.set_page_config(layout="wide")

# -------------------------------- Title ------------------------------------ #
st.title('Performance by type')
st.subheader('Performance')

col_select_1, col_select_2, col_select_3 = st.columns([3, 4, 8])


type_select = col_select_1.selectbox(
    'Typ',
    ("🏃 Laufen", "🚴 Fahrrad", "🏊‍♂️ Schwimmen"))

date_select = col_select_2.date_input(
    "Zeitspanne",
    value=(datetime.date(2019, 7, 6), datetime.date(2022, 7, 6)))


col_select_1.subheader(f'Typ: {type_select}')
col_select_2.subheader(f'Date: {date_select}')
