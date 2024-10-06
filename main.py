import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit_extras
from Homepage import Home
from preprocessing import Preprocessing
from modelling import Clustering
from prediction import Prediction
from test import Plotting


def main():
    # setting the sidebar
    with st.sidebar:
        raw_data = st.file_uploader("Upload csv file")
        st.image("file.png", width=150)

    # Link to html code
    with open("style.html", "r") as html_file:
        html_content = html_file.read()
        st.sidebar.markdown(html_content, unsafe_allow_html=True)
    # Sign-out button
    if st.sidebar.button("Sign Out"):
        st.session_state.login_success = False
        st.session_state.animation = False
        st.session_state.tries = 4

    # Options menu
    options = option_menu(
        menu_title=None,
        options=["Home", "Preprocessing", "Clusterings", "Visualizations", "Predictions"],
        icons=["house    ", "hammer", "collection-fill", "pie-chart-fill", "gear-fill"],
        orientation="horizontal"
    )
    # Global variables

    if "preprocessed_data" not in st.session_state:
        st.session_state.preprocessed_data = None
    if "scaler" not in st.session_state:
        st.session_state.scaler = None
    if "labeller" not in st.session_state:
        st.session_state.labeller = None
    if "model" not in st.session_state:
        st.session_state.model = None

    # Pages --> Instantiations
    if raw_data:
        df = pd.read_csv(raw_data)
        if options == "Home Page":
            home = Home(df)
            home.datasetOverview()

        if options == "Preprocessing":
            preprocessing = Preprocessing(df)
            scale, label, data = preprocessing.text()
            st.session_state.scaler = scale
            st.session_state.labeller = label
            st.session_state.preprocessed_data = data
        if options == "Clustering":
            if st.session_state.labeller is not None and st.session_state.scaler is not None and st.session_state.preprocessed_data is not None:
                model = Clustering(st.session_state.preprocessed_data)
                m = model.text()
                st.session_state.model = m
            else:
                st.warning("Complete Preprocessing")
        if options == "Visualizations":
            visual = Plotting(st.session_state.preprocessed_data)
            visual.pairplot()
        if options == "Prediction":
            if st.session_state.model is not None:
                model_instance = Prediction(st.session_state.preprocessed_data, st.session_state.scaler,
                                            st.session_state.labeller, st.session_state.model)
                model_instance.cluster_predict()
            else:
                st.warning("Complete clustering")
    else:
        st.warning("No file uploaded")
