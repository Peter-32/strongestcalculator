from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
import streamlit as st
from streamlit import caching, line_chart, text, write, bar_chart, sidebar
import pandas as pd

caching.clear_cache()

@st.cache
def initial_read():
    champions = pd.read_csv("average_win_rates.csv")
    all_champions = ['None'] + list(champions['champion_id'])
    top_champions = champions.loc[champions['role'] == "Top"]
    jungle_champions = champions.loc[champions['role'] == "Jungle"]
    middle_champions = champions.loc[champions['role'] == "Middle"]
    adc_champions = champions.loc[champions['role'] == "ADC"]
    support_champions = champions.loc[champions['role'] == "Support"]
    roles = ['Top', 'Jungle', 'Middle', 'ADC', 'Support']
    win_rates = pd.read_csv("win_rates.csv")
    average_win_rates = pd.read_csv("average_win_rates.csv")
    cc = pd.read_csv("cc.csv")
    color = pd.read_csv("color.csv")
    melee = pd.read_csv("melee.csv")
    mobility = pd.read_csv("mobility.csv")
    spikes = pd.read_csv("spikes.csv")
    tanks = pd.read_csv("tanks.csv")
    return champions, all_champions, roles, win_rates, average_win_rates, cc, color, melee, mobility, spikes, tanks

champions, all_champions, roles, win_rates, average_win_rates, cc, color, melee, mobility, spikes, tanks = initial_read()

inputs = {}
for team in ['Ally', 'Enemy']:
    for role in roles:
        inputs[f'{team} {role}'] = st.sidebar.selectbox(f'{team} {role}', all_champions)

st.header(inputs['Ally Top'])
st.header(inputs['Enemy Top'])
st.header(inputs['Enemy Top'])
temp = win_rates.loc[win_rates['role'] == "Top"]
temp = temp.loc[temp['champion_id'] == inputs['Ally Top']]
temp = temp.loc[temp['enemy_champion_id'] == inputs['Enemy Top']]
top_win_rate = temp['in_lane']
top_early_game_win_rate = temp['win_rate']






































# end
