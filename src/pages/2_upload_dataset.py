import streamlit as st
import numpy as np
import pandas as pd
import os

from config import params

def upload_file(dataset_name, uploaded_file):
    # Upload file to GCS Bucket
    bytes_data = uploaded_file.read()

    # save to disk
    os.makedirs(params["local_data_path"], exist_ok=True)
    with open(params["local_data_path"] + dataset_name + ".csv", "wb") as f:
        f.write(bytes_data)

    gs_path = params["gcs_data_path"] + dataset_name + ".csv"
    os.system(f"gsutil cp {params['local_data_path']}/{dataset_name}.csv {gs_path}" )

    #write filename to datasets_list
    with open("datasets_list.csv", "a") as f:
        f.write(dataset_name + "," + gs_path + "\n")
    st.success(f'Dataset {dataset_name} successfully uploaded!', icon="✅")

def upload_bq(dataset_name=None, bq_dataset=None, bq_table=None):
    if dataset_name is None:
        return
    # Upload table to GCS Bucket
    gs_path = params["gcs_data_path"] + dataset_name + "*.csv"
    os.system(f"bq extract --destination_format=CSV schackfest.{bq_dataset}.{bq_table} {gs_path}" )

    #write filename to datasets_list
    with open("datasets_list.csv", "a") as f:
        f.write(dataset_name + "," + gs_path + "\n")
    st.success(f'Dataset {dataset_name} successfully uploaded!', icon="✅")


st.header("Upload Dataset")

tab1, tab2 = st.tabs(["CSV Upload", "BQ Table"])

with tab1:
    st.header("CSV Upload")
    dataset_id = st.text_input("Enter the name of the dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    # if file is uploaded, show dtale
    if uploaded_file is not None:
        # read csv file
        st.write("Showing samples..")
        df = pd.read_csv(uploaded_file, nrows=10)
        st.write(df)

    st.button("Upload dataset", on_click=upload_file, args=(dataset_id, uploaded_file,))


with tab2:
    st.header("BQ Upload")
    bq_table=None
    bq_dataset=None
    dataset_id=None

    # get BQ tables list
    bq_datasets = os.popen("bq ls --project_id=schackfest").read().split("\n")[2:]
    #st.write(bq_datasets)
    # show dropdown menu
    bq_dataset = st.selectbox(
        'Select a Dataset:',
        bq_datasets)

    if bq_dataset:
        st.write("Loading...")
        bq_tables = [ x.strip().split(" ")[0] for x in os.popen(f"bq ls --project_id=schackfest {bq_dataset}").read().split("\n")[2:] ]
        # show dropdown menu
        bq_table = st.selectbox(
            'Select a Table:',
            bq_tables)

        if bq_table:
            st.write(bq_dataset, bq_table)

    # add text input for dataset name
    dataset_id_bq = st.text_input("Enter the name of the dataset", key="bq")
    st.button("Upload dataset", on_click=upload_bq, args=(dataset_id_bq, bq_dataset,bq_table), key="bq_upload")





    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)


