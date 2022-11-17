import streamlit as st
import torch

st.write("# Welcome to CUTUMB ZERO SHOT TEMP 2! 👋")

# print('hello')


from PIL import Image
from autogluon.multimodal import download

url = "https://farm4.staticflickr.com/3445/3262471985_ed886bf61a_z.jpg"
image = download(url)

pil_img = Image.open(image)
# # display(pil_img)

st.image(pil_img)
# # exit()

# from autogluon.multimodal import MultiModalPredictor

# class_texts = ['This is a Husky', 'This is a Golden Retriever', 'This is a German Sheperd', 'This is a Samoyed.']

# predictor = MultiModalPredictor(pipeline="zero_shot_image_classification")
# prob = predictor.predict_proba({"image": [image]}, {"text": class_texts})
# prob_tensor = torch.tensor(prob[0])
# print("Label probs:", prob_tensor)

# values, indices = prob_tensor.topk(3)
# print(indices)