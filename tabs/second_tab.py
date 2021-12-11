import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go



title = "Data analysis"
sidebar_name = "Data analysis"



def run():


    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        Let's start with exploring the dataset!
        """
    )

    df_day = pd.read_csv('df_day.csv', sep =',', index_col='Unnamed: 0')
    df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date
    df_day[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']] = df_day[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']].apply(pd.to_numeric, errors='coerce')
    df_day[['month', 'year']] = df_day[['month', 'year']].apply(pd.to_numeric, errors='coerce')
    df_cons_day = df_day.groupby(['Date'], as_index= False)['Consommation (MW)'].sum()
    #st.write(df_day)

    st.header("Consumption")
    st.markdown("---")


    #Plot of the the global consumption
    fig2 = px.line(df_cons_day, x='Date', y='Consommation (MW)', width=850, height=500)
    fig2.update_xaxes(showgrid=False, zeroline= False)
    fig2.update_yaxes(showgrid=False)
    fig2.update_layout(title_text='National consumption from 2013 to 2021')
    ts_chart = st.plotly_chart(fig2)

    st.markdown(
        """
        * Clear seasonnality
        * Hi consumption in winter low in summer
        """
    )
    
    
    #ANALYSE AND BAX PLOT OF THE GLOBAL CONSUMPTION INTO ONE WEEK
    df_cons_day2 = df_day.groupby(['Date','weekday'],as_index=False)['Consommation (MW)'].sum()
    fig3 = px.box(df_cons_day2, x='weekday', y = 'Consommation (MW)', width = 800, height= 500)
    fig3.update_traces(marker_color='darkblue')
    fig3.update_xaxes(title_text='', showgrid=False, zeroline= False)
    fig3.update_yaxes(showgrid=False)
    fig3.update_layout(title_text='National weekly consumption range')
    #fig3.update_xaxes(type='category')
    st.write(fig3)
    st.markdown(
        """
        * Consumption is about 10% lower on weekends.
        """
    )

    #COMPARISON OF THE DAILY CONSUMPTION RANGE BY REGION
    #We group the consumption by region and by date and make the daily sum
    df_cons_day3 = df_day.groupby(['Région', 'Date'],as_index=False)['Consommation (MW)'].sum()
    #consumption range plot
    fig_plot2 = px.box(df_cons_day3, x="Région", y="Consommation (MW)", width=850, height= 600)
    fig_plot2.update_traces(marker_color='green')
    fig_plot2.update_xaxes(title_text='', showgrid=False, zeroline= False)
    fig_plot2.update_yaxes(showgrid=False)
    fig_plot2.update_layout(title_text='Regional consumption range')
    st.write(fig_plot2)
    st.markdown(
        """
        * Île-de-France and Auvergne-Rhône-Alpes comsume the most electricity, 
        * Bourgogne-Franche-Conté and Centre-Val de Loire the least.
        """
    )



    st.header("Production")
    st.markdown('---')
    #st.subheader("National electricity production from 2013 to 2021")

    st.markdown(
        """
        With the menu below, choose which national electricity production you want to display.
        """
    )

    prod_type = st.selectbox(
        'Which electricity production do you want to display ?', ('Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)', 'Ech. physiques (MW)'))
    st.write('You selected:', prod_type)

    def prod_plot(prod):
        df_cons_day = df_day.groupby(['Date'], as_index= False)[prod].sum()
        #st.write(df_day)

        fig = px.line(df_cons_day, x='Date', y= prod, width = 850, height=500 )
        fig.update_xaxes(showgrid=False, zeroline= False)
        fig.update_yaxes(showgrid=False, zeroline= False)
        fig.update_layout(title_text='National electricity production from 2013 to 2021')
        ts_chart = st.plotly_chart(fig)

    prod_plot(prod_type)

    st.markdown(
        """
        * Stable evolution for thermal energy production.
        * Annual increase for wind, sun and bio energy, our green energies.
        * Annual decrease for nuclear energy.
        * The amplitude of energy exchange is increasing over time. 
        """
    )

    st.header("Regional comparison of energy production, consumption and exchange")
    st.markdown('---')



    fig10 = make_subplots(rows=1, cols=2)

    #Energy production repartition by region
    #We group the different columns of electricity productions by region and make the sum
    df_rep_reg = df_day.groupby(['Région'],as_index=False)['Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'].sum()
    pd.DataFrame(df_rep_reg).head()



    """
    fig10.add_trace(
        go.bar(df_rep_reg, x="Région", y=['Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Bioénergies (MW)'], width=850, height=720),
        row=1, col=1
    )
    """

    #st.write(fig)



    x= df_rep_reg['Région']
    fig13 = go.Figure(go.Bar(x=x, y=df_rep_reg['Eolien (MW)'], name='Eolien'))
    fig13.add_trace(go.Bar(x=x, y=df_rep_reg['Solaire (MW)'], name='Solaire'))
    fig13.add_trace(go.Bar(x=x, y=df_rep_reg['Nucléaire (MW)'], name='Nucléaire'))
    fig13.add_trace(go.Bar(x=x, y=df_rep_reg['Thermique (MW)'], name='Thermique'))
    fig13.add_trace(go.Bar(x=x, y=df_rep_reg['Hydraulique (MW)'], name='Hydraulique'))
    fig13.add_trace(go.Bar(x=x, y=df_rep_reg['Bioénergies (MW)'], name='Bioénergiues'))

    fig13.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'}, height=600, width=1100, title_text = 'Régional Energie Production Mix')
    st.write(fig13)
    """
    #st.subheader("Regional electricity consumption")
    #Energy consumption by region
    #We group the different columns of electricity consumption by region and make the sum
    df_reg_cons = df_day.groupby(['Région'], as_index = False)['Consommation (MW)'].sum()
    fig6 = px.bar(df_reg_cons, x = 'Région', y='Consommation (MW)', width=850, height=700);
    #st.write(fig6)

    #st.subheader("Regional electricity exchange")
    #Energy exchange by region
    #We group the different columns of electricity exchange by region and make the sum
    df_ech = df_day.groupby(['Région'],as_index=False)['Ech. physiques (MW)'].sum()
    fig7 = px.bar(df_ech, x = 'Région', y='Ech. physiques (MW)', width=850, height=700)
    fig7.update_traces(marker_color='green')
    #st.write(fig7)
    """
    df_reg_cons = df_day.groupby(['Région'], as_index = False)['Consommation (MW)'].sum()
    df_ech = df_day.groupby(['Région'],as_index=False)['Ech. physiques (MW)'].sum()
    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(
        go.Bar(x = df_reg_cons['Région'], y= df_reg_cons['Consommation (MW)']),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x = df_ech['Région'], y= df_ech['Ech. physiques (MW)']),
        row=1, col=2
    )

    fig.update_layout(height=500, width=1100, showlegend=False)
    #, title_text="Side By Side Subplots"
    st.write(fig)

    st.markdown(
        """
        * Nuclear still first from far
        * High consumption and low production like Île-de-France need to import electricity
        * Higher production than consumption in region -> capacity to export (Centre-Val de Loire, Grand-Est, Auvergne-Rhône Alpes)
        
        """
    )


