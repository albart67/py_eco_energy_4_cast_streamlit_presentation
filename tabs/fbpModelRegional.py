import streamlit as st
import pandas as pd
import numpy as np
import json
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import cross_validation


title = "Regional energy production forecast with Facebook Prophet"
sidebar_name = "Regional production forecast"


def run():

    st.title(title)

    st.markdown("---")


    st.markdown(
        """
        Let's apply the Facebook Prophet model on regional energy production. How does the quality of this forecast compare with the national model?
        """
    )

    df_day = pd.read_csv('df_day.csv', sep =',', index_col='Unnamed: 0')
    df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date
    df_day[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']] = df_day[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']].apply(pd.to_numeric, errors='coerce')
    df_day[['month', 'year']] = df_day[['month', 'year']].apply(pd.to_numeric, errors='coerce')


    prod_type = st.selectbox(
        'Which energy do you want to display ?', ('Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'))
    st.write('You selected the energy:', prod_type)

    region = st.selectbox(
        'Which region do you want to display?', ('Pays de la Loire',
                                                                 'Normandie',
                                                                 'Grand Est',
                                                                 'Centre-Val de Loire',
                                                                 'Bourgogne-Franche-Comté',
                                                                 'Île-de-France',
                                                                 'Auvergne-Rhône-Alpes',
                                                                 'Bretagne',
                                                                 'Occitanie',
                                                                 'Hauts-de-France',
                                                                 "Provence-Alpes-Côte d'Azur",
                                                                 'Nouvelle-Aquitaine'))

    st.write('You selected the region:', region)

    def pred_plot_reg(reg, prod):
        df_pred = df_day[df_day['Région'] == reg].groupby(['Date'], as_index=False)[prod].sum()
        prophet_df = df_pred.rename(columns = {'Date' : 'ds', prod : 'y'})
        m = Prophet()
        m.fit(prophet_df)
        future = m.make_future_dataframe(periods = 365)
        forecast = m.predict(future)
        fig1 = m.plot(forecast)
        #fig2 = m.plot_components(forecast)
        df_cv = cross_validation(m, initial='2457 days', horizon = '615 days')
        df_p = performance_metrics(df_cv)
        st.write('Mean performance values :', df_p.mean())
        st.write(fig1)


    pred_plot_reg(region, prod_type)

    st.markdown(
        """
        Forecasting regional energy production is more complicated. 
        - Except for nuclear production and solar production in the southern regions MAPE is over 100%.
        - The energy exchange make series unstable.
        - Number of data are 12 times lower for region
        - Production for green energy grow up fast
        """
    )

