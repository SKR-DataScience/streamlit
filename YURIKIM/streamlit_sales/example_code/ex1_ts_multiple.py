import streamlit as st
import pandas as pd
import altair as alt
import os

# Load data
data = pd.read_csv(os.getcwd() + '/supermarket_sales - Sheet1.csv')
data['time'] = pd.to_datetime(data['Date'].astype(str) + ' ' + data['Time'], format='%m/%d/%Y %H:%M')
data['date'] = pd.to_datetime(data['time'].dt.date)
data = data.drop(columns = ['Date','Time']).rename(columns={'Total':'revenue'})
data.columns = [i.lower() for i in data.columns]

# Define branch options
branch_options = list(set(data['branch']))

# Create multi-select widget for selecting branches
selected_branches = st.multiselect('Select Branches', branch_options)

# Filter data by selected branches
data_filtered = data[data['branch'].isin(selected_branches)]

# Create time series plot using Altair
chart = alt.Chart(data_filtered).mark_line().encode(
    x='date',
    y='revenue',
    color='branch'
).properties(
    width=800,
    height=400
)

# Display plot
st.altair_chart(chart)
