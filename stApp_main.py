import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_extras.dataframe_explorer import dataframe_explorer 

st.set_page_config(
    page_title="Prediction Dashboard",
    page_icon=":bar_chart",
    layout="wide"
)

st.title("Prediction Output Dashboard")
st.write("Prototype v0.2.1_")

@st.cache_data
def load_data(path: str):
    data = pd.read_csv(path, sep='\t', index_col=0, header=0)
    ##perform more data cleaning here
    return data

with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is None:
    st.info(" Upload a file through config", icon="ℹ️")
    st.stop()

dF = load_data(uploaded_file)

filter_dF = dataframe_explorer(dF, case=False)

with st.expander("Data Explorer"):
    st.dataframe(filter_dF, use_container_width=True)

day = st.slider("Choose how many days ahead to plot", 1, 30, 10)

alpha = pd.to_numeric(dF[f'prediction_change{day}d'])
beta = pd.to_numeric(dF[f'relative_avgOpenClose_ahead{day}'])


def plot_prediction_treemap():
    fig = px.treemap(dF, path=[px.Constant("S&P 500"), 'EOD_underlying_stock_sector',
                               'EOD_underlying_stock_industry', 'EOD_option_underlying_ticker'], values=alpha,
                               hover_data=[f'relative_avgOpenClose_ahead{day}'],
                               color=np.abs(alpha - beta),
                               color_continuous_scale='RdBu_r',
                               color_continuous_midpoint=0
    )
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig, use_container_width=True)

def plot_changes_treemap():
    fig = px.treemap(dF, path=[px.Constant("S&P 500"), 'EOD_underlying_stock_sector',
                               'EOD_underlying_stock_industry', 'EOD_option_underlying_ticker'], values='EOD_underlying_total_volume',
                               hover_data=[f'relative_avgOpenClose_ahead{day}'],
                               color=(beta),
                               color_continuous_scale='RdYlGn',
                               color_continuous_midpoint=np.average(beta)
    )
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig, use_container_width=True)

st.write(f"Prediction Treemap +{day} Days")
plot_prediction_treemap()
st.write(f"Actual Future Changes +{day} Days")
plot_changes_treemap()