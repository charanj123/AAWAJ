'''import streamlit as st
import os

def dashboard():
    st.title("Video Dashboard")

    # Function to count videos in a specified folder
    def count_videos(folder):
        if os.path.exists(folder):
            video_files = os.listdir(folder)
            return len(video_files)
        else:
            return 0

    # Show the counts
    st.subheader("Count")
    st.write("Uploaded videos:", count_videos("uploaded_videos"))
    st.write("Dubbed videos:", count_videos("dubbed_videos"))

# Call the dashboard function
if __name__ == "__main__":
    dashboard()'''
import streamlit as st
import os

def dashboard():
    st.title("Video Dashboard")

    # Function to count videos in a specified folder
    def count_videos(folder):
        if os.path.exists(folder):
            video_files = os.listdir(folder)
            return len(video_files)
        else:
            return 0

    # Show the counts
    st.subheader("Count")
    st.write("Uploaded videos:", count_videos("uploaded_videos"))
    st.write("Dubbed videos:", count_videos("dubbed_videos"))

# Call the dashboard function
if __name__ == "__main__":
    dashboard()
