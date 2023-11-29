#!/usr/bin/python3
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
from data.loading import *
import plotly_express as px


st.set_page_config("Agricultural land usage", layout="wide")
st.subheader("2022 Agricultural season land usage in Rwanda")
st.divider()


@st.cache_data
def load_land():
    return load_land_a(), load_and_b(), load_land_c()


@st.cache_data
def load_production():
    return load_crop_production_a(), load_crop_production_b(), load_crop_production_c()


@st.cache_data
def load_yield():
    return load_crop_yield_a(), load_crop_yield_b(), load_crop_yield_c()


@st.cache_data
def load_harvested():
    return load_harvested_a(), load_harvested_b(), load_harvested_c()


land_a_df, land_b_df, land_c_df = load_land()
production_a_df, production_b_df, production_c_df = load_production()
yield_a_df, yield_b_df, yield_c_df = load_yield()
harvested_a, harvested_b, harvested_c = load_harvested()
#a = harvested_a.columns.to_list()[24]
#st.write(a)
#st.write(len(a))
#st.write(1)
#st.write(harvested_b.columns.to_list())
#st.write(harvested_c.columns.to_list())


@st.cache_data
def processing(land_df, production_df, yield_df, season_name):
    st.write(season_name)

    def cards():
        max_land = land_df.max().max()
        max_land_district = land_df[land_df == max_land].stack().index[0][1]
        max_land_crop = land_df[land_df == land_df.max().max()].stack().index[0][0]
        ####
        max_production = production_df.max().max()
        max_pro_district = production_df[production_df == max_production].stack().index[0][1]
        max_pro_crop = production_df[production_df == production_df.max().max()].stack().index[0][0]
        ###
        max_yield = yield_df.max().max()
        max_yield_district = yield_df[yield_df == max_yield].stack().index[0][1]
        max_yield_crop = yield_df[yield_df == yield_df.max().max()].stack().index[0][0]
        #st.write(max_land_crop)
        card_1, card_2, card_3, card_4 = st.columns(4)
        card_1.metric("Top Land Usage (Hectars):", value=f"{max_land:,.2f}",
                      delta=f"{max_land_district}  {max_land_crop.upper()}")
        card_2.metric("Top Production (in MT)", value=f"{max_production:,.2f}",
                      delta=f"{max_pro_district}  {max_pro_crop.upper()}")
        card_3.metric("Top Average Yield (in kg/Ha)", value=f"{max_yield:,.2f}",
                      delta=f"{max_yield_district}  {max_yield_crop.upper()}")
        card_4.metric("Total land used Nation Wide", value=0, delta="Total")
        style_metric_cards(background_color="#696865")


    cards()
    st.write("")
    st.write("")
    st.write("")
    # plotting barchart and pie chart representation of data
    land_fig = px.bar(land_df, barmode="group", y=land_df.columns.to_list(), x=land_df.index.to_list(),
                     title="land used vs crop grown by Districts")
    land_fig.update_layout(xaxis_title="CROP", yaxis_title="LAND USED (in ha)")
    land_fig.update_layout(yaxis=dict(dtick=250), height=600)
    # processing and plotting the graph for the creop production
    production_fig = px.bar(production_df, barmode="group", y=production_df.columns.to_list(),
                            x=production_df.index.to_list(), title="various crop production by district")
    # processing and plotting the garph for the the yield

    yield_fig = px.bar(yield_df, barmode="group", y=yield_df.columns.to_list(), x=yield_df.index.to_list(),
                      title="Average crop yield by district(kg/Ha)")



    tab1, tab2, tab3 = st.tabs([":bar_chart: Land Usage(in hectars)", ":bar_chart: Crop production(in MegaTonne)",
                                ":bar_chart: Average crop yield by district(kg/Ha)"])
    with tab1:
        with st.expander("see Table"):
            st.dataframe(land_df, use_container_width=True)
        st.plotly_chart(land_fig, use_container_width=True)
        st.caption("                    testing caption")
    with tab2:
        with st.expander("see Table"):
            st.dataframe(production_df, use_container_width=True)
        st.plotly_chart(production_fig, use_container_width=True)
    with tab3:
        with st.expander("See Table"):
            st.dataframe(yield_df, use_container_width=True)
        st.plotly_chart(yield_fig, use_container_width=True)

    st.divider()



with st.sidebar:
    season = option_menu("SEASONS",
                         ["Season A", "Season B", "Season C"],
                         menu_icon="house")


if season == "Season A":
    land_df = land_a_df
    production_df = production_a_df
    production_df.drop(32)
    production_df.drop(33)
    yield_df = yield_a_df
    name = "Season A"
    land_df = land_df.drop(32)
    land_df.set_index("District", inplace=True)
    production_df.set_index("District", inplace=True)
    yield_df.set_index("District", inplace=True)
    with st.sidebar:
        st.subheader("Filter")
        districts = st.multiselect("District", land_df.index, default=[land_df.index[0], land_df.index[1], land_df.index[2],
                                                                       land_df.index[3], land_df.index[4]])
        crops = st.multiselect("Crops", land_df.columns, default=[land_df.columns[0], land_df.columns[1], land_df.columns[2]])
    if districts and crops:
        # create dataframe with the selected crops and Districts
        land_df = land_df.loc[districts, crops]
        production_df = production_df.loc[districts, crops]
        yield_df = yield_df.loc[districts, crops]
    processing(land_df, production_df, yield_df, name)
elif season == "Season B":
    land_df = land_b_df
    production_df = production_b_df
    production_df.drop(32)
    production_df.drop(33)
    yield_df = yield_b_df
    name = "Season B"
    land_df = land_df.drop(32)
    land_df.set_index("District", inplace=True)
    production_df.set_index("District", inplace=True)
    yield_df.set_index("District", inplace=True)
    with st.sidebar:
        st.subheader("Filter")
        districts = st.multiselect("District", land_df.index,
                                   default=[land_df.index[0], land_df.index[1], land_df.index[2],
                                            land_df.index[3], land_df.index[4]])
        crops = st.multiselect("Crops", land_df.columns,
                               default=[land_df.columns[0], land_df.columns[1], land_df.columns[2]])
    if districts and crops:
        # create dataframe with the selected crops and Districts
        land_df = land_df.loc[districts, crops]
        production_df = production_df.loc[districts, crops]
        yield_df = yield_df.loc[districts, crops]
    processing(land_df, production_df, yield_df, name)
    with st.container():
        col1, col2, col3 = st.columns([0.13, 0.74, 0.13])
        land = land_b_df
        land = land.drop(32)
        land.set_index("District", inplace=True)
        with col1:
            option = st.selectbox("chose a district", land.index.to_list())
        with col3:
            district = st.multiselect("select crop", land.columns.to_list(), default=[land.columns[0], land.columns[1],
                                                                                      land.columns[2]])
        ###########
        harvest = harvested_b
        harvest.set_index("District", inplace=True)
        #############
        row1 = land.loc[f"{option}"].rename(index="cultivated land")
        row1 = row1[0:23]
        row2 = harvest.loc[f"{option}"].rename(index="harvested land")
        row2 = row2[0:23]
        row2 = pd.DataFrame(row2)
        row1 = pd.DataFrame(row1)
        row2.index = row1.index.to_list()
        new_df = pd.concat([row1, row2], axis=1)
        st.write("")
        st.write("")
        st.write("")
        with col2:
            st.write(f"                       {option}")
            st.caption("testing caption")
            fig_1 = px.bar(new_df, x=new_df.index, y=["cultivated land", "harvested land"])
            st.plotly_chart(fig_1, use_container_width=True)
        with st.container():
            if district and option:
                new_df = new_df.loc[district, option]
            st.dataframe(new_df, use_container_width=True)


else:
    land_df = land_c_df
    production_df = production_c_df
    production_df.drop(32)
    production_df.drop(33)
    yield_df = yield_c_df
    name = "Season C"
    land_df = land_df.drop(32)
    land_df.set_index("District", inplace=True)
    production_df.set_index("District", inplace=True)
    yield_df.set_index("District", inplace=True)
    with st.sidebar:
        st.subheader("Filter")
        districts = st.multiselect("District", land_df.index,
                                   default=[land_df.index[0], land_df.index[1], land_df.index[5],
                                            land_df.index[3], land_df.index[4]])
        crops = st.multiselect("Crops", land_df.columns,
                               default=[land_df.columns[0], land_df.columns[1], land_df.columns[3]])
    if districts and crops:
        # create dataframe with the selected crops and Districts
        land_df = land_df.loc[districts, crops]
        production_df = production_df.loc[districts, crops]
        yield_df = yield_df.loc[districts, crops]
    processing(land_df, production_df, yield_df, name)






hide_default_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden}
                </style>
                """
st.markdown(hide_default_style, unsafe_allow_html=True)
