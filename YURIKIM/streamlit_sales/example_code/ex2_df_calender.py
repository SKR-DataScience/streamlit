import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.getcwd())
import conf

df = pd.read_csv(conf.sales)
df_cols = ['invoice id', 'branch', 'time','customer type','gender','product line','gross income']
df['time'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'], format='%m/%d/%Y %H:%M')
df['date'] = pd.to_datetime(df['time'].dt.date)
df = df.drop(columns = ['Date','Time']).rename(columns={'Total':'revenue'})
df.columns = [i.lower() for i in df.columns]
# df = df.assign(revenue=lambda x: x['quantity']*x['unit price'],
#                    weekday = lambda x: x['date'].dt.day_name())

# Create a pandas DataFrame with some data
# df = pd.DataFrame({'date': ['2023-04-25', '2023-04-26', '2023-04-27', '2023-04-28', '2023-04-29'], 'value': [10, 20, 30, 40, 50]})

# Convert the date column to a datetime format
# df['date'] = pd.to_datetime(df['date'])

# Get the minimum and maximum dates in the DataFrame
min_date = df['date'].min()
max_date = df['date'].max()

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
