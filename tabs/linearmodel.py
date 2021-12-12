from re import template
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly_express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error



title = "Linear model"
sidebar_name = "Linear model"


def run():

    st.title(title)

    st.markdown("---")

    # Read the csv file
    daily_temper = pd.read_csv('df_t_dly.csv', sep = ',')

    # Scale the consumption values to GW 
    daily_temper['Consommation (MW)'] /= 1000

    # Make region selector
    regions = ['Auvergne-Rhône-Alpes', 'Bretagne', "Provence-Alpes-Côte d'Azur"]

    # Extract data for each region from df
    reg_1_x = daily_temper[daily_temper['region'] == regions[0]]['tmoy']
    reg_1_y = daily_temper[daily_temper['region'] == regions[0]]['Consommation (MW)']

    reg_2_x = daily_temper[daily_temper['region'] == regions[1]]['tmoy']
    reg_2_y = daily_temper[daily_temper['region'] == regions[1]]['Consommation (MW)']
    
    reg_3_x = daily_temper[daily_temper['region'] == regions[2]]['tmoy']
    reg_3_y = daily_temper[daily_temper['region'] == regions[2]]['Consommation (MW)']
    
    # Make a subplot for each region
    fig1 = make_subplots(rows=1, cols=3,
    subplot_titles=(regions[0], regions[1], regions[2]),
    shared_xaxes=True,
    print_grid=False
    )

    fig1.add_trace(
    go.Scatter(x = reg_1_x, y = reg_1_y, mode="markers+text"),
    row=1, col=1
    )

    fig1.add_trace(
    go.Scatter(x = reg_2_x, y = reg_2_y, mode="markers+text"),
    row=1, col=2
    )

    fig1.add_trace(
    go.Scatter(x = reg_3_x, y = reg_3_y, mode="markers+text"),
    row=1, col=3
    )

    fig1.update_xaxes(title_text="Mean temperature (°C)")
    fig1.update_yaxes(title_text="Energy comsumption (GW)", row=1, col=1)
    fig1.update_xaxes(showgrid=False, zeroline= False)
    fig1.update_yaxes(showgrid=False)
    fig1.update_layout(height=500, width=800, 
    title_text="Mean temperature & energy consumption (April 2019 - May 2021)",
        showlegend= False)
    
    st.write(fig1)

    
    # Polynomial model

    region = regions[0]

    temp = reg_1_x
    cons = reg_1_y

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(temp, cons, 
    test_size = .2, random_state = 321, shuffle = False
    )

    # Build a pipeline with scaler, polynomial features and linear regression
    scaler = StandardScaler()

    pol_feat = PolynomialFeatures(degree=2, include_bias=False)

    lin_reg = LinearRegression()

    pipe = Pipeline([('scaler', scaler), ("polynomial_features", pol_feat), ("linear_regression", lin_reg)])

    # Fit the pipeline
    pipe.fit(X_train[:, np.newaxis], y_train)

    # Predict the consumption based on the temperature in X_test
    pred = pipe.predict(X_train[:, np.newaxis])
    pred_test = pipe.predict(X_test[:, np.newaxis])

    # Create a dataframe to store the results in
    lin_res = pd.DataFrame(pred_test, columns = ['pred_test'])
    lin_res['X_test'] = X_test.values
    lin_res['y_test'] = y_test.values
    lin_res['squared errors'] = np.square(lin_res['y_test'] - lin_res['pred_test'])
    lin_res['percentage errors'] = (lin_res['y_test'] - lin_res['pred_test']) / lin_res['y_test']
    lin_res.sort_values(by = 'X_test', inplace = True)

    # Plot the results
    fig2 = make_subplots(rows=1, cols=1,
    )

    fig2.add_trace(
    go.Scatter(x = X_train, y = y_train, mode="markers", name="Train"),
    row=1, col=1
    )

    fig2.add_trace(
    go.Scatter(x = X_test, y = y_test, mode="markers", name="Test"),
    row=1, col=1
    )

    fig2.add_trace(
    go.Scatter(x = lin_res['X_test'], y = lin_res['pred_test'], mode = "lines", name="Model"),
    row=1, col=1
    )

    fig2.update_xaxes(title_text="Mean temperature (°C)")
    fig2.update_yaxes(title_text="Energy comsumption (GW)", row=1, col=1)
    fig2.update_xaxes(showgrid=False, zeroline= False)
    fig2.update_yaxes(showgrid=False)
    fig2.update_layout(height=500, 
    width=800, 
    showlegend= True, title_text=region
    )

    fig2.add_annotation(x=-3, y=350,
            text="Train R²: "+str(pipe.score(X_train[:, np.newaxis], y_train).round(2)),
            showarrow=False,
            align="left")

    fig2.add_annotation(x=-3, y=320,
            text="Test R²: "+str(pipe.score(X_test[:, np.newaxis], y_test).round(2)),
            showarrow=False,
            align="left")

    fig2.add_annotation(x=-3, y=290,
            text="Train RMSE: "+str(np.sqrt(mean_squared_error(y_train, pred)).round(1)),
            showarrow=False,
            align="left")

    fig2.add_annotation(x=-3, y=260,
            text="Test RMSE: "+str(np.sqrt(mean_squared_error(y_test, pred_test)).round(1)),
            showarrow=False,
            align="left")

    fig2.add_annotation(x=12.5, y=575,
            text="{} - {}x + {}x²".format(round(abs(lin_reg.intercept_),2), round(abs(lin_reg.coef_[0]),2), round(abs(lin_reg.coef_[1]),2)),
            showarrow=False,
            align="center")

    st.write(fig2)

    col1, col2, col3 = st.columns(3)
    col2.metric('Test R²', str(pipe.score(X_test[:, np.newaxis], y_test).round(2)*100)+' %')
    col3.metric('MAPE', str(round(abs(lin_res['percentage errors']).mean()*100,1))+' %')
    
    
    









