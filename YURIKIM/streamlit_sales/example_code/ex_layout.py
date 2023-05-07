import streamlit as st
import pandas as pd
import plotly.express as px

# Create a pandas DataFrame with some data
df = pd.DataFrame({'date': ['2023-04-25', '2023-04-26', '2023-04-27', '2023-04-28', '2023-04-29'], 'value': [10, 20, 30, 40, 50]})

# Convert the date column to a datetime format
df['date'] = pd.to_datetime(df['date'])

# Get the minimum and maximum dates in the DataFrame
min_date = df['date'].min()
max_date = df['date'].max()

# Create a layout with four cells
row1 = st.columns((2, 2))
cell_11 = row1[0]
cell_12 = row1[1]
row2 = st.columns((2, 2))
cell_21 = row2[0]
cell_22 = row2[1]

# Add the DataFrame to the first cell
# Add the filtered DataFrame to the first cell
with cell_11:
    st.write("")
with cell_12:
    st.write("")

with cell_11:
    st.subheader('Filtered DataFrame')
    # Get the user input for the date range
    start_date = st.date_input('Start date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input('End date', min_value=min_date, max_value=max_date, value=max_date)
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date)
    # Filter the DataFrame based on the date range
    filtered_df = df[(df['date'] >= start_datetime) & (df['date'] <= end_datetime)]
    # Show a warning message if the date range is invalid
    if filtered_df.empty:
        st.warning('No data available for the selected date range.')
    # Show the filtered DataFrame
    else:
        st.write(filtered_df)

# Add a line chart to the second cell
with cell_12:
    st.subheader('Line Chart')
    fig = px.line(df, x='date', y='value')
    st.plotly_chart(fig)

# Add a bar chart to the third cell
with cell_21:
    st.subheader('Bar Chart')
    fig = px.bar(df, x='date', y='value')
    st.plotly_chart(fig)

# Add a scatter chart to the fourth cell
with cell_22:
    st.subheader('Scatter Chart')
    fig = px.scatter(df, x='date', y='value')
    st.plotly_chart(fig)
