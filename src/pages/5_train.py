import streamlit as st
import pandas as pd
import os
from autogluon.tabular import TabularDataset, TabularPredictor

from config import params

st.header("Train Model")

df_datasets = pd.read_csv('datasets_list.csv')

dataset_expander = st.expander("Select Dataset")
with dataset_expander:
    st.write("""
    Select a modality and dataset to train a model on.
    """)
    modality_option = st.radio(
        "Select Modality",
            [ "Tabular", "Image", "Video", "Text"],
        horizontal=True,
    )

    if modality_option=="Tabular" or modality_option=="Text":
        # show dropdown menu
        dataset_option = st.selectbox(
            'Select a Dataset:',
                df_datasets['dataset_id'].values)
    else:
        dataset_option = st.text_input("Enter Dataset path in GCS", "gs://autogluon-data/autogluon_open_images_v6/classification/train")

evaluation_expander = st.expander("Select Evaluation Metrics")
with evaluation_expander:
    st.write("""
    Select evaluation paradigms
    """)
    optimize_for = st.selectbox(
        'select a metric',
            ["AUROC", "AUPRC", "Accuracy", "F1", "Precision", "Recall"],)
    evaluation_option = st.selectbox(
        'Select a metric:',
            ["AUROC", "AUPRC", "Accuracy", "F1", "Precision", "Recall"],)



label_option = None
if dataset_option and dataset_option != "<select>":
    remote_gcs_path = f"gs://{params['gcs_data_path']}/{dataset_option}.csv"
    downloaded_file = f"{params['local_data_path']}/{dataset_option}.csv"
    print(f"gsutil cp {remote_gcs_path} {downloaded_file}")
    os.system(f"gsutil cp {remote_gcs_path} {downloaded_file}")
    dataset_df_columns = pd.read_csv(downloaded_file).columns

    # show dropdown menu label column name
    label_option = st.selectbox(
        'Select a label:',
            dataset_df_columns)


def train_model(csv_path, label_option, modality_option):
    # Show train data
    train_data = TabularDataset(csv_path)
    subsample_size = 500  # subsample subset of data for faster demo, try setting this to much larger values
    train_data = train_data.sample(n=subsample_size, random_state=0)
    st.write(train_data.head())

    # Fit the model
    save_path = 'agModels-predictClass'  # specifies folder to store trained models
    predictor = TabularPredictor(label=label_option, path=save_path).fit(train_data, )

    """
    Run on GPU
    hyperparameters = {
        'GBM': [
            {'ag_args_fit': {'num_gpus': 0}},  # Train with CPU
            {'ag_args_fit': {'num_gpus': 1}}   # Train with GPU. This amount needs to be <= total num_gpus granted to TabularPredictor
        ]
    }
    predictor = TabularPredictor(label=label).fit(
        train_data,
        num_gpus=1,
        hyperparameters=hyperparameters,
    )
    """

    """
    Optional
    Maximizing predictive performance:
    time_limit = 60  # for quick demonstration only, you should set this to longest time you are willing to wait (in seconds)
    metric = 'roc_auc'  # specify your evaluation metric here
    predictor = TabularPredictor(label, eval_metric=metric).fit(train_data, time_limit=time_limit, presets='best_quality')
    predictor.leaderboard(test_data, silent=True)

    """
    # Show the fit summary
    results = predictor.fit_summary(show_plot=True)


if st.button('Train Model...'):
    st.write('Awesome!! Model training started')

    train_model(csv_path = f"{params['local_data_path']}/{dataset_option}.csv",
                label_option = label_option,
                modality_option = modality_option
    )
else:
    st.write('🤩 Waiting for you to Start Training')

st.write("-------------------")

