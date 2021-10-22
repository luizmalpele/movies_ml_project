import streamlit as st
import numpy as np

from PIL import Image

img = Image.open("/Users/OmarMateo/OneDrive - Florida Polytechnic University/Fall 2021/CEN4010 Software Engineering/Project NO DELETE/Website/icons/disney+_icon.png")


st.button(st.image(img))