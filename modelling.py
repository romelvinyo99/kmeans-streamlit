import warnings
from kneed import KneeLocator
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import streamlit as st


class Clustering:
    def __init__(self, dataframe):
        self.data = dataframe
        self.target = self.data[dataframe.columns]
        self.model = None
        self.clusters = None

    @classmethod
    def kmeans_summary(cls):
        st.write("""
        **K-Means Clustering** is a popular unsupervised machine learning algorithm used to partition a dataset into *K* distinct, non-overlapping subsets (or clusters). 
        The objective of K-Means is to minimize the within-cluster variance while maximizing the distance between clusters.
        """)

        st.subheader("How It Works")
        st.write("""
        1. **Initialization**: Select *K* initial centroids randomly from the dataset.
        2. **Assignment Step**: Assign each data point to the nearest centroid, forming *K* clusters.
        3. **Update Step**: Recalculate the centroids as the mean of all points in each cluster.
        4. **Convergence**: Repeat the assignment and update steps until the centroids no longer change significantly or a set number of iterations is reached.
        """)

        st.subheader("Applications")
        st.write("""
        - Market segmentation
        - Image compression
        - Anomaly detection
        - Document clustering
        """)

        st.subheader("Advantages and Limitations")
        st.write("""
        **Advantages**:
        - Simple and easy to implement.
        - Efficient for large datasets.

        **Limitations**:
        - Requires the number of clusters (*K*) to be specified in advance.
        - Sensitive to initial centroid placement.
        - May converge to local minima.
        """)

    def text(self):
        st.header("Dataframe")
        st.dataframe(self.data)
        st.subheader("1.K-Means clustering algorithm Overview")
        Clustering.kmeans_summary()
        st.subheader("2.Selecting optimal clusters")
        st.write("Getting the optimal number of clusters for the model --> point of convergence")
        st.code("""
        with warnings.catch_warnings:
            warnings.simplefilter("ignore")
            SSE = []
            k_range = range(1, 100)
            for n in k_range:
                km = KMeans(n_clusters=n)
                km.fit(self.target)
                SSE.append(km.inertia_)
            kneedle = KneeLocator(k_range, SSE, curve="convex", direction="decreasing")
            optimal_k = kneedle.elbow
        """, language="python")
        st.subheader("3.Plotting the optimal value of k")
        optimal_k, k_range, SSE = self.optimal_clusters()
        self.plotting()
        st.header("4.Clustering")
        st.write("Clustering the data")
        st.code("""
        with warnings.catch_warnings:
            warnings.simplefilter("ignore")
            model = KMeans(n_clusters=n)
            self.data["clusters"] = model.fit_predict(self.target)
            return model, self.data
        """, language="python")
        self.model, self.target, self.clusters = self.clustering()
        st.dataframe(self.data)
        st.subheader("Cluster Centres")
        cluster_centers = self.model.cluster_centers_
        try:
            user_selection = int(st.slider("Select cluster", min_value=0, max_value=optimal_k))
        except ValueError:
            st.warning("Please input value")
            return None
        selected_cluster = []
        if not user_selection:
            st.warning("Input fields must be filled")

        col1, col2, col3 = st.columns([1, 0.6, 1])
        with col2:
            if st.button("select"):
                selected_cluster = cluster_centers[user_selection]
        st.success(f"Center Coordinates = {selected_cluster}")

        st.subheader("Summary")
        st.write(f"""
            **The model came out with {self.clusters} clusters.**

            **Note:** This is a form of unsupervised learning:
            1. No form of distribution was assumed.
            2. No anomaly detection - Assumed all data points are equally important.

            **Accuracy Measurement:**
            There is no measure of accuracy because we do not have anything to compare with. 
            The only form of accuracy was generating the optimal value for the cluster number.
        """)
        return self.model

    def optimal_clusters(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            SSE = []
            k_range = range(1, 100)
            for n in k_range:
                km = KMeans(n_clusters=n)
                km.fit(self.target)
                SSE.append(km.inertia_)
            kneedle = KneeLocator(k_range, SSE, curve="convex", direction="decreasing")
            optimal_k = kneedle.elbow
            return optimal_k, k_range, SSE

    def plotting(self):
        optimal_k, k_range, SSE = self.optimal_clusters()
        fig, axs = plt.subplots(1, 1, figsize=(12, 6))
        axs.plot(k_range, SSE, label="SSE")
        axs.vlines(optimal_k, plt.ylim()[0], plt.ylim()[1], linestyle="dashed", label=f"optimal value = {optimal_k}", )
        axs.set_title("Cluster approximation")
        axs.set_xlabel("k")
        axs.set_ylabel("SSE")
        axs.legend()
        axs.grid()
        st.pyplot(fig)

    def clustering(self):
        n, k, s = self.optimal_clusters()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = KMeans(n_clusters=n)
            self.data["clusters"] = model.fit_predict(self.target)
            return model, self.data, n
