import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Financial Ledger", layout="wide")

st.title("Financial Ledger Viewer")

file = st.file_uploader("Upload CSV File", type=["csv"])

if file is not None:
    data = pd.read_csv(file)

    st.sidebar.header("Controls")

    row_count = st.sidebar.slider("Select Rows", 1, len(data), 20)
    filtered_data = data.head(row_count)

    numeric_columns = filtered_data.select_dtypes(include=["int64","float64"]).columns.tolist()

    if len(numeric_columns) > 0:
        column = st.sidebar.selectbox("Select Column", numeric_columns)
        graph_type = st.sidebar.selectbox("Select Graph Type", ["Bar", "Area", "Histogram"])

        col1, col2, col3 = st.columns(3)

        col1.metric("Mean", round(filtered_data[column].mean(),2))
        col2.metric("Max", filtered_data[column].max())
        col3.metric("Min", filtered_data[column].min())

        st.subheader(f"{graph_type} Chart")

        fig, ax = plt.subplots()

        if graph_type == "Bar":
            ax.bar(range(len(filtered_data[column])), filtered_data[column])
        elif graph_type == "Area":
            ax.fill_between(range(len(filtered_data[column])), filtered_data[column])
        else:
            ax.hist(filtered_data[column], bins=10)

        st.pyplot(fig)