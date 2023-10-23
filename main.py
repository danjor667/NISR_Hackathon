#!/usr/bin/python3

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
from data.loading import load_season_a, load_season_b, load_season_c
import plotly_express as px


st.set_page_config("Agricultural land usage", layout="wide")
st.subheader("2022 Agricultural season land usage in Rwanda")


@st.cache_data
def load():
    return load_season_a(), load_season_b(), load_season_c()


season_A, season_B, season_C = load()


@st.cache_data
def processing(dataframe, season_name, nation_land):
    # processing and plotting graph for season B data
    st.write(season_name)

    def cards(national_land):
        total_area = 0
        for land_used in dataframe.sum():
            total_area += land_used

        min_land = dataframe.sum().min()
        max_land = dataframe.sum().max()

        card_1, card_2, card_3, card_4 = st.columns(4)
        card_1.metric(f"Min Land Used:", value=min_land, delta="min land", delta_color="inverse")
        card_2.metric(f"Max Land Used:", value=max_land, delta="max land")
        card_3.metric("Total Land used in selected districts (in ha)", value=total_area, delta="Selected District")
        card_4.metric("Total land used Nation Wide", value=national_land, delta="Total")
        style_metric_cards(background_color="#6600ff")
        return total_area

    with st.container():
        total_land = cards(nation_land)
        div_1, div_2 = st.columns([0.45, 0.55], gap="small")
        with div_1:
            description_df = dataframe.sum()
            description_df.columns = ["crop", "total land used"]
            st.dataframe(description_df, use_container_width=True)
            st.write("Table Description")
        with div_2:
            with st.expander("See Table"):
                st.dataframe(dataframe, height=247, use_container_width=True)

    # plotting barchart and pie chart representation of data
    bar_fig = px.bar(dataframe, barmode="group", y=dataframe.columns.to_list(), x=dataframe.index.to_list(),
                     title="land used vs crop grown by Districts")
    bar_fig.update_layout(xaxis_title="CROP", yaxis_title="LAND USED (in ha)")
    bar_fig.update_layout(yaxis=dict(dtick=250), height=600)
    # plotting a bar-chart diag for the df
    with st.container():
        st.plotly_chart(bar_fig, use_container_width=True)
    # plotting pie-chart
    new_df = dataframe.reset_index()
    new_df = new_df.melt(id_vars="District", var_name="Crop", value_name="land_used")
    pie_fig = px.pie(new_df, values='land_used', names="Crop", color="Crop",
                     title='Percentage of land used for various crops in selected districts')
    with st.container():
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            st.plotly_chart(pie_fig, use_container_width=True)
            st.write(f"Total Land Used: {total_land}")


with st.sidebar:
    season = option_menu("SEASONS",
                         ["Season A", "Season B", "Season C"],
                         menu_icon="house")


if season == "Season A":
    df = season_A
    name = "Season A"
    national = df.iloc[-1]
    TOTAL = 0
    for land in national[1:]:
        TOTAL += land
    df = df.drop(32)
    df.set_index("District", inplace=True)
    with st.sidebar:
        st.subheader("Filter")
        districts = st.multiselect("District", df.index, default=[df.index[0], df.index[1], df.index[2],
                                                                  df.index[3], df.index[4]])
        crops = st.multiselect("Crops", df.columns, default=[df.columns[0], df.columns[1], df.columns[2]])
    if districts and crops:
        # create dataframe with the selected crops and Districts
        df = df.loc[districts, crops]
    processing(df, name, TOTAL)
elif season == "Season B":
    df = season_B
    name = "Season B"
    national = df.iloc[-1]
    TOTAL = 0
    for land in national[1:]:
        TOTAL += land
    df = df.drop(32)
    df.set_index("District", inplace=True)
    with st.sidebar:
        st.subheader("Filter")
        districts = st.multiselect("District", df.index, default=[df.index[0], df.index[1], df.index[2],
                                                                  df.index[3], df.index[4]])
        crops = st.multiselect("Crops", df.columns, default=[df.columns[0], df.columns[1], df.columns[2]])
    if districts and crops:
        # create dataframe with the selected crops and Districts
        df = df.loc[districts, crops]
    else:
        # define default district and crops to plot as the whole df can't be visualised at once on the graph
        df = df.loc[[df.index[0], df.index[1], df.index[2], df.index[3], df.index[4]], [df.columns[0], df.columns[5],
                                                                                        df.columns[3]]]
    processing(df, name, TOTAL)

else:
    df = season_C
    name = "Season C"
    national = df.iloc[-1]
    TOTAL = 0
    for land in national[1:]:
        TOTAL += land
    df = df.drop(32)
    df.set_index("District", inplace=True)
    with st.sidebar:
        st.subheader("Filter")
        districts = st.multiselect("District", df.index, default=[df.index[0], df.index[1], df.index[2],
                                                                  df.index[3], df.index[4]])
        crops = st.multiselect("Crops", df.columns, default=[df.columns[0], df.columns[1], df.columns[2]])
    if districts and crops:
        # create dataframe with the selected crops and Districts
        df = df.loc[districts, crops]
    processing(df, name, TOTAL)

hide_default_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden}
                </style>
                """
st.markdown(hide_default_style, unsafe_allow_html=True)
