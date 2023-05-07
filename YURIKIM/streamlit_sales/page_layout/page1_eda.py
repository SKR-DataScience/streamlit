import streamlit as st
import numpy as np
import pandas as pd
import os
import sys
import plotly.express as px
from datetime import timedelta
import altair as alt

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# sys.path.append(os.getcwd())
import conf


# Define function for page 1
def page1():
    df = pd.read_csv(conf.sales)
    df_cols = ['invoice id', 'branch', 'time','customer type','gender','product line','quantity','gross income']
    df['time'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'], format='%m/%d/%Y %H:%M')
    df['date'] = pd.to_datetime(df['time'].dt.date)
    df = df.drop(columns = ['Date','Time']).rename(columns={'Total':'revenue'})
    df.columns = [i.lower() for i in df.columns]

    st.markdown("<h2 style='color: blue;'>계약 현황 & 매출 통계</h2>", unsafe_allow_html=True)
    # st.header("계약현황 & 매출 통계")
    min_date = df['date'].min()
    max_date = df['date'].max()
    
    # --------------------------- 1행 --------------------------- #
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('최근 일주일 계약 내역')
        # 조회일자
        start_date_col2, end_date_col2 = st.columns(2)
        with start_date_col2:
            start_date = st.date_input('계약 조회 시작일자', 
                                       value=(max_date -timedelta(days=7)).date(), 
                                       min_value=min_date.date(), 
                                       max_value=max_date.date())
        with end_date_col2:
            end_date = st.date_input('계약 조회 종료일자', 
                                     value=max_date.date(), 
                                     min_value=min_date.date(), 
                                     max_value=max_date.date())
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)
    
        # Check if the selected dates are within the range of dates in the DataFrame
        if start_datetime < min_date or end_datetime > max_date:
            st.warning(f"해당일자의 데이터는 존재하지 않습니다.")
        else:
            # Apply the filter condition to the DataFrame using boolean indexing
            filtered_df = df.loc[(df['date'] >= start_datetime) & (df['date'] <= end_datetime), df_cols].reset_index(drop=True)
            filtered_df.index = filtered_df.index + 1
            # Show the filtered DataFrame
            st.write('데이터 조회 결과:', filtered_df)

    with col2:
        st.subheader('일자 별 지점 매출 등락')
        # 조회일자
        start_date_col2, end_date_col2 = st.columns(2)
        with start_date_col2:
            start_date = st.date_input('매출 조회 시작일자', 
                                       value=(max_date -timedelta(days=7)).date(), 
                                       min_value=min_date.date(), 
                                       max_value=max_date.date())
        with end_date_col2:
            end_date = st.date_input('매출 조회 종료일자', 
                                     value=max_date.date(), 
                                     min_value=min_date.date(), 
                                     max_value=max_date.date())
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)

        # 조회지점 
        branch_options = np.sort(list(set(df['branch']))).tolist()
        selected_branches = st.multiselect('지점 선택(복수 선택 가능)', options = branch_options, default=branch_options[0])

        # Filter data by selected branches
        data_filtered = df[(df['branch'].isin(selected_branches)) & \
                           (df['date'] >= start_datetime) & (df['date'] <= end_datetime)].\
                               groupby(['branch','date'])['revenue'].sum().reset_index()

        # Create time series plot using Altair
        chart = alt.Chart(data_filtered).mark_line().encode(
            x=alt.X('date', title='일자', axis = alt.Axis(format='%Y-%m-%d')),
            y=alt.Y('revenue', title='일 매출'),
            color=alt.Color('branch', legend=alt.Legend(title='지점'))
        ).properties(
            width=600,
            height=400
        ).configure_legend(
            orient='top-left',
            symbolSize=150,
        ).configure_axis(
            labelAngle=270
        )

        # Display plot
        st.altair_chart(chart, use_container_width=True)

    # --------------------------- 2행 --------------------------- #
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader('상품군 별 매출 비율')
        
        # 조회일자
        start_date_col2, end_date_col2 = st.columns(2)
        with start_date_col2:
            start_date = st.date_input('상품군 매출 조회 시작일자', 
                                       value=(max_date -timedelta(days=7)).date(), 
                                       min_value=min_date.date(), 
                                       max_value=max_date.date())
        with end_date_col2:
            end_date = st.date_input('상품군 매출 조회 종료일자', 
                                     value=max_date.date(), 
                                     min_value=min_date.date(), 
                                     max_value=max_date.date())
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)
        
        # Group the dataframe by "branch" and "item" columns
        df_grouped = df[(df['date'] >= start_datetime) & (df['date'] <= end_datetime)].groupby(['branch', 'product line'])['revenue'].sum().reset_index()

        # Pivot the dataframe to create a stacked bar chart
        df_pivot = df_grouped.pivot_table(index='branch', columns='product line', values='revenue')

        # Draw the stacked bar chart using Streamlit
        st.bar_chart(df_pivot, width=0, height=0, use_container_width=True)

    with col4:
        st.subheader('고객군 별 매출 비율')
        
        # 조회일자
        start_date_col2, end_date_col2 = st.columns(2)
        with start_date_col2:
            start_date = st.date_input('고객군 매출 조회 시작일자', 
                                       value=(max_date -timedelta(days=7)).date(), 
                                       min_value=min_date.date(), 
                                       max_value=max_date.date())
        with end_date_col2:
            end_date = st.date_input('고객군 매출 조회 종료일자', 
                                     value=max_date.date(), 
                                     min_value=min_date.date(), 
                                     max_value=max_date.date())
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)
        
        # Group the dataframe by "branch" and "item" columns
        df_grouped = df[(df['date'] >= start_datetime) & (df['date'] <= end_datetime)].groupby(['branch','customer type', 'gender'])['revenue'].sum().reset_index().\
            assign(group = lambda x: x['customer type'] +'_' + x['gender'])
        # Pivot the dataframe to create a stacked bar chart
        df_pivot = df_grouped.pivot_table(index='branch', columns='group', values='revenue')

        # Draw the stacked bar chart using Streamlit
        st.bar_chart(df_pivot, width=0, height=0, use_container_width=True)

