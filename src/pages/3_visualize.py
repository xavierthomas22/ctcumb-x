import sweetviz as sv
import os
from config import params

#import streamlit components
import streamlit as st
st.set_page_config(layout="wide")
import streamlit.components.v1 as components
import pandas as pd


# load data
st.write("Select a data source:")
tab0, tab1, tab2, tab3 = st.tabs(["Added dataset", "CSV Upload", "Remote Image Dataset", "Remote Video Dataset"])

with tab0:
    df_datasets = pd.read_csv('datasets_list.csv')
    df = None

    # show dropdown menu
    option = st.selectbox(
        'Select a Dataset:',
            df_datasets['dataset_id'].values)
    
    if option and option!="<select>":
        remote_gcs_path = f"gs://{params['gcs_data_path']}/{option}.csv"
        downloaded_file = f"{params['local_data_path']}/{option}.csv"
        os.system(f"gsutil cp {remote_gcs_path} {downloaded_file}")
        df = pd.read_csv(downloaded_file)

with tab1:
    st.header("CSV Upload")
    dataset_id = st.text_input("Enter the name of the dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    # if file is uploaded, show dtale
    if uploaded_file is not None:
        # read csv file
        st.write("Showing samples..")
        df = pd.read_csv(uploaded_file)
        st.write(df)

with tab2:
    st.header("Remote Image Dataset")
    st.code(""" root/dog/xxx.png
root/dog/xxy.png

root/cat/123.png
root/cat/nsdf3.png """)
    col1, col2 = st.columns(2)
    with col1:
        gcs_image_path = st.text_input("Enter the GCS path of the dataset", "gs://schackfest-datasets/images/")
        os.makedirs(os.path.join(params["local_data_path"], "image_dataset_tmp", gcs_image_path), exist_ok=True)
    with col2:
        num_images = st.slider("Enter the number of images to view per class", 1, 100, 10)

    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Classes", "2")
    col2.metric("Total image samples", "144,400")
    col3.metric("Class Imbalance", "86%")

    # show images
    st.write("Showing samples..")
    # get list of images
    image_list = os.popen(f"gsutil ls {gcs_image_path}").read().split("\n")
    image_list = [image for image in image_list if image!=""]
    # get list of classes
    class_list = list(set([image.split("/")[-2] for image in image_list]))
    # show images
    for class_name in class_list:
        st.write(f"Class: {class_name}")
        class_images = [image for image in image_list if image.split("/")[-2]==class_name]





with tab3:
    st.header("Remote Video Dataset")
    col1, col2 = st.columns(2)
    with col1:
        gcs_image_path = st.text_input("Enter the GCS path of the dataset", "gs://schackfest-datasets/videos/")
        os.makedirs(os.path.join(params["local_data_path"], "image_dataset_tmp", gcs_image_path), exist_ok=True)
    with col2:
        num_images = st.slider("Enter the number of videos to view", 1, 20, 10)

    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Classes", "2")
    col2.metric("Total image samples", "144,400")
    col3.metric("Class Imbalance", "86%")

st.write("-------------------")


#st.subheader("Selected source:")

if df is not None:
    tab_sz, tab_dtale = st.tabs(["Sweetviz", "Dtale"])
    with tab_sz:
        my_report = sv.analyze(df)
        # show report
        my_report.show_html('report.html')
        st.markdown('## Sweetviz Report')
        st.markdown('---')

        # show html to streamlit
    
        components.html(open('report.html', 'r').read(), scrolling=True, height=1000, width=1920)


