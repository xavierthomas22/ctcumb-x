
# visualize using sweetviz

import sweetviz as sv

#import streamlit components
import streamlit as st
st.set_page_config(layout="wide")
import streamlit.components.v1 as components
import pandas as pd


# load data

# get input file from user
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# if file is uploaded, show dtale
if uploaded_file is not None:
    # read csv file
    df = pd.read_csv(uploaded_file)

    # analyze data
    
    my_report = sv.analyze(df)
    
    # show report
    
    my_report.show_html('report.html')


st.markdown('## Sweetviz Report')
st.markdown('---')

# show html to streamlit

components.html(open('report.html', 'r').read(), scrolling=True, height=1000, width=1920)

