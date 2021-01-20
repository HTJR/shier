import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import string 
import random
import os 
import numpy as np
from streamlit_lottie import st_lottie
import requests

st.title("Shitter")
st.write("Dump all your shit here")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets6.lottiefiles.com/private_files/lf30_nj9klqqz.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json)



# Specify canvas parameters in application
stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
#bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
)
# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgb(255, 165, 0)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color= bg_color,
    background_image=None,
    update_streamlit=True,
    height=550,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Do something interesting with the image data and paths
im=canvas_result.image_data
#im=Image.fromarray((im*255).astype(np.uint8))
#im = im.convert('rgb')
if st.button("post"):
    img_float32 = np.float32(im)
    im=cv2.cvtColor(img_float32, cv2.COLOR_RGB2BGR)
    letters = string.ascii_lowercase
    na=''.join(random.choice(letters) for i in range(10))
    cv2.imwrite("images/"+na+".jpg",im) 

st.markdown("# Posts")
for i in os.listdir("./images"):
    im=cv2.imread("./images/"+i)
    st.image(im,caption='Draw',clamp=True,use_column_width=True)