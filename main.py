import streamlit as st
import numpy as np
import cv2

profils = {
    "Rose smiley flower": {
        "lower": 95,
        "higher": 344
    } ,
    "Blue smiley flower": {
        "lower": 100,
        "higher": 150
    }
}

# Load image.
uploaded_file = st.sidebar.file_uploader("Upload an image:")

if uploaded_file is not None:

    npimg = np.fromstring(uploaded_file.getvalue(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for object_name in profils.keys():
        lower_h = profils[object_name]["lower"]
        upper_h = profils[object_name]["higher"]
        mask = cv2.inRange(hsv, (lower_h,100,100), (upper_h,255,255))


        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if contours:
            contour = sorted(contours, key = cv2.contourArea, reverse=True)[0]

            rect = cv2.boundingRect(contour)
            x,y,w,h = rect

            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 2)

            cv2.putText(frame, object_name, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    st.image(frame)