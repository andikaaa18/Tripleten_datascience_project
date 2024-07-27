import streamlit as st
from PIL import Image
import numpy as np
from tensorflow import keras

def input_form():
    # form title
    st.title("Age Estimation Using Modified ResNet50V2 for Enhanced Supermarket Services")

    # option to upload a photo or take a photo
    st.header("Upload Method", divider='grey')
    method = st.radio("Please choose a method to upload a photo", 
                      ['Upload a photo', 'Take a photo', 'Dummy Photo'],
                      index=2)

    if method == 'Upload a photo':
        photo = st.file_uploader("Upload the photo here in JPG, JPEG or PNG format!", type=['jpg', 'jpeg', 'png'])
        if photo != None:
            photo = Image.open(photo)

    elif method == 'Take a photo':
        photo = st.camera_input("Please position your face at the center of the frame!")
        if photo != None:
            photo = Image.open(photo)

    else:
        photo = Image.open("./assets/sample_photo.png")

    return photo

def resize_and_crop(photo, size=(150,150)):
    # resize
    width, height = photo.size
    aspect_ratio = width/height
    if aspect_ratio > size[0]/size[1]:
        # Gambar asli lebih lebar (landscape) dari pada gambar target
        new_height = size[1]
        new_width = int(aspect_ratio*new_height)
    else:
        # Gambar asli lebih tinggi (portrait) dari pada gambar target
        new_width = size[0]
        new_height = int(new_width/aspect_ratio)

    photo = photo.resize((new_width, new_height))
    
    # crop
    width, height = photo.size
    cropbox = ((width-size[0])/2, (height-size[1])/2, (width+size[0])/2, (height+size[1])/2)
    photo = photo.crop(cropbox)

    return photo

    pass

def feature_engineering(photo):
    # resizing an image
    photo = resize_and_crop(photo)
    # converting to RGB/3-channel format
    photo = photo.convert('RGB')
    # normalization
    arr = np.array(photo) / 255.0
    # resizing array
    arr = np.expand_dims(arr, axis=0)

    return arr

def model_predict(array):
    model = keras.models.load_model('./assets/best_checkpoint.model.keras')
    prediction = model.predict(array)
    
    return prediction

with st.spinner("In progres..."):
    photo = input_form()
    execute = st.button("Run the model")
    if execute & (photo != None):
        row1 = st.columns([0.25, 0.75])

        # display the image
        row1[0].image(resize_and_crop(photo), caption="Photo to be predicted", use_column_width="auto")
        # predict age
        arr = feature_engineering(photo)
        with st.spinner("in process..."):
            prediction = model_predict(arr)
        row1[1].metric("The Predicted Age", f"{int(prediction[0][0])} - years")

