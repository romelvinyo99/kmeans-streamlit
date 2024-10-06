from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import streamlit as st
import pandas as pd


class Preprocessing:
    def __init__(self, dataframe):
        self.data = dataframe
        self.scaler = None
        self.labeller = None

    def text(self):
        st.header("Dataset Overview")
        st.dataframe(self.data)
        st.header("1.Dropping Unnecessary columns")
        reason = "The CustomerID column was dropped as it is a unique identifier and does not provide useful information for analysis or modeling."
        st.write(reason)
        st.code("""dataframe.drop(columns=["Customer"], axis=1, inplace=True)""", language="python")
        self.data = self.droppingColumns()
        st.dataframe(self.data)
        st.header("2.Labelling Categorical Columns")
        self.data, self.labeller = self.labelling()
        label_encoding_reason = "Label encoding is used to convert categorical variables into numerical values, allowing machine learning algorithms to process and interpret them while preserving the ordinal relationship of the categories."
        st.write(label_encoding_reason)
        st.code("""
        labeller = LabelEncoder()
        categorical_columns = dataframe.select_dtypes(include=["object"]).columns
        dataframe[categorical_columns] = labeller.fit_transform(dataframe[categorical_columns])""", language="python")
        st.dataframe(self.data)
        st.header("3.Scaling")
        self.data, self.scaler = self.scaling()
        minmax_scaler_description = "Min-Max Scaler was used to convert the data into the range of 0 to 1, which does not assume any specific distribution of the data."
        st.write(minmax_scaler_description)
        formula = r"""
        x' = \frac{x - \min(X)}{\max(X) - \min(X)}
        """
        st.latex(formula)
        description = """
        x' : Scaled value
        x  : Original value
        min(X) : Minimum value in the feature
        max(X) : Maximum value in the feature
        """
        st.text(description)
        code = """
        scaler = MinMaxScaler()
        self.scaler = scaler
        numerical_columns = self.data.select_dtypes(include=["number"]).columns
        self.data[numerical_columns] = scaler.fit_transform(self.data[numerical_columns])"""
        st.code(code, language="python")
        st.dataframe(self.data)
        st.text("Dataset is ready for modelling")
        return self.scaler, self.labeller, self.data

    def droppingColumns(self):
        self.data.drop(columns=["CustomerID"], axis=1, inplace=True)
        return self.data

    def labelling(self):
        le = LabelEncoder()
        categorical_columns = self.data.select_dtypes(include=["object"]).columns
        self.data["Gender"] = le.fit_transform(self.data["Gender"])
        self.labeller = le
        return self.data, self.labeller

    def scaling(self):
        scaler = MinMaxScaler()
        numerical_columns = self.data.select_dtypes(include=["number"]).columns
        self.data[numerical_columns] = scaler.fit_transform(self.data[numerical_columns])
        self.scaler = scaler
        return self.data, self.scaler
