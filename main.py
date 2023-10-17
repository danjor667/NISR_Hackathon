#!/usr/bin/python3

import streamlit as st
from data.loading import load_season_a, load_season_b, load_season_c
import plotly_express as px

st.set_page_config(layout="wide")


@st.cache_data
def load():
    return load_season_a(), load_season_b(), load_season_c()


season_A, season_B, season_C = load()


st.title("insight of the 2022 agricultural season in Rwanda:bar_chart:")
graph = st.selectbox("season", ("season A", "season B", "season C"))
st.sidebar.header("filter")

with st.sidebar:
    districts = st.multiselect("Select Districts", season_A["District"].tolist())
    crops = st.multiselect("Select Crop", season_A.columns.tolist()[1:-1], default=season_A.columns.tolist()[1:-1])
if districts and crops:
    new_df = season_A.loc[season_A["District"].isin(districts), crops]
else:
    new_df = season_A

season_A_fig1 = season_A.drop("Total developed land", axis=1).drop(32).melt(id_vars='District', var_name='Crop',value_name='Land_Used')
fig_1 = px.line(season_A_fig1, x='Crop', y='Land_Used', color='District',
                title='Land Used vs Various Crop Grown by District SEASON A 2022')
fig_1.update_layout(yaxis=dict(dtick=1000), height=600, width=800)

season_A_fig2 = season_A.drop(32).drop("Total developed land", axis=1).melt(id_vars='District', var_name="Crop",
                                                                            value_name='Land_used')
fig_2 = px.pie(season_A_fig2, values='Land_used', names='Crop', color='Crop',
               title='percentage of land used by each crop Nation-wide')
fig_2.update_traces(textinfo=None, textposition="inside")

with st.container():
    if graph == "season A":
        with st.expander("see DataFrame"):
            st.dataframe(new_df, use_container_width=True)
    col1, col2 = st.columns([0.62, 0.38], gap="medium")

with col1:
    if graph == "season A":
        st.plotly_chart(fig_1, use_container_width=True)
    else:
        st.write("not yet done")

with col2:
    if graph == "season A":
        st.plotly_chart(fig_2, use_container_width=True)
    else:
        st.write("not yet done")
