#!/usr/bin/python3

import streamlit as st
import pandas as pd


@st.cache_data
def load_season_a():
    season_a_data = pd.read_excel('data/2022_Tables.xlsx', sheet_name="Table 11")
    season_a_data = season_a_data.drop("List of Tables", axis=1)
    season_a_data = season_a_data.drop(0)
    season_a_data.columns = season_a_data.iloc[0]
    season_a_data = season_a_data[1:32]
    season_a_data = season_a_data.fillna(0)
    season_a_data.at[32, "District"] = "National"
    season_a_data = season_a_data.drop("Total developed land", axis=1)
    return season_a_data


# loading and cleaning season B data
@st.cache_data
def load_season_b():
    season_b_data = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 12 ")
    season_b_data = season_b_data.drop("List of Tables", axis=1)
    season_b_data = season_b_data.drop(0)
    season_b_data.columns = season_b_data.iloc[0]
    season_b_data = season_b_data[1:32]
    season_b_data = season_b_data.fillna(0)
    season_b_data.rename(columns={"District/Crop category": "District"}, inplace=True)
    season_b_data.at[32, "District"] = "National"
    season_b_data = season_b_data.drop("Total developed land", axis=1)
    return season_b_data


# loading and cleaning season C data
@st.cache_data
def load_season_c():
    season_c_data = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 13")
    season_c_data = season_c_data.drop(columns=["List of Tables", "Unnamed: 1"], axis=1)
    season_c_data = season_c_data.drop(0)
    season_c_data.columns = season_c_data.iloc[0]
    season_c_data = season_c_data[1:32]
    season_c_data = season_c_data.fillna(0)
    season_c_data.rename(columns={"District/Crop": "District"}, inplace=True)
    season_c_data.at[32, "District"] = "National"
    season_c_data = season_c_data.drop("Developed land", axis=1)
    return season_c_data
