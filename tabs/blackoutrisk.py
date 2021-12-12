import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly_express as px
import plotly.graph_objects as go


title = "Blackout risk"
sidebar_name = "Blackout risk"


def run():

    st.title(title)

    st.markdown("---")

    # Read the csv file
    daily_shortage = pd.read_csv('daily_shortage.csv', 
                                 sep = ',')
     
    daily_shortage_pos = daily_shortage[daily_shortage['Shortage'] > 0]

    daily_shortage_pos['Shortage'] /= 2

    max_val = daily_shortage_pos['Shortage'].max()
    max_date = daily_shortage_pos[daily_shortage_pos['Shortage'] == max_val]['Date']
    # https://en.selectra.info/energy-france/guides/tips/bills/average: 
    # 2 person household electricity consumption: 1669 kWh / year
    max_2_person_households = int(round(max_val*1000 / (1669/365),0))

    fig1 = px.line(daily_shortage_pos,
                   x = 'Date', y = 'Shortage',
                   #range_y = [-10,10], 
                   title = 'National electricity shortage', 
                   labels = {'Shortage': 'MWh', 'Date':'Date'},
                   width=800)

    fig1.update_xaxes(showgrid=False, zeroline= False)
    fig1.update_yaxes(showgrid=False, zeroline= False)
    
    fig1.update_layout(showlegend=False)
    
    st.write(fig1)
    
    col1, col2, col3, col4 = st.columns(4)
    col2.metric('Shortage days', str(round(len(daily_shortage_pos) / len(daily_shortage)*100,1))+' %')
    col3.metric('Max shortage', str(max_val)+' MWh')
    col4.metric('Max 2P households', str(max_2_person_households))    

    
    ##############################
    # Read a file for second chart
    df_blackout = pd.read_csv('df_blackout.csv', sep = ',', index_col='Unnamed: 0')

    # Select one region
    regions = ['Bretagne', 'Nouvelle-Aquitaine', 'Île-de-France',
       'Auvergne-Rhône-Alpes', 'Normandie', 'Bourgogne-Franche-Comté',
       'Centre-Val de Loire', 'Grand Est', 'Hauts-de-France',
       'Pays de la Loire', 'Occitanie', "Provence-Alpes-Côte d'Azur"]
    region = regions[6]

    # Compute the data
    df_blackout_region = df_blackout[(df_blackout['Région'] == region) & (df_blackout['Person Blackout'] > 0) & (pd.to_datetime(df_blackout['Date']).dt.year > 2013)]
    
    # Modify the df for plotting
    plot_df = pd.DataFrame(df_blackout_region[['Consommation (MW)','Person Blackout','warm month']])
    plot_df['Consommation (MW)'] = plot_df['Consommation (MW)']/1000/2
    plot_df = plot_df.rename(mapper={'Consommation (MW)':'Electricity consumption (GWh)', 
    'Person Blackout': 'Persons affected', 'warm month': 'warm_month'}, axis = 1)
    plot_df = plot_df.astype({'warm_month':'str'})

    # Plot the data
           
    fig2 = px.scatter(plot_df, 
                      x = 'Electricity consumption (GWh)', 
                      y = 'Persons affected',
                      color = 'warm_month', 
                      title = 'Regional blackout risk for '+ region,
                      labels={"warm_month": '',},
                      category_orders = {'warm_month': ['0.0','1.0']},
                      width=800)
    
    fig2.update_xaxes(showgrid=False, zeroline= False)
    fig2.update_yaxes(showgrid=False, zeroline= False)
    fig2.update_layout(legend=dict(y=0.97, x=0.78))

    newnames = {'0.0':'Cold month', '1.0': 'Warm month'}
    fig2.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
    st.write(fig2)
    
    col1, col2, col3, col4 = st.columns(4)
    col2.metric('Max persons', int(round(plot_df['Persons affected'].max(),0)))
    col3.metric('> 500 persons', str(len(plot_df[plot_df['Persons affected']>500]))+' days')
    col4.metric('> 500 persons', str(round(len(plot_df[plot_df['Persons affected']>500])/len(plot_df['Persons affected'])*100,1))+' %')