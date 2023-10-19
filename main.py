#!/usr/bin/python3

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
from data.loading import load_season_a, load_season_b, load_season_c
import plotly_express as px


st.set_page_config("seasons Insight", layout="wide")
st.subheader("2022 Agricultural seasons Insight")



@st.cache_data
def load():
    return load_season_a(), load_season_b(), load_season_c()


season_A, season_B, season_C = load()



def season_a():
    # processing and plotting the graph for seasons A
    st.write("season A")




def season_b():
    # processing and plotting graph for season B data
    st.write("season B")
    #st.dataframe(season_B)
    with st.sidebar:
        pass


def season_c():
    # processing and plotting graphs for the season C data
    df = season_C
    df.set_index("District", inplace=True)
    st.write("season C")
    with st.sidebar:
        st.subheader("Filter")
        districts = st.multiselect("District", df.index)
        crops = st.multiselect("Crops", df.columns)
    if districts and crops:
        # create dataframe with the selected crops and Districts
        df = df.loc[districts, crops]
    else:
        # define default district and crops to plot as the whole df can't be visualised at once on the graph
        df = df.loc[[df.index[0], df.index[1], df.index[2], df.index[3], df.index[4]], [df.columns[0], df.columns[5], df.columns[3]]]

    def cards():
        total_land = 0
        for land in df.sum():
           total_land += land

        #st.write(df.sum())

        card_1, card_2, card_3 = st.columns(3)
        card_1.metric("Min Land Used:", value=0)
        card_2.metric("Max Land Used:", value=0)
        card_3.metric("Total Land used in Ha", value=total_land)
        style_metric_cards(background_color="#6600ff")

    with st.container():
        cards()
        div_1, div_2 = st.columns([0.45, 0.55], gap="small")
        with div_1:
            description_df = df.sum()
            description_df.columns = ["crop", "total land used"]
            #st.write(description_df.columns)
            st.dataframe(description_df, use_container_width=True)
            st.write("Table Description")
        with div_2:
            with st.expander("See Table"):
                st.dataframe(df, height=247, use_container_width=True)



    # plotting barchart and pie chart representation of data
    bar_fig = px.bar(df, barmode="group", y=df.columns.to_list(), x=df.index.to_list())
    # plotting a pie-chart diag for the df
    pie_fig = px.pie(df)
    with st.container():
        st.plotly_chart(bar_fig, use_container_width=True)
    with st.container():
        st.plotly_chart(pie_fig, use_container_width=True)



with st.sidebar:
    season = option_menu("SEASONS",
                         ["Season A", "Season B", "Season C"],
                         menu_icon="house")

if season == "Season A":
    # call function for season A
    season_a()
elif season == "Season B":
    # call function for season b
    season_b()
else:
    # call function for season C
    season_c()
