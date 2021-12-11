import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly_express as px
import json

title = "Regional consumption and supply"
sidebar_name = "Regional evolution"


def run():

    # TODO: choose between one of these GIFs
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/1.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        - A color map allows us to get a view on electricity consumption and supply by regions.
        
        - Shifting the year selection from left to right displays the evolution over time.
        
        - The color map from energy exchanges (Ech. physiques) shows the main energy flows between regions.
        """
    )

    df_maps = pd.read_csv('df_map.csv', sep =',', index_col='Unnamed: 0')
    #df_maps['year'] = pd.to_datetime(df_maps['year']).dt.date
    df_maps[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']] = df_maps[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']].apply(pd.to_numeric, errors='coerce')
    df_maps[['year']] = df_maps[['year']].apply(pd.to_numeric, errors='coerce')
    df_maps.rename({'Code INSEE région': 'code'}, axis=1, inplace=True)
    #st.write(df_maps)

    france_reg = json.load(open("regions.geojson", "r"))
    sf = gpd.read_file('regions.geojson')
    df1 = sf[0:9]
    df2 = sf[14:17]
    gdf = pd.concat([df1, df2])
    gdf["code"] = pd.to_numeric(gdf["code"])
    jf = gdf.merge(df_maps, left_on='code', right_on='code')
    #st.write(jf)

    option = st.selectbox(
         'Which parameter do you want to display?', ('Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)'))
    st.write('You selected:', option)

    year = st.select_slider(
         'Which year do you want to display?',
                 options=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])
    st.write('You selected year: ', year)

    """
    year = st.selectbox(
        'Which year do you want to display ?', (2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021))
    st.write('You selected the year:', year)
    """
    def plot_map(param):
            jf_year = jf[jf['year'] == year]
            fig = px.choropleth_mapbox(jf_year, geojson=france_reg, locations='code',
                        color= param,
                        color_continuous_scale ='YlOrRd',
                        #color_continuous_scale="Viridis",
                        #range_color=(0, 68e6),
                        #scope="europe",
                        featureidkey="properties.code",
                        #projection="mercator",
                        labels={ param, 'unemployment rate'},
                        #color_continuous_scale=px.colors.diverging.BrBG,
                        mapbox_style="carto-positron", zoom=3.8,
                        center={"lat": 47, "lon": 2},
                        #opacity = 0.8
                        )
            #48°52'N et 2°19'
            #46° 36′ 22″ N, 1° 52′ 31″

            #            projection="mercator")
            fig.update_geos(fitbounds="locations", visible=False)

            #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.write(fig)

    plot_map(option)


    df_day = pd.read_csv('df_day.csv', sep =',', index_col='Unnamed: 0')
    df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date
    df_day[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']] = df_day[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']].apply(pd.to_numeric, errors='coerce')
    df_day[['month', 'year']] = df_day[['month', 'year']].apply(pd.to_numeric, errors='coerce')
    df_cons_day = df_day.groupby(['Date'], as_index= False)['Consommation (MW)'].sum()


    st.markdown(
        """
        With the menu below, choose which parameter and region you want to display on a date axis.
        """
    )

    prod_type2 = st.selectbox(
        'Which parameter do you want to display?', ('Consommation (MW)','Nucléaire (MW)', 'Thermique (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'))
    st.write('You selected:', prod_type2)

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

    def prod_plot_reg(prod, reg):
        df_day_reg = df_day[df_day['Région'] == reg]
        df_cons_day = df_day_reg.groupby(['Date'], as_index= False)[prod].sum()
        #st.write(df_day)

        fig = px.line(df_cons_day, x='Date', y= prod, width = 850, height=500 )
        fig.update_xaxes(showgrid=False, zeroline= False)
        fig.update_yaxes(showgrid=False)
        ts_chart = st.plotly_chart(fig)

    prod_plot_reg(prod_type2, region)






