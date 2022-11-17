import streamlit as st
import torch
import IPython
import autogluon
import pandas as pd
import os
import random
from IPython.display import Image, display
from autogluon.multimodal import download
from autogluon.multimodal import MultiModalPredictor
from config import params
import random
from datetime import datetime
import streamlit
# from sentence_transformers import SentenceTransformer

st.write("# Welcome to CUTUMB ZERO SHOT! 👋")

st.write("Select a data source:")
tab0, tab1, tab2, tab3 = st.tabs(["Image Upload", "STL-10 Dataset", "Image Search", "Upload Image Folder"])

option = "stl10_images"
sampled_ids = [i+1 for i in range(10)]
dataset_path = 'data/stl10_images/'
if not os.path.isdir(dataset_path):
    with st.spinner('Fetching 10 images from the STL-10 Dataset'):
        for i in sampled_ids:
            remote_gcs_path = f"gs://{params['gcs_data_path']}/{option}/train_image_png_{i}.png"
            downloaded_file = f"{params['local_data_path']}/{option}/train_image_png_{i}.png"
            os.system(f"gsutil cp {remote_gcs_path} {downloaded_file}")

predictor = MultiModalPredictor(pipeline="zero_shot_image_classification")

with tab0:

    # url = "https://farm4.staticflickr.com/3445/3262471985_ed886bf61a_z.jpg"
    url = st.text_input("Enter url (example: https://farm4.staticflickr.com/3445/3262471985_ed886bf61a_z.jpg)")
    if url:
        try:
            image = download(url)

            pil_img = Image(filename=image)
            st.image(image, caption='Example Image')

            class_names = st.text_input("Enter Class Names (comma seperated) (example: Husky, Labrador, Bulldog)")
            if class_names:
                class_names = [x for x in class_names.split(',') if x]

                class_texts = [f'This is a {i}' for i in class_names]

                with st.spinner('Computing.....'):

                    prob = predictor.predict_proba({"image": [image]}, {"text": class_texts})
                    prob_tensor = torch.tensor(prob[0])

                    values, indices = prob_tensor.topk(len(class_names))

                    zero_shot_dict = {}
                    for i in range(len(indices)):
                        zero_shot_dict[class_names[indices[i]]] = round(values[i].item()*100, 2)

                    zero_shot_df = pd.DataFrame.from_dict(zero_shot_dict,  orient='index', columns=['Acc'])
                    st.table(zero_shot_df)
        except:
            st.error("Invalid URL, Please see the example given")

with tab1:
    st.header("STL-10 Dataset")

    class_names = ['airplane', 'bird', 'car', 'cat', 'deer', 'dog', 'horse', 'monkey', 'ship', 'truck']
    class_texts = [f'This is a {i}' for i in class_names]
    file_list = os.listdir(dataset_path)

    if 'count' not in st.session_state:
	    st.session_state.count = 0

    def increment_counter():
	    st.session_state.count += 1

    def get_zero_shot():

        random.seed(datetime.now())

        sampled_images = file_list
        image = sampled_images[st.session_state.count-1]

        image = "data/stl10_images/" + image
        pil_img = Image(filename=image, width=256)
        st.image(image, caption='Target Image', width=256)

        with st.spinner('Computing.....'):

            prob = predictor.predict_proba({"image": [image]}, {"text": class_texts})
            prob_tensor = torch.tensor(prob[0])

            values, indices = prob_tensor.topk(len(class_names))

            zero_shot_dict = {}
            for i in range(len(indices)):
                zero_shot_dict[class_names[indices[i]]] = round(values[i].item()*100, 2)

            zero_shot_df = pd.DataFrame.from_dict(zero_shot_dict,  orient='index', columns=['Acc'])
            st.table(zero_shot_df)

    # while True:
    if st.button('Click to generate image'):
        increment_counter()
        if st.session_state.count == 10:
            st.session_state.count = 0
        get_zero_shot()

with tab2:
    st.header("Image Search")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("Upload Image Folder")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)