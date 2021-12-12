from collections import OrderedDict

import streamlit as st
import pandas as pd
import plotly_express as px

# TODO : change TITLE, TEAM_MEMBERS and PROMOTION values in config.py.
import config

# TODO : you can (and should) rename and add tabs in the ./tabs folder, and import them here.
from tabs import intro, second_tab, maps, linearmodel, fbpModelNational, fbpModelRegional, fbpModelRegionalRegT,fbpModelRegionalProdRegT, blackoutrisk, conclusion


st.set_page_config(
    page_title=config.TITLE,
    page_icon="https://datascientest.com/wp-content/uploads/2020/03/cropped-favicon-datascientest-1-32x32.png",
)

with open("style.css", "r") as f:
    style = f.read()

st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)


# TODO: add new and/or renamed tab in this ordered dict by
# passing the name in the sidebar as key and the imported tab
# as value as follow :
TABS = OrderedDict(
    [
        (intro.sidebar_name, intro),
        (second_tab.sidebar_name, second_tab),
        (maps.sidebar_name, maps),
        (blackoutrisk.sidebar_name, blackoutrisk),
        (linearmodel.sidebar_name, linearmodel),
        (fbpModelNational.sidebar_name, fbpModelNational),
        (fbpModelRegional.sidebar_name, fbpModelRegional),
        (fbpModelRegionalRegT.sidebar_name, fbpModelRegionalRegT),
        (fbpModelRegionalProdRegT.sidebar_name, fbpModelRegionalProdRegT),
        (conclusion.sidebar_name, conclusion),
    ]

)


def run():
    st.sidebar.image(
        "https://dst-studio-template.s3.eu-west-3.amazonaws.com/logo-datascientest.png",
        width=200,
    )

    tab_name = st.sidebar.radio("", list(TABS.keys()), 0)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"## {config.PROMOTION}")

    st.sidebar.markdown("### Team members:")
    for member in config.TEAM_MEMBERS:
        st.sidebar.markdown(member.sidebar_markdown(), unsafe_allow_html=True)

    tab = TABS[tab_name]

    tab.run()


if __name__ == "__main__":
    run()


