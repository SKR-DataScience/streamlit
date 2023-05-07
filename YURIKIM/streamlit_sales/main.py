import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import conf
from page_layout.page1_eda import page1
from page_layout.page2_ml import page2

# Define function for page 2
# def page2():
#     st.header("Page 2")
#     st.write("This is the content for Page 2.")
    
# Define function to display the selected page
def display_page(page_num):
    if page_num == 1:
        page1()
    elif page_num == 2:
        page2()
    
        
# Define app layout
st.set_page_config(page_title="매출관리 대시보드", page_icon=":guardsman:", layout="wide")
menu = ["계약 현황 & 매출 통계", "매출 예측"]
page_style = """
    background-color: #F0F0F0;
    border-radius: 10px;
    padding: 10px;
"""

page = st.sidebar.radio("조회할 페이지를 선택하세요.", menu)

# Display the selected page
if page == "계약 현황 & 매출 통계":
    display_page(1)
elif page == "매출 예측":
    display_page(2)
