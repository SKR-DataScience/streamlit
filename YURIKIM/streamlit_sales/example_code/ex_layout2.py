import streamlit as st
import pandas as pd
import plotly.express as px
import os

df = pd.read_csv(os.getcwd()+'/supermarket_sales - Sheet1.csv')
df_cols = ['invoice id', 'branch', 'time','customer type','gender','product line','gross income']
df['time'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'], format='%m/%d/%Y %H:%M')
df['date'] = pd.to_datetime(df['time'].dt.date)
df = df.drop(columns = ['Date','Time']).rename(columns={'Total':'revenue'})
df.columns = [i.lower() for i in df.columns]
df = df.assign(revenue=lambda x: x['quantity']*x['unit price'],
                   weekday = lambda x: x['date'].dt.day_name())

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

with cell_21:
    start_date_col, end_date_col = st.columns(2)
    # Add a date input widget to set the filter condition for start date
    with start_date_col:
        start_date = st.date_input('조회 시작일자', value=min_date.date(), min_value=min_date.date(), max_value=max_date.date())

    # Add a date input widget to set the filter condition for end date
    with end_date_col:
        end_date = st.date_input('조회 종료일자', value=max_date.date(), min_value=min_date.date(), max_value=max_date.date())


    # Convert the date input to datetime objects
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date)

    # Check if the selected dates are within the range of dates in the DataFrame
    if start_datetime < min_date or end_datetime > max_date:
        st.warning(f"해당일자의 데이터는 존재하지 않습니다.")
    else:
        # Apply the filter condition to the DataFrame using boolean indexing
        filtered_df = df.loc[(df['date'] >= start_datetime) & (df['date'] <= end_datetime), df_cols]

        # Show the filtered DataFrame
        st.write('데이터 조회 결과:', filtered_df)

# Create a pandas DataFrame with some data
df = pd.DataFrame({'date': ['2023-04-25', '2023-04-26', '2023-04-27', '2023-04-28', '2023-04-29'], 'value': [10, 20, 30, 40, 50]})

# Convert the date column to a datetime format
df['date'] = pd.to_datetime(df['date'])

# Add a line chart to the second cell
with cell_11:
    st.subheader('Line Chart')
    fig = px.line(df, x='date', y='value')
    st.plotly_chart(fig, margin=dict(l=10, r=10, t=10, b=10))

# Add a bar chart to the third cell
with cell_21:
    st.subheader('Bar Chart')
    fig = px.bar(df, x='date', y='value')
    st.plotly_chart(fig)

# Add a scatter chart to the fourth cell
with cell_22:
    st.subheader('Scatter Chart')
    fig = px.scatter(df, x='date', y='value')
    st.plotly_chart(fig, margin=dict(l=10, r=10, t=10, b=10))
