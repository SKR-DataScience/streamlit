from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.linear_model import Ridge
from functools import reduce

import os 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def prepare_data():
    df = pd.read_csv(os.getcwd()+'/data_sales.csv')

    df['time'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'], format='%m/%d/%Y %H:%M')
    df['date'] = pd.to_datetime(df['time'].dt.date)
    df = df.drop(columns = ['Date','Time']).rename(columns={'Total':'revenue'})
    df.columns = [i.lower() for i in df.columns]

    df = df.assign(revenue=lambda x: x['quantity']*x['unit price'],
                    weekday = lambda x: x['date'].dt.day_name())

    merge_col = ['branch','date']
    df_list = []
    for col in ['gender','product line']:
        df_list.append(
            df.groupby(merge_col + [col]).size().rename('size').reset_index().\
            pivot_table(index = ['branch','date'], columns=[col], values='size').fillna(0).reset_index()
        )
    for col in ['quantity','revenue']:
        df_list.append(
            df.groupby(merge_col)[col].sum().reset_index()
        )
    df_model = reduce(lambda df1,df2: pd.merge(df1,df2, on=['branch','date']), df_list)
    df_model['weekend'] = df_model['date'].apply(lambda x: 1 if x.weekday()>=5 else 0)
    df_model = reduce(lambda df1,df2: pd.merge(df1,df2, on=['branch','date']), df_list)
    return df_model

def page2():
    merge_col = ['branch','date']
    df_model = prepare_data()
    
    steps = 36
    shift = 7

    df_model_ = df_model[df_model['branch']=='A'].reset_index(drop=True)
    df_model_.loc[:,y_col] = df_model_[y_col].shift(-shift)
    df_model_.index = pd.date_range(min(df_model_['date']), max(df_model_['date']))

    df_train = df_model_.iloc[:-steps, :]
    df_test  = df_model_.iloc[-steps:, :]

    y_col = 'revenue'
    exog_col = [col for col in df_model.columns if col not in merge_col + [y_col]]


    forecaster = ForecasterAutoreg(
                        regressor = Ridge(),
                        lags      = 3
                    )

    forecaster.fit(
        y    = df_train[y_col],
        exog = df_train[exog_col]
    )

    steps = 36
    predictions = forecaster.predict(
                    steps = steps,
                    exog = df_test[exog_col]
                )
    # Add datetime index to predictions
    predictions = pd.Series(data=predictions, index=df_test.index)
    predictions.head(10)