import streamlit as st
import os 

st.title("AWAJ.....")

def input():
    video_uploader=st.file_uploader("Uploade the video file",type="mp4")

    if  video_uploader is not None:
        # Display the uploaded video
        st.video(video_uploader)

    

input()