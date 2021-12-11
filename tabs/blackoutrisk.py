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
     
    daily_shortage = daily_shortage[daily_shortage['Shortage'] > 0]

    daily_shortage['Shortage'] /= 2

    fig1 = px.line(daily_shortage,
                   x = 'Date', y = 'Shortage',
                   #range_y = [-10,10], 
                   title = 'National electricity shortage', 
                   labels = {'Shortage': 'MWh', 'Date':'Date'})

    fig1.update_xaxes(showgrid=False, zeroline= False)
    fig1.update_yaxes(showgrid=False, zeroline= False)
    
    fig1.update_layout(showlegend=False)
    st.write(fig1)

    max_val = daily_shortage['Shortage'].max()
    max_date = daily_shortage[daily_shortage['Shortage'] == max_val]['Date']
    max_2_person_households = int(round(max_val*1000 / 5.5,0))

    st.markdown(
    '''
    * Energy shortage is the difference between energy supply and energy consumption.
    * The maximum value is '''+str(max_val)+''' MWh on '''+str(pd.to_datetime(max_date[1655]).month_name())+''' '''+str(pd.to_datetime(max_date[1655]).day)+str(', ')+str(pd.to_datetime(max_date[1655]).year)+str('.')+'''
    * On this date, '''+str(max_2_person_households)+''' two-person households would theoretically suffer from energy shortage.
    '''
     )
   
   
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
                      category_orders = {'warm_month': ['0.0','1.0']})
    
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

    st.markdown(
    '''
    * We define regional blackout risk as the number of persons that are affected from energy shortage in that region.
    * The number of persons affected equals regional energy shortage divided by the average electricity consumption per person in this region. 
    * During warm month (May - September), the effect of energy shortage affects a higher number of people than during colder months.
    * Possible explanation: Energy suppliers expect lower consumption during summer and therefore supply lower amounts of energy, which could lead to energy shortage when consumption peaks unexpectedly.
    * Centre-Val de Loire, as an energy exporter, has a higher risk of energy shortage at low values of energy consumption compared with other regions.
    '''
    )