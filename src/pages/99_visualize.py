# Dtale demo streamlit

# Path: pages/3_dtale.py
import streamlit as st
import pandas as pd
import dtale


# get input file from user
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# if file is uploaded, show dtale
if uploaded_file is not None:
    # read csv file
    df = pd.read_csv(uploaded_file)
    # show dtale
    dtale.show(df, port=11000, force=True)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")

