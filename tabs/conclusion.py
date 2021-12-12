import streamlit as st


title = "Conclusion"
sidebar_name = "Conclusion"


def run():

    st.title(title)
    st.header('Good forecasts of green energy production will be a key factor for the ongoing energy transition!')

    st.markdown("---")

    st.markdown(
        """

        * We have learned a lot ... including what not worked.

        * We could apply working time series and linear model.

        * Importance of includng additional data for green energy (temperature data)

        * Importantce of regional model.

        How could we continue?
        - Larger weather dataset (local wind speeds, sunshine hours, ...).
        - Economic data about energy investment in each region.
        
        """

    )

    
