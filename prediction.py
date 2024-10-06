import numpy as np
import streamlit as st


class Prediction:
    def __init__(self, dataframe, scaler, labeller, model):
        self.data = dataframe
        self.scaler = scaler
        self.labeller = labeller
        self.model = model

    def cluster_predict(self):
        try:
            gender = st.selectbox(
                "sex",
                [] + ["Male", "Female"])
            age = int(st.text_input("Age", "0"))
            income = int(st.text_input("Income", "0"))
            spending_score = int(st.text_input("Spending Score", "0"))
        except ValueError:
            st.warning("Please input value for all fields")
            return None
        if not (gender, age, income, spending_score):
            st.warning("All inputs must be filled with valid inputs")
        col1, col2, col3 = st.columns([1, 0.6, 1])
        with col2:
            if st.button("predict"):
                gender = self.labeller.transform([gender])
                values = np.array([[gender[0], age, income, spending_score]])
                scaled = self.scaler.transform(values)
                prediction = self.model.predict(scaled)
                st.success(f"cluster = {prediction[0]}")
                return prediction
