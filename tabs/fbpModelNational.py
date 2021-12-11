import streamlit as st
import pandas as pd
import numpy as np
import json
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import cross_validation


title = "National energy forecast with Facebook Prophet"
sidebar_name = "National energy forecast"


def run():

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        We have seen that consumption has a seasonal trend. We will use Facebook Prophet to
        forecast national electricity consumption and production.
        """
    )

    st.header('Consumption model')
    st.markdown("---")

    st.markdown(
        """
        Performance evaluation : 
        * 80 % of the daily consumption data for train
        * 20 % of the data (615 days) for test
        """
    )

    with open('serialized_model.json', 'r') as fin:
        m1 = model_from_json(json.load(fin))  # Load model

    #We use the cross validation method from fb prophet and take 80% (initial) of the datas for predict and 20% to test (horizon)
    df_cv = cross_validation(m1, initial='2457 days', horizon = '615 days')
    df_p = performance_metrics(df_cv)
    fig = plot_cross_validation_metric(df_cv, metric='mape')

    #st.write('Mean MAPE value :', df_p.mape.mean())
    st.write(fig)
    #st.write('Mean absolute percentage error :', round(df_p.mean().mape*100, 2), " %")

    st.markdown(
        '''
        The mean absolute percent error is '''+str(round(df_p.mean().mape*100, 2))+'''%. The seasonal trend results in good model efficiency.'''
    )

    #st.subheader("Consumption forecast and model decompositon")

    st.markdown(
        """
        * Forecasting of the 365 next days        
        * The black points are real values
        * In blue the model prediction
        """
    )

    #We want predict the consumption during one year after the end from our dataset. The make_future method create a dataframe
    future = m1.make_future_dataframe(periods = 365)
    forecast = m1.predict(future)
    fig1 = m1.plot(forecast)
    fig2 = m1.plot_components(forecast)
    st.write(fig1)

    st.markdown(
        """
        Facebook Prophet can decompose the model in 3 components
        """
    )

    st.write(fig2)



    st.header('Production model')
    st.markdown("---")
    
    st.markdown(
        """
        Same method with production
        """
    )

    df_day = pd.read_csv('df_day.csv', sep =',', index_col='Unnamed: 0')
    df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date
    df_day[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']] = df_day[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']].apply(pd.to_numeric, errors='coerce')
    df_day[['month', 'year']] = df_day[['month', 'year']].apply(pd.to_numeric, errors='coerce')




    with open('bioenergies_model.json', 'r') as fin:
        model_prod_bio = model_from_json(json.load(fin))  # Load model

    with open('ech_ physiques_model.json', 'r') as fin:
        model_ech = model_from_json(json.load(fin))  # Load model

    with open('eolien_model.json', 'r') as fin:
        model_prod_eol = model_from_json(json.load(fin))  # Load model

    with open('hydraulique_model.json', 'r') as fin:
        model_prod_hydr = model_from_json(json.load(fin))  # Load model

    with open('nucleaire_model.json', 'r') as fin:
        model_prod_nucl = model_from_json(json.load(fin))  # Load model

    with open('pompage_model.json', 'r') as fin:
        model_prod_pomp = model_from_json(json.load(fin))  # Load model

    with open('solaire_model.json', 'r') as fin:
        model_prod_sol = model_from_json(json.load(fin))  # Load model

    with open('thermique_model.json', 'r') as fin:
        model_prod_therm = model_from_json(json.load(fin))  # Load model



    prod_type = st.selectbox(
        'Which energy do you want to display?', ('Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'))
    st.write('You selected the energy:', prod_type)

    def prod_plot(prod):
        if prod == 'Thermique (MW)':
            m = model_prod_therm
        if prod_type == 'Nucléaire (MW)':
            m = model_prod_nucl
        if prod_type == 'Eolien (MW)':
            m = model_prod_eol
        if prod_type == 'Solaire (MW)':
            m = model_prod_sol
        if prod_type == 'Hydraulique (MW)':
            m = model_prod_hydr
        if prod_type == 'Pompage (MW)':
            m = model_prod_pomp
        if prod_type == 'Bioénergies (MW)':
            m = model_prod_bio
        future = m.make_future_dataframe(periods = 365)
        forecast = m.predict(future)
        fig1 = m.plot(forecast)
        #fig2 = m.plot_components(forecast)
        df_cv = cross_validation(m, initial='2457 days', horizon = '615 days')
        df_p = performance_metrics(df_cv)
        fig2 = plot_cross_validation_metric(df_cv, metric='mape')
        #st.write('Mean MAPE value :', df_p.mape.mean())
        
        st.write(fig1)
        st.write('Mean absolute percentage error:', (round(df_p.mean().mape, 2)*100), " %")
        #st.write(fig2)

    prod_plot(prod_type)

    st.markdown(
        """
        * The production forecast is not as accurate as for consumption -> less obvious seasonal pattern. 
        
        Trends:
        - Highest MAPEs for wind and solar (69% and 71 %), natural energies are unstable.
        - Best MAPE (16 %) for nuclear, controlable and stable.
        - Thermal energy has a high MAPE (67 %), backup energy.
        - Bioenergy has a good MAPE (7 %), low amplitude and stable production.
        
        """
    )

