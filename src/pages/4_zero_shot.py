import streamlit as st
import torch

st.write("# Welcome to CUTUMB ZERO SHOT TEMP 2! 👋")

# print('hello')


from PIL import Image
from autogluon.multimodal import download

url = "https://farm4.staticflickr.com/3445/3262471985_ed886bf61a_z.jpg"
image = download(url)

pil_img = Image.open(image)
st.image(image, caption='Example Image')
# # exit()

from autogluon.multimodal import MultiModalPredictor

class_names = ['Husky', 'Golden Retriever', 'German Sheper', 'Samoyed']
class_texts = [f'A photo of a {i}' for i in class_names]

predictor = MultiModalPredictor(pipeline="zero_shot_image_classification")
prob = predictor.predict_proba({"image": [image]}, {"text": class_texts})
prob_tensor = torch.tensor(prob[0])
print("Label probs:", prob_tensor)

values, indices = prob_tensor.topk(3)
print(indices)
st.write(f"{indices}")