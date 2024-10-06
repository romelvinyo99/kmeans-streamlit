import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


class Plotting:
    def __init__(self, dataframe):
        self.data = dataframe
        self.hue = None
        self.diagonal_kind = None
        self.kind = None
        self.x_vars = None
        self.y_vars = None

    def pairplot(self):
        st.subheader("1.Pairplot Summary")
        st.write("""
        ### How to Use the Pairplot Customization Tool:

        1. **Group-by (hue):**  
           This dropdown allows you to color the data points based on a categorical variable.  
           - Select **None** to disable grouping.  
           - Select **Clusters** to color the points based on cluster assignments.  
           - Select **Gender** to color the points based on gender categories.

        2. **Diagonal Plot:**  
           This option controls the type of plot that will appear on the diagonal of the pairplot.  
           - **scatter:** Simple scatter plots for diagonal pairs.  
           - **kde:** Kernel Density Estimation plots, useful for visualizing the distribution of data.  
           - **hist:** Histogram plots, which give a bar chart visualization of the distribution of data.  
           - **reg:** Adds a regression line on top of scatter plots to show trends in the data.

        3. **Offset Plot (Diagonal Kind):**  
           This option changes the diagonal plot further:  
           - **hist:** Plots histograms on the diagonal, showing the frequency distribution of each variable.  
           - **kde:** Plots Kernel Density Estimations on the diagonal, which are smooth curves showing probability distribution.  
           - **None:** No special plot on the diagonal.

        4. **x-axis Exclusion:**  
           This dropdown allows you to exclude a specific variable from the x-axis of the pairplot.  
           - Select **None** to include all variables in the x-axis.  
           - If you choose a variable (e.g., **Gender**, **Age**, **Annual-Income**, or **Score**), it will not appear on the x-axis of the plot.

        5. **y-axis Exclusion:**  
           Similarly, this dropdown allows you to exclude a specific variable from the y-axis of the pairplot.  
           - Select **None** to include all variables in the y-axis.  
           - If you choose a variable, it will not be plotted on the y-axis.

        ### What Happens Behind the Scenes:
        - Based on your selections, the app adjusts the **pairplot** parameters accordingly.  
        - The selected **hue** (if not **None**) will group your data by the chosen category.  
        - The type of diagonal plot you choose will be applied across the diagonal of the pairplot.  
        - If you choose to exclude variables from the x-axis or y-axis, they will not be plotted, allowing you to focus on the most relevant variables.

        ### Result:
        Once you’ve made your selections, the app will generate a customized pairplot to help you explore the relationships between the selected variables in your dataset.

        """)

        st.write("")
        st.subheader("2.Pairplots")

        # UI selections
        self.hue = st.selectbox("Group-by (hue)", ["None", "Clusters", "Gender"])
        self.kind = st.selectbox("Diagonal Plot", ["scatter", "kde", "hist", "reg"])
        self.diagonal_kind = st.selectbox("Offset Plot", ["None", "hist", "kde"])
        self.x_vars = st.selectbox("x-axis Exclusion", ["None", "Gender", "Age", "Annual-Income", "Score"])
        self.y_vars = st.selectbox("y-axis Exclusion", ["None", "Gender", "Age", "Annual-Income", "Score"])

        # Prepare kwargs for pairplot
        pairplot_kwargs = {}

        # Handle hue selection
        if self.hue == "None":
            pairplot_kwargs['hue'] = None
        elif self.hue == "clusters":
            pairplot_kwargs['hue'] = "clusters"
        else:
            pairplot_kwargs['hue'] = "Gender"

        # Handle kind selection (affects diagonal plots)
        if self.kind:
            pairplot_kwargs['kind'] = self.kind

        # Handle diagonal_kind (kde, hist or None)
        if self.diagonal_kind != "None":
            pairplot_kwargs['diag_kind'] = self.diagonal_kind

        # Handle x_vars and y_vars (exclude specific variables)
        x_columns = list(self.data.columns)
        y_columns = list(self.data.columns)

        if self.x_vars != "None":
            x_columns = [col for col in x_columns if col != self.x_vars]

        if self.y_vars != "None":
            y_columns = [col for col in y_columns if col != self.y_vars]

        # Add x_vars and y_vars to kwargs
        pairplot_kwargs['x_vars'] = x_columns if self.x_vars != "None" else None
        pairplot_kwargs['y_vars'] = y_columns if self.y_vars != "None" else None

        # Generate pairplot based on user preferences
        fig = sns.pairplot(self.data, **pairplot_kwargs)

        # Display the plot
        st.pyplot(fig)
