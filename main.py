#!/usr/bin/python3
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
# importing all the cleaned dataFrames
from data.loading import *
import plotly_express as px


st.set_page_config("2022 Agricultural Season", layout="wide")
st.title("Insight Of The 2022 Agricultural Season In Rwanda")
st.divider()
st.caption("use the sidebar to change the season")


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


LAND_A_USAGE_DF, LAND_B_USAGE_DF, LAND_C_USAGE_DF = load_land()

PRODUCTION_A_DF, PRODUCTION_B_DF, PRODUCTION_C_DF = load_production()

YIELD_A_DF, YIELD_B_DF, YIELD_C_DF = load_yield()

HARVESTED_A_DF, HARVESTED_B_DF, HARVESTED_C_DF = load_harvested()


@st.cache_data
def processing(land_df, production_df, yield_df):  # function to process the data and plot the 1st graphs

    def cards():  # processing the cards metrics
        maxTab, minTab = st.tabs(["max", "min"])
        max_land = land_df.max().max()
        min_land = land_df.min().min()
        max_land_district = land_df[land_df == max_land].stack().index[0][1]
        min_land_district = land_df[land_df == min_land].stack().index[0][1]
        max_land_crop = land_df[land_df == max_land].stack().index[0][0]
        min_land_crop = land_df[land_df == min_land].stack().index[0][0]
        #########
        max_production = production_df.max().max()
        min_production = production_df.min().min()
        max_pro_district = production_df[production_df == max_production].stack().index[0][1]
        min_pro_district = production_df[production_df == min_production].stack().index[0][1]
        max_pro_crop = production_df[production_df == max_production].stack().index[0][0]
        min_pro_crop = production_df[production_df == min_production].stack().index[0][0]
        ########
        max_yield = yield_df.max().max()
        min_yield = yield_df.min().min()
        max_yield_district = yield_df[yield_df == max_yield].stack().index[0][1]
        min_yield_district = yield_df[yield_df == min_yield].stack().index[0][1]
        max_yield_crop = yield_df[yield_df == max_yield].stack().index[0][0]
        min_yield_crop = yield_df[yield_df == min_yield].stack().index[0][0]

        with maxTab:
            card_1, card_2, card_3 = st.columns(3)
            card_1.metric("Top Land Usage (in Hectares):", value=f"{max_land:,.2f}",
                          delta=f"{max_land_district}  {max_land_crop.upper()}", help="Most land used to cultivate a "
                                                                                      "single crop amoung all the "
                                                                                      "selected districts ")
            card_2.metric("Top Production (in MT)", value=f"{max_production:,.2f}",
                          delta=f"{max_pro_district}  {max_pro_crop.upper()}", help="Greatest crop production amoung "
                                                                                    "all the selected crops and "
                                                                                    "districts")
            card_3.metric("Top Average Yield (in kg/Ha)", value=f"{max_yield:,.2f}",
                          delta=f"{max_yield_district}  {max_yield_crop.upper()}", help="Best average yield of crop "
                                                                                        "amoung all the selected "
                                                                                        "crops and districts")
            style_metric_cards(background_color="#696865")
        with minTab:
            card1, card2, card3 = st.columns(3)
            card1.metric("Least Land Usage (in Hectars):", value=f"{min_land:,.2f}",
                         delta=f"{min_land_district}  {min_land_crop.upper()}", delta_color="inverse",
                         help="least land sed to cultivate a single crop amoung all the selected districts")

            card2.metric("Least Production (in MT)", value=f"{min_production:,.2f}",
                         delta=f"{min_pro_district}  {min_pro_crop.upper()}", delta_color="inverse",
                         help="least crop production amoung all the selected crops and districts")

            card3.metric("Least Average Yield (in kg/Ha)", value=f"{min_yield:,.2f}",
                         delta=f"{min_yield_district}  {min_yield_crop.upper()}", delta_color="inverse",
                         help="worst average yield of crop amoung all the selected crops and districts")

    cards()

    # plotting bar chart  for land usage, crop production, and average yield data

    # land usage
    land_fig = px.bar(land_df, barmode="group", y=land_df.columns.to_list(), x=land_df.index.to_list(),
                      title="land used vs crop grown by Districts")
    land_fig.update_layout(xaxis_title="CROP", yaxis_title="LAND USED (in ha)")
    land_fig.update_layout(yaxis=dict(dtick=600), height=600)

    # crop production
    production_fig = px.bar(production_df, barmode="group", y=production_df.columns.to_list(),
                            x=production_df.index.to_list(), title="various crop production by district in (MT)")
    production_fig.update_layout(xaxis_title="CROP", yaxis_title="Crop production (in MegaTonnes)")
    production_fig.update_layout(yaxis=dict(dtick=600), height=600)

    # average yield
    yield_fig = px.bar(yield_df, barmode="group", y=yield_df.columns.to_list(), x=yield_df.index.to_list(),
                       title="Average crop yield by district(kg/Ha)")
    yield_fig.update_layout(xaxis_title="CROP", yaxis_title="Average yield (in Kg/Ha)")
    yield_fig.update_layout(yaxis=dict(dtick=600), height=600)

    tab1, tab2, tab3 = st.tabs([":bar_chart: crop Land Usage by district(in hectares)",
                                ":bar_chart: Crop production by district(in MegaTonne)",
                                ":bar_chart: Average crop yield by district(kg/Ha)"])

    # showing graphs under different Tabs
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

# sidebar: selecting the season data to display

with st.sidebar:
    season = option_menu("SEASONS",
                         ["Season A", "Season B", "Season C"],
                         menu_icon="house")


if season == "Season A":
    land_df = LAND_A_USAGE_DF
    land_df = land_df.drop(32)
    production_df = PRODUCTION_A_DF
    production_df = production_df.drop(32)
    production_df = production_df.drop(33)
    yield_df = YIELD_A_DF
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c2:
            st.header("Season A")

    land_df.set_index("District", inplace=True)
    production_df.set_index("District", inplace=True)
    yield_df.set_index("District", inplace=True)

    st.subheader("Filter")
    with st.container():
        ct1, ct2, ct3 = st.columns(3)
        with ct1:
            districts = st.multiselect("District", land_df.index, default=[land_df.index[0], land_df.index[1],
                                                                           land_df.index[2], land_df.index[4]])
        with ct3:
            crops = st.multiselect("Crops", land_df.columns, default=[land_df.columns[0], land_df.columns[5],
                                   land_df.columns[6], land_df.columns[8]])

    # assigning all the districts to the district variable if user clear the multiselect box
    if not districts:
        districts = land_df.index.to_list()[0:]

    # assigning all the districts to the district variable if user clear the multiselect box
    if not crops:
        crops = land_df.columns

    if districts or crops:
        # create dataframe with the selected crops and Districts
        land_df = land_df.loc[districts, crops]
        production_df = production_df.loc[districts, crops]
        yield_df = yield_df.loc[districts, crops]

    processing(land_df, production_df, yield_df)

    # processing and plotting the 2nd graph (cultivated land vs harvested land)
    with st.container():
        col1, col2, col3 = st.columns([0.15, 0.70, 0.15])
        land = LAND_A_USAGE_DF
        land = land.drop(32)
        land.set_index("District", inplace=True)
        with col1:
            districtA = st.selectbox("chose a district", land.index.to_list())
        with col3:
            cropsA = st.multiselect("select crops", land.columns.to_list(), default=[land.columns[0], land.columns[5],
                                                                                     land.columns[6]])
        harvest = HARVESTED_A_DF
        harvest.set_index("District", inplace=True)
        row1 = land.loc[f"{districtA}"].rename(index="cultivated land")
        row1 = row1[0:23]
        row2 = harvest.loc[f"{districtA}"].rename(index="harvested land")
        row2 = row2[0:23]
        row2 = pd.DataFrame(row2)
        row1 = pd.DataFrame(row1)
        row2.index = row1.index.to_list()
        new_df = pd.concat([row1, row2], axis=1)
        with col2:
            if cropsA and districtA:
                new_df = new_df.loc[cropsA]
            fig_1 = px.bar(new_df, x=new_df.index, y=["cultivated land", "harvested land"], title=f"cultivated land "
                                                                                                  f"vs harvested land"
                                                                                                  f" for various crop "
                                                                                                  f"in the {districtA} "
                                                                                                  f"district")
            fig_1.update_layout(yaxis=dict(dtick=300), height=700, width=400)
            fig_1.update_layout(xaxis_title="Crops", yaxis_title="land in (Ha)")
            st.plotly_chart(fig_1, use_container_width=True)
        with st.container():
            st.dataframe(new_df, use_container_width=True)
elif season == "Season B":
    land_df = LAND_B_USAGE_DF
    land_df = land_df.drop(32)
    production_df = PRODUCTION_B_DF
    production_df.drop(32)
    production_df.drop(33)
    yield_df = YIELD_B_DF
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c2:
            st.header("Season B")

    land_df.set_index("District", inplace=True)
    production_df.set_index("District", inplace=True)
    yield_df.set_index("District", inplace=True)

    st.subheader("Filter")
    with st.container():
        ct1, ct2, ct3 = st.columns(3)
        with ct1:
            districts = st.multiselect("District", land_df.index,
                                       default=[land_df.index[0], land_df.index[1], land_df.index[2],
                                                land_df.index[4]])
        with ct3:
            crops = st.multiselect("Crops", land_df.columns, default=[land_df.columns[0], land_df.columns[4],
                                                                      land_df.columns[7], land_df.columns[8]])

    # assigning all the districts to the district variable if user clear the multiselect box
    if not districts:
        districts = land_df.index.to_list()[0:]
    # assigning all the districts to the district variable if user clear the multiselect box
    if not crops:
        crops = land_df.columns

    if districts or crops:
        # create dataframe with the selected crops and Districts
        land_df = land_df.loc[districts, crops]
        production_df = production_df.loc[districts, crops]
        yield_df = yield_df.loc[districts, crops]
    processing(land_df, production_df, yield_df)
    with st.container():
        col1, col2, col3 = st.columns([0.15, 0.70, 0.15])
        land = LAND_B_USAGE_DF
        land = land.drop(32)
        land.set_index("District", inplace=True)
        with col1:
            districtA = st.selectbox("chose a district", land.index.to_list())
        with col3:
            cropsA = st.multiselect("select crops", land.columns.to_list(), default=[land.columns[0], land.columns[1],
                                                                                     land.columns[6]])
        harvest = HARVESTED_B_DF
        harvest.set_index("District", inplace=True)
        row1 = land.loc[f"{districtA}"].rename(index="cultivated land")
        row1 = row1[0:23]
        row2 = harvest.loc[f"{districtA}"].rename(index="harvested land")
        row2 = row2[0:23]
        row2 = pd.DataFrame(row2)
        row1 = pd.DataFrame(row1)
        row2.index = row1.index.to_list()
        new_df = pd.concat([row1, row2], axis=1)
        with col2:
            if cropsA and districtA:
                new_df = new_df.loc[cropsA]
            fig_1 = px.bar(new_df, x=new_df.index, y=["cultivated land", "harvested land"], title=f"cultivated land "
                                                                                                  f"vs harvested land"
                                                                                                  f" for various crop "
                                                                                                  f"in the {districtA} "
                                                                                                  f"district")
            fig_1.update_layout(yaxis=dict(dtick=500), height=600)
            fig_1.update_layout(xaxis_title="Crops", yaxis_title="land in (Ha)")
            st.plotly_chart(fig_1, use_container_width=True)
        with st.container():
            st.dataframe(new_df, use_container_width=True)


else:
    land_df = LAND_C_USAGE_DF
    land_df = land_df.drop(32)
    production_df = PRODUCTION_C_DF
    production_df.drop(32)
    production_df.drop(33)
    yield_df = YIELD_C_DF
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c2:
            st.header("Season C")

    land_df.set_index("District", inplace=True)
    production_df.set_index("District", inplace=True)
    yield_df.set_index("District", inplace=True)

    st.subheader("Filter")
    with st.container():
        ct1, ct2, ct3 = st.columns(3)
        with ct1:
            districts = st.multiselect("District", land_df.index,
                                       default=[land_df.index[0], land_df.index[1], land_df.index[2],
                                                land_df.index[4]])
        with ct3:
            crops = st.multiselect("Crops", land_df.columns, default=[land_df.columns[0], land_df.columns[5],
                                                                      land_df.columns[6],land_df.columns[7]])

    # assigning all the districts to the district variable if user clear the multiselect box
    if not districts:
        districts = land_df.index.to_list()[0:]
        print(districts)

    # assigning all the districts to the district variable if user clear the multiselect box
    if not crops:
        crops = land_df.columns

    if crops or districts:
        # create dataframe with the selected crops and Districts
        land_df = land_df.loc[districts, crops]
        production_df = production_df.loc[districts, crops]
        yield_df = yield_df.loc[districts, crops]
    processing(land_df, production_df, yield_df)

    with st.container():
        col1, col2, col3 = st.columns([0.15, 0.70, 0.15])
        land = LAND_C_USAGE_DF
        land = land.drop(32)
        land.set_index("District", inplace=True)
        with col1:
            districtA = st.selectbox("chose a district", land.index.to_list())
        with col3:
            cropsA = st.multiselect("select crops", land.columns.to_list(), default=[land.columns[0], land.columns[2],
                                                                                     land.columns[6]])
        harvest = HARVESTED_C_DF
        harvest.set_index("District", inplace=True)
        row1 = land.loc[f"{districtA}"].rename(index="cultivated land")
        row1 = row1[0:8]
        row2 = harvest.loc[f"{districtA}"].rename(index="harvested land")
        row2 = row2[1:9]
        row2 = pd.DataFrame(row2)
        row1 = pd.DataFrame(row1)
        row2.index = row1.index.to_list()
        new_df = pd.concat([row1, row2], axis=1)
        with col2:
            if cropsA and districtA:
                new_df = new_df.loc[cropsA]
            fig_1 = px.bar(new_df, x=new_df.index, y=["cultivated land", "harvested land"], title=f"cultivated land "
                                                                                                  f"vs harvested land"
                                                                                                  f" for various crop "
                                                                                                  f"in the {districtA} "
                                                                                                  f"district")
            fig_1.update_layout(yaxis=dict(dtick=200), height=600)
            fig_1.update_layout(xaxis_title="Crops", yaxis_title="land in (Ha)")
            st.plotly_chart(fig_1, use_container_width=True)
        with st.container():
            st.dataframe(new_df, use_container_width=True)


hide_default_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden}
                </style>
                """
st.markdown(hide_default_style, unsafe_allow_html=True)
