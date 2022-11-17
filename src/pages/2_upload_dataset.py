import streamlit as st
import numpy as np
import pandas as pd

from config import params

st.header("Upload Dataset")

tab1, tab2 = st.tabs(["CSV Upload", "BQ Table"])

with tab1:
    st.header("CSV Upload")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    # if file is uploaded, show dtale
    if uploaded_file is not None:
        # read csv file
        st.write("Showing samples..")
        df = pd.read_csv(uploaded_file, nrows=10)
        st.write(df)

        st.button("Upload dataset")


with tab2:
    st.header("BQ Upload")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)


