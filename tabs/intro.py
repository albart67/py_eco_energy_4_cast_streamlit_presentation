import streamlit as st


title = "Py Eco Energy 4 cast project"
sidebar_name = "Introduction"


def run():

    # TODO: choose between one of these GIFs
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/1.gif")
    st.image("windturbinebyRichardPaterson.gif", caption='© Richard Paterson')
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        Our project's scope is to analyze an energy (electricity) dataset for France.
        
        The data source is the RTE website Eco2mix. RTE is the manager of the electricity transmission network, 
        ensuring the balance between production and consumption every second in France.
        
        Dataset link: https://opendata.reseaux-energies.fr/explore/dataset/eco2mix-regional-cons-def/information/?disjunctive.libelle_region&disjunctive.nature&sort=-date_heure
               
        Our goal is to come up with data analysis ideas and visualizations which provide useful information to 
        stakeholders of the energy transition towards a future with more green energy.
        

        """

    )
