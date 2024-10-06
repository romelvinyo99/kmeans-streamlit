import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from io import StringIO


class Home:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def datasetOverview(self):
        st.header("1.Dataset Overview")
        filtered_df = dataframe_explorer(self.dataframe)
        st.dataframe(filtered_df, use_container_width=True)
        st.header("2.Summary Information")
        buffer = StringIO()
        self.dataframe.info(buf=buffer)
        st.text(buffer.getvalue())
        st.header("3.Conclusion")
        # Conclusion based on the df.info() output

        conclusion = """
        The dataset contains 200 entries and 5 columns. Each column has 200 non-null values, indicating that there are no missing values in the dataset.

        - **CustomerID**: This column holds unique identifiers for customers and contains integer data.
        - **Gender**: This column contains categorical data (object type), representing the gender of the customers.
        - **Age**: This column holds integer values representing the age of customers, with no missing values.
        - **Annual Income (k$)**: This column contains integer values representing the annual income of customers in thousands of dollars.
        - **Spending Score (1-100)**: This column holds integer values that represent the spending score of customers, on a scale from 1 to 100.

        The data types of the columns are appropriate for their contents: four integer columns and one object (categorical) column. The memory usage is 7.9 KB, which is minimal.

        **Conclusion**:
        The dataset is clean, with no missing values. The data types are well-suited for the columns, and the dataset is small, requiring minimal memory. It is ready for further analysis or modeling without the need for data cleaning or type conversions.
        """
        st.write(conclusion)
