from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json
import requests

from nsfw_detector import predict
import numpy as np
import requests
import matplotlib.pyplot as plt
from PIL import Image
# import tensorflow as tf

#VIDEO
import cv2
import tensorflow as tf
from tensorflow import keras
# from PIL import Image
# from nsfw_detector import predict
# import numpy as np
# import requests
# from PIL import Image
import pathlib
from pathlib import Path
import skvideo

#Path('ffmpeg') / 'bin'#
# Path('ffmpeg') / 'bin' #
import os.path
ffmpeg_path = os.path.join('ffmpeg','bin')
# ffmpeg_path = "C:\\code\\justo_nudity_classifier\\ffmpeg\\bin"
skvideo.setFFmpegPath(ffmpeg_path)
import skvideo.io


model_path = Path('model_mobilenet')/ 'saved_model.h5'

model=predict.load_model(model_path)#("C:\\code\\justo_nudity_classifier\\model_mobilenet\\saved_model.h5")

app = FastAPI()

class model_input(BaseModel):
    message: str

#DONT FORGET TO ADD zlibwapi.dll to  C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin

def image_nsfw_detector(file_path):
    # file_path="C:\\code\\justo_nudity_classifier\\sexy3.jpg"
    res=predict.classify(model,file_path)  
    return res


def video_nsfw_detector(video_path):
    videodata = skvideo.io.vread(video_path)
    flag=''
    frame_num=0
    for i in range(len(videodata)):
        frame = videodata[i]
        im=Image.fromarray(frame).resize((224,224))
        image = keras.preprocessing.image.img_to_array(im)
        image /=255
        image=np.expand_dims(image,axis=0)

        res=predict.classify_nd(model,image)[0]
        # print(res)
        if ((res.get('porn')>0.7) or (res.get('sexy')>0.7) or (res.get('hentai')>0.5)):
            flag='x'
            frame_num=i
            # print(f"@frame: {i}")
            # print(res)
            # print("Obscene content detected!")
            # cv2.imshow(frame)
            break
        
    if flag!='x':
        # print("Video is safe for publishing!")
        result="Video is safe for publishing!"
    else:
        # print(f'Obscene content detected! at frame {frame_num}')
        result=f"Obscene content detected @ frame {frame_num}"

    return result


@app.post('/justo_image_nsfw')
def justo_image_nsfw(input_parameters: model_input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    file_path = input_dictionary['message']
    detected_nsfw=image_nsfw_detector(file_path)

    # return detected_nsfw
    return detected_nsfw


@app.post('/justo_video_nsfw')
def justo_video_nsfw(input_parameters: model_input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    file_path = input_dictionary['message']
    detected_nsfw=video_nsfw_detector(file_path)

    # return detected_nsfw
    return detected_nsfw









