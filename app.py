from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
import streamlit as st
from streamlit import caching, line_chart, text, write, bar_chart, sidebar
import pandas as pd

caching.clear_cache()

@st.cache
def initial_read():
    champions = pd.read_csv("cc.csv")
    all_champions = ['None'] + list(set(list(champions['Champion'])))
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

st.header("Top")

temp = win_rates.loc[win_rates['role'] == "Top"]
temp = temp.loc[temp['champion_id'] == inputs['Ally Top']]
temp = temp.loc[temp['enemy_champion_id'] == inputs['Enemy Top']]
Top_win_rate = None if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
Top_early_game_win_rate = None if temp.shape[0] == 0 else temp['win_rate'].iloc[0]

if Top_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "Top"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally Top']]
    first_top_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['win_rate'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "Top"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy Top']]
    second_top_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['win_rate'].iloc[0]
    Top_win_rate = (first_top_early_game_win_rate + second_top_early_game_win_rate) / 2
if Top_early_game_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "Top"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally Top']]
    first_top_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "Top"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy Top']]
    second_top_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['in_lane'].iloc[0]
    Top_early_game_win_rate = (first_top_early_game_win_rate + second_top_early_game_win_rate) / 2
Top_win_rate, Top_early_game_win_rate = (50 if Top_win_rate == None else Top_win_rate), (50 if Top_early_game_win_rate == None else Top_early_game_win_rate)


temp = spikes.loc[spikes['champion'] == inputs['Ally Top']]
Top_ally_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]

temp = spikes.loc[spikes['champion'] == inputs['Enemy Top']]
Top_enemy_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]

Top_power_spike_delta = Top_ally_early_power_spike - Top_enemy_early_power_spike

temp = color.loc[color['champion'] == inputs['Ally Top']]
Top_ally_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]

temp = color.loc[color['champion'] == inputs['Enemy Top']]
Top_enemy_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]


temp = tanks.loc[tanks['champion'] == inputs['Ally Top']]
Top_ally_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]

temp = tanks.loc[tanks['champion'] == inputs['Enemy Top']]
Top_enemy_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]


temp = mobility.loc[mobility['Champion'] == inputs['Ally Top']]
Top_ally_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]

temp = mobility.loc[mobility['Champion'] == inputs['Enemy Top']]
Top_enemy_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]


temp = melee.loc[melee['Champion'] == inputs['Ally Top']]
Top_ally_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

temp = melee.loc[melee['Champion'] == inputs['Enemy Top']]
Top_enemy_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

Top_melee_vs_melee = 1 if Top_ally_melee == 'Melee' and Top_enemy_melee == 'Melee' else 0

temp = cc.loc[cc['Champion'] == inputs['Ally Top']]
Top_ally_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
Top_ally_cc
temp = cc.loc[cc['Champion'] == inputs['Enemy Top']]
Top_enemy_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
Top_enemy_cc
bonus_for_lane_Top = 2
bonus_for_lane_Top

final_score_Top = ((Top_early_game_win_rate - 50)/4) + \
                Top_power_spike_delta + \
                (2 if Top_ally_champion_color == "Red" else 0) + \
                (2 if Top_enemy_champion_color == "Red" else 0)  + \
                (-1 if Top_ally_champion_color == "Yellow" else 0)  + \
                (1 if Top_enemy_champion_color == "Yellow" else 0)  + \
                (1 if Top_enemy_squishy == "Squishy" else 0)  + \
                (0.5*Top_ally_mobility + 1.0*Top_enemy_mobility) + \
                (4*Top_melee_vs_melee) + \
                (1 if Top_ally_cc == "Low CC" else 2 if Top_ally_cc == "Medium CC" else 3 if Top_ally_cc == "High CC" else 0) + \
                (-1*(1 if Top_enemy_cc == "Low CC" else 2 if Top_enemy_cc == "Medium CC" else 3 if Top_enemy_cc == "High CC" else 0))
st.header("Score")
final_score_Top



st.header("Jungle")

temp = win_rates.loc[win_rates['role'] == "Jungle"]
temp = temp.loc[temp['champion_id'] == inputs['Ally Jungle']]
temp = temp.loc[temp['enemy_champion_id'] == inputs['Enemy Jungle']]
Jungle_win_rate = None if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
Jungle_early_game_win_rate = None if temp.shape[0] == 0 else temp['win_rate'].iloc[0]

if Jungle_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "Jungle"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally Jungle']]
    first_Jungle_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['win_rate'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "Jungle"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy Jungle']]
    second_Jungle_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['win_rate'].iloc[0]
    Jungle_win_rate = (first_Jungle_early_game_win_rate + second_Jungle_early_game_win_rate) / 2
if Jungle_early_game_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "Jungle"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally Jungle']]
    first_Jungle_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "Jungle"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy Jungle']]
    second_Jungle_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['in_lane'].iloc[0]
    Jungle_early_game_win_rate = (first_Jungle_early_game_win_rate + second_Jungle_early_game_win_rate) / 2
Jungle_win_rate, Jungle_early_game_win_rate = (50 if Jungle_win_rate == None else Jungle_win_rate), (50 if Jungle_early_game_win_rate == None else Jungle_early_game_win_rate)


temp = spikes.loc[spikes['champion'] == inputs['Ally Jungle']]
Jungle_ally_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]

temp = spikes.loc[spikes['champion'] == inputs['Enemy Jungle']]
Jungle_enemy_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]

Jungle_power_spike_delta = Jungle_ally_early_power_spike - Jungle_enemy_early_power_spike

temp = color.loc[color['champion'] == inputs['Ally Jungle']]
Jungle_ally_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]

temp = color.loc[color['champion'] == inputs['Enemy Jungle']]
Jungle_enemy_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]


temp = tanks.loc[tanks['champion'] == inputs['Ally Jungle']]
Jungle_ally_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]

temp = tanks.loc[tanks['champion'] == inputs['Enemy Jungle']]
Jungle_enemy_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]


temp = mobility.loc[mobility['Champion'] == inputs['Ally Jungle']]
Jungle_ally_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]

temp = mobility.loc[mobility['Champion'] == inputs['Enemy Jungle']]
Jungle_enemy_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]


temp = melee.loc[melee['Champion'] == inputs['Ally Jungle']]
Jungle_ally_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

temp = melee.loc[melee['Champion'] == inputs['Enemy Jungle']]
Jungle_enemy_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

Jungle_melee_vs_melee = 1 if Jungle_ally_melee == 'Melee' and Jungle_enemy_melee == 'Melee' else 0

temp = cc.loc[cc['Champion'] == inputs['Ally Jungle']]
Jungle_ally_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
Jungle_ally_cc
temp = cc.loc[cc['Champion'] == inputs['Enemy Jungle']]
Jungle_enemy_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
Jungle_enemy_cc
bonus_for_lane_Jungle = 2
bonus_for_lane_Jungle

final_score_Jungle = ((Jungle_early_game_win_rate - 50)/4) + \
                Jungle_power_spike_delta + \
                (2 if Jungle_ally_champion_color == "Red" else 0) + \
                (2 if Jungle_enemy_champion_color == "Red" else 0)  + \
                (-1 if Jungle_ally_champion_color == "Yellow" else 0)  + \
                (1 if Jungle_enemy_champion_color == "Yellow" else 0)  + \
                (1 if Jungle_enemy_squishy == "Squishy" else 0)  + \
                (0.5*Jungle_ally_mobility + 1.0*Jungle_enemy_mobility) + \
                (4*Jungle_melee_vs_melee) + \
                (1 if Jungle_ally_cc == "Low CC" else 2 if Jungle_ally_cc == "Medium CC" else 3 if Jungle_ally_cc == "High CC" else 0) + \
                (-1*(1 if Jungle_enemy_cc == "Low CC" else 2 if Jungle_enemy_cc == "Medium CC" else 3 if Jungle_enemy_cc == "High CC" else 0))
st.header("Score")
final_score_Jungle



st.header("Middle")

temp = win_rates.loc[win_rates['role'] == "Middle"]
temp = temp.loc[temp['champion_id'] == inputs['Ally Middle']]
temp = temp.loc[temp['enemy_champion_id'] == inputs['Enemy Middle']]
Middle_win_rate = None if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
Middle_early_game_win_rate = None if temp.shape[0] == 0 else temp['win_rate'].iloc[0]

if Middle_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "Middle"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally Middle']]
    first_Middle_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['win_rate'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "Middle"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy Middle']]
    second_Middle_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['win_rate'].iloc[0]
    Middle_win_rate = (first_Middle_early_game_win_rate + second_Middle_early_game_win_rate) / 2
if Middle_early_game_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "Middle"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally Middle']]
    first_Middle_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "Middle"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy Middle']]
    second_Middle_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['in_lane'].iloc[0]
    Middle_early_game_win_rate = (first_Middle_early_game_win_rate + second_Middle_early_game_win_rate) / 2
Middle_win_rate, Middle_early_game_win_rate = (50 if Middle_win_rate == None else Middle_win_rate), (50 if Middle_early_game_win_rate == None else Middle_early_game_win_rate)


temp = spikes.loc[spikes['champion'] == inputs['Ally Middle']]
Middle_ally_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]

temp = spikes.loc[spikes['champion'] == inputs['Enemy Middle']]
Middle_enemy_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]

Middle_power_spike_delta = Middle_ally_early_power_spike - Middle_enemy_early_power_spike

temp = color.loc[color['champion'] == inputs['Ally Middle']]
Middle_ally_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]

temp = color.loc[color['champion'] == inputs['Enemy Middle']]
Middle_enemy_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]


temp = tanks.loc[tanks['champion'] == inputs['Ally Middle']]
Middle_ally_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]

temp = tanks.loc[tanks['champion'] == inputs['Enemy Middle']]
Middle_enemy_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]


temp = mobility.loc[mobility['Champion'] == inputs['Ally Middle']]
Middle_ally_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]

temp = mobility.loc[mobility['Champion'] == inputs['Enemy Middle']]
Middle_enemy_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]


temp = melee.loc[melee['Champion'] == inputs['Ally Middle']]
Middle_ally_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

temp = melee.loc[melee['Champion'] == inputs['Enemy Middle']]
Middle_enemy_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

Middle_melee_vs_melee = 1 if Middle_ally_melee == 'Melee' and Middle_enemy_melee == 'Melee' else 0

temp = cc.loc[cc['Champion'] == inputs['Ally Middle']]
Middle_ally_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
Middle_ally_cc
temp = cc.loc[cc['Champion'] == inputs['Enemy Middle']]
Middle_enemy_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
Middle_enemy_cc
bonus_for_lane_Middle = 2
bonus_for_lane_Middle

final_score_Middle = ((Middle_early_game_win_rate - 50)/4) + \
                Middle_power_spike_delta + \
                (2 if Middle_ally_champion_color == "Red" else 0) + \
                (2 if Middle_enemy_champion_color == "Red" else 0)  + \
                (-1 if Middle_ally_champion_color == "Yellow" else 0)  + \
                (1 if Middle_enemy_champion_color == "Yellow" else 0)  + \
                (1 if Middle_enemy_squishy == "Squishy" else 0)  + \
                (0.5*Middle_ally_mobility + 1.0*Middle_enemy_mobility) + \
                (4*Middle_melee_vs_melee) + \
                (1 if Middle_ally_cc == "Low CC" else 2 if Middle_ally_cc == "Medium CC" else 3 if Middle_ally_cc == "High CC" else 0) + \
                (-1*(1 if Middle_enemy_cc == "Low CC" else 2 if Middle_enemy_cc == "Medium CC" else 3 if Middle_enemy_cc == "High CC" else 0))
st.header("Score")
final_score_Middle



st.header("ADC")

temp = win_rates.loc[win_rates['role'] == "ADC"]
temp = temp.loc[temp['champion_id'] == inputs['Ally ADC']]
temp = temp.loc[temp['enemy_champion_id'] == inputs['Enemy ADC']]
ADC_win_rate = None if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
ADC_early_game_win_rate = None if temp.shape[0] == 0 else temp['win_rate'].iloc[0]

if ADC_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "ADC"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally ADC']]
    first_ADC_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['win_rate'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "ADC"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy ADC']]
    second_ADC_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['win_rate'].iloc[0]
    ADC_win_rate = (first_ADC_early_game_win_rate + second_ADC_early_game_win_rate) / 2
if ADC_early_game_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "ADC"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally ADC']]
    first_ADC_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "ADC"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy ADC']]
    second_ADC_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['in_lane'].iloc[0]
    ADC_early_game_win_rate = (first_ADC_early_game_win_rate + second_ADC_early_game_win_rate) / 2
ADC_win_rate, ADC_early_game_win_rate = (50 if ADC_win_rate == None else ADC_win_rate), (50 if ADC_early_game_win_rate == None else ADC_early_game_win_rate)


temp = spikes.loc[spikes['champion'] == inputs['Ally ADC']]
ADC_ally_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]

temp = spikes.loc[spikes['champion'] == inputs['Enemy ADC']]
ADC_enemy_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]

ADC_power_spike_delta = ADC_ally_early_power_spike - ADC_enemy_early_power_spike

temp = color.loc[color['champion'] == inputs['Ally ADC']]
ADC_ally_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]

temp = color.loc[color['champion'] == inputs['Enemy ADC']]
ADC_enemy_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]


temp = tanks.loc[tanks['champion'] == inputs['Ally ADC']]
ADC_ally_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]

temp = tanks.loc[tanks['champion'] == inputs['Enemy ADC']]
ADC_enemy_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]


temp = mobility.loc[mobility['Champion'] == inputs['Ally ADC']]
ADC_ally_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]

temp = mobility.loc[mobility['Champion'] == inputs['Enemy ADC']]
ADC_enemy_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]


temp = melee.loc[melee['Champion'] == inputs['Ally ADC']]
ADC_ally_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

temp = melee.loc[melee['Champion'] == inputs['Enemy ADC']]
ADC_enemy_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

ADC_melee_vs_melee = 1 if ADC_ally_melee == 'Melee' and ADC_enemy_melee == 'Melee' else 0

temp = cc.loc[cc['Champion'] == inputs['Ally ADC']]
ADC_ally_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
ADC_ally_cc
temp = cc.loc[cc['Champion'] == inputs['Enemy ADC']]
ADC_enemy_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
ADC_enemy_cc
bonus_for_lane_ADC = 2
bonus_for_lane_ADC

final_score_ADC = ((ADC_early_game_win_rate - 50)/4) + \
                ADC_power_spike_delta + \
                (2 if ADC_ally_champion_color == "Red" else 0) + \
                (2 if ADC_enemy_champion_color == "Red" else 0)  + \
                (-1 if ADC_ally_champion_color == "Yellow" else 0)  + \
                (1 if ADC_enemy_champion_color == "Yellow" else 0)  + \
                (1 if ADC_enemy_squishy == "Squishy" else 0)  + \
                (0.5*ADC_ally_mobility + 1.0*ADC_enemy_mobility) + \
                (4*ADC_melee_vs_melee) + \
                (1 if ADC_ally_cc == "Low CC" else 2 if ADC_ally_cc == "Medium CC" else 3 if ADC_ally_cc == "High CC" else 0) + \
                (-1*(1 if ADC_enemy_cc == "Low CC" else 2 if ADC_enemy_cc == "Medium CC" else 3 if ADC_enemy_cc == "High CC" else 0))
st.header("Score")
final_score_ADC



st.header("Support")

temp = win_rates.loc[win_rates['role'] == "Support"]
temp = temp.loc[temp['champion_id'] == inputs['Ally Support']]
temp = temp.loc[temp['enemy_champion_id'] == inputs['Enemy Support']]
Support_win_rate = None if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
Support_early_game_win_rate = None if temp.shape[0] == 0 else temp['win_rate'].iloc[0]

if Support_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "Support"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally Support']]
    first_Support_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['win_rate'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "Support"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy Support']]
    second_Support_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['win_rate'].iloc[0]
    Support_win_rate = (first_Support_early_game_win_rate + second_Support_early_game_win_rate) / 2
if Support_early_game_win_rate == 0:
    temp = average_win_rates.loc[average_win_rates['role'] == "Support"]
    temp = temp.loc[temp['champion_id'] == inputs['Ally Support']]
    first_Support_early_game_win_rate = 50 if temp.shape[0] == 0 else temp['in_lane'].iloc[0]
    temp = average_win_rates.loc[average_win_rates['role'] == "Support"]
    temp = temp.loc[temp['champion_id'] == inputs['Enemy Support']]
    second_Support_early_game_win_rate = 50 if temp.shape[0] == 0 else 100 - temp['in_lane'].iloc[0]
    Support_early_game_win_rate = (first_Support_early_game_win_rate + second_Support_early_game_win_rate) / 2
Support_win_rate, Support_early_game_win_rate = (50 if Support_win_rate == None else Support_win_rate), (50 if Support_early_game_win_rate == None else Support_early_game_win_rate)


temp = spikes.loc[spikes['champion'] == inputs['Ally Support']]
Support_ally_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]

temp = spikes.loc[spikes['champion'] == inputs['Enemy Support']]
Support_enemy_early_power_spike = None if temp.shape[0] == 0 else temp['Early'].iloc[0]
Support_enemy_early_power_spike
Support_power_spike_delta = Support_ally_early_power_spike - Support_enemy_early_power_spike

temp = color.loc[color['champion'] == inputs['Ally Support']]
Support_ally_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]

temp = color.loc[color['champion'] == inputs['Enemy Support']]
Support_enemy_champion_color = None if temp.shape[0] == 0 else temp['Color'].iloc[0]


temp = tanks.loc[tanks['champion'] == inputs['Ally Support']]
Support_ally_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]

temp = tanks.loc[tanks['champion'] == inputs['Enemy Support']]
Support_enemy_squishy = None if temp.shape[0] == 0 else temp['squishy_vs_tank'].iloc[0]


temp = mobility.loc[mobility['Champion'] == inputs['Ally Support']]
Support_ally_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]

temp = mobility.loc[mobility['Champion'] == inputs['Enemy Support']]
Support_enemy_mobility = None if temp.shape[0] == 0 else temp['mobility'].iloc[0]


temp = melee.loc[melee['Champion'] == inputs['Ally Support']]
Support_ally_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

temp = melee.loc[melee['Champion'] == inputs['Enemy Support']]
Support_enemy_melee = None if temp.shape[0] == 0 else temp['Type'].iloc[0]

Support_melee_vs_melee = 1 if Support_ally_melee == 'Melee' and Support_enemy_melee == 'Melee' else 0

temp = cc.loc[cc['Champion'] == inputs['Ally Support']]
Support_ally_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
Support_ally_cc
temp = cc.loc[cc['Champion'] == inputs['Enemy Support']]
Support_enemy_cc = None if temp.shape[0] == 0 else temp['cc'].iloc[0]
Support_enemy_cc
bonus_for_lane_Support = 2
bonus_for_lane_Support

final_score_Support = ((Support_early_game_win_rate - 50)/4) + \
                Support_power_spike_delta + \
                (2 if Support_ally_champion_color == "Red" else 0) + \
                (2 if Support_enemy_champion_color == "Red" else 0)  + \
                (-1 if Support_ally_champion_color == "Yellow" else 0)  + \
                (1 if Support_enemy_champion_color == "Yellow" else 0)  + \
                (1 if Support_enemy_squishy == "Squishy" else 0)  + \
                (0.5*Support_ally_mobility + 1.0*Support_enemy_mobility) + \
                (4*Support_melee_vs_melee) + \
                (1 if Support_ally_cc == "Low CC" else 2 if Support_ally_cc == "Medium CC" else 3 if Support_ally_cc == "High CC" else 0) + \
                (-1*(1 if Support_enemy_cc == "Low CC" else 2 if Support_enemy_cc == "Medium CC" else 3 if Support_enemy_cc == "High CC" else 0))
st.header("Score")
final_score_Support
