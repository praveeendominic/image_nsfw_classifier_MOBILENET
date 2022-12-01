
import streamlit as st
import os

import pathlib
from pathlib import Path
from nsfw_detector import predict

model_path = Path('model_mobilenet')/ 'saved_model.h5'
model=predict.load_model(model_path)


st.header('IMAGE NUDITY DETECTOR')
st.write("Please select an image for nudity check.")

image_uploaded=st.file_uploader(label= "Please upload a file",accept_multiple_files=False, type = ['jpg', 'jpeg', 'png'])
if image_uploaded is not None:
    st.image(image_uploaded)
    st.write(image_uploaded.name)

    # uploaded_image_path=os.path.join('tmp_dir',image_uploaded.name)
    # st.write(uploaded_image_path)
    fname=os.path.splitext(image_uploaded.name)
    file_ext=fname[1]
    # st.write(file_ext)
    fname_u='tmp'+file_ext
    st.write(fname_u)
    
    # saving file
    with open(image_uploaded.name, 'wb') as f:
        f.write(image_uploaded.getbuffer())
        st.success("File Saved")



    def image_nsfw_detector(file_path):
        res=predict.classify(model,file_path)  
        return res

    result = image_nsfw_detector(image_uploaded.name)
    st.write(result)

# print(result)


