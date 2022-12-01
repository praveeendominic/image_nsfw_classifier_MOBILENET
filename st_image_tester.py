
import streamlit as st



st.header('TEST IMAGE NUDITY')


st.write("Please select an image for nudity check.")

image_uploaded=st.file_uploader(label= "Please upload a file",accept_multiple_files=False, type = ['jpg', 'jpeg', 'png'])
if image_uploaded is not None:
    st.image(image_uploaded)
    
    #saving file
    with open(image_uploaded.name, 'wb') as f:
        uploaded_image_path=os.path.join('tmp_dir',image_uploaded.name)
        f.write(uploaded_image_path.getbuffer())
        st.success("File Saved")


# import nudity_api
# from nudity_api import image_nsfw_detector


# result = image_nsfw_detector(image_uploaded)

# st.write(result)

# print(result)


