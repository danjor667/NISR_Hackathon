#!/usr/bin/python3

import streamlit as st
import pandas as pd


# cleaning data for the land usage section
@st.cache_data
def load_land_a():
    season_a_data = pd.read_excel('data/2022_Tables.xlsx', sheet_name="Table 11")
    season_a_data = season_a_data.drop("List of Tables", axis=1)
    season_a_data = season_a_data.drop(0)
    season_a_data.columns = season_a_data.iloc[0]
    season_a_data = season_a_data[1:32]
    season_a_data = season_a_data.fillna(0)
    season_a_data.at[32, "District"] = "National"
    season_a_data = season_a_data.drop("Total developed land", axis=1)
    season_a_data.rename(columns={"Beans": "Bean"}, inplace=True)
    return season_a_data


# loading and cleaning season B data
@st.cache_data
def load_and_b():
    season_b_data = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 12 ")  # trailing whit space in sheet name
    season_b_data = season_b_data.drop("List of Tables", axis=1)
    season_b_data = season_b_data.drop(0)
    season_b_data.columns = season_b_data.iloc[0]
    season_b_data = season_b_data[1:32]
    season_b_data = season_b_data.fillna(0)
    season_b_data.rename(columns={"District/Crop category": "District"}, inplace=True)
    season_b_data.at[32, "District"] = "National"
    season_b_data = season_b_data.drop("Total developed land", axis=1)
    season_b_data.rename(columns={"Bean": "Beans"}, inplace=True)
    season_b_data.rename(columns={"Chia seed": "Chia seeds"}, inplace=True)
    season_b_data.rename(columns={"Sweet potato": "Sweet potatoes"}, inplace=True)
    season_b_data.rename(columns={"Irish potato": "Irish potatoes"}, inplace=True)
    season_b_data.rename(columns={"Taro & Yams": "Yams & Taro"}, inplace=True)
    season_b_data.rename(columns={"Banana": "Bananas"}, inplace=True)
    season_b_data.rename(columns={"Cooking banana": "Cooking Banana"}, inplace=True)
    season_b_data.rename(columns={"Pea": "Peas"}, inplace=True)
    season_b_data.rename(columns={"Groundnut": "Ground nuts"}, inplace=True)
    season_b_data.rename(columns={"Soybean": "Soya beans"}, inplace=True)
    season_b_data.rename(columns={"Other cereals": "Other Cereals"}, inplace=True)
    return season_b_data


# loading and cleaning season C data
@st.cache_data
def load_land_c():
    season_c_data = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 13")
    season_c_data = season_c_data.drop(columns=["List of Tables", "Unnamed: 1"], axis=1)
    season_c_data = season_c_data.drop(0)
    season_c_data.columns = season_c_data.iloc[0]
    season_c_data = season_c_data[1:32]
    season_c_data = season_c_data.fillna(0)
    season_c_data.rename(columns={"District/Crop": "District"}, inplace=True)
    season_c_data.rename(columns={"Sweet potato": "Sweet potatoes"}, inplace=True)
    season_c_data.rename(columns={"Irish potato": "Irish potatoes"}, inplace=True)
    season_c_data.rename(columns={"Beans": "Bean"}, inplace=True)
    season_c_data.rename(columns={"Pea": "Peas"}, inplace=True)
    season_c_data.rename(columns={"Soybean": "Soya beans"}, inplace=True)
    season_c_data.rename(columns={"vegetables": "Vegetables"}, inplace=True)
    season_c_data.at[32, "District"] = "National"
    season_c_data = season_c_data.drop("Developed land", axis=1)
    return season_c_data


# cleaning data for the crop production section

def load_crop_production_a():
    df = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 23")
    df = df.drop("List of Tables", axis=1)
    df = df.drop(0)
    df.columns = df.iloc[0]
    df = df[1:33]
    df = df.fillna(0)
    df.rename(columns={"Vegetables": "vegetables"}, inplace=True)
    df.rename(columns={"Other Cereals": "Other cereals"}, inplace=True)
    df.rename(columns={"Cooking Banana": "Cooking banana"}, inplace=True)
    return df


def load_crop_production_b():
    df = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 24")
    df = df.drop("List of Tables", axis=1)
    df = df.drop(0)
    df = df.drop(1)
    df = df.drop(2)
    df.columns = df.iloc[0]
    df = df[1:33]
    df = df.fillna(0)
    return df


def load_crop_production_c():
    df = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 25")
    df = df.drop("List of Tables", axis=1)
    df = df.drop(0)
    df = df.drop(1)
    df.columns = df.iloc[0]
    df = df.drop(df.columns[0], axis=1)
    df = df[1:33]
    df = df.fillna(0)
    df.rename(columns={" Bean": "Bean"}, inplace=True)
    df.rename(columns={"District/Crop": "District"}, inplace=True)
    return df


# cleaning data for the crop yield
def load_crop_yield_a():
    df = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 17")
    df = df.drop("List of Tables", axis=1)
    df = df.drop(0)
    df.columns = df.iloc[0]
    df = df[1:32]
    df = df.fillna(0)
    df.rename(columns={"District/Crop category": "District"}, inplace=True)
    return df


def load_crop_yield_b():
    df = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 18 ")  # trailing spaceat the end of the sheet name
    df = df.drop("List of Tables", axis=1)
    df = df.drop(0)
    df = df.drop(1)
    df.columns = df.iloc[0]
    df = df[1:32]
    df = df.fillna(0)
    df.rename(columns={"District/Crop category": "District"}, inplace=True)
    return df


def load_crop_yield_c():
    df = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 19")
    df = df.drop("List of Tables", axis=1)
    df = df.drop(0)
    df.columns = df.iloc[0]
    df = df.drop(df.columns[0], axis=1)
    df = df[1:32]
    df = df.fillna(0)
    df.rename(columns={"District/Crop": "District"}, inplace=True)
    return df


def load_harvested_a():
    df = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 14")
    df = df.drop("List of Tables", axis=1)
    dev = df.columns.to_list()[24]
    df = df.drop(dev, axis=1)
    df = df.drop(0)
    df.columns = df.iloc[0]
    df = df[1:32]
    df = df.fillna(0)
    df.rename(columns={"District/Crop category": "District"}, inplace=True)
    return df


def load_harvested_b():
    df = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 15 ") #trailing white space
    df = df.drop("List of Tables", axis=1)
    dev = df.columns.to_list()[24]
    df = df.drop(dev, axis=1)
    df = df.drop(0)
    df.columns = df.iloc[0]
    df = df[1:32]
    df = df.fillna(0)
    df.rename(columns={"District/Crop category": "District"}, inplace=True)
    return df


def load_harvested_c():
    df = pd.read_excel("data/2022_Tables.xlsx", sheet_name="Table 16")
    df = df.drop("List of Tables", axis=1)
    #df = df.drop("Developed land", axis=1)
    df = df.drop(0)
    df.columns = df.iloc[0]
    df = df[1:32]
    df = df.fillna(0)
    df.rename(columns={"District/Crop category": "District"}, inplace=True)
    return df
